"""
Buttons designed with an icon display.
"""
__all__ = ["IconButton", "GearButton", "GearValidButton"]

from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QIcon

from bapsf_qt.buttons.core import StyleButton, ValidButton
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


class GearValidButton(ValidButton):
    def __init__(self, parent=None):
        self._valid_color = QColor(52, 161, 219, 240)
        self._invalid_color = QColor(250, 66, 45, 200)

        icon_name = icon_name_dict["gear"]
        self._valid_icon = qta.icon(icon_name, color=self._valid_color)
        self._invalid_icon = qta.icon(icon_name, color=self._invalid_color)
        self._disabled_icon = qta.icon(icon_name)

        super().__init__(self._invalid_icon, "", parent=parent)

        self.update_style_sheet(
            styles={"background-color": "rgb(95, 95, 95)"},
            action="pressed",
        )
        self.update_style_sheet(
            styles={"background-color": "rgb(123, 123, 123)"},
            action="checked",
        )  # checked state is the valid state

        self.setIcon(self._invalid_icon)

        self._size = None
        self.setFixedSize(32)

        self._icon_size = None
        self.setIconSize(28)

        self.setChecked(False)

    def set_valid(self, state: bool = True):
        _icon = self._valid_icon if state else self._invalid_icon
        self.setIcon(_icon)
        super().set_valid(state=state)

    def set_invalid(self):
        self.setIcon(self._invalid_icon)
        super().set_invalid()

    def setIconSize(self, size: int):
        if not isinstance(size, int):
            return
        elif size <= 0:
            return

        self._icon_size = size
        size = QSize(size, size)
        super().setIconSize(size)

    def setFixedSize(self, size: int):
        if not isinstance(size, int):
            return
        elif size <= 0:
            return

        self._size = size
        size = QSize(size, size)
        super().setFixedSize(size)

    def setFixedHeight(self, h):
        self.setFixedSize(h)

    def setFixedWidth(self, w):
        self.setFixedSize(w)

    def _change_validation_icon(self):
        _icon = self._valid_icon if self.is_valid else self._invalid_icon
        self.setIcon(_icon)

    def setDisabled(self, arg__1):
        self.setEnabled(not arg__1)

    def setEnabled(self, arg__1):
        self.set_invalid()
        if not arg__1:
            self.setIcon(self._disabled_icon)

        super().setEnabled(arg__1)
