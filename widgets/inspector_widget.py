from logging import getLogger
logger = getLogger(__name__)

from PySide import QtGui, QtCore

from scene import Node


class InspectorWidget(QtGui.QWidget):
    def __init__(self, parent)->None:
        super().__init__(parent)

        layout = QtGui.QVBoxLayout(self)
        self.setLayout(layout)

        form_layout = QtGui.QFormLayout(self)
        # name
        self.name = QtGui.QLineEdit(self)
        form_layout.addRow(QtGui.QLabel('name'), self.name)

        # pos
        self.translation = QtGui.QLineEdit(self)
        form_layout.addRow(QtGui.QLabel('translation'), self.translation)

        # rotation
        self.rotation = QtGui.QLineEdit(self)
        form_layout.addRow(QtGui.QLabel('rotation'), self.rotation)

        layout.addLayout(form_layout)
        layout.addStretch(1)

    def set_node(self, node: Node)->None:
        if not node:
            return

        self.name.setText(node.name)
        self.translation.setText(str(node.model.pos))
        self.rotation.setText(str(node.model.rot))
