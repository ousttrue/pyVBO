from logging import getLogger, Handler, DEBUG, WARNING, ERROR
logger = getLogger(__name__)

import sys
import time
import pathlib

from PySide import QtGui, QtCore
from PIL import Image

import glglue.pysidegl
from scene import Scene
import pyvbo
from renderer import Drawer, SubMesh, Texture


class QPlainTextEditLogger(Handler):
    '''
    https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
    '''

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        if not self.widget:
            print(msg)
            return

        if record.levelno == DEBUG:
            msg = f'<font color="gray">{msg}</font><br>'
        elif record.levelno == WARNING:
            msg = f'<font color="orange">{msg}</font><br>'
        elif record.levelno == ERROR:
            msg = f'<font color="red">{msg}</font><br>'
        else:
            msg = f'{msg}<br>'

        self.widget.textCursor().movePosition(QtGui.QTextCursor.Start)
        self.widget.textCursor().insertHtml(msg)
        self.widget.moveCursor(QtGui.QTextCursor.End)

    def write(self, m):
        pass


class MainWindow(QtGui.QMainWindow):
    def __init__(self, scene: Scene):
        super().__init__()
        self.scene = scene
        self._open_dir = None
        self.setWindowTitle('pyVboViewer')

        # setup opengl widget
        self.glwidget = glglue.pysidegl.Widget(self, scene)
        self.setCentralWidget(self.glwidget)

        # logger dock
        self.log_widget = QtGui.QTextEdit(self)
        self.log_handler = QPlainTextEditLogger(self.log_widget)
        self.logger_dock = QtGui.QDockWidget("logger", self)
        self.logger_dock.setWidget(self.log_widget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.logger_dock)

        self.setup_menu()

    def closeEvent(self, evnt):
        if self.onClosed:
            self.onClosed()
        super().closeEvent(evnt)

    def setup_menu(self):
        '''
        https://github.com/pyside/Examples/blob/master/examples/mainwindows/menus.py
        '''
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        openAction = QtGui.QAction("&Open...", self,
                                   shortcut=QtGui.QKeySequence.Open,
                                   statusTip="Open an existing file",
                                   triggered=self.open)
        fileMenu.addAction(openAction)

    def open(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            self, 'Open file',
            str(self._open_dir) if self._open_dir else None,
            ';;'.join([
                'Models(*.pmd *.obj)',
                'Images (*.png *.xpm *.jpg)'
            ]))
        if not filename:
            return

        path = pathlib.Path(filename)
        self._open_dir = path.parent
        logger.info('open %s', path)

        model = pyvbo.load(path)
        logger.info(model)

        # fix scale
        for i in range(len(model.vertices)):
            model.vertices[i].pos.x *= model.metadata.to_meter
            model.vertices[i].pos.y *= model.metadata.to_meter
            model.vertices[i].pos.z *= model.metadata.to_meter

        mesh = Drawer.from_pmd(model)

        def create_submesh(material):
            texture = Texture()
            if material.texture:
                texture_file = path.parent / material.texture.decode('cp932')
                if texture_file.exists():
                    logger.debug("%s exists", texture_file)
                    with texture_file.open('rb') as f:
                        image = Image.open(f)
                        image.convert('RGBA')
                    texture.create_texture(
                        image.width, image.height, image.tobytes())
                else:
                    logger.warning("%s not exists", texture_file)
            return SubMesh(self.scene.shader, material.index_count, material.color, texture)
        mesh.submeshes = [create_submesh(x) for x in model.materials]

        self.scene.add_mesh(model.metadata.name, mesh)


def loop(app, window, scene):
    # window.closeEvent.
    closed = False

    def OnWindowClosed():
        nonlocal closed
        closed = True
    window.onClosed = OnWindowClosed
    # window.closeEvent.connect(OnWindowClosed)
    app.lastWindowClosed.connect(OnWindowClosed)
    # for OpenGL
    count = 0
    last_render_time = time.clock()
    frame_time = 1 / 30
    while not closed:
        count += 1
        app.processEvents(QtCore.QEventLoop.AllEvents)

        now = time.clock()
        delta = now - last_render_time

        # update opengl
        scene.update(delta * 0.001)
        window.glwidget.update()

        sleep_time = frame_time - (time.clock() - now)
        if sleep_time > 0:
            time.sleep(sleep_time)

        last_render_time = now


def main():
    from logging import basicConfig
    basicConfig(level=DEBUG)

    scene = Scene()

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(scene)

    # add handler to rootLogger
    getLogger('').addHandler(window.log_handler)
    logger.debug('set logger')

    window.resize(640, 480)
    window.show()

    loop(app, window, scene)
    logger.info('loop exit')
    sys.exit(0)


if __name__ == "__main__":
    main()
