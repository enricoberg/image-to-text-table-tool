import sys, json
from PyQt5 import QtWidgets, QtCore, QtGui
#from PIL import ImageGrab



class ToolWindow(QtWidgets.QWidget):
    overlay_mode=None

    def __init__(self):        
        super().__init__()  
        self.setGeometry(0, 0, QtWidgets.QApplication.desktop().screenGeometry().width(),
                         QtWidgets.QApplication.desktop().screenGeometry().height())      
        
        
    
    def set_overlay_view(self):
        self.overlay_mode=True        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.rectangles = []
        self.squares = []
        self.update_rectangles()
        self.update()
        self.show()

    def set_drawing_view(self):
        self.overlay_mode=False        
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.squares = []
        self.rectangles = []
        self.setWindowOpacity(0.05)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.update()
        self.show()
        



    def update_rectangles(self):
        with open("rectangles_coordinates.json", "r") as file:
            data = json.load(file)
            for obj in data:
                self.add_rectangle(QtCore.QRect(obj["x"], obj["y"], obj["width"], obj["height"]))    

    def clear_rectangles(self):
        self.rectangles=[]
        self.update()

    def add_rectangle(self, rect):
        self.rectangles.append(rect)
        self.update()

    def paintEvent(self, event):
        if self.overlay_mode==True:
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, 128), 3, QtCore.Qt.SolidLine))
            for rect in self.rectangles:
                painter.drawRect(rect)
        else:
            qp = QtGui.QPainter(self)
            qp.setPen(QtGui.QPen(QtGui.QColor('red'), 5))
            qp.setBrush(QtGui.QColor(128, 128, 255, 128))
            for rect in self.squares:
                qp.drawRect(rect)
            if self.begin and self.end:
                qp.drawRect(QtCore.QRect(self.begin, self.end))

    def keyPressEvent(self, event):
        if self.overlay_mode==True:
            if event.key() == QtCore.Qt.Key_Escape:
                QtWidgets.qApp.quit()
            elif event.key() == QtCore.Qt.Key_Return:
                print("Enter key pressed")
            elif event.key() == QtCore.Qt.Key_N:
                self.clear_rectangles()
                self.set_drawing_view()
                print("N pressed")
        else:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                self.save_snapshots()
    
    def mousePressEvent(self, event):
        if self.overlay_mode==False:
            self.begin = event.pos()
            self.end = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if self.overlay_mode==False:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.overlay_mode==False:
            x1 = min(self.begin.x(), self.end.x())
            y1 = min(self.begin.y(), self.end.y())
            x2 = max(self.begin.x(), self.end.x())
            y2 = max(self.begin.y(), self.end.y())

            self.squares.append(QtCore.QRect(x1, y1, x2 - x1, y2 - y1))
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            self.update()

    def save_snapshots(self):
        data = []
        for i, rect in enumerate(self.squares):
            x1, y1, width, height = rect.getRect()
            data.append({"Rectangle": i + 1, "x": x1, "y": y1, "width": width, "height": height})

        with open('rectangles_coordinates.json', 'w') as json_file:
            json.dump(data, json_file)        
        self.set_overlay_view()




if __name__ == '__main__':  
    overlay_mode=True     
    app = QtWidgets.QApplication(sys.argv)
    window=ToolWindow()   
    if overlay_mode==False:
        window.set_overlay_view()
    else:
        window.set_drawing_view()
    window.show()
    sys.exit(app.exec_())
    