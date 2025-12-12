"""
alphabeta.py
Implémentation de l'algorithme Alpha-Beta (optimisation de Min-Max)

Alpha-Beta est une optimisation de Min-Max qui élague les branches
qui ne peuvent pas influencer la décision finale.

Gain : Réduit drastiquement le nombre de nœuds explorés
"""

import math
from game import PLAYER_1, PLAYER_2
from heuristic import heuristic


class AlphaBetaStats:
    """Classe pour collecter les statistiques de l'algorithme"""
    def __init__(self):
        self.nodes_explored = 0  # Nombre de nœuds explorés
        self.nodes_pruned = 0    # Nombre de nœuds élagues
        self.max_depth_reached = 0  # Profondeur maximale atteinte
        
    def reset(self):
        """Réinitialise les compteurs"""
        self.nodes_explored = 0
        self.nodes_pruned = 0
        self.max_depth_reached = 0


# Instance globale pour les statistiques
stats = AlphaBetaStats()


def alphabeta(game, depth, alpha, beta, maximizing_player):
    """
    Algorithme Alpha-Beta avec élagage
    
    Args:
        game (Connect4): État actuel du jeu
        depth (int): Profondeur restante à explorer
        alpha (float): Meilleur score garanti pour MAX
        beta (float): Meilleur score garanti pour MIN
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
            new_score, _ = alphabeta(temp_game, depth - 1, alpha, beta, False)
            
            # Mettre à jour le meilleur score
            if new_score > value:
                value = new_score
                best_col = col
            
            # Mise à jour d'alpha
            alpha = max(alpha, value)
            
            # ÉLAGAGE BETA : Si alpha >= beta, on peut arrêter
            if alpha >= beta:
                stats.nodes_pruned += 1
                break  # Coupure Beta
        
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
            new_score, _ = alphabeta(temp_game, depth - 1, alpha, beta, True)
            
            # Mettre à jour le meilleur score
            if new_score < value:
                value = new_score
                best_col = col
            
            # Mise à jour de beta
            beta = min(beta, value)
            
            # ÉLAGAGE ALPHA : Si alpha >= beta, on peut arrêter
            if alpha >= beta:
                stats.nodes_pruned += 1
                break  # Coupure Alpha
        
        return value, best_col


def find_best_move_alphabeta(game, depth):
    """
    Trouve le meilleur coup à jouer avec l'algorithme Alpha-Beta
    
    Args:
        game (Connect4): État actuel du jeu
        depth (int): Profondeur de recherche
        
    Returns:
        tuple: (meilleure_colonne, score, statistiques)
    """
    # Réinitialiser les statistiques
    stats.reset()
    
    # Lancer Alpha-Beta avec les bornes initiales
    score, col = alphabeta(game, depth, -math.inf, math.inf, True)
    
    # Retourner le résultat avec les statistiques
    return col, score, {
        'nodes_explored': stats.nodes_explored,
        'nodes_pruned': stats.nodes_pruned,
        'max_depth': stats.max_depth_reached
    }


# EXPLICATION DE L'ALGORITHME ALPHA-BETA :
"""
PRINCIPE :
----------
Alpha-Beta est une OPTIMISATION de Min-Max qui élague (coupe) les branches
de l'arbre qui ne peuvent pas influencer la décision finale.

VARIABLES :
-----------
α (alpha) : Meilleur score garanti pour MAX (borne inférieure)
β (beta)  : Meilleur score garanti pour MIN (borne supérieure)

Au départ : α = -∞, β = +∞

RÈGLES D'ÉLAGAGE :
------------------
1. Niveau MAX : Si le score ≥ β → COUPURE (élagage beta)
   Raison : MIN a déjà une meilleure option ailleurs
   
2. Niveau MIN : Si le score ≤ α → COUPURE (élagage alpha)
   Raison : MAX a déjà une meilleure option ailleurs

EXEMPLE ILLUSTRÉ :
------------------
                    [MAX] α=-∞, β=+∞
                   /     \
                  /       \
              [MIN]       [MIN]
              α=-∞,β=+∞   α=3,β=+∞
              /  \         /  \
          [MAX][MAX]   [MAX][MAX]
           3     5      2    ?
           
Étape 1 : MAX trouve 3 → α devient 3
Étape 2 : MAX trouve 5 → MIN prend 3 (minimum)
Étape 3 : La branche droite explore et trouve 2
Étape 4 : Comme 2 < α (3), on sait que MAX ne choisira
          JAMAIS cette branche → ÉLAGAGE !
          Pas besoin d'explorer le "?" !

GAIN DE PERFORMANCE :
---------------------
Min-Max     : Explore O(b^d) nœuds
Alpha-Beta  : Explore O(b^(d/2)) nœuds (dans le meilleur cas)

Exemple avec Puissance 4 (b=7, d=6) :
- Min-Max     : 7^6 = 117,649 nœuds
- Alpha-Beta  : 7^3 = 343 nœuds (meilleur cas)
- Gain        : ~99.7% de nœuds en moins !

ORDRE D'EXPLORATION :
---------------------
L'efficacité dépend de l'ordre d'exploration des coups :
- Meilleur cas : Explorer les meilleurs coups d'abord
- Pire cas     : Explorer les pires coups d'abord
- Astuce       : Privilégier les colonnes centrales

COMPARAISON MIN-MAX vs ALPHA-BETA :
------------------------------------
┌─────────────────┬──────────┬──────────────┐
│                 │ Min-Max  │ Alpha-Beta   │
├─────────────────┼──────────┼──────────────┤
│ Nœuds explorés  │ TOUS     │ Optimisé     │
│ Résultat        │ Optimal  │ Optimal      │
│ Complexité      │ O(b^d)   │ O(b^(d/2))   │
│ Vitesse         │ Lent     │ Rapide       │
└─────────────────┴──────────┴──────────────┘

CONCLUSION :
------------
Alpha-Beta trouve la MÊME solution que Min-Max mais beaucoup plus rapidement
en évitant d'explorer des branches inutiles.
"""