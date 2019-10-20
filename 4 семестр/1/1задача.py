from collections import deque


def open_file():
    with open("in.txt", "r") as f:
        data = f.readlines()
        node_count = int(data[0])
        adjacency_list = list()
        for line in data[1:len(data)]:
            line = line.rstrip().split(" ")
            k = line[0:-1]
            if k == []:
                adjacency_list.append(["0"])
            else:
                adjacency_list.append(k)
    return node_count, adjacency_list


def bfs(adjacency_list, s):
    queue = deque()
    visited = list()
    visited.append(s)
    queue.append(s)

    while queue:
        current = queue.popleft()
        for neighbor in adjacency_list[current-1]:
            if int(neighbor) not in visited:
                visited.append(int(neighbor))
                queue.append(int(neighbor))
    print(visited)
    return sorted(visited)


def write_result_in_file(number_of_comp, components):
    with open("out.txt", "w") as f:
        f.write(str(number_of_comp)+ "\n")
        for i in components:
            for k in i:
                f.write(str(k) + " ")
            f.write("0\n")


def main():
    nodes, adjacency_list = open_file()
    data = set()
    for i in range(nodes):
        if adjacency_list[i] == ["0"]:
            data.add(tuple([i+1]))
        else:
            x = bfs(adjacency_list, i+1)
            data.add(tuple(x))
    finish = sorted([list(i) for i in data])
    for i in range(len(finish)-1):
        if set(finish[i+1]).intersection(set(finish[i])):
            finish.pop(i+1)
            break
    write_result_in_file(len(finish), finish)
    #print(len(finish), finish)


if __name__ == "__main__":
    main()
