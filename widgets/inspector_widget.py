from logging import getLogger
logger = getLogger(__name__)

from typing import List

from PySide import QtGui, QtCore

from scene import Node, MeshComponent

from renderer import Drawer


class VertexModel(QtCore.QAbstractTableModel):
    def __init__(self, mesh: Drawer)->None:
        super().__init__()
        self.mesh = mesh


class MeshComponentWidget(QtGui.QWidget):
    def __init__(self, parent: QtGui.QWidget, mesh: MeshComponent)->None:
        super().__init__(parent)
        self.mesh = mesh
        layout = QtGui.QVBoxLayout(self)
        self.setLayout(layout)

        label = QtGui.QLabel('Mesh')
        label.setStyleSheet('background-color:gray; color:white;')
        layout.addWidget(label)

        # Topology
        topology_layout = QtGui.QHBoxLayout(self)
        topology_layout.addWidget(QtGui.QLabel('topology'))
        topology = QtGui.QLineEdit(self)
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


class InspectorWidget(QtGui.QWidget):
    def __init__(self, parent)->None:
        super().__init__(parent)
        self.component_widgets: List[QtGui.QWidget] = []

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

        # compoonent placeholder
        self.component_layout = QtGui.QVBoxLayout(self)
        layout.addLayout(self.component_layout)

        layout.addStretch(1)

    def set_node(self, node: Node)->None:
        # clear
        for x in self.component_widgets:
            self.component_layout.removeWidget(x)

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
