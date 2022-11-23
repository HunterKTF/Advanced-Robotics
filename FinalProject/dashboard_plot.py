import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QFrame, QGridLayout, QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt, QEvent, QMimeData, QTimer
from PyQt5.QtGui import QDrag
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import os
from random import randint


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('black')

        pen = pg.mkPen(color=(255, 255, 255))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
