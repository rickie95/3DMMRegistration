import os
from graphicInterface.plot_interactive_figure import PlotInteractiveFigure
from graphicInterface.rotatable_figure import RotatableFigure
from graphicInterface.show_displacement import DisplacementMapWindow
from graphicInterface.upper_toolbar import *
from pointRegistration.batchRegistration import BatchRegistrationThread
from pointRegistration.model import Model
from pointRegistration.registration import Registration


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        Logger.addRow(str("Starting up.."))
        self.source_model = Model(os.path.join(".", "data", "avgModel_bh_1779_NE.mat"))
        self.target_model = None
        self.sx_widget = None
        self.dx_widget = None
        self.registration_thread = None
        self.toolbar = None
        self.registrated = None
        Logger.addRow(str("Ready."))
        self.initUI()

    def initUI(self):
        grid_central = QGridLayout(self)
        self.setLayout(grid_central)
        self.sx_widget = PlotInteractiveFigure(self, self.source_model, title="Source")
        self.dx_widget = RotatableFigure(self, None, title="Target")
        grid_central.addWidget(self.sx_widget, 1, 0, 1, 2)
        self.sx_widget.draw_data()
        grid_central.addWidget(self.dx_widget, 1, 2, 1, 2)
        self.dx_widget.draw_data()
        self.toolbar = UpperToolbar(self)
        grid_central.addWidget(self.toolbar, 0, 0, 1, 4)
        grid_central.setRowStretch(0, 1)
        grid_central.setRowStretch(1, 30)

    def load_target(self):
        filters = "OFF Files (*.off);;WRML Files (*.wrml);;MAT Files (*.mat)"
        file_name = load_file_dialog(self, filters)
        if file_name is None:
            return

        self.toolbar.start_registration_button.setEnabled(True)
        self.target_model = Model(file_name)
        self.dx_widget.load_model(self.target_model)
        self.dx_widget.draw_data(clear=True)
        Logger.addRow(str("File loaded correctly: " + file_name))
        self.toolbar.save_target_btn.setEnabled(True)

    def load_source(self):
        filters = "OFF Files (*.off);;WRML Files (*.wrml);;MAT Files (*.mat)"
        file_name = load_file_dialog(self, filters)
        if file_name is None:
            return

        self.toolbar.start_registration_button.setEnabled(True)
        self.source_model = Model(file_name)
        self.sx_widget.load_model(self.source_model)
        self.sx_widget.draw_data()
        Logger.addRow(str("File loaded correctly: " + file_name))

    def restore(self):
        self.restore_highlight()
        if self.dx_widget.has_model():
            self.restore_target()
            self.toolbar.start_registration_button.setEnabled(True)

    def restore_highlight(self):
        self.sx_widget.highlight_data([-1])

    def restore_target(self):
        self.dx_widget.restore_model()

    def landmark_selected(self, colors):
        self.dx_widget.set_landmarks_colors(colors)

    def data_selected(self, x_coord, y_coord, width, height):    # apply color to target
        self.dx_widget.select_area(x_coord, y_coord, width, height)

    def registrate(self, method, percentage):
        if not self.sx_widget.there_are_points_highlighted():  # names are everything
            QMessageBox.critical(self, 'Error', "No rigid points have been selected.")
            raise Exception("No rigid points selected")

        if self.dx_widget.model is None:
            QMessageBox.critical(self, 'Error', "Please, load a target model.")
            raise Exception("Target model is not present.")

        if self.registration_thread is None:
            self.toolbar.show_displacement_btn.setEnabled(False)
            self.parent().setStatus("Busy...")
            self.registration_thread = Registration(method, self.source_model, self.target_model, percentage,
                                                    self.registration_completed_callback,
                                                    self.dx_widget.update_plot_callback)
            self.registration_thread.start()

    def stop_registration_thread(self):
        if self.registration_thread is not None:
            Logger.addRow(str("Trying to stop registration thread..."))
            self.registration_thread.stop()

    def show_displacement_map(self):
        DisplacementMapWindow(self.parent(), self.source_model.compute_displacement_map(self.target_model, 3))  # FIXME
        self.parent().setStatusReady()

    def save_target(self):
        if self.target_model is None:
            QMessageBox.critical(self, 'Error', "The source model was not registered yet.")
            return

        filters = "MAT File (*.mat);;OFF File (*.off);;"
        filename = save_file_dialog(self, filters)
        if filename is None:
            return
        self.target_model.save_model(filename) #fixme controllare che venga realmente salvato

    def registration_completed_callback(self, model):
        Logger.addRow(str("Registration completed."))
        self.target_model.bgImage = self.dx_widget.bgImage
        self.dx_widget.clear()

        self.dx_widget.set_secondary_model(model)
        self.dx_widget.load_model(self.target_model)
        self.target_model = model

        self.dx_widget.draw_data()
        self.parent().setStatusReady()
        self.registration_thread = None
        self.toolbar.stop_registration_button.setEnabled(False)
        self.toolbar.show_displacement_btn.setEnabled(True)
        self.registrated = True
        self.parent().setStatus("Registration completed, displacement map available. Click Show Displacement Map.")
        # Target and Source are now plotted in target widget

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
