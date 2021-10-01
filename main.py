from access.ServicesOrders import *
from access.controller import *

PATH = './files/'


def run():
    # delete_all()
    # ServicesAddFileOrdersOrigin('PEDIDOS-RECOPIILACION DE PEDIDOS 2019 A HOY.xls')
    # ServicesReadOrders('2021-09-07')
    # ServicesAddNewOrders()
    # ServicesReadOrders()
    ServicesAddFileOrders('Ordenes.xlsx')


if __name__ == '__main__':
    run()
