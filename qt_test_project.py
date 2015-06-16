

import os
import sys

# use if use PyQt4 (linux)
# from PyQt4 import QtCore, QtGui
# from PyQt4.QtCore import Qt

from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from stylesheet import STYLESHEET


class App(QtGui.QWidget):


    def __init__(self,parent=None):
        super(App, self).__init__(parent)
        self.setWindowTitle('testApp')
        self.setStyleSheet(STYLESHEET)
	self.setMinimumWidth (400)
	
        main_layout = QtGui.QVBoxLayout()

        self.button = QtGui.QPushButton('Exit')
        button2 = QtGui.QPushButton('Button2')
        self.button.released.connect(self._exit)
        button2.released.connect(self._test)

        text = QtGui.QPlainTextEdit()
        text.setPlainText('test string start')
        text.setReadOnly(True)

        self.tableview = QtGui.QTableView()
        self.model = QtGui.QStandardItemModel()
        self.tableview.setModel(self.model)


        h_header = self.tableview.horizontalHeader()

        main_layout.addWidget(self.button)
        main_layout.addWidget(button2)
        main_layout.addWidget(text)
        main_layout.addWidget(self.tableview)

        self.setLayout(main_layout)

        timer = QtCore.QTimer()
        # timer.singleShot(500,self._exit)

    def _exit(self):
        QtGui.QApplication.quit()

    def _test(self):
        # self.button.released.emit()
        row = []
        for i in range(3):
            row_item = QtGui.QStandardItem()
            row_item.setText('test item: %i' %i)
            row.append(row_item)

        self.model.appendRow(row)
        self.model.setHeaderData(0, Qt.Horizontal,"Name")


if __name__ == '__main__':

    _app = QtGui.QApplication(sys.argv)
    _app.setApplicationName('testApp')

    myProgram = App()
    myProgram.show()

    sys.exit(_app.exec_())
