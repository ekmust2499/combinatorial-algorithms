from copy import copy


def open_file():
    array = list()
    with open("in.txt", "r") as f:
        data = f.readlines()
        counts = data[0]
        counts = counts.rstrip().split(" ")
        count_in_X = counts[0]
        count_in_Y = counts[1]
        size_array = int(data[1].rstrip())
        data = data[2:]
        for element in data:
            elements = element.rstrip().split(" ")
            for number in elements:
                array.append(int(number))
    edges = list()
    count = 0
    share_X = set()
    share_Y = set()
    list_isolated_nodes = []
    metka = True
    while metka:
        if array[count] == 0:
            list_isolated_nodes.append(str(count) +"X")
            count += 1
        elif array[array[count]-1] == 32767:
            metka = False
            break
        else:
            if array[count] < array[count + 1]:
                for i in array[array[count] - 1:array[count + 1] - 1]:
                    element = (str(count) + 'X', str(i) + 'Y')
                    share_X.add(str(count) + 'X')
                    share_Y.add(str(i) + 'Y')
                    edges.append(element)
                    #print(element)
                count += 1

            else:
                y = count
                x = count
                while array[x+1] == 0:
                    x += 1
                count = x+1
                for i in array[array[y]-1:array[count]-1]:
                    element = (str(y) + 'X', str(i) + 'Y')
                    share_X.add(str(y) + 'X')
                    share_Y.add(str(i) + 'Y')
                    edges.append(element)
                count = y+1
    #print(edges)
    #print(list_isolated_nodes)
    return count, count_in_Y, list(share_X), list(share_Y), edges, list_isolated_nodes


def add_s_t(edges):
    edges2 = copy(edges)
    for i in edges2:
        edges.append(('s', i[0]))
        edges.append((i[1], 't'))
    edg = set(edges)
    return list(edg)


def write_result_in_file(list_isolated_nodes, result, share_X, count_in_X):
    share = []

    for i in share_X:
        k = i[:-1]
        share.append(k)
    share.sort()

    len_list = len(list_isolated_nodes)

    #if len_list != 0:
    #    end = ['0'] * (count_in_X-len_list)
    #else:
    end = ['0'] * count_in_X

    for edge in result:
        if edge[0][:-1] in share:
            end[int(edge[0][:-1])] = edge[1][:-1]

    #if len_list != 0:
    #   for i in list_isolated_nodes:
    #        end.insert(int(i[:-1]), '0')
    #if is_isolated_node:
     #   end.insert(0, "0")

    if count_in_X == len(end):
        with open("out.txt", "w") as f:
            num = 0
            for i in end:
                f.write(str(i) + " ")
                num += 1
                if num == 10:
                    f.write("\n")
                    num = 0
    #print(result)
    #print(end)


class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v
        self.capacity = w


class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}

    def add_vertex(self, vertex):
        self.adj[vertex] = []

    def get_edges(self, v):
        return self.adj[v]

    def add_edge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w)
        redge = Edge(v,u,0)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0

    def find_path(self, source, sink, path, path_set):
        if source == sink:
            return path
        for edge in self.get_edges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge, residual) in path_set:
                path_set.add((edge, residual))
                result = self.find_path(edge.sink, sink, path +
                [(edge,residual)], path_set)
                if result != None:
                    return result

    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [], set())
        while path != None:
            flow = min(res for edge,res in path)
            for edge, res in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [], set())

        res = []
        for key, value in self.flow.items():
            if key.source != 's' and key.sink != 't':
                if self.flow[key] == 1:
                    res.append((key.source, key.sink))
        size_flow = sum(self.flow[edge] for edge in self.get_edges(source))
        return res


def main():
    count_nodes_in_X, count_nodes_in_Y, share_X, share_Y, edges, list_isolated_nodes = open_file()
    nodes = ['s'] + share_X + share_Y + ['t']
    edges_with_s_t = add_s_t(edges)
    g = FlowNetwork()
    [g.add_vertex(v) for v in nodes]
    for edge in edges_with_s_t:
        g.add_edge(edge[0], edge[1], 1)

    result = g.max_flow('s', 't')
    write_result_in_file(list_isolated_nodes, result, share_X, count_nodes_in_X)


if __name__ == "__main__":
    main()
