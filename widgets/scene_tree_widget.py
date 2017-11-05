from logging import getLogger
logger = getLogger(__name__)

from typing import Iterable

from PySide import QtGui
from observable_property import ListPropEvent, RGBAf

from scene import Node


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
        gizmo_tree = QtGui.QTreeWidget(self)
        gizmo_tree.setHeaderLabels(["gizmos"])

        def from_prop(event: ListPropEvent, nodes: Iterable[Node]):
            logger.info('%s: %s', event, nodes)
            if event == ListPropEvent.Updated:
                gizmo_tree.clear()
                for x in nodes:
                    gizmo_tree.addTopLevelItem(QtGui.QTreeWidgetItem([x.name]))
            elif event == ListPropEvent.Added:
                for x in nodes:
                    gizmo_tree.addTopLevelItem(QtGui.QTreeWidgetItem([x.name]))
            else:
                logger.warning('unknown event: %s', event)

        self.scene.gizmos.connect(from_prop)

        return gizmo_tree

    def create_scene_tree(self)->QtGui.QWidget:
        scene_tree = QtGui.QTreeWidget(self)
        scene_tree.setHeaderLabels(["models"])

        def from_prop(event: ListPropEvent, nodes: Iterable[Node]):
            logger.info('%s: %s', event, nodes)
            if event == ListPropEvent.Updated:
                scene_tree.clear()
                for x in nodes:
                    scene_tree.addTopLevelItem(QtGui.QTreeWidgetItem([x.name]))
            elif event == ListPropEvent.Added:
                for x in nodes:
                    scene_tree.addTopLevelItem(QtGui.QTreeWidgetItem([x.name]))
            else:
                logger.warning('unknown event: %s', event)
        self.scene.nodes.connect(from_prop)

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
