"""
Foundational / core buttons.  These inherit directly from
`~PySide6.QtWidgets.QPushButton` and are intended to help design other
button classes.
"""

__all__ = ["StyleButton"]

from PySide6.QtWidgets import QPushButton


class StyleButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._default_base_style = {
            "border-radius": "4px",
            f"border": f"2px solid rgb(123, 123, 123)",
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
