# -*- coding: utf-8 -*-

import sys
from collections import defaultdict, deque
from itertools import combinations

class Edge:
    def __init__(self, from_node, to_node, weight, directed, name):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.directed = directed
        self.name = name

class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)
        self.vertices = set()
        self.edges = []

    def add_vertex(self, node):
        self.vertices.add(node)

    def add_edge(self, from_node, to_node, weight, directed, name):
        edge = Edge(from_node, to_node, weight, directed, name)
        self.adj_list[from_node].append(edge)
        self.edges.append(edge)
        if not directed:
            reverse_edge = Edge(to_node, from_node, weight, directed, name)
            self.adj_list[to_node].append(reverse_edge)

    def is_weighted(self):
        return any(edge.weight != 1 for edge in self.edges)

    def is_directed(self):
        return any(edge.directed for edge in self.edges)

    def is_connected(self):
        if not self.vertices:
            return True
        
        def dfs(vertex, visited):
            visited.add(vertex)
            for edge in self.adj_list[vertex]:
                if edge.to_node not in visited:
                    dfs(edge.to_node, visited)
        
        visited = set()
        start = next(iter(self.vertices))
        dfs(start, visited)
        return len(visited) == len(self.vertices)
    
    def is_strongly_connected(self):
        """Kontroluje silnou souvislost orientovaného grafu."""
        if not self.is_directed():
            return self.is_connected()

        def dfs(vertex, visited, adj_list):
            visited.add(vertex)
            for edge in adj_list[vertex]:
                if edge.to_node not in visited:
                    dfs(edge.to_node, visited, adj_list)

        # Pro každý vrchol zkontroluj, zda se dostaneme do všech ostatních
        for start in self.vertices:
            visited = set()
            dfs(start, visited, self.adj_list)
            if len(visited) != len(self.vertices):
                return False

        return True

    def is_simple(self):
        """Graf je prostý, pokud nemá rovnoběžné hrany."""
        edge_set = set()
        for edge in self.edges:
            edge_pair = (edge.from_node, edge.to_node)
            if edge_pair in edge_set:
                return False
            if not edge.directed and (edge.to_node, edge.from_node) in edge_set:
                return False
            edge_set.add(edge_pair)
        return True

    def is_elementary(self):
        """Graf je jednoduchý, pokud nemá smyčky ani rovnoběžné hrany."""
        # Kontrola smyček
        for edge in self.edges:
            if edge.from_node == edge.to_node:
                return False
        
        # Kontrola rovnoběžných hran
        return self.is_simple()

    def is_finite(self):
        return len(self.vertices) > 0 and len(self.vertices) < float('inf')

    def is_complete(self):
        n = len(self.vertices)
        if n < 2:
            return True
            
        required_edges = n * (n - 1) // 2  # pro neorientovaný graf
        if self.is_directed():
            required_edges *= 2  # pro orientovaný graf
            
        # Kontrola, zda existuje hrana mezi každými dvěma vrcholy
        actual_edges = set()
        for edge in self.edges:
            actual_edges.add((edge.from_node, edge.to_node))
            if not edge.directed:
                actual_edges.add((edge.to_node, edge.from_node))
                
        return len(actual_edges) == required_edges

    def get_vertex_degree(self, vertex):
        """Vrátí stupeň vrcholu (in-degree + out-degree pro orientovaný graf)"""
        in_degree = sum(1 for edge in self.edges if edge.to_node == vertex)
        out_degree = sum(1 for edge in self.edges if edge.from_node == vertex)
        return in_degree + out_degree if self.is_directed() else out_degree

    def is_regular(self):
        if not self.vertices:
            return True
        
        # Získej stupeň prvního vrcholu jako referenci
        first_vertex = next(iter(self.vertices))
        degree = self.get_vertex_degree(first_vertex)
        
        # Zkontroluj, zda mají všechny vrcholy stejný stupeň
        return all(self.get_vertex_degree(vertex) == degree for vertex in self.vertices)

    def is_bipartite(self):
        if not self.vertices:
            return True
            
        colors = {}  # -1: nenavštíveno, 0: první barva, 1: druhá barva
        
        def can_color_bipartite(start):
            queue = deque([(start, 0)])
            colors[start] = 0
            
            while queue:
                vertex, color = queue.popleft()
                for edge in self.adj_list[vertex]:
                    neighbor = edge.to_node
                    if neighbor not in colors:
                        colors[neighbor] = 1 - color
                        queue.append((neighbor, 1 - color))
                    elif colors[neighbor] == color:
                        return False
            return True
            
        # Zkus obarvit všechny komponenty
        for vertex in self.vertices:
            if vertex not in colors:
                if not can_color_bipartite(vertex):
                    return False
        return True

    def has_k5_subgraph(self):
        if len(self.vertices) < 5:
                return False
        
        # Vytvoříme množinu všech hran pro rychlejší vyhledávání
        edge_set = set()
        for edge in self.edges:
                edge_set.add((edge.from_node, edge.to_node))
                if not edge.directed:
                        edge_set.add((edge.to_node, edge.from_node))
    
        # Pro každou pětici vrcholů
        for v1 in self.vertices:
                for v2 in self.vertices:
                        if v2 == v1:
                                continue
                        for v3 in self.vertices:
                                if v3 in (v1, v2):
                                        continue
                                for v4 in self.vertices:
                                        if v4 in (v1, v2, v3):
                                                continue
                                        for v5 in self.vertices:
                                                if v5 in (v1, v2, v3, v4):
                                                        continue
                            
                                                # Kontrola existence všech 10 hran mezi vrcholy
                                                edges_exist = (
                                                        (v1, v2) in edge_set and (v1, v3) in edge_set and
                                                        (v1, v4) in edge_set and (v1, v5) in edge_set and
                                                        (v2, v3) in edge_set and (v2, v4) in edge_set and
                                                        (v2, v5) in edge_set and (v3, v4) in edge_set and
                                                        (v3, v5) in edge_set and (v4, v5) in edge_set
                                                )
                                                
                                                if edges_exist:
                                                        return True
        return False

    def has_k33_subgraph(self):
        if len(self.vertices) < 6:
                return False
        
        # Vytvoříme množinu všech hran pro rychlejší vyhledávání
        edge_set = set()
        for edge in self.edges:
                edge_set.add((edge.from_node, edge.to_node))
                if not edge.directed:
                        edge_set.add((edge.to_node, edge.from_node))
    
        vertices = list(self.vertices)
        # Pro každou trojici vrcholů na levé straně
        for i in range(len(vertices)-2):
                for j in range(i+1, len(vertices)-1):
                        for k in range(j+1, len(vertices)):
                                left_set = set([vertices[i], vertices[j], vertices[k]])
                
                                # Pro každou trojici vrcholů na pravé straně
                                for x in range(len(vertices)-2):
                                        if vertices[x] in left_set:
                                                continue
                                        for y in range(x+1, len(vertices)-1):
                                                if vertices[y] in left_set:
                                                        continue
                                                for z in range(y+1, len(vertices)):
                                                        if vertices[z] in left_set:
                                                                continue
                                
                                                        right_set = set([vertices[x], vertices[y], vertices[z]])
                            
                                                        # Kontrola existence všech 9 hran mezi množinami
                                                        all_edges_exist = True
                                                        for v1 in left_set:
                                                                for v2 in right_set:
                                                                        if (v1, v2) not in edge_set:
                                                                                all_edges_exist = False
                                                                                break
                                                                if not all_edges_exist:
                                                                        break
                            
                                                        if all_edges_exist:
                                                                return True
        return False

    def is_planar(self):
        # Základní kontrola podle Eulerovy formule
        n = len(self.vertices)
        m = len(self.edges)
    
        if n < 5:
                return True
        
        if m > 3*n - 6:
                return False
        
        # Kontrola zakázaných podgrafů
        if self.has_k5_subgraph():
                return False
        
        if self.has_k33_subgraph():
                return False
        
        return True
            
    def print_adjacency_matrix(self):
        vertex_list = sorted(self.vertices)
        matrix = [[0] * len(vertex_list) for _ in range(len(vertex_list))]

        print("\nMatice sousednosti:")
        print(("   " + " ".join(vertex_list)))
        print(("--+" + "--" * len(vertex_list)))

        for edge in self.edges:
            i = vertex_list.index(edge.from_node)
            j = vertex_list.index(edge.to_node)
            matrix[i][j] = 1
            if not edge.directed:
                matrix[j][i] = 1

        for i, vertex in enumerate(vertex_list):
            print((vertex + " |" + " ".join(str(matrix[i][j]) for j in range(len(vertex_list)))))

    def print_sign_matrix(self):
        vertex_list = sorted(self.vertices)
        matrix = [['-'] * len(vertex_list) for _ in range(len(vertex_list))]

        print("\nZnaménková matice:")
        print(("   " + " ".join(vertex_list)))
        print(("--+" + "--" * len(vertex_list)))

        for edge in self.edges:
            i = vertex_list.index(edge.from_node)
            j = vertex_list.index(edge.to_node)
            matrix[i][j] = '+'
            if not edge.directed:
                matrix[j][i] = '+'

        for i, vertex in enumerate(vertex_list):
            print((vertex + " |" + " ".join(matrix[i][j] for j in range(len(vertex_list)))))

    def print_incidence_matrix(self):
        vertex_list = sorted(self.vertices)

        # Upravené řazení hran - podle čísel v názvu
        def edge_sort_key(name):
            # Extrahuje číslo z názvu hrany (např. 'h1' -> 1)
            # Odstraní všechny nečíselné znaky a převede na číslo
            number = ''.join(filter(str.isdigit, name))
            return int(number)

        sorted_edges = sorted(self.edges, key=lambda edge: edge_sort_key(edge.name))

        matrix = [[0] * len(sorted_edges) for _ in range(len(vertex_list))]
        max_edge_name_length = max(len(edge.name) for edge in sorted_edges)

        print("\nMatice incidence:")
        print((" " * (max_edge_name_length + 2) + "|" + " ".join(edge.name.ljust(max_edge_name_length + 1) for edge in sorted_edges)))
        print(("-" * (max_edge_name_length + 2) + "+" + "-" * (max_edge_name_length + 1) * len(sorted_edges)))

        for e, edge in enumerate(sorted_edges):
            from_index = vertex_list.index(edge.from_node)
            to_index = vertex_list.index(edge.to_node)
            if edge.directed:
                matrix[from_index][e] = 1
                matrix[to_index][e] = -1
            else:
                matrix[from_index][e] = 1
                matrix[to_index][e] = 1

        for i, vertex in enumerate(vertex_list):
            print((vertex.ljust(max_edge_name_length) + "|" + " ".join(str(matrix[i][j]).rjust(max_edge_name_length + 1) for j in range(len(sorted_edges)))))

    def print_distance_matrix(self):
        INF = "*"  # Použijeme text místo nekonečna
        vertex_list = sorted(self.vertices)
        matrix = [[float('inf')] * len(vertex_list) for _ in range(len(vertex_list))]

        # Inicializace matice
        for i in range(len(vertex_list)):
            matrix[i][i] = 0
        for edge in self.edges:
            i = vertex_list.index(edge.from_node)
            j = vertex_list.index(edge.to_node)
            matrix[i][j] = edge.weight
            if not edge.directed:
                matrix[j][i] = edge.weight

        # Najít maximální šířku
        max_width = max(len(str(val)) if val != float('inf') else len(INF) for row in matrix for val in row)
        column_width = max_width + 1

        print("\nMatice delek:")
        # Hlava
        header = " " * (column_width + 1) + "|"
        for vertex in vertex_list:
            header += vertex.center(column_width)
        print(header)

        # Oddělovač
        print(("---+" + "-" * (column_width * len(vertex_list))))

        # Řádky matice
        for i, vertex in enumerate(vertex_list):
            row = vertex.ljust(column_width) + "|"
            for j in range(len(vertex_list)):
                if matrix[i][j] == float('inf'):
                    val = INF
                else:
                    val = str(matrix[i][j])
                row += val.rjust(column_width)
            print(row)

    def print_previous_list(self):
        print()
        print("Seznam predchudcu:")
        # For each vertex, find all vertices that have edges pointing to it
        for v in sorted(self.vertices):
            # Find all edges where this vertex is the destination
            predecessors = []
            for vertex in self.vertices:
                for edge in self.adj_list[vertex]:
                    if edge.to_node == v:
                        predecessors.append(vertex)
            # Sort predecessors for consistent output
            predecessors.sort()
            print("%s: %s" % (v, ' '.join(predecessors)))
         
    def print_successor_list(self):
        print()
        print("Seznam nasledovniku:")
        for v in sorted(self.vertices):
            # Get all vertices that this vertex points to through outgoing edges
            successors = []
            for edge in self.adj_list[v]:
                successors.append(edge.to_node)
            # Sort successors for consistent output
            successors.sort()
            print("%s: %s" % (v, ' '.join(successors)))

    def print_vertices_and_edges(self):
        print()
        print("Seznam uzlu: " + " ".join(sorted(self.vertices)))
    
        def edge_sort_key(name):
            number = ''.join(filter(str.isdigit, name))
            return int(number)
    
        sorted_edges = sorted(self.edges, key=lambda edge: edge_sort_key(edge.name))
    
        print()
        print("Seznam hran:")
        for edge in sorted_edges:
            print("%s: %s -> %s (delka: %s)" % (edge.name, edge.from_node, edge.to_node, edge.weight))

    def print_incident_edges_table(self):
        print()
        print("Tabulka incidentnich uzlu a hran:")
        print("Uzel | Incidentni hrany")
        print("-----------------------")
        for v in sorted(self.vertices):
            incident_edges = [edge.name for edge in self.edges if edge.from_node == v or edge.to_node == v]
            print("%s      | %s" % (v, ' '.join(incident_edges)))

    def print_predecessor_matrix(self):
        INF = 99999
        vertex_list = sorted(self.vertices)
        dist = [[INF] * len(vertex_list) for _ in range(len(vertex_list))]
        pred = [['-'] * len(vertex_list) for _ in range(len(vertex_list))]

        for i in range(len(vertex_list)):
            dist[i][i] = 0

        for edge in self.edges:
            i = vertex_list.index(edge.from_node)
            j = vertex_list.index(edge.to_node)
            dist[i][j] = edge.weight
            if not edge.directed:
                dist[j][i] = edge.weight

        for i in range(len(vertex_list)):
            for j in range(len(vertex_list)):
                if i != j and dist[i][j] != INF:
                    pred[i][j] = vertex_list[i]

        print()
        print("Matice predchudcu:")
        print("   " + " ".join(vertex_list))
        print("--+" + "--" * len(vertex_list))

        for i, vertex in enumerate(vertex_list):
            print(vertex + " |" + " ".join(pred[i][j] for j in range(len(vertex_list))))

    def matrix_multiply(self, matrix1, matrix2):
        """Násobení dvou matic"""
        rows1 = len(matrix1)
        cols1 = len(matrix1[0])
        cols2 = len(matrix2[0])

        result = [[0 for _ in range(cols2)] for _ in range(rows1)]

        for i in range(rows1):
            for j in range(cols2):
                for k in range(cols1):
                    result[i][j] += matrix1[i][k] * matrix2[k][j]

        return result

    def get_adjacency_matrix_power(self, power):
        """Vypočítá n-tou mocninu matice sousednosti"""
        vertex_list = sorted(self.vertices)
        n = len(vertex_list)
        
        # Vytvoření matice sousednosti
        matrix = [[0] * n for _ in range(n)]
        for edge in self.edges:
            i = vertex_list.index(edge.from_node)
            j = vertex_list.index(edge.to_node)
            matrix[i][j] = 1
            if not edge.directed:
                matrix[j][i] = 1
        
        # Výpočet mocniny násobením matic
        result = matrix
        for _ in range(power - 1):
            result = self.matrix_multiply(result, matrix)
        
        return result, vertex_list

    def print_adjacency_matrix_power(self, power):
        """Vytiskne n-tou mocninu matice sousednosti"""
        result, vertex_list = self.get_adjacency_matrix_power(power)
        
        print(f"\nMatice sousednosti na {power}. mocninu:")
        print("   " + " ".join(vertex_list))
        print("--+" + "--" * len(vertex_list))
        
        for i, vertex in enumerate(vertex_list):
            row = vertex + " |" + " ".join(str(result[i][j]) for j in range(len(vertex_list)))
            print(row)

    def get_matrix_determinant(self, matrix):
        """Vypočítá determinant matice rekurzivně pomocí rozvoje podle prvního řádku"""
        n = len(matrix)
        
        # Pro 1x1 matici
        if n == 1:
            return matrix[0][0]
        
        # Pro 2x2 matici
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        determinant = 0
        # Rozvoj podle prvního řádku
        for j in range(n):
            # Vytvoření podmatice
            submatrix = []
            for i in range(1, n):
                row = []
                for k in range(n):
                    if k != j:
                        row.append(matrix[i][k])
                submatrix.append(row)
            
            # Přičtení členu k determinantu
            sign = (-1) ** j
            determinant += sign * matrix[0][j] * self.get_matrix_determinant(submatrix)
        
        return determinant

    def get_laplacian_matrix(self):
        """Vytvoří Laplaceovu matici"""
        vertex_list = sorted(self.vertices)
        n = len(vertex_list)
        
        # Vytvoření matice sousednosti
        adj_matrix = [[0] * n for _ in range(n)]
        for edge in self.edges:
            i = vertex_list.index(edge.from_node)
            j = vertex_list.index(edge.to_node)
            adj_matrix[i][j] = 1
            if not edge.directed:
                adj_matrix[j][i] = 1
        
        # Vytvoření Laplaceovy matice
        laplacian = [[0] * n for _ in range(n)]
        for i in range(n):
            # Diagonální prvky jsou stupně vrcholů
            degree = sum(adj_matrix[i])
            laplacian[i][i] = degree
            # Mimodiagonální prvky jsou záporné hodnoty z matice sousednosti
            for j in range(n):
                if i != j:
                    laplacian[i][j] = -adj_matrix[i][j]
        
        # Výpočet determinantu
        determinant = self.get_matrix_determinant(laplacian)
        
        return laplacian, vertex_list, determinant

    def print_laplacian_matrix(self):
        """Vytiskne Laplaceovu matici"""
        laplacian, vertex_list, determinant = self.get_laplacian_matrix()
        n = len(vertex_list)
        
        # Pro každý sloupec najít maximální šířku čísla
        col_widths = []
        for j in range(n):
            col_width = max(len(str(abs(laplacian[i][j]))) for i in range(n))
            col_width = max(col_width + 1, len(vertex_list[j]))  # +1 pro mínus
            col_widths.append(col_width)

        print("\nLaplaceova matice:")
        # Hlavička
        header = "    " + " ".join(vertex.ljust(col_widths[i]) for i, vertex in enumerate(vertex_list))
        print(header)
        print("--+" + "-" * (len(header) - 3))  # -3 pro "   "
        
        # Řádky matice
        for i, vertex in enumerate(vertex_list):
            values = [str(laplacian[i][j]).rjust(col_widths[j]) for j in range(n)]
            row = vertex + " |" + " ".join(values)
            print(row)

        # Pro stromy platí, že determinant kofaktoru je roven počtu koster grafu
        if n > 1:
            submatrix = [row[:-1] for row in laplacian[:-1]]
            cofactor = self.get_matrix_determinant(submatrix)
            print(" ")
            print(f"Determinant: {cofactor}")
            if cofactor > 0:
                print(f"Počet koster grafu: {cofactor}")

    def get_in_degree(self, vertex):
        """Vrátí vstupní stupeň vrcholu (počet hran směřujících do vrcholu)"""
        return sum(1 for edge in self.edges if edge.to_node == vertex)
    
    def get_out_degree(self, vertex):
        """Vrátí výstupní stupeň vrcholu (počet hran vycházejících z vrcholu)"""
        return sum(1 for edge in self.edges if edge.from_node == vertex)
    
    def print_vertex_degree(self):
        """Vytiskne vstupní a výstupní stupně všech vrcholů"""
        print("\nStupně vrcholů:")
        print("Vrchol | Vstupní | Výstupní")
        print("-------------------------")
        for v in sorted(self.vertices):
            in_deg = self.get_in_degree(v)
            out_deg = self.get_out_degree(v)
            print(f"{v:6} | {in_deg:8} | {out_deg:9}")

    def get_input_neighborhood(self, vertex):
        """Vrátí množinu vrcholů, ze kterých vede hrana do daného vrcholu"""
        return {edge.from_node for edge in self.edges if edge.to_node == vertex}
    
    def get_output_neighborhood(self, vertex):
        """Vrátí množinu vrcholů, do kterých vede hrana z daného vrcholu"""
        return {edge.to_node for edge in self.edges if edge.from_node == vertex}

    def print_neighborhoods(self):
        """Vytiskne vstupní a výstupní okolí všech vrcholů"""
        print("\nOkolí vrcholů:")
        for v in sorted(self.vertices):
            in_neigh = sorted(self.get_input_neighborhood(v))
            out_neigh = sorted(self.get_output_neighborhood(v))
            print(f"Vrchol {v}:")
            print(f"  Vstupní okolí:  {' '.join(in_neigh)}")
            print(f"  Výstupní okolí: {' '.join(out_neigh)}")


