from tkinter import CURRENT, Tk, Canvas, Menu, StringVar, mainloop, filedialog, simpledialog
from Lib import *


names = []
edges = {}
selected = []

master = Tk()


def onCanvasClick(event):
    if variable.get() == "node":
        r = 50
        name = simpledialog.askstring("Node Name", "Enter Name:")
        name = name.replace(" ", "_").replace("-", "~")
        if name != None and len(name) > 0 and name not in names and "-" not in name:
            tagname = "-" + name
            names.append(name)
            event.widget.create_oval(
                event.x - r, event.y - r, event.x + r, event.y + r, fill="red", tags=(tagname, "node"))
            event.widget.create_text(
                event.x, event.y, text=name, tags=(tagname, "nodetext"))
            event.widget.tag_bind(tagname, '<Button-1>', onObjectClick)


def onObjectClick(event):
    global selected
    global variable
    if event.widget.find_withtag(CURRENT):
        if variable.get() == "edges":
            if len(selected) == 0:
                tags = event.widget.gettags(
                    event.widget.find_withtag(CURRENT)[0])
                for x in tags:
                    if x[0] == "-":
                        selected.append(x[1:])
                print(selected)
                event.widget.itemconfig(CURRENT, fill="blue")
            elif len(selected) == 1 and "blue" not in event.widget.itemconfig(CURRENT)["fill"]:
                value = simpledialog.askinteger("Edge Value", "Enter number:")
                tags = event.widget.gettags(
                    event.widget.find_withtag(CURRENT)[0])
                for x in tags:
                    if x[0] == "-":
                        selected.append(x[1:])
                event.widget.itemconfig("node", fill="red")
                edgeName = "{}-{}".format(selected[0], selected[1])
                dx1, dy1, dx2, dy2 = event.widget.coords(
                    event.widget.find_withtag(CURRENT)[0])
                ox1, oy1, ox2, oy2 = event.widget.coords(
                    event.widget.find_withtag("-" + selected[0])[0])
                x1 = (dx1 + dx2) / 2
                x2 = (ox1 + ox2) / 2
                y1 = (dy1 + dy2) / 2
                y2 = (oy1 + oy2) / 2
                edges[edgeName] = value
                event.widget.create_line(
                    x1, y1, x2, y2, width=15, tags=("-" + edgeName, "edge"))
                event.widget.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2, text=value, fill="white", tags=("-" + edgeName, "edgetext"))
                event.widget.tag_lower("-" + edgeName)
                event.widget.tag_bind(
                    "-" + edgeName, '<Button-1>', onObjectClick)
                print(edges)
                selected = []
        elif variable.get() == "delete":
            if "edge" in event.widget.gettags(event.widget.find_withtag(CURRENT)[0]):
                tags = event.widget.gettags(
                    event.widget.find_withtag(CURRENT)[0])
                for x in tags:
                    if x[0] == "-":
                        event.widget.delete(x)
                        del edges[x[1:]]
            elif "node" in event.widget.gettags(event.widget.find_withtag(CURRENT)[0]):
                tags = event.widget.gettags(
                    event.widget.find_withtag(CURRENT)[0])
                for x in tags:
                    if x[0] == "-":
                        edgesdel = [edge for edge in edges if x[:1] in edge]
                        for edge in edgesdel:
                            event.widget.delete("-" + edge)
                            del edges[edge]
                        event.widget.delete(x)
                        names.remove(x[1:])


def calculate():
    global names
    global edges
    if len(edges) > 0:
        path = find_route(names, edges)
        w.itemconfig("edge", fill="black")
        for edge in path:
            w.itemconfig("-" + edge, fill="green")
            w.itemconfig("edgetext", fill="white")


def reset_canvas():
    global names
    global edges
    global selected
    w.delete("all")
    names = []
    edges = {}
    selected = []


def save():
    filename = filedialog.asksaveasfilename(
        filetypes=[("SVG file", ".svg")], defaultextension=u".svg")
    if filename != None:
        canvasvg.saveall(filename, w)


def find_route(names, edges):
    def queue_edges(node, pq, visited, nodes):
        for edge in node.neighbours:
            if not (edge.nodes[0] in visited and edge.nodes[1] in visited):
                pq.insert(edge)
    nodes = {x: Graph.Node(x) for x in names}
    for key, value in edges.items():
        Graph.Edge(nodes[key.split("-")[0]], nodes[key.split("-")[1]], value)
    visited = [nodes[names[0]]]
    path = []
    pq = PriorityQueue.PriorityQueue()

    queue_edges(nodes[names[0]], pq, visited, nodes)

    while len(visited) < len(nodes):
        print(pq)
        best_edge = pq.remove()
        print(best_edge)
        print(pq)
        for x in [x for x in range(2) if best_edge.nodes[x] not in visited and best_edge.nodes[(x + 1) % 2].connections < 2]:
            visited.append(best_edge.nodes[x])
            path.append(best_edge)
            best_edge.nodes[x].connections += 1
            best_edge.nodes[(x + 1) % 2].connections += 1
            queue_edges(best_edge.nodes[x], pq, visited, nodes)

    return [str(x) for x in path]

w = Canvas(master, width=700, height=700)
w.pack()
menu = Menu(master, tearoff=0)
variable = StringVar(master)
variable.set("node")
modesMenu = Menu(menu)
modesMenu.add_radiobutton(label="Node", var=variable, value="node")
modesMenu.add_radiobutton(label="Edge", var=variable, value="edges")
modesMenu.add_radiobutton(label="Delete", var=variable, value="delete")
menu.add_cascade(label="Mode", menu=modesMenu)
menu.add_command(label="Calculate", command=calculate)
menu.add_command(label="Save", command=save)
menu.add_command(label="Reset", command=reset_canvas)
w.bind('<Button-1>', onCanvasClick)
master.config(menu=menu)
master.title("Prim's Algorithm")


mainloop()
