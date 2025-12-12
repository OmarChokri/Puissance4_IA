"""
minimax.py
Implémentation de l'algorithme Min-Max pour le jeu Puissance 4

L'algorithme Min-Max explore l'arbre de jeu en alternant entre :
- Niveaux MAX : L'IA cherche à maximiser son score
- Niveaux MIN : L'adversaire cherche à minimiser le score de l'IA
"""

import math
from game import PLAYER_1, PLAYER_2
from heuristic import heuristic


class MinMaxStats:
    """Classe pour collecter les statistiques de l'algorithme"""
    def __init__(self):
        self.nodes_explored = 0  # Nombre de nœuds explorés
        self.max_depth_reached = 0  # Profondeur maximale atteinte
        
    def reset(self):
        """Réinitialise les compteurs"""
        self.nodes_explored = 0
        self.max_depth_reached = 0


# Instance globale pour les statistiques
stats = MinMaxStats()


def minimax(game, depth, maximizing_player):
    """
    Algorithme Min-Max récursif
    
    Args:
        game (Connect4): État actuel du jeu
        depth (int): Profondeur restante à explorer
        maximizing_player (bool): True si c'est le tour de MAX (IA)
        
    Returns:
        tuple: (meilleur_score, meilleure_colonne)
    """
    # Incrémenter le compteur de nœuds
    stats.nodes_explored += 1
    
    # Mettre à jour la profondeur maximale atteinte
    current_depth = stats.max_depth_reached
    if depth > current_depth:
        stats.max_depth_reached = depth
    
    # Récupérer les coups valides
    valid_locations = game.get_valid_locations()
    
    # Condition d'arrêt : nœud terminal ou profondeur = 0
    is_terminal = game.is_terminal_node()
    
    if depth == 0 or is_terminal:
        if is_terminal:
            # États terminaux
            if game.check_win(PLAYER_2):
                return (100000000, None)  # IA gagne
            elif game.check_win(PLAYER_1):
                return (-100000000, None)  # Adversaire gagne
            else:
                return (0, None)  # Match nul
        else:
            # Profondeur limite atteinte : évaluer avec heuristique
            return (heuristic(game, PLAYER_2), None)
    
    if maximizing_player:
        # Niveau MAX : L'IA cherche à maximiser
        value = -math.inf
        best_col = valid_locations[0]  # Colonne par défaut
        
        for col in valid_locations:
            # Créer une copie du jeu et simuler le coup
            temp_game = game.copy()
            row = temp_game.get_next_open_row(col)
            temp_game.drop_piece(row, col, PLAYER_2)
            
            # Appel récursif pour le niveau MIN
            new_score, _ = minimax(temp_game, depth - 1, False)
            
            # Mettre à jour le meilleur score
            if new_score > value:
                value = new_score
                best_col = col
        
        return value, best_col
    
    else:
        # Niveau MIN : L'adversaire cherche à minimiser
        value = math.inf
        best_col = valid_locations[0]  # Colonne par défaut
        
        for col in valid_locations:
            # Créer une copie du jeu et simuler le coup
            temp_game = game.copy()
            row = temp_game.get_next_open_row(col)
            temp_game.drop_piece(row, col, PLAYER_1)
            
            # Appel récursif pour le niveau MAX
            new_score, _ = minimax(temp_game, depth - 1, True)
            
            # Mettre à jour le meilleur score
            if new_score < value:
                value = new_score
                best_col = col
        
        return value, best_col


def find_best_move_minimax(game, depth):
    """
    Trouve le meilleur coup à jouer avec l'algorithme Min-Max
    
    Args:
        game (Connect4): État actuel du jeu
        depth (int): Profondeur de recherche
        
    Returns:
        tuple: (meilleure_colonne, score, statistiques)
    """
    # Réinitialiser les statistiques
    stats.reset()
    
    # Lancer Min-Max
    score, col = minimax(game, depth, True)
    
    # Retourner le résultat avec les statistiques
    return col, score, {
        'nodes_explored': stats.nodes_explored,
        'max_depth': stats.max_depth_reached
    }


# EXPLICATION DE L'ALGORITHME MIN-MAX :
"""
PRINCIPE :
----------
Min-Max est un algorithme de décision pour les jeux à deux joueurs.
Il explore l'arbre de jeu en alternant entre deux types de nœuds :

1. Nœuds MAX (IA) : Cherche à MAXIMISER le score
2. Nœuds MIN (Adversaire) : Cherche à MINIMISER le score

FONCTIONNEMENT :
----------------
                    [MAX]  <- IA veut maximiser
                   /  |  \
                  /   |   \
              [MIN] [MIN] [MIN]  <- Adversaire veut minimiser
              / \   / \   / \
           [MAX][MAX][MAX][MAX][MAX][MAX]  <- IA veut maximiser
            |    |    |    |    |    |
           [5]  [3]  [8]  [2]  [9]  [1]   <- Évaluation heuristique

Remontée des scores :
- MIN choisit 3 (min de 5,3)
- MIN choisit 2 (min de 8,2)
- MIN choisit 1 (min de 9,1)
- MAX choisit 3 (max de 3,2,1)

AVANTAGES :
-----------
✓ Explore toutes les possibilités
✓ Trouve la solution optimale
✓ Facile à comprendre et implémenter

INCONVÉNIENTS :
---------------
✗ Explore TOUS les nœuds → très lent
✗ Complexité : O(b^d) où b = branches, d = profondeur
✗ Pour Puissance 4 : 7^6 = 117,649 nœuds à profondeur 6 !

OPTIMISATION :
--------------
→ C'est pourquoi on utilise ALPHA-BETA (voir alphabeta.py)
  qui élague les branches inutiles !

EXEMPLE CONCRET :
-----------------
Profondeur 3, 3 coups possibles [A, B, C]

Tour IA (MAX):
  Coup A:
    Tour Adversaire (MIN):
      Coup A1: Score = 5
      Coup A2: Score = 3  → MIN choisit 3
  Coup B:
    Tour Adversaire (MIN):
      Coup B1: Score = 8
      Coup B2: Score = 2  → MIN choisit 2
  Coup C:
    Tour Adversaire (MIN):
      Coup C1: Score = 9
      Coup C2: Score = 1  → MIN choisit 1

MAX choisit le coup B avec score 2 (max de 3, 2, 1)
"""