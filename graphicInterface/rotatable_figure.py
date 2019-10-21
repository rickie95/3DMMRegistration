from graphicInterface.plot_button_collection import PlotButtonCollection
from graphicInterface.plot_figure import PlotFigure


class RotatableFigure(PlotFigure):

    def __init__(self, parent, model=None, landmarks=True, title=None):
        super().__init__(parent, model, landmarks, title)
        self.rotate_buttons = None

    def rotate(self, axis, theta, registered=False):
        if self.model is not None:
            if registered:
                self.rotate_view(axis, theta)
            else:
                self.model.rotate(axis, theta)
            self.draw(clear=True)

    def load_model(self, model):
        super().load_model(model)
        if self.rotate_buttons is None:
            self.rotate_buttons = PlotButtonCollection(self.rotate, self)

    def rotate_view(self, axis, theta):
        data = self.scatter.get_offsets()
        data = self.model.rotate_model(axis, theta, data)
        self.load_data()