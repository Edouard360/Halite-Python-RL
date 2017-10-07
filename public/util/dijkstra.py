"""The dijkstra module"""
import numpy as np


class Prioritydictionary(dict):
    """A priority dictionary"""
    def __init__(self):
        """Initialize Prioritydictionary by creating binary heap of
        pairs (value,key). Note that changing or removing a dict entry
        will not remove the old pair from the heap until it is found by
        smallest() or until the heap is rebuilt."""
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        """Find smallest item after removing deleted items from front of
        heap."""
        if len(self) == 0:
            raise IndexError("smallest of empty Prioritydictionary")
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            last_item = heap.pop()
            insertion_point = 0
            while 1:
                small_child = 2 * insertion_point + 1
                if small_child + 1 < len(heap) and \
                                heap[small_child] > heap[small_child + 1]:
                    small_child += 1
                if small_child >= len(heap) or last_item <= heap[small_child]:
                    heap[insertion_point] = last_item
                    break
                heap[insertion_point] = heap[small_child]
                insertion_point = small_child
        return heap[0][1]

    def __iter__(self):
        """Create destructive sorted iterator of Prioritydictionary."""

        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]

        return iterfn()

    def __setitem__(self, key, val):
        """Change value stored in dictionary and add corresponding pair
        to heap. Rebuilds the heap if the number of deleted items gets
        large, to avoid memory leakage."""
        dict.__setitem__(self, key, val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v, k) for k, v in self.items()]
            self.__heap.sort()
            # builtin sort probably faster than O(n)-time heapify
        else:
            new_pair = (val, key)
            insertion_point = len(heap)
            heap.append(None)
            while insertion_point > 0 and \
                            new_pair < heap[(insertion_point - 1) // 2]:
                heap[insertion_point] = heap[(insertion_point - 1) // 2]
                insertion_point = (insertion_point - 1) // 2
            heap[insertion_point] = new_pair

    def setdefault(self, key, val):
        """Reimplement setdefault to pass through our customized __setitem__."""
        if key not in self:
            self[key] = val
        return self[key]


def dijkstra(g, start, end=None):
    """The dijkstra algorithm"""
    d = {}  # dictionary of final distances
    p = {}  # dictionary of predecessors
    q = Prioritydictionary()  # estimated distances of non-final vertices
    q[start] = 0

    for v in q:
        d[v] = q[v]
        if v == end:
            break

        for w in g[v]:
            vw_length = d[v] + g[v][w]
            if w in d:
                if vw_length < d[w]:
                    raise ValueError("Dijkstra: found better path to already-final vertex")
            elif w not in q or vw_length < q[w]:
                q[w] = vw_length
                p[w] = v

    return d, p


class Graph:
    """The Graph object"""
    def __init__(self):
        self.g = {}

    def add_node(self, value):
        if value not in self.g:
            self.g[value] = {}

    def add_edge(self, from_node, to_node):
        self.g[from_node][to_node] = 1
        self.g[to_node][from_node] = 1

    def remove_node(self, value):
        for to in self.g[value]:
            self.g[to].pop(value, None)
        self.g.pop(value, None)

    def update(self, new_state, previous_state):
        for (i, j), k in np.ndenumerate(new_state - previous_state):
            if k == 1:
                self.add_node((i, j))
                for i1, j1 in [(i - 1, j), (i, j + 1), (i, j - 1), (i + 1, j)]:
                    if (i1, j1) in self.g:
                        self.add_edge((i, j), (i1, j1))
            elif k == -1:
                self.remove_node((i, j))


def build_graph_from_state(state):
    """Build the graph from the state"""
    def take(state, i, j):
        return np.take(np.take(state, j, axis=1, mode='wrap'), i, axis=0, mode='wrap')

    g = Graph()
    g.add_node(0)
    for (i, j), k in np.ndenumerate(state):
        if k == 1:
            g.add_node((i, j))
            n, e, w, s = take(state, i - 1, j), take(state, i, j + 1), take(state, i, j - 1), take(state, i + 1, j)
            if s:
                g.add_node(((i + 1) % state.shape[0], j))
                g.add_edge((i, j), ((i + 1) % state.shape[0], j))
            if e:
                g.add_node((i, (j + 1) % state.shape[1]))
                g.add_edge((i, j), (i, (j + 1) % state.shape[1]))
            if n * e * w * s == 0:
                g.add_edge((i, j), 0)
    return g
