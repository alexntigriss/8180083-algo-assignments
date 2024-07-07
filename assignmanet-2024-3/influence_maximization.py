import argparse
import random
from collections import defaultdict, deque

class Graph:
    def __init__(self, filename):
        self.graph = defaultdict(list)
        self._parse_and_load_graph(filename)

    def _parse_and_load_graph(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                edge, vertex = map(int, line.split())
                if edge not in self.graph:
                    self.graph[edge] = []
                self.graph[edge].append(vertex)

    def get_neighbors(self, node):
        return self.graph[node]

class SeedSelector:
    def __init__(self, graph):
        self.graph = graph

    def select_max_degree_seeds(self, k):
        degrees = {}
        for node, neighbors in self.graph.graph.items():
            degrees[node] = len(neighbors)
        sorted_nodes = []
        for node in degrees:
            sorted_nodes.append(node)
        sorted_nodes.sort(key=lambda x: degrees[x], reverse=True)
        return sorted_nodes[:k]


    def select_greedy_seeds(self, k, p, mc):
        seeds = []
        for _ in range(k):
            best_node = None
            max_influence = -1e100
            for node in set(self.graph.graph.keys()) - set(seeds):
                test_seeds = seeds + [node]
                total_influence = 0
                for i in range(mc):
                    total_influence += IndependentCascadeModel(self.graph, test_seeds, p).exec() / (i + 1)
                influence = total_influence / mc
                if influence > max_influence:
                    max_influence = influence
                    best_node = node
            seeds.append(best_node)
        return seeds
    
class IndependentCascadeModel:
    def __init__(self, graph, seeds, p):
        self.graph = graph
        self.active = set(seeds)
        self.queue = deque(seeds)
        self.probability = p

    def exec(self):
        while self.queue:
            u = self.queue.popleft()
            for v in self.graph.get_neighbors(u):
                if v not in self.active and random.random() < self.probability:
                    self.active.add(v)
                    self.queue.append(v)
        return len(self.active)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('graph', type=str)
    parser.add_argument('k', type=int)
    parser.add_argument('method', choices=['max_degree', 'greedy'])
    parser.add_argument('probability', type=float)
    parser.add_argument('mc', type=int)
    parser.add_argument('-r', '--random_seed', type=int, default=None)
    args = parser.parse_args()

    graph_path = args.graph
    k = args.k
    method = args.method
    p = args.probability
    mc = args.mc
    rs = args.random_seed


    if rs is not None:
        random.seed(rs)
    else:
        random.seed()

    graph = Graph(graph_path)
    seedSelector = SeedSelector(graph)

    if method == 'max_degree':
        seeds = seedSelector.select_max_degree_seeds(k)
    elif method == 'greedy':
        seeds = seedSelector.select_greedy_seeds(k, p, mc)

    influences = [sum(IndependentCascadeModel(graph, seeds[:i+1], p).exec() for _ in range(mc)) / mc for i in range(len(seeds))]

    
    print(f"Selected Seeds: {seeds}")
    print(f"Influences: {influences}")

if __name__ == "__main__":
    main()