# gui.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QMessageBox
)
from solver import solve_lp
from visualization import plot_feasible_region

class SimplexGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simplex Method Solver')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Objective Function Input
        self.obj_label = QLabel('Objective Function Coefficients (comma-separated):')
        self.obj_input = QLineEdit()
        self.obj_type = QComboBox()
        self.obj_type.addItems(['Maximize', 'Minimize'])

        # Constraints Table
        self.constraints_table = QTableWidget()
        self.constraints_table.setColumnCount(3)
        self.constraints_table.setHorizontalHeaderLabels(['Coefficients', 'Relation', 'RHS'])

        # Buttons
        self.add_constraint_btn = QPushButton('Add Constraint')
        self.add_constraint_btn.clicked.connect(self.add_constraint)
        self.solve_btn = QPushButton('Solve')
        self.solve_btn.clicked.connect(self.solve_lp)

        # Add widgets to layout
        layout.addWidget(self.obj_label)
        layout.addWidget(self.obj_input)
        layout.addWidget(self.obj_type)
        layout.addWidget(self.constraints_table)
        layout.addWidget(self.add_constraint_btn)
        layout.addWidget(self.solve_btn)

        central_widget.setLayout(layout)

    def add_constraint(self):
        row_position = self.constraints_table.rowCount()
        self.constraints_table.insertRow(row_position)

        # Coefficients Input
        coeff_input = QLineEdit()
        self.constraints_table.setCellWidget(row_position, 0, coeff_input)

        # Relation Input
        relation_input = QComboBox()
        relation_input.addItems(['<=', '>=', '='])
        self.constraints_table.setCellWidget(row_position, 1, relation_input)

        # RHS Input
        rhs_input = QLineEdit()
        self.constraints_table.setCellWidget(row_position, 2, rhs_input)

    def solve_lp(self):
        # Collect data from the GUI
        try:
            objective_coeffs = [float(c.strip()) for c in self.obj_input.text().split(',')]
            problem_type = self.obj_type.currentText()
            constraints = self.get_constraints()

            # Solve the problem using the solver module
            solution, objective_value = solve_lp(objective_coeffs, problem_type, constraints)

            # Display the results
            self.display_results(solution, objective_value)

            # Plot the feasible region if applicable
            if len(objective_coeffs) == 2:
                plot_feasible_region(objective_coeffs, constraints, solution)
        except Exception as e:
            self.display_error(str(e))

    def get_constraints(self):
        constraints = []
        for row in range(self.constraints_table.rowCount()):
            coeff_widget = self.constraints_table.cellWidget(row, 0)
            relation_widget = self.constraints_table.cellWidget(row, 1)
            rhs_widget = self.constraints_table.cellWidget(row, 2)

            coeffs_text = coeff_widget.text()
            if not coeffs_text:
                raise ValueError("Constraint coefficients cannot be empty.")
            coeffs = [float(c.strip()) for c in coeffs_text.split(',')]

            relation = relation_widget.currentText()

            rhs_text = rhs_widget.text()
            if not rhs_text:
                raise ValueError("Constraint RHS cannot be empty.")
            rhs = float(rhs_text)

            constraints.append({'coefficients': coeffs, 'relation': relation, 'rhs': rhs})
        return constraints

    def display_results(self, solution, objective_value):
        result_text = f'Optimal Objective Value: {objective_value}\n'
        for var_name, value in solution.items():
            result_text += f'{var_name} = {value}\n'
        QMessageBox.information(self, 'Optimal Solution', result_text)

    def display_error(self, message):
        QMessageBox.critical(self, 'Error', message)
