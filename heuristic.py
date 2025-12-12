"""
heuristic.py
Fonction heuristique pour évaluer la qualité d'une position
Plus le score est élevé, meilleure est la position pour l'IA (PLAYER_2)
"""

from game import ROWS, COLS, PLAYER_1, PLAYER_2, EMPTY


def evaluate_window(window, piece):
    """
    Évalue une fenêtre de 4 cases consécutives
    
    Args:
        window (list): Liste de 4 valeurs du plateau
        piece (int): Le joueur à évaluer (PLAYER_2 pour l'IA)
        
    Returns:
        int: Score de la fenêtre
    """
    score = 0
    opponent = PLAYER_1 if piece == PLAYER_2 else PLAYER_2
    
    # Compter les pions dans la fenêtre
    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opponent_count = window.count(opponent)
    
    # Scoring basé sur le nombre de pions alignés
    if piece_count == 4:
        score += 100  # Victoire !
    elif piece_count == 3 and empty_count == 1:
        score += 5    # 3 alignés avec possibilité de gagner
    elif piece_count == 2 and empty_count == 2:
        score += 2    # 2 alignés avec possibilités
    
    # Pénalité si l'adversaire peut gagner
    if opponent_count == 3 and empty_count == 1:
        score -= 4    # Bloquer l'adversaire est important
    
    return score


def evaluate_position(board, piece):
    """
    Évalue la qualité globale d'une position sur le plateau
    
    Cette fonction évalue :
    1. Le contrôle du centre (colonnes centrales valent plus)
    2. Les alignements horizontaux possibles
    3. Les alignements verticaux possibles
    4. Les alignements diagonaux possibles
    
    Args:
        board (numpy.ndarray): Le plateau de jeu
        piece (int): Le joueur à évaluer (PLAYER_2 pour l'IA)
        
    Returns:
        int: Score total de la position (plus c'est élevé, mieux c'est pour piece)
    """
    score = 0
    
    # 1. BONUS POUR LE CENTRE
    # Le centre est stratégiquement important
    center_array = [int(i) for i in list(board[:, COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    
    # 2. ÉVALUATION HORIZONTALE
    # Parcourir toutes les fenêtres de 4 cases horizontales
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)
    
    # 3. ÉVALUATION VERTICALE
    # Parcourir toutes les fenêtres de 4 cases verticales
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)
    
    # 4. ÉVALUATION DIAGONALE POSITIVE (/)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # 5. ÉVALUATION DIAGONALE NÉGATIVE (\)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    return score


def heuristic(game, piece):
    """
    Fonction heuristique principale appelée par Min-Max et Alpha-Beta
    
    Args:
        game (Connect4): L'état du jeu à évaluer
        piece (int): Le joueur à évaluer (PLAYER_2 pour l'IA)
        
    Returns:
        int: Score heuristique de la position
             > 0 : Avantageux pour l'IA
             < 0 : Avantageux pour l'adversaire
             = 0 : Position équilibrée
    """
    # Vérifier les états terminaux
    if game.check_win(piece):
        return 100000000  # Victoire de l'IA : score maximal
    elif game.check_win(PLAYER_1 if piece == PLAYER_2 else PLAYER_2):
        return -100000000  # Victoire de l'adversaire : score minimal
    elif len(game.get_valid_locations()) == 0:
        return 0  # Match nul
    
    # Évaluer la position
    return evaluate_position(game.board, piece)


# EXPLICATIONS DE LA FONCTION HEURISTIQUE :
"""
La fonction heuristique évalue une position du jeu en attribuant un score.

PRINCIPES :
-----------
1. Score positif = bon pour l'IA (PLAYER_2)
2. Score négatif = bon pour l'adversaire (PLAYER_1)
3. Plus le score absolu est grand, plus la position est décisive

CRITÈRES D'ÉVALUATION :
-----------------------
1. CONTRÔLE DU CENTRE (×3 points par pion)
   - Les colonnes centrales offrent plus d'opportunités d'alignement
   
2. FENÊTRES HORIZONTALES (toutes lignes)
   - 4 pions alignés : +100 (victoire)
   - 3 pions + 1 vide : +5 (menace directe)
   - 2 pions + 2 vides : +2 (possibilité future)
   - 3 pions adverses + 1 vide : -4 (danger à bloquer)

3. FENÊTRES VERTICALES (toutes colonnes)
   - Même scoring que horizontal

4. FENÊTRES DIAGONALES (/ et \)
   - Même scoring que horizontal

EXEMPLE :
---------
Position : O O O _
           X _ _ _
           
Fenêtre [O,O,O,_] horizontale :
- 3 pions O + 1 vide → Score +5
- Si l'adversaire joue X dans le vide → il peut gagner → -4

Score total = somme de toutes les fenêtres évaluées
"""