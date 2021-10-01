class ControlView:
    def __init__(self) -> None:
        pass

    def input_number(self, message: str) -> int:
        flag = False
        while (not flag):
            number: str = input(message)
            flag = str(number).isnumeric()
            if flag:
                number: int = int(number)
            else:
                print('Por favor ingresar solo numeros')
        return number

    def input_date(self, message: str) -> str:
        date: str = input(message)
        return date

    def input_string(self, message: str) -> str:
        string: str = input(message)
        return string

    def output(self, message) -> None:
        print(message)