"""
`PySide6` widgets for displaying messages issued by the Python
`logging` package.
"""
__all__ = ["QLogHandler", "QLogger"]

import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QTextEdit,
    QPlainTextEdit,
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QSlider,
)


class QLogHandler(logging.Handler):

    def __init__(self, log_widget: QTextEdit | QPlainTextEdit, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(log_widget, (QTextEdit, QPlainTextEdit)):
            raise TypeError(
                f"Expected an instance of 'QTextEdit' or 'QPlainTextEdit', "
                f"but received type {type(log_widget)}."
            )
        self._log_widget = log_widget

    @property
    def log_widget(self) -> QTextEdit | QPlainTextEdit:
        return self._log_widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)

        if isinstance(self.log_widget, QTextEdit):
            self.log_widget.append(msg)
        elif isinstance(self.log_widget, QPlainTextEdit):
            self.log_widget.appendPlainText(msg)

    def handle(self, record: logging.LogRecord) -> None:
        self.emit(record)


class QLogger(QWidget):
    _verbosity = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }

    def __init__(
        self,
        logger: logging.Logger,
        parent: QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._logger = logger  # type: logging.Logger

        # TEXT WIDGETS
        _label = QLabel("LOG", parent=self)
        _font = _label.font()
        _font.setPointSize(14)
        _font.setBold(True)
        _label.setFont(_font)
        self.title_txt = _label

        self.slider_labels = []
        for text in self._verbosity.keys():
            _label = QLabel(text, parent=self)
            _label.setAlignment(
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            )
            _label.setMinimumWidth(24)

            font = _label.font()
            font.setPointSize(12)
            _label.setFont(font)

            self.slider_labels.append(_label)

        # ADVANCED WIDGETS

        slider = QSlider(Qt.Orientation.Horizontal, parent=self)
        slider.setMinimum(1)
        slider.setMaximum(4)
        slider.setTickInterval(1)
        slider.setSingleStep(1)
        slider.setTickPosition(slider.TickPosition.TicksBelow)
        slider.setFixedHeight(16)
        slider.setMinimumWidth(100)
        slider.setValue(2)  # logging.INFO
        self.slider_widget = slider

        log_widget = QTextEdit(parent=self)
        log_widget.setReadOnly(True)
        font = log_widget.font()
        font.setPointSize(10)
        font.setFamily("Courier New")
        log_widget.setFont(font)
        self.log_widget = log_widget

        self._handler = self._setup_log_handler()  # type: QLogHandler

        self.setLayout(self._define_layout())
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.slider_widget.valueChanged.connect(self.update_log_verbosity)

    @property
    def handler(self) -> QLogHandler:
        return self._handler

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def _define_layout(self):
        slider_layout = QGridLayout()
        slider_layout.addWidget(self.slider_widget, 0, 1, 1, 6)
        for ii, lw in enumerate(self.slider_labels):
            slider_layout.addWidget(lw, 1, 2 * ii, 1, 2)

        layout = QVBoxLayout()
        layout.addWidget(
            self.title_txt,
            alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )
        layout.addLayout(slider_layout)
        layout.addWidget(self.log_widget)

        return layout

    def _setup_log_handler(self):
        handler = QLogHandler(log_widget=self.log_widget)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s - [%(levelname)s] { %(name)s }  %(message)s",
                datefmt="%H:%M:%S",
            ),
        )
        vindex = self.slider_widget.value() - 1
        vkey = list(self._verbosity.keys())[vindex]
        handler.setLevel(self._verbosity[vkey])
        self.logger.addHandler(handler)

        return handler

    @Slot()
    def update_log_verbosity(self):
        vindex = self.slider_widget.value() - 1
        vkey = list(self._verbosity.keys())[vindex]

        self.handler.setLevel(self._verbosity[vkey])

        self.logger.info(f"Changed log verbosity to {vkey} ({self._verbosity[vkey]}).")
