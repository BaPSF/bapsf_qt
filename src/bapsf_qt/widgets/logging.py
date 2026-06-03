"""
`PySide6` widgets for displaying messages issued by the Python
`logging` package.
"""
__all__ = ["QLogHandler"]

import logging

from PySide6.QtWidgets import QTextEdit, QPlainTextEdit


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
