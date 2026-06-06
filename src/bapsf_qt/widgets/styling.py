"""
A collection of styling (non-active) based `PySide6` widgets.
"""

from __future__ import annotations

__all__ = ["HLinePlain", "VLinePlain", "QTAIconLabel"]

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QFrame, QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget

# import of qtawesome must happen after the PySide6 imports
import qtawesome as qta  # noqa


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


class QTAIconLabel(QLabel):
    def __init__(self, icon_name: str, parent: QWidget | None = None):
        super().__init__(parent=parent)

        self._icon_name = None
        self._icon = None
        self.setIcon(icon_name)

        self.setFixedSize(32)
        self.setIconSize(28)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

    @property
    def icon_name(self) -> str:
        return self._icon_name

    @property
    def icon(self) -> QIcon:
        return self._icon

    def _get_icon(self):
        return qta.icon(self._icon_name)

    def setIcon(self, icon_name: str):  # noqa
        try:
            _icon = qta.icon(icon_name)
        except Exception:  # noqa
            return

        self._icon_name = icon_name
        self._icon = _icon

    def setIconSize(self, size: int):  # noqa
        if not isinstance(size, int):
            return
        elif size < 1:
            return

        self.setPixmap(self.icon.pixmap(size, size))

    def setFixedSize(self, size: QSize | int):
        if isinstance(size, QSize):
            pass
        elif not isinstance(size, int):
            return
        elif size < 1:
            return
        else:
            size = QSize(size, size)

        super().setFixedSize(size)

    def setFixedWidth(self, w: int):
        self.setFixedSize(w)

    def setFixedHeight(self, h: int):
        self.setFixedSize(h)
