from __future__ import annotations

__all__ = ["QToggleSwitch"]

from PySide6.QtCore import (
    Property,
    Qt,
    QSize,
    QPropertyAnimation,
    QEasingCurve,
    QRect,
    QPointF,
    Slot,
)
from PySide6.QtWidgets import QCheckBox, QMainWindow, QHBoxLayout, QWidget
from PySide6.QtGui import QColor, QPainter, QPen, QBrush
from typing import TYPE_CHECKING

from bapsf_qt.buttons.indicators import LED

if TYPE_CHECKING:
    from PySide6.QtCore import QPoint
    from PySide6.QtGui import QResizeEvent


class QToggleSwitch(QCheckBox):
    # Adapted from Martin Čáp
    # github: https://github.com/martincap94
    # blog: https://www.martincap.io/posts/qtoggle/

    _DEFAULT_ANIMATION_DURATION = 200  # in msec
    _DEFAULT_HANDLE_REL_SIZE = 0.82
    _DEFAULT_PREFERRED_HEIGHT = 20
    _DEFAULT_TEXT_SIDE_PADDING = 8

    def __init__(
        self,
        checked_text: str = "",
        unchecked_text: str = "",
        checked_color: QColor = QColor(0, 176, 255),
        unchecked_color: QColor = QColor(180, 180, 180),
        font_height_fill: float = 0.5,
        parent: QWidget | None = None,
    ):
        super().__init__(parent=parent)

        for state, text in zip(
            ("Checked", "Unchecked"),
            (checked_text, unchecked_text),
        ):
            if not isinstance(text, str):
                raise TypeError(
                    f"{state} text must be a string, got type {type(text)}."
                )

        for state, color in zip(
            ("Checked", "Unchecked"),
            (checked_color, unchecked_color),
        ):
            if not isinstance(color, QColor):
                raise TypeError(
                    f"{state} color must be a QColor instance, got type {type(color)}."
                )

        if not isinstance(font_height_fill, (float, int)):
            raise TypeError(
                f"Argument 'font_height_fill' must be a number, "
                f"got type {type(font_height_fill)}."
            )
        font_height_fill = float(font_height_fill)
        if not (0 < font_height_fill <= 1):
            raise ValueError(
                f"Argument 'font_height_fill' must be a number in the "
                f"range (0, 1], got {font_height_fill}."
            )

        self._checked_text = checked_text
        self._unchecked_text = unchecked_text
        self._font_height_fill = font_height_fill

        self._toggle_fractional_position = 0
        self._animation = QPropertyAnimation(self, b"toggle_fractional_position")
        self._animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._animation.setDuration(self._DEFAULT_ANIMATION_DURATION)

        # configure self
        self._checked_setup = self._build_checked_state_setup(checked_color)
        self._unchecked_setup = self._build_checked_state_setup(unchecked_color)
        self._handle_check_state_text()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # connect signals
        self.stateChanged.connect(self._handle_checked_state_changed)

    def _handle_check_state_text(self):
        text = self._checked_text if self.isChecked() else self._unchecked_text
        self.setText(text)

    @Property(float)
    def toggle_fractional_position(self):
        return self._toggle_fractional_position

    @toggle_fractional_position.setter
    def toggle_fractional_position(self, position):
        self._toggle_fractional_position = position
        self.update()

    def resizeEvent(self, event: QResizeEvent):
        font = self.font()
        font.setBold(True)
        font.setPixelSize(int(event.size().height() * self._font_height_fill))
        self.setFont(font)
        
        super().resizeEvent(event)

    def sizeHint(self):
        max_text_width = float("-inf")
        for text in [self._checked_text, self._unchecked_text]:
            text_qsize = self.fontMetrics().size(Qt.TextFlag.TextSingleLine, text)
            max_text_width = max(max_text_width, text_qsize.width())

        # We use _DEFUALT_PREFERRED_HEIGHT to prevent users from
        # shooting themselves in the foot (visually).
        preferred_height = max(self.minimumHeight(), self._DEFAULT_PREFERRED_HEIGHT)

        # The 1.2 is a magic number creating some padding for the text so
        # that big letters do not overflow the rounded corners.
        return QSize(
            int(
                preferred_height
                + max_text_width * 1.2
                + self._DEFAULT_TEXT_SIDE_PADDING
            ),
            preferred_height,
        )

    def hitButton(self, pos: QPoint):
        """Define the clickable area of the checkbox."""
        # Utilized by parent class AbstractButton
        return self.contentsRect().contains(pos)

    def _handle_checked_state_changed(self, state):
        self._animation.stop()
        if bool(state):
            self._animation.setEndValue(1)
        else:
            self._animation.setEndValue(0)
        self._animation.start()

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        content_box = self.contentsRect()
        diameter = content_box.height()
        radius = diameter / 2

        # Determine current text based on handle position
        # during the animation - switch it right in the middle.
        if self._toggle_fractional_position > 0.5:
            current_text = self._checked_text
        else:
            current_text = self._unchecked_text

        # Determine used brushes based on check state.
        if self.isChecked():
            body_brush = self._checked_setup["body_brush"]
            handle_brush = self._checked_setup["handle_brush"]
        else:
            body_brush = self._unchecked_setup["body_brush"]
            handle_brush = self._unchecked_setup["handle_brush"]

        # Draw the toggle's body.
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(body_brush)
        painter.drawRoundedRect(content_box, radius, radius)
        painter.setPen(QPen(handle_brush.color().darker(110)))
        painter.setBrush(handle_brush)

        # Draw the text.
        painter.save()
        textPosMultiplier = 1.0 - self._toggle_fractional_position
        textRectX = (
            diameter * textPosMultiplier
            + self._DEFAULT_TEXT_SIDE_PADDING * self._toggle_fractional_position
        )
        textRectWidth = content_box.width() - diameter - self._DEFAULT_TEXT_SIDE_PADDING
        textRect = QRect(textRectX, 0, textRectWidth, content_box.height())
        if self.isEnabled():
            # Trick for fading the text through the handle during transition.
            text_opacity = abs(0.5 - self._toggle_fractional_position) * 2
        else:
            # Override text opacity for disabled toggle.
            text_opacity = 0.5
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor.fromRgbF(0, 0, 0, text_opacity)))
        painter.drawText(textRect, Qt.AlignmentFlag.AlignCenter, current_text)
        painter.restore()

        # Adjust the handle drawing brush if the toggle is not enabled.
        if not self.isEnabled():
            color = painter.brush().color()
            color.setAlphaF(0.5)
            painter.setBrush(QBrush(color))

        # Draw the handle.
        travel_distance = content_box.width() - diameter
        handlePosX = (
            content_box.x() + radius + travel_distance * self._toggle_fractional_position
        )
        handle_radius = self._DEFAULT_HANDLE_REL_SIZE * radius
        painter.drawEllipse(
            QPointF(handlePosX, content_box.center().y() + 1),
            handle_radius,
            handle_radius,
        )

        painter.restore()

    def setChecked(self, checked):
        super().setChecked(checked)

        # Ensure we are in the finished animation state if there are
        # signals blocked from the outside!
        if self.signalsBlocked():
            self._toggle_fractional_position = 1 if checked else 0

            # Ensure the toggle is updated visually even though it
            # seems this is not necessary.
            self.update()

        self._handle_check_state_text()

    @staticmethod
    def _build_checked_state_setup(color: QColor):
        return {
            "color": color,
            "handle_brush": QBrush(color),
            "body_brush": QBrush(color.lighter(170)),
        }


class _QToggleSwitchDemo(QMainWindow):

    def __init__(self):
        super().__init__()

        self._define_main_window()

        self.toggle_switch = self._init_toggle_switch()
        self.led = LED(parent=self)

        widget = QWidget()
        widget.setLayout(self._define_layout())
        self.setCentralWidget(widget)

        self._connect_signals()

    def _connect_signals(self):
        self.toggle_switch.checkStateChanged.connect(self._handle_toggle)

    def _define_layout(self):
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.toggle_switch)
        layout.addSpacing(24)
        layout.addWidget(self.led)
        layout.addStretch(1)
        return layout

    def _define_main_window(self):
        self.setWindowTitle("DEMO QToggleSwitch")
        self.resize(300, 150)
        self.setMinimumHeight(200)
        self.setContentsMargins(12, 12, 12, 12)

    def _init_toggle_switch(self):
        toggle = QToggleSwitch("ON", "off", parent=self)
        # toggle.setFixedWidth(60)
        toggle.setFixedHeight(48)
        return toggle

    @Slot()
    def _handle_toggle(self):
        checked = self.toggle_switch.isChecked()
        self.led.setChecked(checked)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    window = _QToggleSwitchDemo()
    window.show()

    app.exec()
