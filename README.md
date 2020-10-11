# ucca-tool

This repository contains various tools to visualize and understand the ucca parse xml files.

# View construction:

To view various linguistic constructions in a passage.

```
python prog/find_construction.py examples/116.xml
```


# visualize a xml file

To visualize a ucca parserd file in xml format in a tree structure.

```
python prog/visualize.py  -o image examples/toy.xml -o 
```

It will create the image (png file) inside the 'image' directory.

# print path 

To print path upto the root node from a given word in a passage


```
python xml-print-path.py example/toy.xml

```
It asks interactively for which word you want to see the path 




