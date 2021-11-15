import random


# Создание узла дерево
def make_node(key):
    if key is not None:
        size = 1
    else:
        size = 0
    return [key, None, None, size, 1]  # [0-key, 1-left, 2-brother, 3-size, 4-high]


# Получение размера узла с учетом поддеревьев
def get_size(node):
    if node is None:
        return 0
    else:
        return node[3]


# Получение высоты узла
def get_high(node):
    if node is None:
        return 0
    else:
        return node[4]


# Удаление пустых узлов
def fix_none_nodes(node):
    if node is None:
        return None
    else:
        if (node[0] is None) and (node[1] is None) and (node[2] is None):
            return None
        else:
            node[1] = fix_none_nodes(node[1])
            node[2] = fix_none_nodes(node[2])
            return node


# Обновление высоты дерева
def fix_high(node, up_high):
    node[4] = up_high + 1
    if node[2] is not None:
        fix_high(node[2], up_high)
    if node[1] is not None:
        fix_high(node[1], node[4])


# Получение максимальной высоты дерева
def get_max_high(node):
    if node[1] is not None:
        left = get_max_high(node[1])
    else:
        left = node[4]
    if node[2] is not None:
        brother = get_max_high(node[2])
    else:
        brother = node[4]
    return max(left, brother)


# Обновление размера дерева
def fix_size(node):
    if node[0] is None:
        node[3] = 0
        return node
    else:
        node[3] = 1
        if node[1] is None:
            return node
        else:
            if node[1][0] is not None:
                node[1] = fix_size(node[1])
                node[3] += get_size(node[1])
            if node[1][2] is not None:
                if node[1][2][0] is not None:
                    node[1][2] = fix_size(node[1][2])
                    node[3] += get_size(node[1][2])
            return node


def rotate_right(node):
    if not node[1]:
        return node
    temp = node[1]
    if temp[1]:
        node[1] = temp[1][2]
    else:
        node[1] = None
        temp[1] = make_node(None)
    temp[1][2] = node
    if not temp[1][2][1]:
        temp[1][2][1] = make_node(None)
    temp[1][2][1][2] = temp[2]
    temp[2] = node[2]
    node[2] = None
    temp[3] = node[3]
    temp = fix_none_nodes(temp)
    temp = fix_size(temp)
    fix_high(temp, 0)
    return temp


def rotate_left(node):
    if node[1][2]:
        if node[0] != node[1][2][0]:
            temp = node[1][2]
        else:
            return node
    else:
        return node
    temp[2] = node[2]
    if temp[1]:
        node[1][2] = list(temp[1])
        node[1][2][2] = None
        node[2] = temp[1][2]
    else:
        node[1][2] = None
        node[2] = None
    temp[1] = node
    temp[3] = node[3]
    temp = fix_none_nodes(temp)
    temp = fix_size(temp)
    fix_high(temp, 0)
    return temp


# Найти значение в дереве
def find(node, key):
    if node is None:
        return ValueError('Key is not found in tree')
    else:
        if node[0] == key:
            return node[0]
        else:
            if key < node[0]:
                return find(node[1], key)
            else:
                return find(node[1][2], key)


# Добавить значение на ветви дерева
def insert(node, key, up_high):
    if node is None:
        return make_node(key)
    else:
        if node[0] is None:
            node[0] = key
        else:
            if key < node[0]:
                node[1] = insert(node[1], key, node[4])
            else:
                if node[1] is None:
                    node[1] = make_node(None)
                node[1][2] = insert(node[1][2], key, node[4])
        node = fix_size(node)
        fix_high(node, up_high)
        return node


# Добавить значение в корень дерева
def insert_root(node, key):
    if node is None:
        return make_node(key)
    else:
        if node[0] is None:
            node[0] = key
            return rotate_right(node)
        else:
            if key < node[0]:
                node[1] = insert_root(node[1], key)
                return rotate_right(node)
            else:
                if node[1] is None:
                    node[1] = make_node(None)
                node[1][2] = insert_root(node[1][2], key)
                return rotate_left(node)


