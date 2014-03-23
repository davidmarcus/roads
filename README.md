roads
=====

An analysis of road network optimization

# Installation
```bash
sudo apt-get -y install ipython
sudo pip install -r requirements.txt
```

# Execution
Code is currently contained entirely within roads.py. It's easiest to interact with the code using an ipython shell.

## Examples
###Create a graph for a 4x4 grid
```python
from roads import *
G = grid_graph(4, 4)
```
###Visualize the graph
```python
show(G)
```
###Calculate key metrics for the graph
```python
print 'graph_length=%s' % graph_length(G)
print 'mean_path_length=%s' % mean_path_length(G)
```
###Drop two edges from the graph
```python
edge = get_removal_target(G)
G.remove_edge(*edge)
edge = get_removal_target(G)
G.remove_edge(*edge)
show(G)
```
###Add an edge to the graph
```python
edge = get_addition_target(G)
add_edge(G, edge)
show(G)
```
###Add or remove edges, depending on whether there is capacity for a new edge without exceeding the target graph_length
```python
for i in xrange(10): # run 10 iterations of adding or removing edges
  iterate(G)
show(G)
```
