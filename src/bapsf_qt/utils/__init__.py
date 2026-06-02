"""
A collection of utility functionality to help build `PySide6` GUIs.
"""

from __future__ import annotations

__all__ = [
    "cast_color_to_rgba_string",
    "get_color_scheme",
    "get_qapplication",
    "icon_name_dict",
]

import ast

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication
from typing import TYPE_CHECKING

from bapsf_qt.utils.icons import icon_name_dict

if TYPE_CHECKING:
    from PySide6.QtCore import Qt


def get_qapplication() -> QCoreApplication | None:
    """
    Get the current active instance of
    `~PySide6.QtWidgets.QApplication`.  This is a convinces function
    to `~PySide6.QtCore.QCoreApplication.instance`.
    """
    app = QApplication.instance()
    return app


def get_color_scheme() -> Qt.ColorScheme:
    """
    Retrieve the color scheme (light or dark mode) of the operating
    system.  The returns the `~PySide6.QtCore.Qt.ColorScheme` `enum`.
    """
    app = get_qapplication()

    if not hasattr(app, "styleHints"):
        raise TypeError(
            "Expected the main application to be an instance of 'QApplication' "
            f"so styleHints().colorScheme() (i.e. light / dark mode) could be "
            f"retrieved, got type {type(app)} instead."
        )

    _scheme = app.styleHints().colorScheme()
    return _scheme


def cast_color_to_rgba_string(color: QColor | str) -> str:
    """
    Cast ``color`` to an RGBA string representation
    ``'rgba(r, g, b, a)'``

    Parameters
    ----------
    color : Union[QColor, str]
        ``color`` can be an instance of `~PySide6.QtGui.QColor` or a
        string representation of hex, rgb, or rgba color code.  It can
        also be a string representation of a `~PySide6.QtGui.QColor`,
        e.g. ``'QColor(r, g, b)'``.
    """
    if isinstance(color, QColor):
        pass
    elif not isinstance(color, str):
        raise TypeError(f"Color {color} is not a valid type, expect str or QColor.")
    elif color.startswith("QColor"):
        color = eval(color)
    elif color.startswith("#"):
        color = QColor(color)
    elif color.startswith("rgba"):
        args = ast.literal_eval(color[4:])
        color = QColor(*args)
    elif color.startswith("rgb"):
        args = ast.literal_eval(color[3:])
        color = QColor(*args)
        color.setAlpha(255)
    else:
        raise ValueError(f"Unable to cast color {color}.")

    return f"rgba{color.getRgb()}"
