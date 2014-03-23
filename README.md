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

G = RoadGraph.grid_graph(4, 4)
```
###Visualize the graph
```python
G.show()
```
###Calculate key metrics for the graph
```python
print 'graph_length=%s' % G.length
print 'mean_path_length=%s' % G.mean_path_length
```
###Drop two edges from the graph
```python
edge = G.get_removal_target()
G.remove_edge(*edge)
edge = G.get_removal_target()
G.remove_edge(*edge)
show(G)
```
###Add an edge to the graph
```python
edge = G.get_addition_target()
G.add_edge(*edge)
show(G)
```
###Add or remove edges, depending on whether there is capacity for a new edge without exceeding the target graph_length
```python
for i in xrange(10): # run 10 iterations of adding or removing edges
  G.iterate()
show(G)
```
