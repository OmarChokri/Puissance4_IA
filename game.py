"""
game.py
Classe représentant le jeu Puissance 4
Contient toutes les règles et mécaniques du jeu
"""

import numpy as np

# Constantes du jeu
ROWS = 6
COLS = 7
PLAYER_1 = 1  # Joueur humain (Rouge)
PLAYER_2 = 2  # IA (Jaune)
EMPTY = 0


class Connect4:
    """Classe représentant le jeu Puissance 4"""
    
    def __init__(self):
        """Initialise un nouveau plateau de jeu vide"""
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.game_over = False
        self.turn = PLAYER_1
        
    def drop_piece(self, row, col, piece):
        """
        Place un pion sur le plateau
        
        Args:
            row (int): Ligne où placer le pion
            col (int): Colonne où placer le pion
            piece (int): Numéro du joueur (1 ou 2)
        """
        self.board[row][col] = piece
        
    def is_valid_location(self, col):
        """
        Vérifie si une colonne n'est pas pleine
        
        Args:
            col (int): Numéro de la colonne
            
        Returns:
            bool: True si la colonne est jouable
        """
        return self.board[ROWS - 1][col] == EMPTY
    
    def get_next_open_row(self, col):
        """
        Retourne la première ligne vide dans une colonne (simulation de la gravité)
        
        Args:
            col (int): Numéro de la colonne
            
        Returns:
            int: Numéro de la ligne disponible, None si colonne pleine
        """
        for r in range(ROWS):
            if self.board[r][col] == EMPTY:
                return r
        return None
    
    def check_win(self, piece):
        """
        Vérifie si un joueur a gagné (4 pions alignés)
        
        Args:
            piece (int): Numéro du joueur (1 ou 2)
            
        Returns:
            bool: True si le joueur a gagné
        """
        # Vérification horizontale
        for c in range(COLS - 3):
            for r in range(ROWS):
                if (self.board[r][c] == piece and 
                    self.board[r][c+1] == piece and
                    self.board[r][c+2] == piece and 
                    self.board[r][c+3] == piece):
                    return True
        
        # Vérification verticale
        for c in range(COLS):
            for r in range(ROWS - 3):
                if (self.board[r][c] == piece and 
                    self.board[r+1][c] == piece and
                    self.board[r+2][c] == piece and 
                    self.board[r+3][c] == piece):
                    return True
        
        # Vérification diagonale positive (/)
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if (self.board[r][c] == piece and 
                    self.board[r+1][c+1] == piece and
                    self.board[r+2][c+2] == piece and 
                    self.board[r+3][c+3] == piece):
                    return True
        
        # Vérification diagonale négative (\)
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if (self.board[r][c] == piece and 
                    self.board[r-1][c+1] == piece and
                    self.board[r-2][c+2] == piece and 
                    self.board[r-3][c+3] == piece):
                    return True
        
        return False
    
    def is_terminal_node(self):
        """
        Vérifie si le jeu est dans un état terminal
        (victoire d'un joueur ou plateau plein)
        
        Returns:
            bool: True si le jeu est terminé
        """
        return (self.check_win(PLAYER_1) or 
                self.check_win(PLAYER_2) or 
                len(self.get_valid_locations()) == 0)
    
    def get_valid_locations(self):
        """
        Retourne la liste des colonnes jouables
        
        Returns:
            list: Liste des numéros de colonnes non pleines
        """
        valid_locations = []
        for col in range(COLS):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations
    
    def copy(self):
        """
        Crée une copie du plateau actuel
        Utilisé par les algorithmes Min-Max et Alpha-Beta
        
        Returns:
            Connect4: Nouvelle instance avec le même état
        """
        new_game = Connect4()
        new_game.board = np.copy(self.board)
        new_game.game_over = self.game_over
        new_game.turn = self.turn
        return new_game
    
    def print_board(self):
        """Affiche le plateau dans la console (pour debug)"""
        print(np.flip(self.board, 0))