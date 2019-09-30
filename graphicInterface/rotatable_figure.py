from graphicInterface.plot_button_collection import PlotButtonCollection
from graphicInterface.plotFigure import PlotFigure


class RotatableFigure(PlotFigure):

    def __init__(self, parent, model=None, landmarks=True, title=None):
        super().__init__(parent, model, landmarks, title)

    def rotate(self, axis, theta):
        if self.model is not None:
            self.model.rotate(axis, theta)
            self.draw_data()

    def load_model(self, model):
        super().load_model(model)
        PlotButtonCollection(self.rotate, self)