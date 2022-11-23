import sys
from time import sleep

from PyQt5.QtCore import *
from PyQt5.QtCore import Qt, QEvent, QMimeData
from PyQt5.QtGui import *
from PyQt5.QtGui import QDrag
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QScrollArea, QFrame, QGridLayout, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from geolocation import Location


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.browser = None
        self.setWindowTitle("Multiple graphs in a window")
        self.setMinimumSize(2000, 1200)
        self.setAcceptDrops(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # graph window container
        self.graphContainer = QWidget()
        self.gridLayout = QGridLayout(self.graphContainer)

        self.scrollArea.setWidget(self.graphContainer)
        self.layout.addWidget(self.scrollArea)

        # Initialize object Location
        self.location = Location()
        # Get object API
        self.location.get_api()
        self.c = 0

        self.charData = [[self.location.dist_arr, self.location.idle_arr, self.location.dist_start_arr],
                         [self.location.alt_arr, self.location.elev_arr, self.location.na_arr]]
        self.createGraphs()
        self.create_map()

        self.timer = QTimer()
        self.timer.setInterval(self.location.sampling_time * 1000)
        self.timer.timeout.connect(self.update_map)
        self.timer.start()

    def update_map(self):
        # Get cellular information
        self.location.get_iphone()

        if self.c < 1:
            self.location.init_location()

            # Initialize local view map
            self.location.print_map()

        else:
            # Get location information from cellular
            self.location.get_location()

            self.location.update_map()

        self.location.ned_coordinates()

        print("Geodetic coords:", self.location.lat, self.location.lon, self.location.alt, end=" | ")
        print("Travelled distance:", self.location.dist, end=" | ")
        print("Idle time:", self.location.idle)
        print("Speed:", self.location.speed, end=" | ")
        print("Acceleration:", self.location.accel, end=" | ")
        print("Distance from current position:", self.location.dist_starting_pos, end=" | ")
        print("Altitude:", self.location.alt, end=" | ")
        print("Elevation:", self.location.elevation)
        print()

        # Save map to location.html
        self.location.save_map()
        self.browser.setUrl(QUrl(
            "http://localhost:63342/FinalProject/location.html?_ijt=at5eo0mv8c4qppaav4jejlvfuq&_ij_reload=RELOAD_ON_SAVE"))

        sleep(2)
        self.c += 1

        self.location.update_arrays()
        self.charData = [[self.location.dist_arr, self.location.idle_arr, self.location.dist_start_arr],
                         [self.location.alt_arr, self.location.elev_arr, self.location.na_arr]]
        self.createGraphs()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            self.mousePressEvent(event)
        elif event.type() == QEvent.MouseMove:
            self.mouseMoveEvent(event)
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            coord = event.windowPos().toPoint()
            self.targetIndex = self.getWindowIndex(coord)
        else:
            self.targetIndex = None

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.targetIndex is not None:
            windowItem = self.gridLayout.itemAt(self.targetIndex)

            drag = QDrag(windowItem)

            pix = windowItem.itemAt(0).widget().grab()

            mimeData = QMimeData()
            mimeData.setImageData(pix)

            drag.setMimeData(mimeData)
            drag.setPixmap(pix)
            drag.setHotSpot(event.pos())
            drag.exec_()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.source().geometry().contains(event.pos()):
            targetWindowIndex = self.getWindowIndex(event.pos())
            if targetWindowIndex is None:
                return

            i, j = max(self.targetIndex, targetWindowIndex), min(self.targetIndex, targetWindowIndex)

            p1, p2 = self.gridLayout.getItemPosition(i), self.gridLayout.getItemPosition(j)
            self.gridLayout.addItem(self.gridLayout.takeAt(i), *p2)
            self.gridLayout.addItem(self.gridLayout.takeAt(j), *p1)

    def getWindowIndex(self, pos):
        for i in range(self.gridLayout.count()):
            if self.gridLayout.itemAt(i).geometry().contains(pos):
                return i

    def createGraphs(self):
        tracker = 0

        titles = [["Travelled distance", "Idle Time", "Starting Point Distance"],
                  ["Altitude", "Elevation", "Visits"]]

        labels = [["Accumulated distance [mtrs]", "Accumulated idle time [secs]", "Distance from starting pos [mtrs]"],
                  ["Altitude [mtrs]", "Elevation [mtrs]", "Visit to not allowed places [n]"]]
        for c in range(2):
            for r in range(3):
                frame = QFrame()
                frame.setStyleSheet('background-color: white;')
                frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

                frameContainer = QVBoxLayout()

                tracker += 1

                # create matplotlib graph
                figure = Figure()
                canvas = FigureCanvas(figure)  # pyqt5 widget
                ax = figure.add_subplot()
                ax.plot(self.location.time_arr, self.charData[c][r], '-')
                figure.suptitle(titles[c][r])
                figure.supxlabel("Time [secs]")
                figure.supylabel(labels[c][r])
                canvas.draw()

                # Drag and drop feature
                canvas.installEventFilter(self)

                frameContainer.addWidget(canvas)

                box = QVBoxLayout()
                box.addWidget(frame)

                self.gridLayout.addLayout(frameContainer, r, c)
                self.gridLayout.setColumnStretch(c % 2, 1)
                self.gridLayout.setRowStretch(r, 1)

    def create_map(self):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(
            "http://localhost:63342/FinalProject/location.html?_ijt=at5eo0mv8c4qppaav4jejlvfuq&_ij_reload=RELOAD_ON_SAVE"))

        self.gridLayout.addWidget(self.browser, 0, 3, 3, 3)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("App is closing")
