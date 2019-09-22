from graphicInterface.plotInteractiveFigure import PlotInteractiveFigure
from pointRegistration.batchRegistration import BatchRegistrationThread
from pointRegistration.registration import Registration
from graphicInterface.plotFigure import PlotFigure
from graphicInterface.upperToolbar import *
from graphicInterface.console import Logger
from pointRegistration.model import Model
from PyQt5.QtWidgets import QMessageBox
import os
import threading


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        Logger.addRow(str("Starting up.."))
        self.source_model = Model(os.path.join(".", "data", "avgModel_bh_1779_NE.mat"))
        self.target_model = None
        self.initUI()
        self.registration_thread = None
        Logger.addRow(str("Ready."))

    def initUI(self):
        # Griglia centrale con i due plot
        grid_central = QGridLayout(self)
        self.setLayout(grid_central)
        self.sx_widget = PlotInteractiveFigure(self, self.source_model, title="Source")
        self.dx_widget = PlotFigure(self, None, title="Target")
        grid_central.addWidget(self.sx_widget, 1, 0, 1, 2)
        self.sx_widget.draw_data()
        grid_central.addWidget(self.dx_widget, 1, 2, 1, 2)
        self.dx_widget.draw_data()
        self.toolbar = UpperToolbar(self)
        grid_central.addWidget(self.toolbar, 0, 0, 1, 4)
        grid_central.setRowStretch(0, 1)
        grid_central.setRowStretch(1, 30)

        # Contenitore per i controlli

    def load_target(self, path):
        self.target_model = Model(path)
        self.dx_widget.load_model(self.target_model)
        self.dx_widget.draw_data()
        Logger.addRow(str("File loaded correctly: " + path))
        self.toolbar.save_target_btn.setEnabled(True)

    def load_source(self, path):
        self.source_model = Model(path)
        self.sx_widget.load_model(self.source_model)
        self.sx_widget.draw_data()
        Logger.addRow(str("File loaded correctly: " + path))

    def restore_highlight(self):
        self.sx_widget.highlight_data([-1])

    def landmark_selected(self, colors):
        self.dx_widget.set_landmarks_colors(colors)

    def data_selected(self, x_coord, y_coord, width, height):    # apply color to target
        self.dx_widget.select_area(x_coord, y_coord, width, height)

    def registrate(self, method, percentage):
        if not self.sx_widget.there_are_points_highlighted():  # names are everything
            QMessageBox.critical(self, 'Error', "No rigid points have been selected.")
            raise Exception("No rigid points selected")

        if self.registration_thread is None and self.sx_widget.there_are_points_highlighted():
            self.parent().setStatus("Busy...")
            self.registration_thread = Registration(method, self.sx_widget.model, self.target_model, percentage,
                                                    self.registrate_callback, self.dx_widget.update_plot_callback)
            self.registration_thread.start()

    def stop_registration_thread(self):
        if self.registration_thread is not None:
            Logger.addRow(str("Trying to stop registration thread..."))
            self.registration_thread.stop()

    def save_displacement_map(self):
        filters = "Serialized Python Obj (*.pickle)"
        filename = self.save_dialog(filters)
        if filename is not None:
            self.target_model.save_displacement_map(filename)

    def save_target(self):
        if self.target_model is None:
            QMessageBox.critical(self, 'Error', "The source model was not registered yet.")
            return

        filters = "MAT File (*.mat);;OFF File (*.off);;"
        filename = self.save_dialog(filters)
        if filename is not None:
            self.dx_widget.model.save_model(filename)

    def save_dialog(self, filters):
        dlg = QFileDialog()
        options = dlg.Options()
        options |= dlg.DontUseNativeDialog
        filename, ext = dlg.getSaveFileName(self, None, "Save model", filter=filters, options=options)

        if filename:
            if ext.find(".off") >= 0 and filename.find(".off") < 0:
                filename += ".off"
            if ext.find(".mat") >= 0 and filename.find(".mat") < 0:
                filename += ".mat"
            if ext.find(".pickle") >= 0 and filename.find(".pickle") < 0:
                filename += ".pickle"
            return filename
        return None

    def registrate_callback(self, model):
        Logger.addRow(str("Registration completed."))
        self.target_model = model
        self.target_model.bgImage = self.dx_widget.bgImage
        self.dx_widget.load_model(self.target_model)
        self.dx_widget.show_displacement()
        self.dx_widget.draw_data()
        self.parent().setStatusReady()
        self.registration_thread = None
        self.toolbar.registBTN.setEnabled(True)
        self.toolbar.stopBTN.setEnabled(False)
        self.toolbar.save_displacement_btn.setEnabled(True)

    def registrate_batch_callback(self):
        try:
            Logger.addRow(str("Registration completed."))
            self.registration_thread = None
            self.parent().setStatus("Ready.")
        except Exception as ex:
            print(ex)

    def registrate_batch(self, method, percentage, filenames):

        if not self.sx_widget.there_are_points_highlighted():  # names are everything
            QMessageBox.critical(self, 'Error', "No rigid points have been selected.")
            raise Exception("No rigid points selected")

        if self.registration_thread is None and self.sx_widget.there_are_points_highlighted():
            self.parent().setStatus("Busy...")

            self.registration_thread = BatchRegistrationThread(self.sx_widget.model, filenames, percentage,
                                                               self.registrate_batch_callback)
            self.registration_thread.start()

    @staticmethod
    def savelog_onfile():
        Logger.save_log()
