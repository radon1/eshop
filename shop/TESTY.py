
class ProtectedView(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)



# class A:
#     value = 2
#
#     def __init__(self, name):
#         self.name = name
#
#
# class B(A):
#     pass
#
#
# a = A("Vasya")
# b = A("Petya")
# print(a.name)
# print(b.name)
#
#
# class Car:
#
#     # создаем конструктор класса Car
#     def __init__(self, model):
#         # Инициализация свойств.
#         self.model = model
#
#     # создаем свойство модели.
#     @property
#     def model(self):
#         return self.__model
#
#     # Сеттер для создания свойств.
#     @model.setter
#     def model(self, model):
#         if model < 2000:
#             self.__model = 2000
#         elif model > 2018:
#             self.__model = 2018
#         else:
#             self.__model = model
#
#     def getCarModel(self):
#         return "Год выпуска модели " + str(self.model + 1)
#
#
# carA = Car(2088)
# print(carA.model)
# print(carA.getCarModel())


# class SimpleIterator:
#     def __iter__(self):
#         return self
#
#     def __init__(self, limit):
#         self.limit = limit
#         self.counter = 0
#
#     def __next__(self):
#         if self.counter < self.limit:
#             self.counter += 1
#             return self.counter
#         else:
#             raise StopIteration
#
#
# s_iter1 = SimpleIterator(5)


# for i in s_iter1:
#     print(i)

#
# def simple_generator(val):
#     while val > 0:
#         val -= 1
#         yield val
#     return "Good"
#
#
# gen_iter = simple_generator(5)
# print(type(gen_iter))
# print(next(gen_iter))
# print(next(gen_iter))
# print(next(gen_iter))
# print(next(gen_iter))
# print(next(gen_iter))
# print(next(gen_iter))


