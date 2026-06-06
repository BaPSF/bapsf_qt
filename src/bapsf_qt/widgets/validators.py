"""
A collection of `PySide6` `~PySide6.QtGui.QValidator` sub-class widgets.
"""

__all__ = ["IPv4Validator"]

import logging
import re

from PySide6.QtGui import QValidator


class IPv4Validator(QValidator):
    def __init__(self, logger=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

        log_name = "" if logger is None else f"{logger.name}."
        log_name += "IPv4Validator"
        self._logger = logging.getLogger(log_name)

    def validate(self, arg__1: str, arg__2: int) -> object:
        string = arg__1.replace("_", "")

        match = self._pattern.fullmatch(string)
        if match is None:
            self._logger.warning(f"IP address is invalid, '{string}'.")
            return QValidator.State.Intermediate

        return QValidator.State.Acceptable
