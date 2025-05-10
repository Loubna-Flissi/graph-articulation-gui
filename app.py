import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Manipulation de Graphique")
        self.root.geometry("900x500")
        self.graph = nx.Graph()

        # Interface sombre avec boutons pastel
        self.root.configure(bg="#2e2e2e")

        # Cadre gauche pour les boutons
        self.left_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Cadre droit pour le graphe
        self.right_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Boutons avec couleurs pastel
        buttons = [
            ("Ajouter Nœud", self.ajouter_noeud, "#b2d8b2"),
            ("Ajouter Voisin", self.ajouter_voisin, "#b2e0f2"),
            ("Supprimer Points d'Articulation", self.supprimer_points_articulation, "#f2c6b2"),
            ("Imprimer Graphe", self.imprimer_graphe, "#f2b2b2"),
            ("Points d'Articulation", self.points_articulation, "#f2d9b2"),
            ("Infos Graphe", self.infos_graphe, "#eef2b2"),
            ("Sauvegarder Graphe", self.sauvegarder_graphe, "#d5b2f2"),
            ("Réinitialiser", self.reinitialiser, "#b2b2f2")
        ]

        for text, command, color in buttons:
            button = tk.Button(self.left_frame, text=text, command=command, bg=color, width=25, height=2)
            button.pack(pady=5)

        # Figure pour le graphe
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Variables pour le calcul des points d'articulation
        self.time = 0
        self.visited = set()
        self.discovery_time = {}
        self.low_time = {}
        self.parent = {}
        self.articulation_points = set()

    def ajouter_noeud(self):
        noeud = simpledialog.askstring("Ajouter un nœud", "Entrez le numéro du nœud :")
        if noeud:
            self.graph.add_node(noeud)
            self.afficher_graphe()

    def ajouter_voisin(self):
        noeud1 = simpledialog.askstring("Ajouter Voisin", "Entrez le nom du premier nœud :")
        noeud2 = simpledialog.askstring("Ajouter Voisin", "Entrez le nom du second nœud :")
        
        if noeud1 and noeud2:
            if noeud1 in self.graph and noeud2 in self.graph:
                self.graph.add_edge(noeud1, noeud2)
                self.afficher_graphe()
            else:
                messagebox.showwarning("Erreur", "Les deux nœuds doivent exister dans le graphe.")

    def afficher_graphe(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        nx.draw(self.graph, with_labels=True, node_color="#82c9c4", font_color="white", ax=ax)
        self.canvas.draw()

    def supprimer_points_articulation(self):
        articulations = list(self.calculer_points_articulation())
        self.graph.remove_nodes_from(articulations)
        self.afficher_graphe()
        messagebox.showinfo("Suppression des Points d'Articulation", f"Points d'articulation supprimés : {articulations}")

    def imprimer_graphe(self):
        nodes = self.graph.nodes()
        edges = self.graph.edges()
        messagebox.showinfo("Impression du Graphe", f"Nœuds : {nodes}\nArêtes : {edges}")

    def points_articulation(self):
        articulations = list(self.calculer_points_articulation())
        messagebox.showinfo("Points d'Articulation", f"Points d'articulation : {articulations}")

    def infos_graphe(self):
        nodes = self.graph.nodes()
        edges = self.graph.edges()
        num_nodes = len(nodes)
        num_edges = len(edges)
        info = f"Nombre de nœuds : {num_nodes}\nNombre d'arêtes : {num_edges}"
        messagebox.showinfo("Infos du Graphe", f"Infos du graphe :\n{info}")

    def sauvegarder_graphe(self):
        self.figure.savefig("graphe.png")
        messagebox.showinfo("Sauvegarde du Graphe", "Graphe sauvegardé en tant qu'image PNG dans 'graphe.png'")

    def reinitialiser(self):
        self.graph.clear()
        self.afficher_graphe()
        messagebox.showinfo("Réinitialisation", "Le graphe a été réinitialisé.")

    def dfs(self, u):
        self.visited.add(u)
        self.discovery_time[u] = self.low_time[u] = self.time
        self.time += 1
        children = 0

        for v in self.graph.neighbors(u):
            if v not in self.visited:
                self.parent[v] = u
                children += 1
                self.dfs(v)

                # Mise à jour de low_time[u]
                self.low_time[u] = min(self.low_time[u], self.low_time[v])

                # Condition 1 : Si u est la racine et a plus d'un enfant
                if self.parent.get(u) is None and children > 1:
                    self.articulation_points.add(u)

                # Condition 2 : Si u n'est pas la racine et low_time[v] >= discovery_time[u]
                elif self.parent.get(u) is not None and self.low_time[v] >= self.discovery_time[u]:
                    self.articulation_points.add(u)

            elif v != self.parent.get(u):  # Arête retour
                self.low_time[u] = min(self.low_time[u], self.discovery_time[v])

    def calculer_points_articulation(self):
        self.visited.clear()
        self.articulation_points.clear()
        self.discovery_time = {}
        self.low_time = {}
        self.parent = {}
        self.time = 0

        for node in self.graph.nodes():
            if node not in self.visited:
                self.dfs(node)

        return self.articulation_points


# Lancer l'application
root = tk.Tk()
app = GraphApp(root)
root.mainloop()




