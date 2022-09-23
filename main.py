import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidgetItem
import pandas as pd
import wine_type_list


class MainForm(QDialog):

    def __init__(self):
        super(MainForm, self).__init__()
        loadUi("main_form.ui", self)
        self.tableWidget.setRowCount(7)
        for row in range(7):
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(row, 0, chkBoxItem)

        self.tableWidget.setItem(0, 1, QTableWidgetItem("red meat"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("beef lamb, venison"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("cured meat"))
        self.tableWidget.setItem(1, 2, QTableWidgetItem("salami, prosciutto, bacon"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("pork"))
        self.tableWidget.setItem(2, 2, QTableWidgetItem("roast, tenderloin, pork chops"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("poultry"))
        self.tableWidget.setItem(3, 2, QTableWidgetItem("chicken, duck, turkey"))
        self.tableWidget.setItem(4, 1, QTableWidgetItem("mollusk"))
        self.tableWidget.setItem(4, 2, QTableWidgetItem("oyster, mussel, clam"))
        self.tableWidget.setItem(5, 1, QTableWidgetItem("fish"))
        self.tableWidget.setItem(5, 2, QTableWidgetItem("tuna, trout, cod, bass"))
        self.tableWidget.setItem(6, 1, QTableWidgetItem("shellfish"))
        self.tableWidget.setItem(6, 2, QTableWidgetItem("shrimp, crab, lobster"))

        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(2)

        self.tableWidget.itemClicked.connect(self.item_click)
        self.tableWidget.cellClicked.connect(self.cell_click)

    def item_click(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            row = item.row()
            self.tableWidget
        else:
            print("unclicked")

    def cell_click(self, row, col):
        print(f"cell clicked, row {row}, col {col}")


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
