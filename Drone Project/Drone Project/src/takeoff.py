from cmath import sin
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QPushButton, QLabel, QListWidget, QLineEdit
from PyQt5.QtGui import QIcon
import pickle


############################################################################################################
# Command:
############################################################################################################

class Command:
    def __init__(self, command, value):
        self.command = command
        self.value = value

    def get_command(self):
        return self.command
    
    def get_value(self):
        return self.value
    
    def set_command(self, command):
        self.command = command
    
    def set_value(self, value):
        self.value = value
    
    def to_string(self):
        return self.command + " " + str(self.value)
    
############################################################################################################
#  Command_List:
############################################################################################################

class Command_List:
    def __init__(self):
        self.command_list = []
    
    def add_command(self, command):
        self.command_list.append(command)

    def delete_command(self, index):
        self.command_list.pop(index)
    
    def edit_command(self, index, command):
        self.command_list[index] = command
    
    def get_command(self, index):
        return self.command_list[index]
    
    def swap_command_down(self, index):
        if index > 0:
            self.command_list[index], self.command_list[index - 1] = self.command_list[index - 1], self.command_list[index]
    
    def swap_command_up(self, index):
        if index < len(self.command_list) - 1:
            self.command_list[index], self.command_list[index + 1] = self.command_list[index + 1], self.command_list[index]

    def shift_command(self, old_index, new_index):
        if old_index < new_index:
            while old_index <= new_index:
                self.swap_command_down(old_index)
                old_index += 1
        elif old_index > new_index:
            while old_index >= new_index:
                self.swap_command_up(old_index)
                old_index -= 1

    def get_command_list(self):
        return self.command_list

    def to_string(self):
        result = ""
        for command in self.command_list:
            result += command.get_command() + " " + str(command.get_value()) + "\n"
        return result
    
    def save_program(self, file_name):
        try:
            with open(file_name, 'w') as file:
                for command in self.command_list:
                    file.write(command.to_string() + "\n")
        except FileNotFoundError:
            print("File not found")

    def load_program(self, file_name):
        self.command_list = []

        try:
            with open(file_name, 'r') as file:
                for line in file:
                    command = line.split()
                    self.add_command(Command(command[0], int(command[1])))
        except FileNotFoundError:
            print("File not found")

############################################################################################################
# Drone_Interface
############################################################################################################

class Drone_Interface:
    boundary_status = False
    connection_status = False
    selected_program = None

    def __init__(self, selected_program):
        if selected_program != None:
            self.selected_program = selected_program

    def send_commands(self, commands):
        for command in commands.get_command_list():
            print(command.get_command() + " " + str(command.get_value()))

    def set_boundary_status(self, status):
        self.boundary_status = status

    def set_connection_status(self, status):
        self.connection_status = status

    def set_selected_program(self, selected_program):
        self.selected_program = selected_program
    
    def get_boundary_status(self):
        return self.boundary_status
    
    def get_connection_status(self):
        return self.connection_status
    
    def get_selected_program(self):
        return self.selected_program

############################################################################################################
# Boundary
############################################################################################################

class Boundary:
    x = 0
    y = 0
    height = 0

    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_height(self):
        return self.height
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def set_height(self, height):  
        self.height = height

    def check_command_list(program):    
        position = [0, 0, 0, 0]
        command_list = program.get_command_list()
        for i in range(0, len(command_list)):
            position = Boundary.new_position(command_list[i], position)
            result = Boundary.check_boundary(position[0], position[1], position[2])

            if result == False:
                return False
        return True

    def new_position(command, position):
        if command.get_command() == "forward":
            position[0] += int(math.cos(position[3]) * command.get_value())
            position[1] += int(sin(position[3]) * command.get_value())

        elif command.get_command() == "backward":
            position[0] -= int(math.cos(position[3]) * command.get_value())
            position[1] -= int(sin(position[3]) * command.get_value())
        
        elif command.get_command() == "right":    
            position[3] = Boundary.theta_adjustment(position[3], 90)
            position[0] += int(math.cos(theta) * command.get_value())
            position[1] += int(math.sin(position[3]) * command.get_value())

        elif command.get_command() == "left":
            theta = Boundary.theta_adjustment(position[3], -90)
            position[0] += int(math.cos(theta) * command.get_value())
            position[1] += int(math.sin(position[3]) * command.get_value())

        elif command.get_command() == "cw":
            position[3] = Boundary.theta_adjustment(position[3], command.get_value())
            
        elif command.get_command() == "ccw":
            position[3] = Boundary.theta_adjustment(position[3], -command.get_value())

        elif command.get_command() == "up":
            position[2] += command.get_value() 
        
        elif command.get_command() == "down":
            position[2] -= command.get_value()
        
        return position
    
