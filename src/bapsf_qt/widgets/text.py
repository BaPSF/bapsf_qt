from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QLineEdit


class QLineEditSpecialized(QLineEdit):
    editingFinishedPayload = Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.editingFinished.connect(self._send_payload)

    @Slot()
    def _send_payload(self):
        self.editingFinishedPayload.emit(self)