def parse_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    graph = Graph()
    edge_name_map = {}
    
    # Process each line, skipping empty ones
    for line in lines:
        # Remove whitespace and semicolon if present
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        if line[-1] == ';':
            line = line[:-1]
            
        # Split the line into parts and filter out empty strings
        parts = [part for part in line.split() if part]
        
        if not parts:  # Skip if line is empty after splitting
            continue

        if parts[0] == 'u':
            vertex = parts[1]
            graph.add_vertex(vertex)

        elif parts[0] == 'h':
            from_node = parts[1]
            separator = parts[2]  # <, >, or -
            to_node = parts[3]
            
            # Automatically add vertices if they don't exist
            if from_node not in graph.vertices:
                graph.add_vertex(from_node)
            if to_node not in graph.vertices:
                graph.add_vertex(to_node)

            # Process weight and edge name
            weight = None
            edge_name = None

            if len(parts) > 4:
                weight_part = parts[4]
                # Check if weight is a number
                if weight_part.isdigit():
                    weight = int(weight_part)
                    edge_name = parts[5][1:] if len(parts) > 5 else None
                elif weight_part.startswith(':'):
                    edge_name = weight_part[1:]  # Remove colon

            if len(parts) == 6:
                if parts[5].startswith(':'):
                    edge_name = parts[5][1:]  # Remove colon

            directed = separator != '-'
            if directed and separator == '<':
                from_node, to_node = to_node, from_node

            graph.add_edge(from_node, to_node, weight or 1, directed, edge_name)

    return graph
    
