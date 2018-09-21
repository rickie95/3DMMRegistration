from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QTextCursor
import time
import datetime

class Logger:

    instance = None
    lock = False

    class _PrivateLog(QPlainTextEdit):

        def __init__(self):
            super().__init__()
            self.setReadOnly(True)
            self.setLineWrapMode(QPlainTextEdit.NoWrap)
            self.cursor = QTextCursor(self.document())
            self.setTextCursor(self.cursor)

        def save_onfile(self):
            now = datetime.datetime.now()
            filename = ("log-%d-%d_%d-%d-%d.txt" % (now.hour, now.minute, now.year, now.month, now.day))
            file = open(filename, "w")
            file.write(self.toPlainText())
            file.close()

    def __init__(self):
        if Logger.instance is None:
            Logger.instance = self._PrivateLog()

    @staticmethod
    def addRow(row):
        if Logger.instance is not None:
            Logger.instance.insertPlainText(row+"\n")
            time.sleep(0.1)
            Logger.instance.moveCursor(QTextCursor.End)
            time.sleep(0.1)
        print(row)

    @staticmethod
    def setParent(parent):
        if Logger.instance is not None:
            Logger.instance.setParent(parent)

    @staticmethod
    def save_log():
        if Logger.instance is not None:
            Logger.instance.save_onfile()
