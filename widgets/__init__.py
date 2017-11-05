from logging import getLogger
logger = getLogger(__name__)

from typing import TypeVar, Generic, List, Callable, Iterable
from enum import Enum
from PySide import QtGui, QtCore


T = TypeVar('T')


class Prop(Generic[T]):

    def __init__(self, value: T, callbacks: Iterable[Callable[[T], None]] = None)->None:
        self._value = value
        self.callbacks: List[Callable[[T], None]] = [x for x in callbacks] if callbacks else []

    def connect(self, callback: Callable[[T], None])->None:
        callback(self._value)
        self.callbacks.append(callback)

    @property
    def value(self)->T:
        return self._value

    @value.setter
    def value(self, value: T):
        if self._value == value:
            return
        self._value = value
        self.emit(self._value)

    def emit(self, value: T):
        # logger.debug('emit')
        for x in self.callbacks:
            x(value)


class ListPropEvent(Enum):
    Updated = 0
    Added = 1
    Removed = 2
    Cleared = 3


class ListProp(Generic[T]):
    def __init__(self, values: List[T])->None:
        self.values: List[T] = values[:]
        self.callbacks: List[Callable[[ListPropEvent, Iterable[T]], None]] = []

    def connect(self, callback: Callable[[ListPropEvent, Iterable[T]], None])->None:
        callback(ListPropEvent.Updated, self.values)
        self.callbacks.append(callback)


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

        return gizmo_tree

    def create_scene_tree(self)->QtGui.QWidget:
        self.nodes_prop = ListProp(self.scene.nodes)
        scene_tree = QtGui.QTreeWidget(self)
        scene_tree.setHeaderLabels(["name"])

        return scene_tree

    def create_backbround_color(self)->QtGui.QWidget:
        self.background_color_prop = Prop[QtGui.QColor](
            QtGui.QColor.fromRgbF(*self.scene.background_color))
        background_color = QtGui.QPushButton(self)

        def from_prop(value: QtGui.QColor):
            background_color.setStyleSheet(
                f'background-color: rgb({value.red()}, {value.green()}, {value.blue()})')
            self.scene.background_color = (
                value.redF(), value.greenF(), value.blueF(), value.alphaF())
        self.background_color_prop.connect(from_prop)

        '''
        def x()->None:
            pass
        self.background_color_prop.connect(x)
        '''

        def background_color_clicked():
            self.background_color_prop.value = QtGui.QColorDialog.getColor()
        background_color.clicked.connect(background_color_clicked)

        return background_color
