from sqlite3.dbapi2 import Date
from view.ControlView import ControlView
from access.ServicesOrders import *


class ViewMain():
    control_view = ControlView()

    MENU = """\t\tMenu principal
        1. Consultas
        2. Insertar nuevas ordenes
        3. Generar informe
        4. Actualizar base de datos de ordenes ya ingresadas
        5. Eliminar rango de ordenes ya ingresadas
        6. Salir"""

    MENU_2 = """\t\tMenu de generacion de informe
        1. Generar informe completo
        2. Generar informe desde una fecha indicada
        3. Salir"""

    MENU_QUERIES = """\t\tMenu Consultas
        1. Dinamica
        2. Salir"""

    def __init__(self) -> None:

        self.init_menu()

    def init_menu(self):

        selection: int = 0
        while(selection != 6):
            self.control_view.output(self.MENU)
            selection = self.control_view.input_number(
                'Por favor seleccione escribiendo el numero: ')
            if selection == 1:
                self.queries_menu()
            elif selection == 2:
                ServicesAddNewOrders()
            elif selection == 3:
                self.report_menu()
            elif selection == 4:
                ServicesAddFileOrders('Ordenes.xlsx')
            elif selection == 5:
                number_min: int = self.control_view.input_number(
                    'Ingrese primer id a eliminar: ')
                number_max: int = self.control_view.input_number(
                    'Ingrese ultimo id a eliminar: ')
                ServicesDeleteRange(number_min, number_max)
            elif selection == 6:
                pass
            else:
                self.control_view.output('Numero ingresado, no valido')

    def report_menu(self, pivot=None):

        selection: int = 0
        while(selection != 3):
            self.control_view.output(self.MENU_2)
            selection = self.control_view.input_number(
                'Por favor seleccione escribiendo el numero: ')
            if selection == 1:
                if not pivot:
                    ServicesReadOrders()
                else:
                    ServicesReadPivot()
            elif selection == 2:
                date = self.control_view.input_date(
                    'Ingrese fecha (2021-12-31): ')
                if not pivot:
                    ServicesReadOrders(date)
                else:
                    ServicesReadPivot(date)
            elif selection == 3:
                pass
            else:
                self.control_view.output('Numero ingresado, no valido')

    def queries_menu(self):
        selection: int = 0
        while(selection != 2):
            self.control_view.output(self.MENU_QUERIES)
            selection = self.control_view.input_number(
                'Por favor seleccione escribiendo el numero: ')
            if selection == 1:
                self.report_menu(pivot=True)
            elif selection == 2:
                pass
            else:
                self.control_view.output('Numero ingresado, no valido')
