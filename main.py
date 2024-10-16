import re
from collections import defaultdict

class Graph:
    def __init__(self):
        self.nodes = {}  # Změněno na slovník pro uchování ohodnocení uzlů
        self.edges = defaultdict(dict)
        self.edge_labels = {}

    def add_node(self, node, value=None):
        self.nodes[node] = value

    def add_edge(self, from_node, to_node, direction, weight=None, label=None):
        self.edges[from_node][to_node] = weight
        if direction in ('-', '<'):
            self.edges[to_node][from_node] = weight
        if label:
            self.edge_labels[(from_node, to_node)] = label

    def is_weighted(self):
        return len(set(weight for edges in self.edges.values() for weight in edges.values() if weight is not None)) > 1 or len(set(self.nodes.values())) > 1

    def is_directed(self):
        for from_node in self.edges:
            for to_node in self.edges[from_node]:
                if to_node not in self.edges or from_node not in self.edges[to_node]:
                    return True
        return False

    def is_connected(self):
        if not self.nodes:
            return True
        visited = set()
        start_node = next(iter(self.nodes))
        self._dfs(start_node, visited)
        return len(visited) == len(self.nodes)

    def _dfs(self, node, visited):
        visited.add(node)
        for neighbor in self.edges[node]:
            if neighbor not in visited:
                self._dfs(neighbor, visited)

    def is_simple(self):
        for from_node in self.edges:
            if from_node in self.edges[from_node]:  # self-loop
                return False
            if len(self.edges[from_node]) != len(set(self.edges[from_node])):  # multiple edges
                return False
        return True

    def is_complete(self):
        n = len(self.nodes)
        for node in self.nodes:
            if len(self.edges[node]) != n - 1:
                return False
        return True

    def is_regular(self):
        degrees = [len(self.edges[node]) for node in self.nodes]
        return len(set(degrees)) == 1

    def is_bipartite(self):
        if not self.nodes:
            return True
        color = {}
        for node in self.nodes:
            if node not in color:
                if not self._is_bipartite_util(node, color):
                    return False
        return True

    def _is_bipartite_util(self, node, color):
        color[node] = 1
        queue = [node]
        while queue:
            u = queue.pop(0)
            for v in self.edges[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return False
        return True

    def _get_bipartite_partitions(self):
        if not self.nodes:
            return []
        color = {}
        for node in self.nodes:
            if node not in color:
                if not self._is_bipartite_util(node, color):
                    return []  # Not bipartite
        
        partition1 = [node for node, c in color.items() if c == 0]
        partition2 = [node for node, c in color.items() if c == 1]
        return [partition1, partition2]

    def is_planar_approximation(self):
        V = len(self.nodes)
        E = sum(len(edges) for edges in self.edges.values()) // 2  # assuming undirected

    # Check Euler's formula
        if E > 3*V - 6:
            return False

    # Check for K5 (complete graph with 5 vertices)
        if V >= 5 and self.is_complete():
            return False

    # Improved check for K3,3 (complete bipartite graph with 3+3 vertices)
        if V == 6 and self.is_bipartite():
        # Count edges between the two partitions
            partitions = self._get_bipartite_partitions()
            if partitions and len(partitions[0]) == 3 and len(partitions[1]) == 3:
                cross_edges = sum(len(set(self.edges[u]) & set(partitions[1])) for u in partitions[0])
                if cross_edges == 9:
                    return False

        return "Pravděpodobně rovinný"


def read_input_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Soubor '{filename}' nebyl nalezen.")
        return []
    except IOError:
        print(f"Chyba při čtení souboru '{filename}'.")
        return []

def parse_input(lines):
    graph = Graph()
    node_pattern = r'u\s+(\w+)(?:\s+(\d+))?'
    edge_pattern = r'h\s+(\w+)\s+([<\->])\s+(\w+)(?:\s+(\d+))?(?:\s+:(\w+))?'

    for line in lines:
        line = line.strip()
        if line.startswith('u'):
            match = re.match(node_pattern, line)
            if match:
                node, value = match.groups()
                graph.add_node(node, int(value) if value else None)
        elif line.startswith('h'):
            match = re.match(edge_pattern, line)
            if match:
                from_node, direction, to_node, weight, label = match.groups()
                if from_node in graph.nodes and to_node in graph.nodes:
                    graph.add_edge(from_node, to_node, direction, int(weight) if weight else None, label)
                else:
                    print(f"Chyba: Hrana {from_node} - {to_node} nemůže být vytvořena, protože jeden nebo oba uzly neexistují.")

    return graph

def analyze_graph(graph):
    properties = {
        'a) ohodnocený': graph.is_weighted(),
        # Ohodnocený graf má přiřazené hodnoty k uzlům nebo hranám.
        # Určuje se kontrolou, zda existují různé nenulové hodnoty pro uzly nebo hrany.

        'b) orientovaný': graph.is_directed(),
        # Orientovaný graf má hrany s určeným směrem.
        # Určuje se kontrolou, zda existuje alespoň jedna hrana, která není obousměrná.

        'c) souvislý': graph.is_connected(),
        # Souvislý graf je takový, kde existuje cesta mezi každými dvěma uzly.
        # Určuje se pomocí prohledávání do hloubky (DFS) z libovolného uzlu.
        # Pokud DFS navštíví všechny uzly, graf je souvislý.

        'd) prostý': graph.is_simple(),
        # Prostý graf nemá smyčky (hrany spojující uzel sám se sebou) ani vícenásobné hrany mezi stejnými uzly.
        # Určuje se kontrolou absence smyček a vícenásobných hran.

        'e) jednoduchý': graph.is_simple() and not graph.is_directed(),
        # Jednoduchý graf je prostý a neorientovaný.
        # Určuje se kombinací kontrol pro prostý a neorientovaný graf.

        'f) rovinný': graph.is_planar_approximation(),
        # Rovinný graf lze nakreslit v rovině bez křížení hran.
        # Přesné určení je složité, proto se používá aproximace:
        # - Kontrola Eulerovy formule (E ≤ 3V - 6, kde E je počet hran a V počet vrcholů)
        # - Kontrola, zda graf neobsahuje podgrafy K5 nebo K3,3

        'g) konečný': True,
        # Konečný graf má konečný počet uzlů a hran.
        # V našem případě je vždy True, protože pracujeme s konečnými vstupními daty.

        'h) úplný': graph.is_complete(),
        # Úplný graf má hranu mezi každými dvěma různými uzly.
        # Určuje se kontrolou, zda každý uzel má hranu ke všem ostatním uzlům.

        'i) regulární': graph.is_regular(),
        # Regulární graf má stejný stupeň pro všechny uzly (každý uzel má stejný počet sousedů).
        # Určuje se kontrolou, zda všechny uzly mají stejný počet sousedních uzlů.

        'j) bipartitní': graph.is_bipartite()
        # Bipartitní graf lze rozdělit na dvě množiny uzlů tak, že každá hrana spojuje uzly z různých množin.
        # Určuje se algoritmem obarvování: pokud lze uzly obarvit dvěma barvami tak, 
        # že sousední uzly mají vždy různé barvy, graf je bipartitní.
    }
    return properties

# Hlavní část programu
if __name__ == "__main__":
    filename = "data2.txt"
    lines = read_input_file(filename)
    
    if lines:
        graph = parse_input(lines)
        results = analyze_graph(graph)

        print(f"Analýza grafu ze souboru '{filename}':")
        for property, value in results.items():
            print(f"{property}: {value}")
    else:
        print("Program ukončen kvůli chybě při čtení vstupního souboru.")