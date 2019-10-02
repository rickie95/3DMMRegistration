from graphicInterface.plot_button_collection import PlotButtonCollection
from graphicInterface.plot_figure import PlotFigure


class RotatableFigure(PlotFigure):

    def __init__(self, parent, model=None, landmarks=True, title=None):
        super().__init__(parent, model, landmarks, title)
        PlotButtonCollection(self.rotate, self)

    def rotate(self, axis, theta):
        if self.model is not None:
            self.model.rotate(axis, theta)
            self.draw_data()
