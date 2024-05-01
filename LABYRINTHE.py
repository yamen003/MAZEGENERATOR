from mazepy import mazepy
from collections import deque
import math as mt
import random as rd
import pygame
import sys
class Graph:
    def __init__(self, L, C):
        self.graph = {}
        self.L = L
        self.C = C

    def ajouterNoeud(self, node):
        if node not in self.graph:
            self.graph[node] = []
    
    def ajouterArc(self, node1, node2, p):
        if (node1 in self.graph.keys() and node2 in self.graph.keys()):
            self.graph[node1].append((node2, p))
            self.graph[node2].append((node1, p))
        else:
            print("1 ou les deux noeuds n'existe pas !!")
    def createEspace(self):
        for i in range(self.L):
            for j in range(self.C):
                self.ajouterNoeud((i,j)) 
    def createrelations(self):
        for i in range(self.L):
            for j in range(self.C):
                self.ajouterArc((i,j),(i,j+1),rd.choice([True, False]))     
    def listerNoeuds(self):
        return list(self.graph.keys())

    def listerArcs(self,node=None):
            if node :
                if node in self.graph:
                    return self.graph.get(node, [])
                else:
                    return []
            arcliste = []
            for node, arcs in self.graph.items():
                arcliste.extend(arcs)
            return arcliste

    def adjacenceNoeud(self, node1, node2):
        return (node1, True) in self.graph.get(node2)


    def AfficherGraphe(self):
        for node in self.graph:
            print(f"{node} -> {self.graph[node]}")
class Pile:
    def __init__(self):
        self.elements = deque()

    def pile_vide(self):
        return len(self.elements) == 0

    def empiler(self, element):
        self.elements.append(element)

    def depiler(self):
        if not self.pile_vide():
            return self.elements.pop()
        else:
            print("La pile est vide.")
    def taille_pile(self):
        return len(self.elements)
class files:
    def __init__(self):
        self.d = deque()

    def filevide(self):
        return len(self.d) == 0

    def enfiler(self, x):
        self.d.append(x)

    def defiler(self):
        if not self.filevide():
            return self.d.popleft()
        else:
            print("File est vide.")

    def taillefile(self):
        return len(self.d)

    def printfile(self):
        for item in self.d:
            print(item)
class SearchLabyrinthe:
    def __init__(self, g):
        self.graph = g
        self.explored = [] 
        self.accessible = {}

    def successeurs(self, current_state):
        return [x[0] for x in self.graph.listerArcs(current_state) if x[1]==True]

    def VerifEtat(self, state):
        return not (state in self.explored or state in self.accessible)

    def succValide(self, current_state):
        return [x[0] for x in self.graph.listerArcs(current_state) if x[1] and self.VerifEtat(x[0])]
    def is_explored(self, state):
        return state in self.explored
    
    def is_accessible(self, state):
        return state in self.accessible

    def DFS(self, start,goal,limit=None):
        p = Pile()
        p.empiler(start)
        while not p.pile_vide():
            top = p.depiler()
            self.explored.append(top)
            if top == goal:
                print("Done", goal)
                return True 
            self.accessible[top] = True  
            succ = self.succValide(top) 
            for successor in succ:
                if successor not in self.explored:
                    p.empiler(successor)
        print("On n'a pas arrivé")
        return False
    def BFS(self, start, goal):
        p = files()
        p.enfiler(start)
        
        while not p.filevide():
            top = p.defiler()
            self.explored.append(top)
            
            if top == goal:
                print("Goal reached:", goal)
                return True
            
            self.accessible[top] = True  
            succ = self.successeurs(top) 
            
            for successor in succ:
                if not self.is_explored(successor) and not self.is_accessible(successor):
                    p.enfiler(successor)
        
        print("Goal not reached")
        return False
    def IterativeDDFS(self, start, goal, limit):
        for depth in range(limit + 1):  
            if self.DFS(start, goal, depth):
                return True
            else:
                self.explored = [] 
        
        return False

#----------------------------------------------------------------------
pygame.init()
RES = WIDTH, HEIGHT = 500, 500
TILE = 100
cols, rows = WIDTH // TILE, HEIGHT // TILE
maze_graph = Graph(rows, cols)
maze_graph.ajouterNoeud((0, 0))
maze_graph.ajouterNoeud((0, 1))
maze_graph.ajouterNoeud((0, 2))
maze_graph.ajouterNoeud((1, 2))
maze_graph.ajouterNoeud((2, 2))
maze_graph.ajouterNoeud((2, 1))
maze_graph.ajouterNoeud((2, 0))
maze_graph.ajouterNoeud((3, 0))
maze_graph.ajouterNoeud((3, 1))
maze_graph.ajouterNoeud((3, 2))
maze_graph.ajouterNoeud((3, 3))
maze_graph.ajouterNoeud((4, 3))
maze_graph.ajouterNoeud((4, 4))
maze_graph.ajouterArc((0, 0), (0, 1), True)
maze_graph.ajouterArc((0, 1), (0, 2), True)
maze_graph.ajouterArc((0, 2), (1, 2), True)
maze_graph.ajouterArc((1, 2), (2, 2), True)
maze_graph.ajouterArc((2, 2), (2, 1), True)
maze_graph.ajouterArc((2, 1), (2, 0), True)
maze_graph.ajouterArc((2, 0), (3, 0), True)
maze_graph.ajouterArc((3, 0), (3, 1), True)
maze_graph.ajouterArc((3, 1), (3, 2), True)
maze_graph.ajouterArc((3, 2), (3, 3), True)
maze_graph.ajouterArc((3, 3), (4, 3), True)
maze_graph.ajouterArc((4, 3), (4, 4), True)
searcher = SearchLabyrinthe(maze_graph)
start = (0, 0)
goal = (3 , 3)
searcher.BFS(start, goal)
path = searcher.explored if goal in searcher.explored else []
screen = pygame.display.set_mode(RES)
pygame.display.set_caption("MAZE GAME")
running = True
font = pygame.font.Font(None, 36)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255)) 
    for node in path:
        pygame.draw.rect(screen, (255,0 , 255), (node[1] * TILE, node[0] * TILE, TILE, TILE))
    pygame.draw.rect(screen, (0, 255, 0), (start[1] * TILE, start[0] * TILE, TILE , TILE ))
    pygame.draw.rect(screen, (255, 0, 0), (goal[1] * TILE, goal[0] * TILE, TILE , TILE ))
    pygame.display.flip()  
pygame.quit()
sys.exit()


