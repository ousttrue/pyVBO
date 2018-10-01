from logging import getLogger
logger = getLogger(__name__)

from typing import List

#from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QFormLayout

from scene import Node, MeshComponent

from renderer import Drawer


class VertexModel(QAbstractTableModel):
    def __init__(self, mesh: Drawer)->None:
        super().__init__()
        self.mesh = mesh

    def rowCount(self, parent: QModelIndex):
        return self.mesh.vertices.count

    def columnCount(self, index: QModelIndex):
        return len(self.mesh.vertices.layouts)

    def data(self, index: QModelIndex, role):
        if not index.isValid():
            return

        if role == Qt.DisplayRole:
            return ', '.join(str(x) for x in self.mesh.vertices.get(index.row(), index.column())).strip()


class MeshComponentWidget(QWidget):
    def __init__(self, parent: QWidget, mesh: MeshComponent)->None:
        super().__init__(parent)
        self.mesh = mesh
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        label = QLabel('Mesh')
        label.setStyleSheet('background-color:gray; color:white;')
        layout.addWidget(label)

        # Topology
        topology_layout = QHBoxLayout(self)
        topology_layout.addWidget(QLabel('topology'))
        topology = QLineEdit(self)
        topology_layout.addWidget(topology)
        topology.setText(mesh.topology.name)
        layout.addLayout(topology_layout)

        # Vertices
        vertices = QtGui.QTableView(self)
        vertices_model = VertexModel(mesh.mesh)
        vertices.setModel(vertices_model)
        layout.addWidget(vertices)

        '''
        # Indices
        indices = QtGui.QTreeView(self)
        layout.addWidget(indices)
        '''


class InspectorWidget(QWidget):
    def __init__(self, parent)->None:
        super().__init__(parent)
        self.component_widgets: List[QWidget] = []

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        form_layout = QFormLayout(self)
        # name
        self.name = QLineEdit(self)
        form_layout.addRow(QLabel('name'), self.name)

        # pos
        self.translation = QLineEdit(self)
        form_layout.addRow(QLabel('translation'), self.translation)

        # rotation
        self.rotation = QLineEdit(self)
        form_layout.addRow(QLabel('rotation'), self.rotation)

        layout.addLayout(form_layout)

        # compoonent placeholder
        self.component_layout = QVBoxLayout(self)
        layout.addLayout(self.component_layout)

        layout.addStretch(1)

    def set_node(self, node: Node)->None:
        # clear
        for x in self.component_widgets:
            x.setParent(None)
            self.component_layout.removeWidget(x)
        self.component_widgets.clear()

        if not node:
            return

        self.name.setText(node.name)
        self.translation.setText(str(node.model.pos))
        self.rotation.setText(str(node.model.rot))

        logger.debug(node.name)
        for x in node.components:
            if isinstance(x, MeshComponent):
                widget = MeshComponentWidget(self, x)
                self.component_layout.addWidget(widget)
                self.component_widgets.append(widget)
            else:
                logger.warning('unknown component: %s', x)
