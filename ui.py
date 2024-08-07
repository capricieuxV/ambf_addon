import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import bpy

class CubeAdder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Add Cube to Blender')

        layout = QVBoxLayout()
        
        self.add_button = QPushButton('Add Cube')
        self.add_button.clicked.connect(self.add_cube)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_cube(self):
        bpy.ops.mesh.primitive_cube_add()
        print("Cube added to Blender.")

def run_qt_app():
    app = QApplication(sys.argv)
    ex = CubeAdder()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_qt_app()
