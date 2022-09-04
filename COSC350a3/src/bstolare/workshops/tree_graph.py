""" 
    Graph: animated graph with Tkinter.
    COSC350/550 Workshop 3
"""

import time
import math
from threading import Thread
from tkinter import *
import sys

# Start global variables #
quit = False
width = 500
height = 500
node_size = 28
delay = 0.05
inter = 0
# node connections - adjacency list - dictionary node number: [list]
node_graph = {1:[2,5,6],
              2:[1,3],
              3:[2,4,5],
              4:[3,7,9],
              5:[1,3,6],
              6:[1,5,7,10],
              7:[4,6,8],
              8:[7,9],
              9:[4,8,10],
              10:[6,9,11],
              11:[10]}
# node locations- node locations have been determined for you:
node_locs = [[98,64],[212,33],[325,31],[390,121],[210,150],[115,235],
             [310,210],[220,290],[325,330],[150,360],[205,470]]

visited = []
explored = []
node_items = []
# End global variables #

def create_node(x, y, r, canvasName,colour,obj_tag): 
    "Create circle with fill colour: (x,y): center coordinates, r: radius "
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,fill=colour,tag=obj_tag)

def create_branch(x0, y0, x1, y1, canvasName,colour,obj_tag): 
    "Create line with fill colour: (x0,y0 to x1,y1): "
    return canvasName.create_line(x0, y0, x1, y1,fill=colour,width=3,tag=obj_tag)

def create_plot(myCanvas):
    " Create initial plot with graph nodes  "
    global node_size
    global node_locs
    global explored
    global node_items
    
    #delete before redraw                              
    for item in node_items:                             
       myCanvas.delete(item)   
    made_cons = []
    for key in node_graph:
        for con in node_graph[key]:
            if {node_locs[key-1][0],node_locs[key-1][1],
                node_locs[con-1][0],node_locs[con-1][1]} not in made_cons:
                create_branch(node_locs[key-1][0],node_locs[key-1][1],
                              node_locs[con-1][0],node_locs[con-1][1],myCanvas,"black","C"+str(key)+str(con))
                made_cons.append({node_locs[key-1][0],node_locs[key-1][1],
                                  node_locs[con-1][0],node_locs[con-1][1]})
                node_items.append("C"+str(key)+str(con))                                  
                                      
    node_label = 1
    #draw/redraw nodes
    for x,y in node_locs:
        node_name = "n"+str(x)+str(y)
        if node_name in explored:
            create_node(x,y,node_size,myCanvas,"green",node_name)
        else:
            create_node(x,y,node_size,myCanvas,"lightgreen",node_name)
        text_name = "t"+str(node_label)
        myCanvas.create_text(x, y, text=str(node_label),tag=text_name, font=(20) )
        node_label = node_label + 1
        if node_name not in node_items:
            node_items.append(node_name)
            node_items.append(node_label)
        



def bfs(graph,start,goal):
    # node_graph, start node, goal node
    
    # Your code goes here - delete pass when ready.
    # Make sure to implement the visited list e.g. visited.append(node)
    global visited
    queue = []
    queue.append(start)
    visited.append(start)
    
    while queue:
        parent = queue.pop(0) # FIFO
        for child in graph[parent]:
            if child not in visited:
                queue.append(child)
                visited.append(child)
            if child == goal:
                queue = []
                break	

    
    
        

def dfs(visited, graph, node,goal,depth):
    # visited nodes, node graph, start node, goal node,
    if depth == 5:
        return
    if node not in visited:
        visited.append(node)
        if node == goal:
            return
        for child in graph[node]:
            dfs(visited,graph,child,goal,depth+1)
        

# calc_distance and sort_q are used for ucs
def calc_distance(start, end):
    # Heuristic function
    # Euclidean distance between two points
    global node_locs
    return math.sqrt((node_locs[start-1][0]-node_locs[end-1][0]) ** 2
                    +(node_locs[start-1][1]-node_locs[end-1][1]) ** 2)
                    
def sort_q(queue):
    # key is set to sort using second element of 
    # sublist lambda has been used
    queue.sort(key = lambda x: x[1])
    return queue        
        
def ucs(graph,start,goal):
    # node_graph, start node, goal node
    
    # Your code goes here - delete pass when ready.
    # Make sure to implement the visited list e.g. visited.append(node)
    # You should implement the following code into the BFS algorithm:
        # queue.append([start,0]) #storing node and proirity
        # parent = (queue.pop(0))[0] # pop and get first element (not cost)
        # cost = calc_distance(parent,child) # calcs cost from parent to child
        # queue.append([child,cost])
                
        # sort_q(queue)    # sorts the queue, making it a priority queue
    
    global visited
    queue = []
    queue.append([start,0])
    visited.append(start)
    
    while queue:
        parent = (queue.pop(0))[0] # FIFO
        for child in graph[parent]:
            if child not in visited:
                cost = calc_distance(parent,child)
                queue.append([child,cost])
                visited.append(child)
            if child == goal:
                queue = []
                break
        sort_q(queue)	


def run_plot():
    " Main feed-back loop : animates tree-graph "
    global quit
    global explored
    global visited
    global node_locs
    global inter
    #stack = queue()
    if quit or inter == len(visited):
        return
    explored.append("n"+str(node_locs[visited[inter]-1][0])+str(node_locs[visited[inter]-1][1]))
    create_plot(myCanvas)    
    
    if not quit:
        inter = inter + 1
        myCanvas.after(500, run_plot)

def close_properly(root):
    global quit
    if quit==False:
        quit = True
    else:
        root.destroy()
    
def on_closing():
    global quit
    if quit==False:
        quit = True
    else:
        root.destroy()
 
root = Tk()
root.title("Node Graph") 
myCanvas = Canvas(root, width=width, height=height, borderwidth=0, highlightthickness=0, bg="white")
myCanvas.pack()

def main():
    " Main function: call and report... "
    global node_graph
    global visited
    create_plot(myCanvas)
    
    Button(root, text="Quit", command = lambda: close_properly(root)).pack()
    
    bfs(node_graph,1,11)
    #dfs(visited, node_graph, 1,11,0)
    #ucs(node_graph,1,11)
    
    print(visited)
    
    run_plot()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    
if __name__ == "__main__":
    main()
