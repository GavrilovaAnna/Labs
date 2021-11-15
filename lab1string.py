import random


# Класс одного элемента внутри дека
class DequeElement:

    def __init__(self, elem_value, prev_element, next_element):
        self.next_e = next_element
        self.prev_e = prev_element
        self.value = elem_value


# Класс дека в целом
class Deque:

    def __init__(self):
        self.Head = None
        self.Tail = None
        self.New = None
        self.Elems_count = 0

    # Добавить элемент в начало
    def PushFront(self, value):
        if self.IsEmpty():
            self.Head = DequeElement(elem_value=value, prev_element=None, next_element=None)
            self.Tail = self.Head
        else:
            self.New = DequeElement(elem_value=value, prev_element=None, next_element=self.Head)
            self.Head.prev_e = self.New
            self.Head = self.New
        self.Elems_count += 1

    # Добавить элемент в конец
    def PushBack(self, value):
        if self.IsEmpty():
            self.Head = DequeElement(elem_value=value, prev_element=None, next_element=None)
            self.Tail = self.Head
        else:
            self.New = DequeElement(elem_value=value, prev_element=self.Tail, next_element=None)
            self.Tail.next_e = self.New
            self.Tail = self.New
        self.Elems_count += 1

    # Проверка пустой ли дек (если - True, если в нем есть хотя бы 1 элемент - False)
    def IsEmpty(self):
        return self.Head is None

    # Метод возвращает количество элементов в деке
    def DequeSize(self):
        return self.Elems_count

    # Извлечь элемент из начала
    def PopFront(self):
        if self.IsEmpty():
            return IndexError('Underflow error! Nothing to pop, because deque is empty.')
        else:
            answer = self.Head.value
            if self.Head.next_e:
                self.Head.next_e.prev_e = None
                self.Head = self.Head.next_e
            else:
                self.Head = None
            self.Elems_count -= 1
            return answer

    # Извлечь элемент из конца
    def PopBack(self):
        if self.IsEmpty():
            return IndexError('Underflow error! Nothing to pop, because deque is empty.')
        else:
            answer = self.Tail.value
            if self.Head != self.Tail:
                self.Tail.prev_e.next_e = None
                self.Tail = self.Tail.prev_e
            else:
                self.Head = None
            self.Elems_count -= 1
            return answer

    # Сортировка дека методом распределяющего подсчета
    def sort(self):
        cnt = []
        result = []

        while not self.IsEmpty():
            cur_el = self.PopFront()
            if len(cnt) <= cur_el:
                for i in range(cur_el - len(cnt) + 1):
                    cnt.append(0)
            cnt[cur_el] += 1

        for num in range(len(cnt)):
            for i in range(cnt[num]):
                result.append(num)

        return result


# Создание и наполнение дека size - количество элементов в деке, limit - максимальный элемент в деке
def DequeFill(size, limit):
    deque = Deque()
    for i in range(size):
        deque.PushBack(value=random.randint(0, limit))
    return deque


if __name__ == '__main__':
    deque = DequeFill(size=20, limit=8)
    result = deque.sort()
    print(result)
