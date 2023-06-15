import networkx as nx
import matplotlib.pyplot as plt
import pydot
from sqlalchemy import create_engine, MetaData

# Configure SQLAlchemy engine
engine = create_engine(r"sqlite:///D:\Sandu\Sandu\PortfolioProject\publicServer\Database\companies.db")

# Reflect the database schema using SQLAlchemy
metadata = MetaData(bind=engine)
metadata.reflect()

# Create an empty directed graph using NetworkX
graph = nx.DiGraph()

# Iterate over the tables in the reflected metadata
for table in metadata.tables.values():
    # Add the table as a node in the graph
    graph.add_node(table.name, shape='box')

    # Add the columns as nodes in the graph
    for column in table.columns:
        column_name = f'{table.name}.{column.name}'
        graph.add_node(column_name, shape='ellipse')
        graph.add_edge(table.name, column_name)

# Create a PyDot graph from NetworkX graph
dot_graph = nx.nx_pydot.to_pydot(graph)

# Customize table and column labels
for table in metadata.tables.values():
    table_node = dot_graph.get_node(table.name)[0]
    table_node.set_label(f'<<table border="0" cellborder="1" cellspacing="0">{table.name}|')
    for column in table.columns:
        column_name = f'{table.name}.{column.name}'
        column_nodes = dot_graph.get_node(column_name)
        if column_nodes:
            column_node = column_nodes[0]
            column_node.set_label(f'<{column_name}>{column.name}|')
    table_node.set_label(f'{table_node.get_label()}>>')

# Save the dot file
dot_graph.write_png('database_diagram.png')

# Display the diagram
image = plt.imread('database_diagram.png')
plt.imshow(image)
plt.axis('off')
plt.show()