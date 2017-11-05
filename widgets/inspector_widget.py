from logging import getLogger
logger = getLogger(__name__)

from PySide import QtGui


class InspectorWidget(QtGui.QWidget):
    def __init__(self, parent)->None:
        super().__init__(parent)
        pass
