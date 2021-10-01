from view.ControlView import ControlView
from access.ServicesOrders import *

class ViewMain():
    control_view = ControlView()

    MENU = """\t\tMenu principal
        1. Insertar nuevas ordenes
        2. Generar informe
        3. Actualizar base de datos de ordenes ya ingresadas
        4. Eliminar rango de ordenes ya ingresadas
        5. Salir"""
    
    MENU_2 = """\t\tMenu de generacion de informe
        1. Generar informe completo
        2. Generar informe desde una fecha indicada
        3. Salir"""
    
    
    def __init__(self) -> None:

        self.init_menu()

    def init_menu(self):
        
        selection: int = 0
        while(selection != 5):
            self.control_view.output(self.MENU)
            selection = self.control_view.input_number('Por favor selecciones escribiendo el numero: ')
            if selection == 1:
                ServicesAddNewOrders()
            elif selection == 2:
                self.report_menu()
            elif selection == 3:
                ServicesAddFileOrders('Ordenes.xlsx')
            elif selection == 4:
                number_min: int = self.control_view.input_number('Ingrese primer id a eliminar: ')
                number_max: int = self.control_view.input_number('Ingrese ultimo id a eliminar: ')
                ServicesDeleteRange(number_min, number_max)
            elif selection == 5:
                pass
            else:
                self.control_view.output('Numero ingresado, no valido')


    def report_menu(self):
        
        selection: int = 0
        while(selection != 3):
            self.control_view.output(self.MENU_2)
            selection = self.control_view.input_number('Por favor selecciones escribiendo el numero: ')
            if selection == 1:
                ServicesReadOrders()
            elif selection == 2:
                date = self.control_view.input_number('Ingrese fecha (2021/12/31): ')
                ServicesReadOrders(date)
            elif selection == 3:
                pass
            else:
                self.control_view.output('Numero ingresado, no valido')
            

