from logging import getLogger
logger = getLogger(__name__)

import sys
from PySide import QtGui  # , QtCore

import glglue.pysidegl
from scene import Scene


class MainWindow(QtGui.QMainWindow):
    def __init__(self, scene: Scene):
        super().__init__()
        self.setWindowTitle('pyVboViewer')
        # setup opengl widget
        self.glwidget = glglue.pysidegl.Widget(self, scene)
        self.setCentralWidget(self.glwidget)


def main():
    from logging import DEBUG, basicConfig
    basicConfig(level=DEBUG)

    scene = Scene()

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(scene)
    window.show()
    window.resize(640, 480)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
