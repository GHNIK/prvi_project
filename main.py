
import os
import sys

import subprocess

from PySide import QtGui, QtCore
from PySide.QtCore import Qt


class MainWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle('Main Widget')
        self.setObjectName('Main Widget')
        _width, _height = 400, 400
        self.resize(_width, _height)

        layout = QtGui.QVBoxLayout()
        button = QtGui.QPushButton()
        button.setText('Start')
        button.released.connect(self._start)
        layout.addWidget(button)

        self.text_area = QtGui.QPlainTextEdit()
        self.text_area.setReadOnly(True)

        layout.addWidget(self.text_area)
        self.setLayout(layout)

        _action_quit = QtGui.QAction('Quit', self)
        _action_quit.setShortcut('Ctrl+Q')
        _action_quit.triggered.connect(self._quit)
        self.addAction(_action_quit)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._read)

        self._proc = None
        self._end = False

    def _quit(self):
        QtGui.QApplication.quit()

    def _reset(self):
        """
        reset the state so we can start another process
        """
        self.timer.stop()
        self._proc = None
        self._end = False

    def _start(self):
        """
        start the process and the timer to read from stdout
        """
        if self._proc is None:
            self._proc = subprocess.Popen(['ls',
                                           '-alh',
                                           '/'], stdout=subprocess.PIPE)
            self.timer.start(5)

    def _read(self):
        """
        read stdout/stderr
        """
        # if we have an active process
        if self._proc:
            line = self._proc.stdout.readline()
            if line != '':
                # do something with the returned line
                self.text_area.appendPlainText(line.rstrip())
            else:
                # we are done with reading everything from stdout
                self._end = True

        # test if process has finished and we reached the end of the stdout
        if not self._proc.poll() is None and self._end:
            return_text = "\n\n Process ended, return code: %i" % self._proc.returncode
            self.text_area.appendPlainText(return_text)
            self._reset()


if __name__ == '__main__':

    _main = QtGui.QApplication(sys.argv)
    _main.setApplicationName('Main Widget')

    main_widget = MainWidget()
    main_widget.show()

    sys.exit(_main.exec_())
