row_count = 0
column_count = 0


def list_of_str_in_list_of_int(line):
    line = list(map(int, line))
    return line


def open_file():
    with open("in.txt", "r") as f:
        data = f.readlines()
        global row_count
        global column_count
        row_count = int(data[0])
        column_count = int(data[1])
        maze = list()
        for line in data[2:row_count+2]:
            line = line.rstrip().split(" ")
            line = list_of_str_in_list_of_int(line)
            maze.append(line)
        start = data[-2].rstrip().split(" ")
        start = list_of_str_in_list_of_int(start)
        finish = data[-1].rstrip().split(" ")
        finish = list_of_str_in_list_of_int(finish)

    return maze, start, finish


def dfs(start, finish, maze):
    visited = list()
    stack = list()
    stack.append(start)
    prev = dict()
    father = dict()
    father[tuple(start)] = 0
    prev[tuple(start)] = "Y"
    while stack:
        current = stack[-1]
        if current not in visited:
            visited.append(current)
        if current == finish:
            return "Y", prev
        neighbors = list()
        if current[0] != row_count:
            neighbor1 = current.copy()
            neighbor1[0] = current[0] + 1
            neighbors.append(neighbor1)
        if current[0] != 1:
            neighbor3 = current.copy()
            neighbor3[0] = current[0] - 1
            neighbors.append(neighbor3)
        if current[1] != column_count:
            neighbor2 = current.copy()
            neighbor2[1] = current[1] + 1
            neighbors.append(neighbor2)
        if current[1] != 1:
            neighbor4 = current.copy()
            neighbor4[1] = current[1] - 1
            neighbors.append(neighbor4)

        count_neighbor = 0
        visited_neighbor = 0
        for i in neighbors:
            if maze[i[0] - 1][i[1] - 1] == 0:
                count_neighbor = count_neighbor + 1
                if i in visited:
                    visited_neighbor = visited_neighbor + 1
                else:
                    stack.append(i)
                    father[tuple(i)] = current
                    prev[tuple(i)] = current
        if count_neighbor == visited_neighbor:
            stack.pop()

    return "N", None


def write_result_in_file(res, path, start, finish):
    with open("out.txt", "w") as f:
        if res == "N":
            f.write("N")
        else:
            num = finish
            res = list()
            f.write("Y\n")
            res.append(finish)
            while num != start:
                num = path[tuple(num)]
                res.append(num)
            res.reverse()
            for num in res:
                f.write("{0} {1}\n".format(str(num[0]), str(num[1])))


def main():
    maze, start, finish = open_file()
    res, path = dfs(start, finish, maze)
    write_result_in_file(res,path, start, finish)


if __name__ == "__main__":
    main()
