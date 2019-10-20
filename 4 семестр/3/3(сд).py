spisok_nodes = dict()
count_nodes = 0


#цель задачи minmax: найти путь, который минимизирует максимальный вес любого из рёбер
#можно интерпретировать как поиск самой ровной дороги, имеющей минимальные углы подъёма и спуска)
#т.е. тот путь, в котором вес самого большого ребра будет минимальным из максимальных ребер всех путей
#по итогу выводим такой путь и вес его самого дорогостоящего ребра.

def input_data():
    global spisok_nodes
    global count_nodes

    with open("in.txt", "r") as f:
        data = f.readlines()
        count_nodes = int(data[0])
        start = int(data[-2])
        finish = int(data[-1])
        for index, element in enumerate(data[1:-2]):
            spisok = dict()
            element = element.strip().split(" ")
            for ind, el in enumerate(element):
                spisok[int(ind)] = int(el)
            spisok_nodes[int(index)] = spisok
    return start-1, finish-1


def algorithm(start, matrix):
    visited = [True] * count_nodes
    weight = [1000000] * count_nodes
    weight[start] = 0
    prev = [start] * count_nodes
    prev[start] = -1
    for _ in range(count_nodes):
        min_weight = 1000001
        ID_min_weight = -1
        #выбираем вершину с минимальным номером, которая еще не посещена (если valid[i] == True)
        for index in range(len(weight)):
            if visited[index] and weight[index] < min_weight:
                min_weight = weight[index]
                ID_min_weight = index
        #для каждой вершины k, если она достижима из выбранной вершины с мин.номером t выбираем
        #максимум между весом предыдущей дороги (т.е. weight[ID_min_weight]) и весом между
        #двумя вершинами t и k (т.е. последнее ребро в дороге до k),
        #если максимум меньше текущей дороги до k, присваиваем этот максимум, а предыдущей вершиной делаем
        #вершину t, из которой пришли.
        for i in range(count_nodes):
            if matrix[ID_min_weight][i] != -32768:
                if weight[i] > max(weight[ID_min_weight], matrix[ID_min_weight][i]):
                    weight[i] = max(weight[ID_min_weight], matrix[ID_min_weight][i])
                    prev[i] = ID_min_weight
            visited[ID_min_weight] = False
    return weight, prev


def find_path(start, finish, prev):
    result = list()
    if prev[finish] < 1000000:
        result.append(str(finish + 1))
        current = finish
        while current != start:
            current = prev[current]
            result.append(str(current + 1))
    result.reverse()
    return result


def write_result_in_file(path, weight):
    with open("out.txt", "w") as f:
        maximum = 0
        if len(path) == 0:
            f.write("N")
        else:
            f.write("Y\n")
            f.write(" ".join(path) + "\n")
            for index, element in enumerate(path):
                if weight[int(element)-1] > maximum:
                    maximum = weight[int(element)-1]
            f.write(str(maximum) + "\n")


def main():
    start, finish = input_data()
    weight, prev = algorithm(start, spisok_nodes)
    path = find_path(start, finish, prev)
    write_result_in_file(path, weight)


if __name__ == "__main__":
    main()
