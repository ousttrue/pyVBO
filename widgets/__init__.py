from logging import getLogger
logger = getLogger(__name__)

from PySide import QtGui, QtCore


class Prop:
    def __init__(self, initial):
        self._value = initial
        self.callbacks = []

    def connect(self, callback):
        callback(self._value)
        self.callbacks.append(callback)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._value == value:
            return
        self._value = value
        self.emit(self._value)

    def emit(self, value):
        logger.debug('emit')
        for x in self.callbacks:
            x(value)


class SceneTreeWidget(QtGui.QWidget):
    def __init__(self, parent, scene):
        super().__init__(parent)
        self.scene = scene

        vbox = QtGui.QVBoxLayout(self)
        self.setLayout(vbox)

        # background color
        self.background_color_prop = Prop(
            QtGui.QColor.fromRgbF(*self.scene.background_color))
        self.background_color = QtGui.QPushButton(self)

        def set_color(value: QtGui.QColor):
            self.background_color.setStyleSheet(
                f'background-color: rgb({value.red()}, {value.green()}, {value.blue()})')
            self.scene.background_color = (
                value.redF(), value.greenF(), value.blueF(), value.alphaF())
        self.background_color_prop.connect(set_color)

        def background_color_clicked():
            self.background_color_prop.value = QtGui.QColorDialog.getColor()
        self.background_color.clicked.connect(background_color_clicked)
        vbox.addWidget(self.background_color)
