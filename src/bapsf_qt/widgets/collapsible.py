
__all__ = ["QVCollapsible"]

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMainWindow,
    QLayout,
    QSizePolicy,
    QLabel,
    QHBoxLayout,
    QSpacerItem
)

from bapsf_qt.buttons import StyleButton

# import of qtawesome must happen after the PySide6 imports
import qtawesome as qta  # noqa


class QVCollapsibleHeaderButton(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(parent)

        self._RIGHT_ARROW = qta.icon("mdi.arrow-right-bold-circle-outline")
        self._DOWN_ARROW = qta.icon("mdi.arrow-down-bold-circle")

        if not isinstance(text, str):
            text = ""

        self.button_text = self._init_button_text(text)
        self.icon_label = self._init_icon_label()
        self.icon_spacer = QSpacerItem(
            self.icon_label.pixmap().width(),
            0,
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )

        self._init_self()
        self.setLayout(self._define_layout())
        self._connect_signals()

    def _connect_signals(self):
        self.toggled.connect(self._handle_toggle)

    def _define_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addSpacerItem(
            QSpacerItem(6, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        )
        layout.addWidget(
            self.icon_label,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )
        layout.addWidget(
            self.button_text,
            alignment=Qt.AlignmentFlag.AlignCenter,
            stretch=1,
        )
        layout.addSpacerItem(self.icon_spacer)
        layout.addSpacerItem(
            QSpacerItem(6, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        )
        return layout

    def _init_icon_label(self):
        icon = QLabel(parent=self)
        icon.setObjectName("collapsible_icon")
        icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        size = self._get_font_pixel_size()
        icon.setPixmap(self._RIGHT_ARROW.pixmap(size, size))
        return icon

    def _init_button_text(self, text: str):
        label = QLabel(text, parent=self)
        label.setObjectName("collapsible_text")
        label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _init_self(self):
        self.setCheckable(True)
        self.setChecked(False)
        self.setStyleSheet("""
        QVCollapsibleHeaderButton {
            border: 1px solid rgb(123, 123, 123);
            border-radius: 2px;
            padding: 6px 0px 6px 0px;
        }
        QVCollapsibleHeaderButton:hover {
            border: 2px solid rgb(30, 60, 90);
            border-radius: 4px;
        }
        QLabel#collapsible_icon {
            padding: 0px;
            margin: 0px;
        }
        QLabel#collapsible_text {
            padding: 0px;
            margin: 0px;
        }
        """)

    def is_collapsed(self) -> bool:
        return not self.isChecked()

    def set_collapsed(self, collapsed: bool):
        if not isinstance(collapsed, bool):
            return

        self.setChecked(not collapsed)

        arrow = self._RIGHT_ARROW if collapsed else self._DOWN_ARROW
        size = self._get_font_pixel_size()
        self.icon_label.setPixmap(arrow.pixmap(size, size))
        self.icon_spacer.changeSize(self.icon_label.pixmap().width(), 0)

    def _get_font_pixel_size(self):
        font = self.button_text.font()
        metrics = QFontMetrics(font)
        size = metrics.height()
        print(f"font size is {size}")
        return size

    def _handle_toggle(self):
        self.blockSignals(True)
        self.set_collapsed(self.is_collapsed())
        self.blockSignals(False)

    def font(self, /):
        return self.button_text.font()

    def setFont(self, arg__1, /):
        self.button_text.setFont(arg__1)

    def setText(self, text: str, /):
        self.button_text.setText(text)


class QVCollapsible(QWidget):

    def __init__(self, header_text: str, parent: QWidget | None = None):
        super().__init__(parent)

        self.header_toggle = self._init_header_toggle(header_text)
        self.content_widget = self._init_content_widget()

        self.setLayout(self._define_layout())
        self._connect_signals()

    def _connect_signals(self):
        self.header_toggle.toggled.connect(self._handle_toggle)

    def _define_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.header_toggle)
        layout.addWidget(self.content_widget)
        return layout

    def _init_content_widget(self):
        content = QWidget(parent=self)
        content.setVisible(False)
        return content

    def _init_header_toggle(self, header_txt: str):
        toggle = QVCollapsibleHeaderButton(header_txt, parent=self)
        toggle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        font = toggle.font()
        font.setPointSize(12)
        font.setBold(True)
        toggle.setFont(font)

        return toggle

    def is_collapsed(self) -> bool:
        return not self.header_toggle.isChecked()

    def set_collapsed(self, collapsed: bool):
        if not isinstance(collapsed, bool):
            return

        self.header_toggle.setChecked(not collapsed)
        self.content_widget.setVisible(not collapsed)

    def set_content_widget(self, widget: QWidget):
        if not isinstance(widget, QWidget):
            return

        old_widget = self.content_widget
        self.content_widget = None

        old_widget.close()
        old_widget.deleteLater()

        self.content_widget = widget
        self.content_widget.setVisible(not self.is_collapsed())

    def set_content_layout(self, layout: QLayout):
        if not isinstance(layout, QLayout):
            return

        if isinstance(self.content_widget.layout(), QLayout):
            return

        self.content_widget.setLayout(layout)

    def _handle_toggle(self):
        self.header_toggle.blockSignals(True)
        self.set_collapsed(self.is_collapsed())
        self.header_toggle.blockSignals(False)


class _QVCollapsibleDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        self._define_main_window()

        self.btn_1 = StyleButton("BTN_1", parent=self)
        self.btn_2 = StyleButton("BTN_2", parent=self)
        self.btn_3 = StyleButton("BTN_3", parent=self)
        self.btn_4 = StyleButton("BTN_4", parent=self)
        self.btn_5 = StyleButton("BTN_5", parent=self)
        self.collapsible_area1 = self._init_collapsible1_area()
        self.collapsible_area2 = self._init_collapsible2_area()

        widget = QWidget()
        widget.setLayout(self._define_layout())
        self.setCentralWidget(widget)

        self._connect_signals()

    def _connect_signals(self): ...

    def _define_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(self.collapsible_area1)
        layout.addWidget(self.collapsible_area2)
        layout.addStretch()
        return layout

    def _define_main_window(self):
        self.setWindowTitle("DEMO QToggleSwitch")
        self.resize(300, 150)
        self.setMinimumHeight(200)
        self.setContentsMargins(12, 12, 12, 12)

    def _define_collapsible1_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(self.btn_1)
        layout.addSpacing(4)
        layout.addWidget(self.btn_2)
        layout.addSpacing(4)
        layout.addWidget(self.btn_3)
        layout.addStretch(1)
        return layout

    def _define_collapsible2_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(self.btn_4)
        layout.addSpacing(4)
        layout.addWidget(self.btn_5)
        layout.addStretch(1)
        return layout

    def _init_collapsible1_area(self):
        collapsible = QVCollapsible("Section 1", parent=self)
        collapsible.set_content_layout(self._define_collapsible1_layout())

        return collapsible

    def _init_collapsible2_area(self):
        collapsible = QVCollapsible("Section 2", parent=self)
        collapsible.set_content_layout(self._define_collapsible2_layout())

        return collapsible


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    window = _QVCollapsibleDemo()
    window.show()

    app.exec()
