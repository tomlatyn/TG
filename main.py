import sys
from io import StringIO
import contextlib

from grafy import parse_graph_from_file

def export_graph_data(graph, output_file):
    # Create a string buffer to capture the output
    output = StringIO()
    
    # Redirect stdout to our string buffer
    with contextlib.redirect_stdout(output):
        print("\n\n=======================================================================================")
        print("VLASTNOSTI GRAFŮ:")
        print("1) Ohodnocený:  {0}".format('ANO' if graph.is_weighted() else 'NE'))
        print("2) Orientovaný: {0}".format('ANO' if graph.is_directed() else 'NE'))
        print("3) Souvislý:    {0}".format('ANO' if graph.is_connected() else 'NE'))
        print("4) Prostý:      {0}".format('ANO' if graph.is_simple() else 'NE'))
        print("5) Jednoduchý:  {0}".format('ANO' if graph.is_elementary() else 'NE'))
        print("6) Konečný:     {0}".format('ANO' if graph.is_finite() else 'NE'))
        print("7) Úplný:       {0}".format('ANO' if graph.is_complete() else 'NE'))
        print("8) Regulární:   {0}".format('ANO' if graph.is_regular() else 'NE'))
        print("9) Bipartitní:  {0}".format('ANO' if graph.is_bipartite() else 'NE'))
        print("\nMATICE:")

        graph.print_adjacency_matrix()
        graph.print_sign_matrix()
        graph.print_incidence_matrix()
        graph.print_distance_matrix()
        graph.print_predecessor_matrix()
        graph.print_neighbor_list()
        graph.print_vertices_and_edges()
        graph.print_incident_edges_table()

    # Write the captured output to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output.getvalue())

if __name__ == "__main__":
    graph = parse_graph_from_file("grafy/01.tg")
    export_graph_data(graph, "graph_output.txt")
    print("Data has been exported to graph_output.txt")