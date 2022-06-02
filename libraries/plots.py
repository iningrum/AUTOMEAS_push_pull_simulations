import matplotlib.pyplot as plt
class MatrixPlot:
    def __init__(self, rows, columns, title):
        self.columns = columns -1
        self.rows = rows -1 # pyplot counts from 1, we count from 0
        self.unpopulated  = (0, 0)
        self.figure, self.axis = plt.subplots(rows, columns)
        self.figure.suptitle(title)
    def AddPlot(self, X, Y, trace_color, title_xlabel_ylabel, xlimit_low_high = None, ylimit_low_high = None):
        if self.unpopulated is None:
            return None
        free_row, free_column = self.unpopulated
        graph = self.axis[free_row, free_column]
        graph.plot(X, Y, color = trace_color)
        # Titles
        title, x_label, y_label = title_xlabel_ylabel
        graph.set_title(title)
        graph.set_xlabel(x_label)
        graph.set_ylabel(y_label)
        # XY limits
        if xlimit_low_high:
            graph.set_xlim(list(xlimit_low_high))
        if ylimit_low_high:
            graph.set_ylim(list(ylimit_low_high))
        # calculate next free
        if free_row +1 > self.rows:
            self.unpopulated = (0, free_column+1) if not (free_column+1 > self.columns) else None
        else:
            self.unpopulated = (free_row+1, free_column)