def insert_random(node, key):
    if not node:
        return make_node(key)
    if random.randint(0, get_size(node) + 1) == 0:
        node = insert_root(node, key)
        return fix_size(node)
    if key < node[0]:
        node[1] = insert(node[1], key, node[4])
    else:
        if not node[1]:
            node[1] = make_node(None)
        node[1][2] = insert(node[1][2], key, node[4])
    node = fix_none_nodes(node)
    return fix_size(node)


# Объединение деревьев прямым проходом (корень, левый, правый)
def trees_merge_nlr(source, target):
    if source is None:
        return target
    else:
        if source[0] is not None:
            insert(target, source[0], 0)
        if source[1] is not None:
            trees_merge_nlr(source[1], target)
            if source[1][2] is not None:
                trees_merge_nlr(source[1][2], target)
        return target


# Подготовка к выводу дерева обратным проходом (левый, правый, корень)
def print_prepare_lrn(tree, result):
    if tree is None:
        return result
    else:
        if tree[1] is not None:
            print_prepare_lrn(tree[1], result)
            if tree[1][2] is not None:
                print_prepare_lrn(tree[1][2], result)
        if tree[0] is not None:
            result.append(tree[0])
        return result


# Подготовка к выводу симметричным проходом (левый, корень, правый)
def print_prepare_lnr(tree, result):
    if tree is None:
        return result
    else:
        if tree[1] is not None:
            print_prepare_lnr(tree[1], result)
        if tree[0] is not None:
            result.append(tree[0])
        if tree[1] is not None:
            if tree[1][2] is not None:
                print_prepare_lnr(tree[1][2], result)
        return result


# Вывод дерева обратным проходом (левый, правый, корень)
def print_lrn(tree):
    if tree is None:
        return
    else:
        if tree[1] is not None:
            print_lrn(tree[1])
            if tree[1][2] is not None:
                print_lrn(tree[1][2])
        if tree[0] is not None:
            print(tree[0])
        return


# Вывод дерева симметричным проходом (левый, корень, правый)
def print_lnr(tree):
    if tree is None:
        return
    else:
        if tree[1] is not None:
            print_lnr(tree[1])
        if tree[0] is not None:
            print(tree[0])
        if tree[1] is not None:
            if tree[1][2] is not None:
                print_lnr(tree[1][2])
        return


# Создание и заполнение дерева
def TreeFill(size, limit):
    tree = None
    for i in range(size):
        tree = insert_random(node=tree, key=random.randint(1, limit))
    return tree


if __name__ == '__main__':
    # treeA = [3, [2, [1, None, None, 1, 3], [7, None, None, 1, 3], 2, 2], None, 4, 1]
    # treeB = [9, [7, [3, [None, None, [5, None, None, 1, 5], 0, 4], None, 2, 3], None, 3, 2], None, 4, 1]
    # treeA = None
    # treeA = insert(treeA, 3, 0)
    # treeA = insert(treeA, 2, 0)
    # treeA = insert(treeA, 7, 0)
    # treeA = insert(treeA, 1, 0)
    # treeB = None
    # treeB = insert(treeB, 9, 0)
    # treeB = insert(treeB, 7, 0)
    # treeB = insert(treeB, 3, 0)
    # treeB = insert(treeB, 5, 0)
    treeA = TreeFill(1000, 10000)
    treeB = TreeFill(1000, 10000)
    trees_merge_nlr(source=treeB, target=treeA)
    print(print_prepare_lrn(treeA, []))
    print(print_prepare_lnr(treeB, []))
    # print_lrn(treeA)
    # print_lnr(treeB)
    print(f'treeA: size - {get_size(treeA)}, high - {get_max_high(treeA)}')
    print(f'treeB: size - {get_size(treeB)}, high - {get_max_high(treeB)}')
