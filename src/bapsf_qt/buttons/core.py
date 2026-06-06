"""
Foundational / core buttons.  These inherit directly from
`~PySide6.QtWidgets.QPushButton` and are intended to help design other
button classes.
"""

__all__ = ["AutoScaleButton", "StyleButton", "ValidButton"]

import math

from PySide6.QtCore import Slot
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QPushButton


class StyleButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._default_base_style = {
            "border-radius": "4px",
            "border": "2px solid rgb(123, 123, 123)",
            "background-color": "rgb(163, 163, 163)",
            "color": "rgb(50, 50, 50)",
        }
        self._default_hover_style = {"border": "2px solid rgb(30, 60, 90)"}
        self._default_pressed_style = {"background-color": "rgb(111, 111, 111)"}
        self._default_checked_style = {}
        self._default_disabled_style = {"color": "rgb(123, 123, 123)"}

        self._base_style = {**self._default_base_style}
        self._hover_style = {**self._default_hover_style}
        self._pressed_style = {**self._default_pressed_style}
        self._checked_style = {**self._default_checked_style}
        self._disabled_style = {**self._default_disabled_style}

        _font = self.font()
        _font.setBold(True)
        self.setFont(_font)

        self._resetStyleSheet()

    @property
    def _style(self):
        _cls_name = self.__class__.__name__
        _base = "; ".join([f"{k}: {v}" for k, v in self.base_style.items()])
        _hover = "; ".join([f"{k}: {v}" for k, v in self.hover_style.items()])
        _pressed = "; ".join([f"{k}: {v}" for k, v in self.pressed_style.items()])
        _checked = "; ".join([f"{k}: {v}" for k, v in self.checked_style.items()])
        _disabled = "; ".join([f"{k}: {v}" for k, v in self.disabled_style.items()])

        object_name = self.objectName()
        if object_name is None or not isinstance(object_name, str):
            object_name = ""
        elif object_name != "":
            object_name = f"#{object_name}"

        header = f"{_cls_name}{object_name}"

        return f"""
        {header} {{ {_base} }}

        {header}:hover {{ {_hover}  }}

        {header}:pressed {{ {_pressed} }}

        {header}:checked {{ {_checked} }}

        {header}:disabled {{ {_disabled} }}
        """

    @property
    def base_style(self):
        return self._base_style

    @property
    def hover_style(self):
        return self._hover_style

    @property
    def pressed_style(self):
        return self._pressed_style

    @property
    def checked_style(self):
        return self._checked_style

    @property
    def disabled_style(self):
        return self._disabled_style

    def _resetStyleSheet(self):
        self.setStyleSheet(self._style)

    def setPointSize(self, point_size):
        font = self.font()
        font.setPointSize(point_size)
        self.setFont(font)

    def update_style_sheet(self, styles, action="base", reset=False):

        if action not in ("base", "hover", "pressed", "checked", "disabled"):
            return

        if action == "base":
            _style = self.base_style if not reset else {**self._default_base_style}
            self._base_style = {**_style, **styles}
        elif action == "hover":
            _style = self.hover_style if not reset else {**self._default_hover_style}
            self._hover_style = {**_style, **styles}
        elif action == "pressed":
            _style = self.pressed_style if not reset else {**self._default_pressed_style}
            self._pressed_style = {**_style, **styles}
        elif action == "checked":
            _style = self.pressed_style if not reset else {**self._default_checked_style}
            self._checked_style = {**_style, **styles}
        else:  # action == "disabled
            _style = (
                self.disabled_style if not reset else {**self._default_disabled_style}
            )
            self._disabled_style = {**_style, **styles}

        self._resetStyleSheet()


class AutoScaleButton(StyleButton):

    def __init__(self, *args, **kwargs):
        self._max_font_height_ratio = 0.8

        super().__init__(*args, **kwargs)

        self.setFixedHeight(48)
        font = self.font()
        font.setPixelSize(24)
        font.setBold(True)
        self.setFont(font)

        _text = self.text()
        self.setText(_text)

    def _calculate_target_width(
        self,
        text: str | None = None,
        scale: float = 1.0,
    ):
        if text is None:
            text = self.text()

        font = self.font()
        fm = QFontMetrics(font)
        _length = fm.horizontalAdvance(text)
        _padding = 2 * math.ceil(0.5 * scale * (self.height() - fm.height()))
        return _length + _padding

    def setText(self, text: str):
        super().setText(text)

        # allow larger width than the one calculated
        new_width = self._calculate_target_width(text)
        width = new_width if new_width >= self.width() else self.width()
        self.setFixedWidth(width)

    def setFont(self, font: QFont):
        ratio = font.pointSize() / self.height()
        if ratio > self._max_font_height_ratio:
            # automatically shrink font if too large for height
            font_size = math.floor(self._max_font_height_ratio * self.height())
            font.setPointSize(font_size)
        super().setFont(font)

        _txt = self.text()
        self.setText(_txt)

    def setFixedHeight(self, h: int):
        ratio = self.font().pixelSize() / h
        if ratio > self._max_font_height_ratio:
            # automatically shrink font if too large for given height
            font_size = math.floor(self._max_font_height_ratio * h)
            font = self.font()
            font.setPointSize(font_size)
            self.setFont(font)

        super().setFixedHeight(h)
        _txt = self.text()
        self.setText(_txt)

    def shrink_width(self, scale: float = 1.0):
        target_width = self._calculate_target_width(scale=scale)
        self.setFixedWidth(target_width)


class ValidButton(StyleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._is_valid = False

        self.update_style_sheet(
            styles={"background-color": "rgb(95, 95, 95)"},
            action="pressed",
        )
        self.update_style_sheet(
            styles={"background-color": "rgb(123, 123, 123)"},
            action="checked",
        )  # checked state is the valid state

        self.setCheckable(True)
        self.clicked.connect(self._enforce_checked_state)

    @property
    def is_valid(self):
        return self._is_valid

    def setCheckable(self, arg__1):
        super().setCheckable(True)

    def set_valid(self, state: bool = True):
        self.setChecked(state)
        self._is_valid = state

    def set_invalid(self):
        self.set_valid(False)

    @Slot()
    def _enforce_checked_state(self):
        self.setChecked(self.is_valid)
