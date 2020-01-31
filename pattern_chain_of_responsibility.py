from abc import ABC, abstractmethod

GET, SET = "GET", "SET"

# Дан объект класса SomeObject, содержащего три поля: integer_field, float_field и string_field:
class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""

# Необходимо реализовать поведение:

# EventGet(<type>) создаёт событие получения данных соответствующего типа
# EventSet(<value>) создаёт событие изменения поля типа type(<value>)
# Необходимо реализовать классы NullHandler, IntHandler, FloatHandler, StrHandler
# так, чтобы можно было создать цепочку:


class EventGet:
    def __init__(self, kind):
        self._kind = self.kind = kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, kind):
        self._kind = (kind, GET)


class EventSet:
    def __init__(self, kind):
        self._kind = self.kind = kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = (value, SET)

# Базовый объект цепочки событий,
class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)



class IntHandler(NullHandler):

    def handle(self, obj, event):
        set_kind = (type(event.kind[0]), SET)

        if event.kind == (int, GET):
            return obj.integer_field

        elif set_kind == (int, SET):
            obj.integer_field = event.kind[0]
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):

    def handle(self, obj, event):
        set_kind = (type(event.kind[0]), SET)

        if event.kind == (float, GET):
            return obj.float_field

        elif set_kind == (float, SET):
            obj.float_field = event.kind[0]
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):

    def handle(self, obj, event):
        set_kind = (type(event.kind[0]), SET)

        if event.kind == (str, GET):
            return obj.string_field

        elif set_kind == (str, SET):
            obj.string_field = event.kind[0]
        else:
            return super().handle(obj, event)

if __name__ == "__main__":
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = FloatHandler(IntHandler(StrHandler(NullHandler())))

    chain_float = chain.handle(obj, EventGet(float))
    chain_int = chain.handle(obj, EventGet(int))

    chain.handle(obj, EventSet(100))
    print(chain.handle(obj, EventGet(int)))

    chain.handle(obj, EventSet(0.5))
    print(chain.handle(obj, EventGet(float)))

    chain.handle(obj, EventSet('new text'))
    print(chain.handle(obj, EventGet(str)))

# Пример работы
# >>> obj = SomeObject()
# >>> obj.integer_field = 42
# >>> obj.float_field = 3.14
# >>> obj.string_field = "some text"
# >>> chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
# >>> chain.handle(obj, EventGet(int))
# 42
# >>> chain.handle(obj, EventGet(float))
# 3.14
# >>> chain.handle(obj, EventGet(str))
# 'some text'
# >>> chain.handle(obj, EventSet(100))
# >>> chain.handle(obj, EventGet(int))
# 100
# >>> chain.handle(obj, EventSet(0.5))
# >>> chain.handle(obj, EventGet(float))
# 0.5
# >>> chain.handle(obj, EventSet('new text'))
# >>> chain.handle(obj, EventGet(str))
# 'new text'