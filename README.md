# ucca-tool

This repository contains various tools to visualize and understand the ucca parse xml files.

#Print path from a xml file

To print path from word to root node from a ucca parsed xml file

```
python prog/xml-print-path.py example/toy.xml
```
# xml read 

It prints the path as above but in an interactive manner for a given word
```
python prog/xml-read.py example/toy.xml
```


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






