import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget


class MainForm(QDialog):
    def __init__(self):
        super(MainForm, self).__init__()
        loadUi("main_form.ui", self)
        self.pushButton.clicked.connect(self.button_click(self.pushButton))
        self.pushButton_2.clicked.connect(self.button_click(self.pushButton_2))

    def button_click(self, button):
        s = button.text()
        print(s)
        button.setStyleSheet("background-color: rgb(135, 203, 203);")
        button.setText("* "+s+" *")


# main
app = QApplication(sys.argv)
main_form = MainForm()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main_form)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
