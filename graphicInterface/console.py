from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QTextCursor
import datetime
import time
import os


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


class suppress_stdout_stderr(object):
    """
        A context manager for doing a "deep suppression" of stdout and stderr in
        Python, i.e. will suppress all print, even if the print originates in a
        compiled C/Fortran sub-function.
        This will not suppress raised exceptions, since exceptions are printed
        to stderr just before a script exits, and after the context manager has
        exited.
    """

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        for fd in self.null_fds + self.save_fds:
            os.close(fd)