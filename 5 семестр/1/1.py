def open_file():
    with open("in.txt", "r") as f:
        data = f.readlines()
        node_count = int(data[0])
        list_of_edges = set()
        adjacency_list = list()
        for index, line in enumerate(data[1:len(data)]):
            list_for_node = list()
            line = line.rstrip().split(" ")
            if line == [""]:
                list_of_edges.add((index+1, 0, 0))
                list_for_node.append({0: 0})
            else:
                k = line[0:-1]
                count = 0
                while count < len(k):
                    couple = {int(k[count]): int(k[count + 1])} #для списка смежностей
                    list_for_node.append(couple)

                    if index+1 < int(k[count]): #для списка ребер
                        edge = (index+1, int(k[count]), int(k[count + 1]))
                    else:
                        edge = (int(k[count]), index+1, int(k[count + 1]))
                    list_of_edges.add(edge)
                    count += 2
            adjacency_list.append(list_for_node)
    return node_count, list_of_edges, adjacency_list


#сортировка списка ребер
def edge_sorting(list_of_edges, n):
    sorted_list_of_edges = sorted(list_of_edges, key=lambda i: i[n])
    return sorted_list_of_edges


#процедура слияния
def merger(v, w, p, q, name, size, next_node):
    name[v] = p
    u = next_node[w]
    while name[u] != p:
        name[u] = p
        u = next_node[u]
    size[p] = size[p] + size[q]
    vv = next_node[v]
    ww = next_node[w]
    next_node[v] = ww
    next_node[w] = vv
    return name, size, next_node


#Жадный алгоритм Борувки_Краскла
def greedy_algorithm(node_count, list_of_edges):
    name = dict()
    size = dict()
    next_node = dict()
    skeleton = list()
    for node in range(node_count):
        name[node+1] = node+1
        size[node+1] = 1
        next_node[node+1] = node+1
    while len(skeleton) != node_count-1:
        edge = list_of_edges.pop(0)
        v = edge[0]
        w = edge[1]
        p = name[v]
        q = name[w]
        if p != q:
            if size[p] < size[q]:
                name2, size2, next_node2 = merger(v, w, p, q, name, size, next_node)
            else:
                name2, size2, next_node2 = merger(w, v, q, p, name, size, next_node)
            name = name2
            size = size2
            next_node = next_node2
            skeleton.append(edge)
    return skeleton


def write_result_in_file(skeleton, node_count):
    with open("out.txt", "w") as f:
        adjacency_list = dict()
        weight = 0

        for i in range(node_count):
            adjacency_list[i+1] = list()
        for i in skeleton:
            list_one = (i[1], i[2])
            list_two = (i[0], i[2])
            adjacency_list[i[0]].append(list_one)
            adjacency_list[i[1]].append(list_two)
            weight += i[2]

        #print(adjacency_list)

        for key, value in adjacency_list.items():
            adjacency_list[key] = edge_sorting(value, 0) #остортированный список смежных вершин
            for element in adjacency_list[key]:
                f.write(str(element[0]) + " " + str(element[1]) + " ")
            f.write("0\n")
        f.write(str(weight))


def main():
    node_count, list_of_edges, adjacency_list = open_file()
    sorted_list_of_edges = edge_sorting(list(list_of_edges), 2)
    #print(node_count)
    #print(sorted_list_of_edges)
    #print(adjacency_list)
    skeleton = greedy_algorithm(node_count, sorted_list_of_edges)
    #print(skeleton)

    #sorted_skeleton_on_the_first_node = edge_sorting(skeleton, 0)
    #print(sorted_skeleton_on_the_first_node)

    write_result_in_file(skeleton, node_count)


if __name__ == "__main__":
    main()
