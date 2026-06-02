"""
Buttons designed with an icon display.
"""
__all__ = ["IconButton", "GearButton"]

from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QIcon

from bapsf_qt.buttons.core import StyleButton
from bapsf_qt.utils import cast_color_to_rgba_string, icon_name_dict

# import of qtawesome must happen after the PySide6 imports
import qtawesome as qta  # noqa


class IconButton(StyleButton):
    def __init__(
        self,
        qta_icon_name: str,
        *args,
        color: QColor | str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        try:
            if color is not None:
                color = cast_color_to_rgba_string(color)
        except (ValueError, TypeError):
            color = None

        if color is None:
            _palette = self.palette()
            _palette_color = _palette.color(_palette.ColorRole.ButtonText)

            color = self.base_style.get("color", _palette_color)

        if not isinstance(color, QColor):
            color = cast_color_to_rgba_string(color)
            icon_color = color.replace("rgba(", "").replace(")", "")
            r, g, b, a = map(int, icon_color.split(","))
            icon_color = QColor(r, g, b, a=a)
        else:
            icon_color = color

        self.update_style_sheet(styles={"color": color}, action="base")
        self._icon = qta.icon(qta_icon_name, color=icon_color)

        self.setIcon(self._icon)

    @property
    def icon(self) -> QIcon:
        return self._icon

    def setIconSize(self, size: QSize | int):
        if isinstance(size, int):
            size = QSize(size, size)

        if not isinstance(size, QSize):
            return

        super().setIconSize(size)


class GearButton(StyleButton):
    def __init__(self, color: str | None = None, parent=None):
        super().__init__(parent=parent)

        try:
            if color is not None:
                color = cast_color_to_rgba_string(color)
        except (ValueError, TypeError):
            color = None

        if color is None:
            _palette = self.palette()
            _palette_color = _palette.color(_palette.ColorRole.ButtonText)

            color = self.base_style.get("color", _palette_color)

        if not isinstance(color, QColor):
            color = cast_color_to_rgba_string(color)
            icon_color = color.replace("rgba(", "").replace(")", "")
            r, g, b, a = map(int, icon_color.split(","))
            icon_color = QColor(r, g, b, a=a)
        else:
            icon_color = color

        self.update_style_sheet(styles={"color": color}, action="base")
        self._icon = qta.icon(icon_name_dict["gear"], color=icon_color)
        self.setIcon(self._icon)

        self._size = 32
        self._icon_size = 24

        self.setFixedWidth(self._size)
        self.setFixedHeight(self._size)
        self.setIconSize(QSize(self._icon_size, self._icon_size))
