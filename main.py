from logging import getLogger, Handler, DEBUG, WARNING, ERROR
logger = getLogger(__name__)

import sys
import pathlib
from PySide import QtGui, QtCore

import glglue.pysidegl
from scene import Scene


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

    def write(self, m):
        pass


class MainWindow(QtGui.QMainWindow):
    def __init__(self, scene: Scene):
        super().__init__()
        self._open_dir=None
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
        filename, _ = QtGui.QFileDialog.getOpenFileName(self,
                                                        'Open file', 
                                                        str(self._open_dir) if self._open_dir else None,
                                                        'Models(*.obj);;Images (*.png *.xpm *.jpg)')
        if not filename:
            return

        path = pathlib.Path(filename)
        self._open_dir = path.parent
        logger.info('open %s', path)
        # self.scene.open(path)


def main():
    from logging import basicConfig
    basicConfig(level=DEBUG)

    scene = Scene()

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(scene)
    # add handler to rootLogger
    getLogger('').addHandler(window.log_handler)
    logger.debug('set logger')

    window.show()
    window.resize(640, 480)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
