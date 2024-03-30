import  json
from PyQt5 import QtWidgets, QtCore, QtGui


class OverlayWidget(QtWidgets.QWidget):


    def __init__(self):
        
        super().__init__()
        self.setGeometry(0, 0, QtWidgets.QApplication.desktop().screenGeometry().width(),
                         QtWidgets.QApplication.desktop().screenGeometry().height())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.rectangles = []

    def add_rectangle(self, rect):
        self.rectangles.append(rect)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(33, 213, 177, 128), 4, QtCore.Qt.SolidLine))
        for rect in self.rectangles:
            painter.drawRect(rect)

    def update_rectangles(self):
        self.rectangles=[]
        with open("rectangles_coordinates.json", "r") as file:
            data = json.load(file)
        for obj in data:
            self.add_rectangle(QtCore.QRect(obj["x"], obj["y"], obj["width"], obj["height"]))   





            


   
       

    

