"""
`PySide6` widgets for displaying messages issued by the Python
`logging` package.
"""

__all__ = ["QLogHandler", "QLogger"]

import logging
import logging.config

from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from typing import List


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

        # instantiate logger
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger("QLogger")
        self._logger = logger  # type: logging.Logger

        # Initialize Widgets
        self.title_txt = self._init_title_txt()
        self.slider_labels = self._init_slider_labels()
        self.slider_widget = self._init_slider_widget()
        self.log_widget = self._init_log_widget()

        # setup log handler
        # - this needs to happen after slider_widget and log_widget is initialized
        self._handler = self._setup_log_handler()  # type: QLogHandler

        self.setLayout(self._define_layout())
        self._connect_signals()

        if self.logger.name == "QLogger":
            self.logger.warning(
                "The given logger was invalid.  Created a "
                "logging.Logger instance named 'QLogger' in its place "
                "that is available via the `QLogger.logger` property."
            )

    def _init_title_txt(self) -> QLabel:
        _label = QLabel("LOG", parent=self)
        _font = _label.font()
        _font.setPointSize(14)
        _font.setBold(True)
        _label.setFont(_font)
        return _label

    def _init_slider_labels(self) -> List[QLabel]:
        slider_labels = []
        for text in self._verbosity.keys():
            _label = QLabel(text, parent=self)
            _label.setAlignment(
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            )
            _label.setMinimumWidth(24)

            font = _label.font()
            font.setPointSize(12)
            _label.setFont(font)

            slider_labels.append(_label)

        return slider_labels

    def _init_slider_widget(self) -> QSlider:
        slider = QSlider(Qt.Orientation.Horizontal, parent=self)
        slider.setMinimum(1)
        slider.setMaximum(4)
        slider.setTickInterval(1)
        slider.setSingleStep(1)
        slider.setTickPosition(slider.TickPosition.TicksBelow)
        slider.setFixedHeight(16)
        slider.setMinimumWidth(100)
        slider.setValue(2)  # logging.INFO
        return slider

    def _init_log_widget(self) -> QPlainTextEdit:
        log_widget = QPlainTextEdit(parent=self)
        log_widget.setReadOnly(True)
        font = log_widget.font()
        font.setPointSize(10)
        font.setFamily("Courier New")
        log_widget.setFont(font)
        log_widget.setUndoRedoEnabled(False)
        return log_widget

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


class DemoQLogger(QMainWindow):
    def __init__(self):
        super().__init__()

        logging.config.dictConfig(self._logging_config_dict)
        self._logger = logging.getLogger(":: GUI ::")

        # Instantiate widgers
        self.message_input = self._init_message_input()
        self.log_level_select = self._init_log_level_select()
        self.qlogger = self._init_qlogger()
        self.auto_log_cb = self._init_auto_log_cb()
        self.auto_log_timer = QTimer(parent=self, singleShot=True)
        self.auto_log_interval = 100  # in msec
        self.auto_log_counter = 1

        self._define_main_window()

        widget = QWidget()
        widget.setLayout(self._define_layout())
        self.setCentralWidget(widget)

        self._connect_signals()

    def _init_message_input(self) -> QLineEdit:
        message_input = QLineEdit(parent=self)
        message_input.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        message_input.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        return message_input

    def _init_log_level_select(self) -> QComboBox:
        log_level_select = QComboBox(parent=self)
        log_level_select.addItems(list(QLogger._verbosity.keys()))
        log_level_select.setEditable(False)
        log_level_select.setCurrentText(log_level_select.itemText(0))
        return log_level_select

    def _init_qlogger(self) -> QLogger:
        qlogger = QLogger(self._logger, parent=self)
        qlogger.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Ignored,
        )
        return qlogger

    def _init_auto_log_cb(self) -> QCheckBox:
        auto_log_cb = QCheckBox("Generate Auto-Log Messages", parent=self)
        font = auto_log_cb.font()
        font.setPointSize(12)
        auto_log_cb.setFont(font)
        auto_log_cb.setCheckState(Qt.CheckState.Unchecked)
        return auto_log_cb

    def _connect_signals(self) -> None:
        self.message_input.returnPressed.connect(self.enter_log)
        self.auto_log_timer.timeout.connect(self._make_auto_log_entry)
        self.auto_log_cb.checkStateChanged.connect(self.start_stop_auto_log)

    def _define_main_window(self):
        self.setWindowTitle("DEMO QLogger")
        self.resize(800, 900)
        self.setMinimumHeight(600)
        self.setContentsMargins(12, 12, 12, 12)

    def _define_layout(self):

        # first row: Title
        label = QLabel("DEMO    QLogger")
        font = label.font()
        font.setPointSize(14)
        font.setBold(True)
        label.setFont(font)
        header_label = label

        label = QLabel("Message:  ")
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)

        cb_layout = QHBoxLayout()
        cb_layout.setContentsMargins(0, 0, 0, 0)
        cb_layout.addSpacerItem(
            QSpacerItem(78, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        )
        cb_layout.addWidget(self.auto_log_cb)
        cb_layout.addStretch(1)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.addWidget(label)
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.log_level_select)

        # add logger
        qlogger_frame = QFrame(parent=self)
        qlogger_frame.setObjectName("qlogger_frame")
        qlogger_frame.setStyleSheet("""
        QFrame#qlogger_frame {
            border: 3px solid rgb(60, 60, 60);
            border-radius: 5px;
            padding: 24px;
            margin: 0px;
        }""")
        qlogger_frame.setLayout(QVBoxLayout())
        qlogger_frame.layout().addWidget(self.qlogger)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(
            header_label,
            alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        )
        layout.addSpacing(24)
        layout.addLayout(cb_layout)
        layout.addSpacing(8)
        layout.addLayout(input_layout)
        layout.addSpacing(24)
        layout.addWidget(qlogger_frame)

        return layout

    @property
    def _logging_config_dict(self):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "class": "logging.Formatter",
                    "format": "%(asctime)s - [%(levelname)s] %(name)s  %(message)s",
                    "datefmt": "%H:%M:%S",
                },
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "level": "WARNING",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "stderr": {
                    "class": "logging.StreamHandler",
                    "level": "ERROR",
                    "formatter": "default",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                "": {  # root logger
                    "level": "WARNING",
                    "handlers": ["stderr", "stdout"],
                    "propagate": True,
                },
                ":: GUI ::": {
                    "level": "DEBUG",
                    "handlers": ["stderr"],
                    "propagate": True,
                },
            },
        }

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @Slot()
    def _make_auto_log_entry(self):
        self.logger.info(f"--- auto log entry {self.auto_log_counter} ---")
        self.auto_log_counter += 1

        check_state = self.auto_log_cb.isChecked()
        if check_state:
            # keep the auto log runing
            self.auto_log_timer.start(self.auto_log_interval)

    @Slot()
    def start_stop_auto_log(self):
        timer_active = self.auto_log_timer.isActive()
        check_state = self.auto_log_cb.isChecked()

        # timer is active and needs to be turned off
        if timer_active and not check_state:
            self.auto_log_timer.stop()
            return

        # timer is not active and needs to be started
        if not timer_active and check_state:
            self.auto_log_timer.start(self.auto_log_interval)
            return

        # the other two case need no further action
        # 1. timer is active and needs to be running
        # 2. time is inactive and needs to be stopped
        #
        return

    @Slot()
    def enter_log(self):
        message = self.message_input.text()
        lvl_key = self.log_level_select.currentText()
        level = QLogger._verbosity[lvl_key]

        self.logger.log(level=level, msg=message)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    window = DemoQLogger()
    window.show()

    app.exec()
