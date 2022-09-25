import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidgetItem
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

        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(2)

    def cell_click(self, row, col):
        if col != 0:
            _checkState = self.tableWidget.item(row, 0).checkState()
            if _checkState == QtCore.Qt.Checked:
                self.tableWidget.item(row, 0).setCheckState(QtCore.Qt.Unchecked)
            else:
                self.tableWidget.item(row, 0).setCheckState(QtCore.Qt.Checked)

    def button_click(self):
        _selected_items = []
        # make a list with everything user selected in the displayed table
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0).checkState() == QtCore.Qt.Checked:
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
        _selected_items_df = self.data.loc[self.data['name'].isin(self.selections)]
        # select cols that contain value 1
        cols_with_1 = _selected_items_df.columns[_selected_items_df.eq(1).any()]
        # select cols that contain value 2
        cols_with_2 = _selected_items_df.columns[_selected_items_df.eq(2).any()]
        # combine cols_with_1 and cols_with_2 for everything with a 1 or 2
        # these are columns for wines that pair with everything
        # (note: the list(set()) code converts the data to a list, and also assures there are no duplicate items
        out = list(set(cols_with_2.append(cols_with_1)))
        # .sum() adds the values in each column
        # .sort_values(ascending=False) sorts the values (duh) and displays from highest to lowest
        display = _selected_items_df.sum(numeric_only=True).sort_values(ascending=False)

        # display.index is a list of all the series' indexes, i.e., in this case, names of the wine categories
        top_pairing = display.index[0]  # so this is the first wine name on the list, the top pair
        print("The best matching wine category for this meal is " + top_pairing.upper())
        s = ''
        the_list = wine_type_list.wine_types[top_pairing]
        for item in the_list:
            if the_list.index(item) < len(the_list) - 1:
                s += item + ", "
            else:
                s += "and " + item
        print("Examples include " + s)
        # without .to_string() the info is displayed with an added Type:int64 attribute at the end
        # see https://stackoverflow.com/questions/53025207/how-do-i-remove-name-and-dtype-from-pandas-output
        print(f"Here is the complete pairing list (higher numbers are better matches.\n{display.to_string()}\n\n")


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
