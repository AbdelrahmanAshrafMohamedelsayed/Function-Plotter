import sys
import re
import math
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
import matplotlib.pyplot as plt
# PySide2 is a Python binding of the cross-platform GUI toolkit Qt,make you able to bild GUIs with Python.
class FunctionPlotter(QMainWindow):
    def __init__(self): # __init__ is a reseved method in python classes. It is called as a constructor in object oriented terminology. This method is called when an object is created from a class and it allows the class to initialize the attributes of the class.
        super().__init__() # super() function that will make the child class inherit all the methods and properties from its parent.
        self.setWindowTitle("Function Plotter") # setWindowTitle() sets the title of the window.
        self.setMinimumWidth(500) # setMinimumWidth() sets the minimum width of the window.
        self.setStyleSheet("QMainWindow { background-color: #f2f2f2;  }" # setStyleSheet() sets the style sheet of the window.
                           "QWidget { background-color: #f2f2f2;  }"
                           "QLabel { font-weight: bold; color: #333333; }"
                           "QLineEdit { background-color: #ffffff; color: #333333; border: 1px solid #aaaaaa; border-radius: 2px; padding: 5px;  }"
                           "QPushButton { background-color: #0088cc; color: #ffffff; border: none; padding: 5px 10px; border-radius: 2px; }"
                           "QPushButton:hover { background-color: #0077b3;  }"
                           "QPushButton:pressed { background-color: #005299; }")
        # line edits are used for user input
        self.function_label = QLabel("Enter a function of x:") # QLabel() creates a label.
        self.function_input = QLineEdit() # QLineEdit() creates a line edit.
        self.function_input.setStyleSheet("QLineEdit:focus { border: 2px solid #0088cc; }") # setStyleSheet() sets the style sheet of the line edit.
        self.min_label = QLabel("Enter the minimum value of x:") # QLabel() creates a label.
        self.min_input = QLineEdit() # QLineEdit() creates a line edit.
        self.min_input.setStyleSheet("QLineEdit:focus { border: 2px solid #0088cc; }") # setStyleSheet() sets the style sheet of the line edit.
        self.max_label = QLabel("Enter the maximum value of x:") # QLabel() creates a label.
        self.max_input = QLineEdit()
        self.max_input.setStyleSheet("QLineEdit:focus { border: 2px solid #0088cc; }") # setStyleSheet() sets the style sheet of the line edit.
        self.plot_button = QPushButton("Plot") # QPushButton() creates a push button.
        self.plot_button.setFont(QFont("Arial", 12, QFont.Bold)) # setFont() sets the font of the push button.
        
        self.figure = plt.figure() # The self.figure variable is created as an instance of the Figure class from the Matplotlib library. It represents the figure (plot) that will be displayed in the GUI.
        self.canvas = FigureCanvas(self.figure) # self.canvas variable is created as an instance of the FigureCanvas class from the Matplotlib library. It represents the canvas that will be used to display the figure (plot) in the GUI.acts as a bridge between Matplotlib and the PySide2 GUI framework.
        self.toolbar = NavigationToolbar(self.canvas, self) # The self.toolbar variable is created as an instance of the NavigationToolbar class from the Matplotlib library. It represents the toolbar that will be used to navigate the figure (plot) in the GUI.
        self.toolbar.hide()  # Initially hide the toolbar
        layout = QVBoxLayout()  # It represents a vertical box layout that will be used to arrange the GUI elements vertically.
        function_layout = QHBoxLayout() # It represents a horizontal box layout that will be used to arrange the GUI elements horizontally.
        # The function_layout variable is created as an instance of the QHBoxLayout class.
        # It represents a horizontal box layout used to arrange the function label and input field side by side.
        function_layout.addWidget(self.function_label) # addWidget() adds a widget to the layout.
        function_layout.addWidget(self.function_input) 
        layout.addLayout(function_layout)  
        layout.addWidget(self.min_label)
        layout.addWidget(self.min_input)
        layout.addWidget(self.max_label)
        layout.addWidget(self.max_input)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.plot_button.clicked.connect(self.plot_function) # The clicked signal of the plot button is connected to the plot_function method, which will be called when the button is clicked.

    def validate_input(self):
        function = self.function_input.text()
        min_value = self.min_input.text()
        max_value = self.max_input.text()

        if not function or not re.match(r"^[x0-9+\-*/^]+$", function) or re.search(r"[+\-*/^]{2,}", function) or re.search(r"\d[x]", function):
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid function.")
            return False

        if not min_value or not max_value or not re.match(r"-?\d+$", min_value) or not re.match(r"-?\d+$", max_value):
            QMessageBox.warning(self, "Invalid Input", "Please enter valid minimum and maximum values of x.")
            return False

        min_value = int(min_value)
        max_value = int(max_value)

        if min_value >= max_value:
            QMessageBox.warning(self, "Invalid Input", "The minimum value of x must be less than the maximum value.")
            return False

        return True

    def plot_function(self):
        if not self.validate_input(): # The validate_input method is called to validate the user input.
            return
        
        function = self.function_input.text() # The text method is used to get the text entered in the function input field.
        min_value = int(self.min_input.text()) # The text method is used to get the text entered in the minimum value input field.
        max_value = int(self.max_input.text())  # The text method is used to get the text entered in the maximum value input field.
        
        x = list(range(min_value, max_value + 1)) # The range function is used to generate a list of values from the minimum value of x to the maximum value of x.
        y = [] # The y variable is created as an empty list.
        
        for value in x: 
            value_str = '('+str(value)+')' # The value variable is converted to a string and stored in the value_str variable.
            expression = re.sub(r'x', value_str, function) # The re.sub function is used to replace the 'x' in the function with the value of x.re module to perform the replacement.
            expression = re.sub(r'\^', '**', expression) # The re.sub function is used to replace the '^' in the expression with '**'.
            try:
                result = eval(expression) # The eval function is used to evaluate the expression. eval function takes a string as an argument and evaluates it as a Python expression.
                y.append(result) # The result is appended to the y list.
            except (SyntaxError, ZeroDivisionError):
                QMessageBox.warning(self, "Error", f"Error evaluating the function at x = {value}") # A warning message is displayed if an error occurs while evaluating the expression.
                return
        
        self.figure.clear() #This line clears the existing figure.
        plt.plot(x, y, color='#0088cc') # The plot function is used to plot the x and y values.
        plt.xlabel('x') # The xlabel function is used to set the label of the x-axis.
        plt.ylabel('f(x)', labelpad=10) # The ylabel function is used to set the label of the y-axis.labelpad argument is used to set the padding between the axis and the label.
        plt.title('Function Plot', fontweight='bold', fontsize=14) # The title function is used to set the title of the plot.fontweight argument is used to set the font weight of the title.fontsize argument is used to set the font size of the title.
        plt.grid(True, linestyle='--', linewidth=0.5) # The grid function is used to display the grid lines in the plot.linestyle argument is used to set the style of the grid lines.linewidth argument is used to set the width of the grid lines.
        self.canvas.draw() # This line updates the Matplotlib canvas to display the new plot.
        self.toolbar.show()  # Show the toolbar after plotting
if __name__ == '__main__': 
    app = QApplication(sys.argv) # The QApplication class manages the GUI application's control flow and main settings.this line creates an instance of the QApplication class from the PySide2 library, which represents the GUI application.
    plotter = FunctionPlotter() # This line creates an instance of the FunctionPlotter class, which represents the main window of the GUI application for plotting user-entered functions.
    plotter.show() #  It makes the GUI visible to the user.
    sys.exit(app.exec_()) # The exec_ method starts the application's event loop and waits for the user to close the application.
