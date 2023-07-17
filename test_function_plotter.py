
import pytest
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from Function_Plotter import FunctionPlotter
@pytest.fixture
def app(qtbot):
    plotter = FunctionPlotter()
    qtbot.addWidget(plotter)
    return plotter

def test_end_to_end(qtbot, app):
    # Get references to the GUI widgets
    function_input = app.function_input
    min_input = app.min_input
    max_input = app.max_input
    plot_button = app.plot_button
    canvas = app.canvas
    # Simulate user input
    qtbot.keyClicks(function_input, 'x^2')
    qtbot.keyClicks(min_input, '0')
    qtbot.keyClicks(max_input, '5')
    # Click the plot button
    qtbot.mouseClick(plot_button, Qt.LeftButton)
    # Check if the plot is generated correctly
    assert len(canvas.figure.axes) == 1  # One plot is generated
    assert len(canvas.figure.axes[0].lines) == 1  # One line is plotted
    # Check the plotted line data
    x_data = canvas.figure.axes[0].lines[0].get_xdata()
    y_data = canvas.figure.axes[0].lines[0].get_ydata()
    expected_x_data = [0, 1, 2, 3, 4, 5]
    expected_y_data = [0, 1, 4, 9, 16, 25]
    assert list(x_data) == expected_x_data
    assert list(y_data) == expected_y_data

def test_validate_input_valid_input(app):
    app.function_input.setText("x^2")
    app.min_input.setText("0")
    app.max_input.setText("10")
    assert app.validate_input() == True

def test_validate_input_invalid_function_1(app):
    app.function_input.setText("x++2")
    app.min_input.setText("0")
    app.max_input.setText("10")
    assert app.validate_input() == False

def test_validate_input_invalid_function_2(app):
    app.function_input.setText("3x")
    app.min_input.setText("0")
    app.max_input.setText("10")
    assert app.validate_input() == False

def test_validate_input_invalid_function_3(app):
    app.function_input.setText("x**2")
    app.min_input.setText("0")
    app.max_input.setText("10")
    assert app.validate_input() == False

def test_validate_input_invalid_min_value(app):
    app.function_input.setText("x^2")
    app.min_input.setText("a")
    app.max_input.setText("10")
    assert app.validate_input() == False

def test_validate_input_invalid_max_value(app):
    app.function_input.setText("x^2")
    app.min_input.setText("0")
    app.max_input.setText("b")
    assert app.validate_input() == False

def test_validate_input_min_greater_than_max(app):
    app.function_input.setText("x^2")
    app.min_input.setText("10")
    app.max_input.setText("5")
    assert app.validate_input() == False

