"""
A collection of styling (non-active) based `PySide6` widgets.
"""
from __future__ import annotations

__all__ = ["HLinePlain", "VLinePlain"]

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class HLinePlain(QFrame):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)

        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        self.set_color(125, 125, 125)

    def setLineWidth(self, arg__1: int):
        super().setLineWidth(arg__1)
        if self.lineWidth() != self.midLineWidth():
            self.setMidLineWidth(arg__1)

    def setMidLineWidth(self, arg__1: int):
        super().setMidLineWidth(arg__1)
        if self.lineWidth() != self.midLineWidth():
            self.setLineWidth(arg__1)

    def set_color(self, r: int, g: int, b: int):
        palette = self.palette()
        palette.setColor(palette.ColorRole.WindowText, QColor(r, g, b))
        self.setPalette(palette)


class VLinePlain(QFrame):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)

        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        self.set_color(125, 125, 125)

    def setLineWidth(self, arg__1: int):
        super().setLineWidth(arg__1)
        if self.lineWidth() != self.midLineWidth():
            self.setMidLineWidth(arg__1)

    def setMidLineWidth(self, arg__1: int):
        super().setMidLineWidth(arg__1)
        if self.lineWidth() != self.midLineWidth():
            self.setLineWidth(arg__1)

    def set_color(self, r: int, g: int, b: int):
        palette = self.palette()
        palette.setColor(palette.ColorRole.WindowText, QColor(r, g, b))
        self.setPalette(palette)
