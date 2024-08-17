from abc import ABC, abstractmethod
from collections import deque


class RingBuffer(ABC):
    def __init__(self, size):
        self._size = size

    @abstractmethod
    def is_full(self):
        raise NotImplementedError

    @abstractmethod
    def is_empty(self):
        raise NotImplementedError

    @abstractmethod
    def push_element(self, element):
        raise NotImplementedError

    @abstractmethod
    def pop_element(self):
        raise NotImplementedError


class ListBuffer(RingBuffer):
    def __init__(self, size):
        super().__init__(size)
        self._buffer = [ None for i in range(size) ]
        self._first = 0
        self._last = 0
        self._n_elements = 0  # Кол-во элемнтов записанных в буфер

    def is_full(self):
        return self._n_elements == self.size

    def is_empty(self):
        return self._n_elements == 0

    def push_element(self, element):
        if self.is_full():
            self._buffer[self._first] = element
            self._first = (self._first + 1) % self._size
            self._last = (self._last + 1) % self._size
        else:
            self._buffer[self._last] = element
            self._last = (self._last + 1) % self._size
            self._n_elements += 1

    def pop_element(self):
        if self.is_empty():
            raise IndexError('Буфер пуст')
        element = self._buffer[self._first]
        self._buffer[self._first] = None
        self._first = (self._first + 1) % self._size
        self._n_elements -= 1
        return element

    def get_buffer(self):
        print(self._buffer)


class DequeBuffer(RingBuffer):
    def __init__(self, size):
        super().__init__(size)
        self._buffer = deque(maxlen=self._size)

    def is_full(self):
        len(self._buffer) == self._size

    def is_empty(self):
        len(self._buffer) == 0

    def push_element(self, element):
        self._buffer.append(element)

    def pop_element(self):
        return self._buffer.popleft()

    def get_buffer(self):
        print(self._buffer)


'''
Вариант с массивом:
    Плюсы:
        - Простой и интуитивный способ воплощения Ring Buffer'a
    Минусы:
        - Вставка/удаление может быть медленне из-за ипользования 
          индексов и вычичлений переноса позиций 
        - Незаполненные элементы все равно занимают память
    
Вариант с очередью с двумя концами:
    Плюсы:
        - Очередь с двумя концами имеет быструю вставку и удаление 
          в конец и с начала соответственно
        - Имеется полностью встроенный функционал, даже презапись 
          в заполненном буфере и перехват ошибки при удалении из пустого буфера
    Минусы:
        - Может требовать больше памяти из-за внутренней структуры данных deque
        
Быстродействие:
    У обоих реализаций сложность O(1), однако для первой требуется вычисление индекса, а для второго - нет.
    
Вывод:
    В купе всех плюсов и минусов выбор второй реализации более предпочтителен.
'''


if __name__ == '__main__':
    buffer = DequeBuffer(3)
    buffer.push_element(1)
    buffer.get_buffer()
    buffer.push_element(2)
    buffer.push_element(3)
    buffer.get_buffer()
    buffer.pop_element()
    buffer.get_buffer()
    buffer.push_element(4)
    buffer.get_buffer()
    buffer.push_element('A')
    buffer.get_buffer()
    for i in range(4):
        buffer.pop_element()  # Просто чтобы показать, как ведет себя удаление из пустого массива
