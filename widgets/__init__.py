from logging import getLogger
logger = getLogger(__name__)

from typing import TypeVar, Generic, List, Callable, Iterable
from enum import Enum
from PySide import QtGui, QtCore
from scene import Node
from observable_property import Prop, ListProp, ListPropEvent, RGBAf


class SceneTreeWidget(QtGui.QWidget):
    def __init__(self, parent, scene)->None:
        super().__init__(parent)
        self.scene = scene

        vbox = QtGui.QVBoxLayout(self)
        self.setLayout(vbox)

        # background color
        self.background_color = self.create_backbround_color()
        vbox.addWidget(self.background_color)

        # gizmo tree
        self.gizmo_tree = self.create_gizmo_tree()
        vbox.addWidget(self.gizmo_tree)

        # scene tree
        self.scene_tree = self.create_scene_tree()
        vbox.addWidget(self.scene_tree)

    def create_gizmo_tree(self)->QtGui.QWidget:
        self.gizmos_prop = ListProp(self.scene.gizmos)
        gizmo_tree = QtGui.QTreeWidget(self)
        gizmo_tree.setHeaderLabels(["name"])

        def from_prop(event: ListPropEvent, nodes: Iterable[Node]):
            logger.info('%s: %s', event, nodes)
        self.gizmos_prop.connect(from_prop)

        return gizmo_tree

    def create_scene_tree(self)->QtGui.QWidget:
        self.nodes_prop = ListProp(self.scene.nodes)
        scene_tree = QtGui.QTreeWidget(self)
        scene_tree.setHeaderLabels(["name"])

        return scene_tree

    def create_backbround_color(self)->QtGui.QWidget:
        background_color = QtGui.QPushButton(self)

        def from_prop(value: RGBAf):
            int_color = ",".join(str(int(255 * x)) for x in value[:3])
            background_color.setStyleSheet(
                f'background-color: rgb({int_color})')
        self.scene.background_color.connect(from_prop)

        def background_color_clicked():
            color = QtGui.QColorDialog.getColor()
            self.scene.background_color.value = RGBAf(
                color.redF(), color.greenF(), color.blueF(), color.alphaF())
        background_color.clicked.connect(background_color_clicked)

        return background_color