if __name__ == "__main__":
    graph = parse_graph_from_file("data2.txt")
    
    print("\n")
    print("=======================================================================================")
    print("VLASTNOSTI GRAFŮ:")
    print(("1) Ohodnocený:  {0}".format('ANO' if graph.is_weighted() else 'NE')))
    print(("2) Orientovaný: {0}".format('ANO' if graph.is_directed() else 'NE')))
    print(("3) Souvislý:    {0}".format('ANO' if (not graph.is_directed() and graph.is_connected()) or 
                                          (graph.is_directed() and graph.is_strongly_connected()) 
                                   else 'NE')))
    print(("4) Prostý:      {0}".format('ANO' if graph.is_simple() else 'NE')))
    print(("5) Jednoduchý:  {0}".format('ANO' if graph.is_elementary() else 'NE')))
    print(("6) Konečný:     {0}".format('ANO' if graph.is_finite() else 'NE')))
    print(("7) Úplný:       {0}".format('ANO' if graph.is_complete() else 'NE')))
    print(("8) Regulární:   {0}".format('ANO' if graph.is_regular() else 'NE')))
    print(("9) Bipartitní:  {0}".format('ANO' if graph.is_bipartite() else 'NE')))
    
    # Základní charakteristiky
    graph.print_vertex_degree()  # Vstupní/výstupní stupně
    graph.print_neighborhoods()   # Vstupní/výstupní okolí
    graph.print_previous_list()   # Předchůdci
    graph.print_successor_list()  # Následníci
    
    # Matice
    print("\nMATICE:")
    graph.print_adjacency_matrix()
    graph.print_adjacency_matrix_power(2)  # Mocnina matice sousednosti
    graph.print_sign_matrix()
    graph.print_incidence_matrix()
    graph.print_distance_matrix()
    graph.print_predecessor_matrix()
    graph.print_laplacian_matrix()
    
    # Seznamy a tabulky
    graph.print_vertices_and_edges()
    graph.print_incident_edges_table()