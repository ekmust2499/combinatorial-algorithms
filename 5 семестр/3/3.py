from collections import deque


def open_file():
    with open("in.txt", "r") as f:
        data = f.readlines()
        node_count = int(data[0])
        node_for_change = int(data[len(data)-1])
        graph = dict()
        for i in range(node_count):
            graph[i+1] = list()
        count = 1
        for line in data[1:len(data)-1]:
            line = line.rstrip().split(" ")
            nodes = line[1:]
            if nodes is not []:
                for node in nodes:
                    if count == node_for_change:
                        graph[count].append(int(node))
                    else:
                        if int(node) == node_for_change:
                            graph[count].append(int(node_for_change))
                        else:
                            graph[int(node)].append(count)
            count += 1
        #print(graph)
    return node_count, graph, node_for_change


def bfs(graph, root):
    visited = list()
    visited.append(root)
    queue = deque()
    queue.append(root)
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.append(int(neighbor))
                queue.append(neighbor)
    #print(visited)
    return visited


def write_result_in_file(node_for_change, list_for_result):
    with open("out.txt", "w") as f:
        f.write(str(node_for_change) + "\n")
        if "-" in list_for_result:
            f.write("0")
        else:
            f.write("1")


def main():
    node_count, graph, node_for_change = open_file()
    list_for_result = list()
    for i in range(node_count):
        visited_nodes = bfs(graph, i+1)
        if len(visited_nodes) == node_count:
            list_for_result.append("+")
        else:
            list_for_result.append("-")
    write_result_in_file(node_for_change, list_for_result)


if __name__ == "__main__":
    main()