############################################################################################################
# Connection
############################################################################################################

class connection:
    def __init__(self):
        self.status = False

    # def attempt_connection(self):
        
    def connect(self):
        self.status = True
    
    def disconnect(self):
        self.status = False


############################################################################################################
# Boot
############################################################################################################

class Boot:
    def __init__(self):
        self.current_command_list = Command_List()
        self.load_last_command_list()
        
    def load_last_command_list(self):
        self.current_command_list.load_program('Last_Command.txt')
    
    def get_last_command_list(self):
        return self.current_command_list

############################################################################################################
# Program
############################################################################################################

class Program:
    def __init__(self):
        self.current_connection = connection()
        self.current_boundary = Boundary(0, 0, 0)
        self.current_program = Command_List()
    
    boot = Boot()
    current_program = boot.get_last_command_list()

    def save_last_command_list(self):
        self.current_program.save_program('Last_Command.txt')
        

############################################################################################################
# Main Menu
############################################################################################################

class main_menu:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("Tello Drone Interface")
        self.window.setWindowIcon(QIcon("tello_icon.png"))

        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

        self.programming_button = QPushButton("Go to Programming Page")
        self.programming_button.clicked.connect(self.go_to_programming_page)
        self.layout.addWidget(self.programming_button)

        self.fly_button = QPushButton("Go to Fly Page")
        self.fly_button.clicked.connect(self.go_to_fly_page)
        self.layout.addWidget(self.fly_button)

        self.window.show()
        self.app.exec_()

    def go_to_programming_page(self):
        self.programming_page = programming_page()
        self.programming_page.show()
    def go_to_fly_page(self):
        self.fly_page = Fly_Page()
        self.fly_page.show()


############################################################################################################
# Programming Page
############################################################################################################

class programming_page(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Programming Page")

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter a command:")
        self.layout.addWidget(self.label)

        self.command_input = QLineEdit()
        self.layout.addWidget(self.command_input)

        self.add_button = QPushButton("Add Command")
        self.add_button.clicked.connect(self.add_command)
        self.layout.addWidget(self.add_button)

        self.command_list_widget = QListWidget()
        self.layout.addWidget(self.command_list_widget)

        self.setLayout(self.layout)

    def add_command(self):
        command = self.command_input.text()
        self.command_list_widget.addItem(command)
        self.command_input.clear()

############################################################################################################
# Fly Page
############################################################################################################

class Fly_Page(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fly Page")

        self.layout = QVBoxLayout()

        self.boundary_label = QLabel("Set Boundaries:")
        self.layout.addWidget(self.boundary_label)
        # Add widgets for setting boundaries here

        self.upload_button = QPushButton("Upload File")
        #self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        self.send_button = QPushButton("Send Command List")
        #self.send_button.clicked.connect(self.send_command_list)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    #def upload_file(self):
        #file_name, _ = QFileDialog.getOpenFileName(self, "Open File")
        # Add code to handle the uploaded file here

    #def send_command_list(self):
        # Add code

    


def test():
    commands = Command_List()
    commands.add_command(Command("takeoff", 0))
    commands.add_command(Command("Forward", 1))
    commands.add_command(Command("backward", 2))
    commands.add_command(Command("left", 3))
    commands.add_command(Command("right", 4))
    commands.add_command(Command("land", 5))
    commands.shift_command(0, 3)

    # START APP
    takeoff_app = Program()
    #takeoff_app.current_program.shift_command(1, 3)
    main_menu()
    # END APP



test()
