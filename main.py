from logging import getLogger, Handler, DEBUG, WARNING, ERROR
logger = getLogger(__name__)

import sys
import time
import pathlib

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTextEdit, QDockWidget, QFileDialog
from PyQt5.QtGui import QKeySequence, QTextCursor
from PyQt5.QtCore import Qt, QEventLoop

import glglue.pysidegl
from scene import Scene
import pyvbo
from renderer import Drawer
import shaders
from widgets import SceneTreeWidget, InspectorWidget


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

        self.widget.textCursor().movePosition(QTextCursor.Start)
        self.widget.textCursor().insertHtml(msg)
        self.widget.moveCursor(QTextCursor.End)

    def write(self, m):
        pass


class MainWindow(QMainWindow):
    def __init__(self, scene: Scene)->None:
        super().__init__()
        self.scene = scene
        self._open_dir = None
        self.setWindowTitle('pyVboViewer')
        self.menubar = self.menuBar()

        # setup opengl widget
        self.glwidget = glglue.pysidegl.Widget(self, scene)
        self.setCentralWidget(self.glwidget)

        # menu
        self.setup_file_menu()
        self.dock_menu = self.menubar.addMenu('&Dock')

        #
        # dock
        #
        # logger dock
        self.log_widget = QTextEdit(self)
        self.log_handler = QPlainTextEditLogger(self.log_widget)
        self.logger_dock = self.create_dock(
            self.log_widget, "logger", Qt.BottomDockWidgetArea)

        # scene tree dock
        self.scene_widget = SceneTreeWidget(self, scene)
        self.scene_dock = self.create_dock(
            self.scene_widget, "scene", Qt.LeftDockWidgetArea)

        # inspector dock
        self.inspector_widget = InspectorWidget(self)
        self.inspector_dock = self.create_dock(
            self.inspector_widget, "inspector", Qt.RightDockWidgetArea)

        self.scene_widget.selected.connect(self.inspector_widget.set_node)           

    def create_dock(self, widget, name, area):
        dock = QDockWidget(name, self)
        dock.setWidget(widget)
        self.addDockWidget(area, dock)
        self.dock_menu.addAction(dock.toggleViewAction())
        return dock

    def closeEvent(self, evnt):
        if self.onClosed:
            self.onClosed()
        super().closeEvent(evnt)

    def setup_file_menu(self):
        '''
        https://github.com/pyside/Examples/blob/master/examples/mainwindows/menus.py
        '''
        file_menu = self.menubar.addMenu('&File')

        openAction = QAction("&Open...", self,
                                   shortcut=QKeySequence.Open,
                                   statusTip="Open an existing file",
                                   triggered=self.open)
        file_menu.addAction(openAction)

    def open(self):
        filename, _ = QFileDialog.getOpenFileName(
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
            model.vertices[i].pos[0] *= model.metadata.to_meter
            model.vertices[i].pos[1] *= model.metadata.to_meter
            model.vertices[i].pos[2] *= model.metadata.to_meter

        mesh = Drawer.from_pmd(model, shaders.MmdShader)
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
        app.processEvents(QEventLoop.AllEvents)

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

    app = QApplication(sys.argv)
    window = MainWindow(scene)

    # add handler to rootLogger
    getLogger('').addHandler(window.log_handler)
    logger.debug('set logger')

    window.resize(1280, 720)
    window.show()

    loop(app, window, scene)
    logger.info('loop exit')
    #sys.exit(0)


if __name__ == "__main__":
    main()
