import sys

from PyQt5.QtGui import QFont
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidgetItem, QProgressBar
import pandas as pd
import wine_type_list


class MainForm(QDialog):
    # initialize empty DataFrame
    # selected_data = pd.DataFrame()
    # making data frame from csv file
    data = pd.read_csv("food_wine_pairing.csv", encoding='unicode_escape')
    # these are the broad categories making up each table in the UI
    category = ["meat", "preparation", "dairy", "vegetable", "seasoning", "starch", "sweets"]
    # we're going to loop through the categories list one category at a time, starting at index 0
    category_index = 0
    # a list to keep track of everything user selects over multiple screens
    selections = []

    def __init__(self):
        # initialize empty DataFrame
        # self.selected_data = pd.DataFrame()
        # making data frame from csv file
        # self.data = pd.read_csv("food_wine_pairing.csv", encoding='unicode_escape')

        super(MainForm, self).__init__()
        loadUi("main_form.ui", self)
        self.fill_table(self.category[self.category_index])

        self.tableWidget.cellClicked.connect(self.cell_click)
        self.btnNext.clicked.connect(self.button_click)

    def resize_cols(self):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.resizeColumnToContents(i)
        # self.tableWidget.resizeColumnToContents(0)
        # self.tableWidget.resizeColumnToContents(1)
        # self.tableWidget.resizeColumnToContents(2)

    def fill_table(self, category):
        # The choices for a given category, e.g., for category 'preparation' there's grilled, poached, etc.
        _choices = self.data.loc[self.data['category'] == category]
        # Convert choices into a [list]
        _choices_list = _choices.name.to_list()
        # These are the examples that go with each choice; some choices don't have examples, e.g., 'potato'
        _examples_list = _choices.examples.to_list()
        self.tableWidget.setRowCount(len(_choices_list))

        for _choice in _choices_list:
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.CheckState.Unchecked)
            i = _choices_list.index(_choice)
            self.tableWidget.setItem(i, 0, chkBoxItem)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(_choices_list[i]))
            # if there's an example, print it
            # cells without values, however, can be evaluated as NaN (like null)--which is bad
            # also, there's the issue of cells that are blank but still have a space, tab, or other invisible character
            if not (pd.isnull(_examples_list[i]) or _examples_list[i].isspace()):
                self.tableWidget.setItem(i, 2, QTableWidgetItem(_examples_list[i]))
            else:
                self.tableWidget.setItem(i, 2, QTableWidgetItem(''))

        self.resize_cols()

    def cell_click(self, row, col):
        # user clicks on a column other than the one with checkbox
        if col != 0:
            # determine whether the row's already got a checkmark, i.e., been selected by user
            _checkState = self.tableWidget.item(row, 0).checkState()
            # gotta be careful with the order of the IF statements here!
            # if the row's already been selected twice, got back to the initial unchecked/unbolded state
            if _checkState == QtCore.Qt.Checked and self.tableWidget.item(row, 1).font().bold():
                self.tableWidget.item(row, 0).setCheckState(QtCore.Qt.Unchecked)
                font = QFont()
                font.setBold(False)
                self.tableWidget.item(row, 1).setFont(font)
                self.tableWidget.item(row, 2).setFont(font)
            # if this is the first time the row's been checked, add a checkmark
            elif _checkState == QtCore.Qt.Unchecked:
                self.tableWidget.item(row, 0).setCheckState(QtCore.Qt.Checked)
            # if it's already got a checkmark, make it bold
            elif _checkState == QtCore.Qt.Checked:
                font = QFont()
                font.setBold(True)
                self.tableWidget.item(row, 1).setFont(font)
                self.tableWidget.item(row, 2).setFont(font)
        self.resize_cols()





    def button_click(self):
        _selected_items = []
        # make a list with everything user selected in the displayed table
        # if row is bolded, count that selection twice, i.e., weight the selection
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0).checkState() == QtCore.Qt.Checked:
                _selected_items.append(self.tableWidget.item(row, 1).text())
            if self.tableWidget.item(row, 1).font().bold():
                _selected_items.append(self.tableWidget.item(row, 1).text())
        # add user selections to the master list with all user selections
        self.selections.extend(_selected_items)
        # display the next table
        self.category_index = self.category_index + 1
        if self.category_index <= len(self.category) - 1:
            self.fill_table(self.category[self.category_index])
        # if the last table has already been displayed
        else:
            self.process_selections()

    def process_selections(self):
        _selected_items_df = pd.DataFrame()
        for item in self.selections:
            temp = self.data.loc[self.data['name'] == item]
            _selected_items_df=pd.concat([_selected_items_df, temp])
        print(_selected_items_df)
        # _selected_items_df = self.data.loc[self.data['name'].isin(self.selections)]
        # .sum() adds the values in each column
        # .sort_values(ascending=False) sorts the values (duh) and displays from highest to lowest
        display = _selected_items_df.sum(numeric_only=True).sort_values(ascending=False)

        # display.index is a list of all the series' indexes, i.e., in this case, names of the wine categories
        top_pairing = display.index[0]  # so this is the first wine name on the list, the top pair
        print("The best matching wine category for this meal is " + top_pairing.upper())
        s = ''
        examples_list = wine_type_list.wine_types[top_pairing]
        for item in examples_list:
            if examples_list.index(item) < len(examples_list) - 1:
                s += item + ", "
            else:
                s += "and " + item
        print("Examples include " + s)
        # without .to_string() the info is displayed with an added Type:int64 attribute at the end
        # see https://stackoverflow.com/questions/53025207/how-do-i-remove-name-and-dtype-from-pandas-output
        print(f"Here is the complete pairing list (higher numbers are better matches.\n{display.to_string()}\n\n")
        # load sorted list of wines into table
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        # this provides a list of the wines themselves; they're the indexes on the dataframe called "display"
        _wine_list = display.index.tolist()
        # and this provides a list of the numbers, i.e., the sum of the values for each wine
        _value_list = display.values
        self.tableWidget.setRowCount(len(_wine_list))
        for item in _wine_list:
            i = _wine_list.index(item)
            pbar = QProgressBar(self)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(_wine_list[i]))
            match = int((_value_list[i]*100)/(len(_selected_items_df.index)*2))
            pbar.setValue(match)
            self.tableWidget.setCellWidget(i, 1, pbar)
        self.resize_cols()









# main
app = QApplication(sys.argv)
main_form = MainForm()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main_form)
widget.show()
try:
    sys.exit(app.exec_())
except SystemExit:
    print("Exiting")
