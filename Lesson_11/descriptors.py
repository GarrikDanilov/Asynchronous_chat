import sys


class ValidatingPort:
    def __init__(self, logger):
        self.logger = logger

    def __set__(self, instance, value):
        if value < 1024 or value > 65535:
            self.logger.error(f'Некорректный номер порта - {value}. Номер порта должен быть \
в диапазоне от 1024 до 65535')
            sys.exit(1)

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
        