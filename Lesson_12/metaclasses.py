import dis


class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []

        for key, value in clsdict.items():
            try:
                ret = dis.get_instructions(value)
            except TypeError:
                pass
            else:
                for item in ret:
                    if item.opname == 'LOAD_GLOBAL':
                        if item.argval not in methods:
                            methods.append(item.argval)
                    elif item.opname == 'LOAD_ATTR':
                        if item.argval not in attrs:
                            attrs.append(item.argval)
        
        if 'connect' in methods:
            raise TypeError('Недопустимый вызов метода connect')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Отсутствует инициализация сокета')

        super().__init__(clsname, bases, clsdict)


class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []

        for key, value in clsdict.items():
            try:
                ret = dis.get_instructions(value)
            except TypeError:
                pass
            else:
                for item in ret:
                    if item.opname == 'LOAD_GLOBAL':
                        if item.argval not in methods:
                            methods.append(item.argval)
        
        for method in ('accept', 'listen', 'socket'):
            if method in methods:
                raise TypeError(f'Вызов недопустимого метода {method}')
        
        if 'get_msg' in methods or 'send_msg' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами')
        
        super().__init__(clsname, bases, clsdict)
