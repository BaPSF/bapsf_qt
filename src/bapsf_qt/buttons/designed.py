"""
Buttons design for a specific purpose.
"""
__all__ = ["DiscardButton", "DoneButton"]
from bapsf_qt.buttons.core import AutoScaleButton


class DiscardButton(AutoScaleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_style_sheet(
            styles={
                "background-color": "rgb(232, 80, 74)",
                "color": "rgb(30, 30, 30)",
            },
            action="base",
        )
        self.update_style_sheet(
            styles={"background-color": self._default_base_style["background-color"]},
            action="disabled",
        )

        _text = self.text()
        if _text == "":
            _text = "Discard"
        self.setText(_text)


class DoneButton(AutoScaleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        _text = self.text()
        if _text == "":
            _text = "DONE"
        self.setText(_text)

    def _calculate_target_width(self, text: str | None = None, scale: float = 1.0):
        scale = 2 * scale
        return super()._calculate_target_width(text, scale=scale)
