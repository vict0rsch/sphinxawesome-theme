"""Override code from the default HTML builder related to pygments CSS.

This extension extends the default HTML builder by changing the way
Pygments CSS is handled.

- Add a ``pygments_style_dark`` configuration option.
- Append dark mode classes to the main ``pygments.css`` file,
  instead of writing them in a separate file,
  properly prepend all classes for dark mode with `.dark`

:copyright: Copyright Kai Welke.
:license: MIT, see LICENSE for details.
"""

from __future__ import annotations

from os import path

from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.highlighting import PygmentsBridge


class AwesomeHTMLBuilder(StandaloneHTMLBuilder):
    """HTML builder that overrides a few methods related to handling CSS for Pygments."""

    def init_highlighter(self: AwesomeHTMLBuilder) -> None:
        """Initialize Pygments highlighters."""
        # ``pygments_style`` from config
        if self.config.pygments_style is not None:
            style = self.config.pygments_style
        elif self.theme:
            # From the ``pygments_style`` theme setting
            if self.theme.hasattr("pygments_style_default"):
                style = self.theme.pygments_style_default or "none"
            elif self.theme.hasattr("pygments_style"):
                style = self.theme.pygments_style or "none"
        else:
            style = "sphinx"

        self.highlighter = PygmentsBridge("html", style)

        if self.config.pygments_style_dark is not None:
            dark_style = self.config.pygments_style_dark
        elif self.theme:
            dark_style = self.theme.pygments_style_dark  # type: ignore[attr-defined]
        else:
            dark_style = None

        self.dark_highlighter: PygmentsBridge | None  # type: ignore
        if dark_style is not None:
            self.dark_highlighter = PygmentsBridge("html", dark_style)
        else:
            self.dark_highlighter = None

    def create_pygments_style_file(self: AwesomeHTMLBuilder) -> None:
        """Create CSS file for Pygments."""
        stylesheet = self.highlighter.get_stylesheet()
        if self.dark_highlighter:
            stylesheet += self.dark_highlighter.get_stylesheet(arg=".dark")  # type: ignore

        with open(
            path.join(self.outdir, "_static", "pygments.css"), "w", encoding="utf-8"
        ) as f:
            f.write(stylesheet)
