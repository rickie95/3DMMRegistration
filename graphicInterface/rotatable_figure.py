from graphicInterface.plot_button_collection import PlotButtonCollection
from graphicInterface.plot_figure import PlotFigure
from pointRegistration.model import Model


class RotatableFigure(PlotFigure):

    def __init__(self, parent, model=None, landmarks=True, title=None, secondary_model=None):
        self.rotate_buttons = None
        super().__init__(parent, model, landmarks, title)
        self.registered = False
        self.secondary_model = secondary_model

    def rotate(self, axis, theta, registered=False):
        if self.model is not None:
            self.clear()
            self.model.rotate(axis, theta)
            if self.secondary_model is not None:
                self.secondary_model.rotate(axis, theta)

            self.draw_data()

    def load_model(self, model):
        super().load_model(model)
        if self.rotate_buttons is None:
            self.rotate_buttons = PlotButtonCollection(self.rotate, self)

    def set_secondary_model(self, model):
        self.secondary_model = Model.from_model(model)

    def draw_data(self, clear=False):
        if self.secondary_model is not None:
            self.load_data(self.secondary_model.points, "r")
            if self.secondary_model.landmarks is not None:
                self.load_data(self.secondary_model.landmarks, "black")
        super().draw_data(clear=clear)
