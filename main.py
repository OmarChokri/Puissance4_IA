"""
main.py
Programme principal avec interface graphique Pygame
Menu de sélection de l'algorithme et de la profondeur
"""

import pygame
import sys
import time
from game import Connect4, ROWS, COLS, PLAYER_1, PLAYER_2, EMPTY
from minimax import find_best_move_minimax
from alphabeta import find_best_move_alphabeta

# Constantes pour l'interface
SQUARE_SIZE = 100
WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE
RADIUS = int(SQUARE_SIZE / 2 - 5)

# Couleurs
BLUE = (0, 102, 204)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_BLUE = (0, 51, 102)


class Button:
    """Classe pour créer des boutons interactifs"""
    
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        """Dessine le bouton"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        """Vérifie si la souris est sur le bouton"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_clicked):
        """Vérifie si le bouton est cliqué"""
        return self.rect.collidepoint(mouse_pos) and mouse_clicked


def show_menu(screen):
    """
    Affiche le menu de sélection de l'algorithme et de la profondeur
    
    Returns:
        tuple: (algorithm_name, depth) ou (None, None) si annulé
    """
    pygame.display.set_caption('Puissance 4 - Configuration')
    
    # Polices
    font_title = pygame.font.SysFont("Arial", 50, bold=True)
    font_subtitle = pygame.font.SysFont("Arial", 30, bold=True)
    font_text = pygame.font.SysFont("Arial", 24)
    font_button = pygame.font.SysFont("Arial", 28, bold=True)
    
    # Variables de sélection
    selected_algo = None  # 'minimax' ou 'alphabeta'
    selected_depth = 5    # Profondeur par défaut
    
    # Boutons pour les algorithmes
    btn_minimax = Button(100, 200, 250, 80, "Min-Max", RED, (255, 50, 50))
    btn_alphabeta = Button(WIDTH - 350, 200, 250, 80, "Alpha-Beta", BLUE, (50, 150, 255))
    
    # Boutons pour la profondeur
    depth_buttons = []
    depths = [3, 4, 5, 6, 7]
    btn_width = 80
    btn_spacing = 20
    start_x = (WIDTH - (len(depths) * btn_width + (len(depths)-1) * btn_spacing)) // 2
    
    for i, depth in enumerate(depths):
        x = start_x + i * (btn_width + btn_spacing)
        btn = Button(x, 400, btn_width, 60, str(depth), GRAY, GREEN)
        depth_buttons.append((btn, depth))
    
    # Bouton Jouer
    btn_play = Button(WIDTH//2 - 100, 550, 200, 60, "JOUER", GREEN, (0, 200, 0))
    
    running = True
    while running:
        screen.fill(DARK_BLUE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        
        # Titre
        title = font_title.render("PUISSANCE 4 - IA", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        # Section Algorithme
        subtitle_algo = font_subtitle.render("Choisissez l'algorithme :", True, WHITE)
        screen.blit(subtitle_algo, (50, 140))
        
        # Boutons algorithme
        btn_minimax.check_hover(mouse_pos)
        btn_alphabeta.check_hover(mouse_pos)
        
        btn_minimax.draw(screen, font_button)
        btn_alphabeta.draw(screen, font_button)
        
        # Sélection algorithme
        if btn_minimax.is_clicked(mouse_pos, mouse_clicked):
            selected_algo = 'minimax'
        if btn_alphabeta.is_clicked(mouse_pos, mouse_clicked):
            selected_algo = 'alphabeta'
        
        # Indicateur de sélection algorithme
        if selected_algo == 'minimax':
            pygame.draw.rect(screen, YELLOW, btn_minimax.rect, 5, border_radius=10)
        elif selected_algo == 'alphabeta':
            pygame.draw.rect(screen, YELLOW, btn_alphabeta.rect, 5, border_radius=10)
        
        # Section Profondeur
        subtitle_depth = font_subtitle.render("Choisissez la profondeur :", True, WHITE)
        screen.blit(subtitle_depth, (50, 340))
        
        # Boutons profondeur
        for btn, depth in depth_buttons:
            btn.check_hover(mouse_pos)
            btn.draw(screen, font_button)
            
            if btn.is_clicked(mouse_pos, mouse_clicked):
                selected_depth = depth
            
            # Indicateur de sélection
            if selected_depth == depth:
                pygame.draw.rect(screen, YELLOW, btn.rect, 5, border_radius=10)
        
        # Informations sur la profondeur
        depth_info = [
            "Prof. 3-4 : Rapide, IA moyenne",
            "Prof. 5 : Équilibré (recommandé)",
            "Prof. 6-7 : Lent, IA excellente"
        ]
        for i, info in enumerate(depth_info):
            text = font_text.render(info, True, LIGHT_GRAY)
            screen.blit(text, (50, 490 + i * 25))
        
        # Bouton Jouer (actif seulement si algo sélectionné)
        if selected_algo:
            btn_play.check_hover(mouse_pos)
            btn_play.draw(screen, font_button)
            
            if btn_play.is_clicked(mouse_pos, mouse_clicked):
                return selected_algo, selected_depth
        else:
            # Bouton grisé si pas de sélection
            pygame.draw.rect(screen, GRAY, btn_play.rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, btn_play.rect, 3, border_radius=10)
            text_surface = font_button.render("JOUER", True, LIGHT_GRAY)
            text_rect = text_surface.get_rect(center=btn_play.rect.center)
            screen.blit(text_surface, text_rect)
            
            # Message
            msg = font_text.render("Sélectionnez un algorithme", True, YELLOW)
            msg_rect = msg.get_rect(center=(WIDTH//2, 630))
            screen.blit(msg, msg_rect)
        
        pygame.display.update()
    
    return None, None


def draw_board(screen, game, winning_tokens=None):
    """
    Dessine le plateau de jeu avec Pygame
    
    Args:
        screen: Surface Pygame
        game (Connect4): Instance du jeu
        winning_tokens (list): Liste des coordonnées (row, col) des pions gagnants
    """
    # Dessine le fond bleu avec les trous noirs
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, 
                           (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, 
                            SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, 
                             (int(c * SQUARE_SIZE + SQUARE_SIZE/2), 
                              int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), 
                             RADIUS)
    
    # Dessine les pions
    for c in range(COLS):
        for r in range(ROWS):
            if game.board[r][c] == PLAYER_1:
                color = RED
                if winning_tokens and (r, c) in winning_tokens:
                    color = GREEN
                pygame.draw.circle(screen, color, 
                                 (int(c * SQUARE_SIZE + SQUARE_SIZE/2), 
                                  HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE/2)), 
                                 RADIUS)
            elif game.board[r][c] == PLAYER_2:
                color = YELLOW
                if winning_tokens and (r, c) in winning_tokens:
                    color = GREEN
                pygame.draw.circle(screen, color, 
                                 (int(c * SQUARE_SIZE + SQUARE_SIZE/2), 
                                  HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE/2)), 
                                 RADIUS)
    pygame.display.update()


def display_stats(screen, font, algo_name, exec_time, nodes, pruned=None):
    """
    Affiche les statistiques de l'IA sur l'écran
    
    Args:
        screen: Surface Pygame
        font: Police pour le texte
        algo_name (str): Nom de l'algorithme
        exec_time (float): Temps d'exécution en secondes
        nodes (int): Nombre de nœuds explorés
        pruned (int): Nombre de nœuds élagués (pour Alpha-Beta)
    """
    y_offset = HEIGHT - 90
    
    # Nom de l'algorithme
    text = font.render(f"Algo: {algo_name}", True, WHITE)
    screen.blit(text, (10, y_offset))
    
    # Temps d'exécution
    text = font.render(f"Temps: {exec_time:.3f}s", True, WHITE)
    screen.blit(text, (10, y_offset + 20))
    
    # Nœuds explorés
    text = font.render(f"Noeuds: {nodes}", True, WHITE)
    screen.blit(text, (10, y_offset + 40))
    
    # Nœuds élagués (si Alpha-Beta)
    if pruned is not None:
        text = font.render(f"Elagages: {pruned}", True, GREEN)
        screen.blit(text, (10, y_offset + 60))
    
    pygame.display.update()


def play_game(ai_algorithm, search_depth):
    """
    Lance une partie avec les paramètres choisis
    
    Args:
        ai_algorithm (str): 'minimax' ou 'alphabeta'
        search_depth (int): Profondeur de recherche
    """
    # Initialisation de Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f'Puissance 4 - {ai_algorithm.upper()} (Prof. {search_depth})')
    
    # Polices
    font_large = pygame.font.SysFont("monospace", 75)
    font_small = pygame.font.SysFont("monospace", 20)
    
    # Initialisation du jeu
    game = Connect4()
    draw_board(screen, game)
    
    # Variables pour les statistiques
    last_ai_time = 0
    last_ai_nodes = 0
    last_ai_pruned = 0
    
    # Message de fin et jetons gagnants
    end_message = ""
    end_message_color = WHITE
    winning_tokens = []
    
    print(f"\n{'='*70}")
    print(f"PUISSANCE 4 - IA avec {ai_algorithm.upper()}")
    print(f"Profondeur de recherche : {search_depth}")
    print(f"{'='*70}\n")
    
    # Boucle principale
    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Affichage du pion qui suit la souris
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                if game.turn == PLAYER_1:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
                
                # Afficher les stats de la dernière décision de l'IA
                if last_ai_nodes > 0:
                    display_stats(screen, font_small, ai_algorithm.upper(), 
                                last_ai_time, last_ai_nodes, 
                                last_ai_pruned if ai_algorithm == 'alphabeta' else None)
                
                pygame.display.update()
            
            # Gestion du clic (Tour du joueur)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                
                if game.turn == PLAYER_1:
                    posx = event.pos[0]
                    col = int(posx // SQUARE_SIZE)
                    
                    if game.is_valid_location(col):
                        row = game.get_next_open_row(col)
                        game.drop_piece(row, col, PLAYER_1)
                        
                        if game.check_win(PLAYER_1):
                            label = font_large.render("Vous gagnez!", 1, RED)
                            screen.blit(label, (40, 10))
                            game.game_over = True
                            end_message = "VICTOIRE !"
                            end_message_color = RED
                            winning_tokens = game.get_winning_sequence(PLAYER_1)
                            print("\n🎉 VICTOIRE DU JOUEUR ! 🎉\n")
                        
                        game.turn = PLAYER_2
                        draw_board(screen, game, winning_tokens)
        
        # Tour de l'IA (PLAYER_2)
        if game.turn == PLAYER_2 and not game.game_over:
            # Afficher "L'IA réfléchit..."
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            label = font_small.render("L'IA reflechit...", 1, YELLOW)
            screen.blit(label, (WIDTH//2 - 100, 10))
            pygame.display.update()
            
            print(f"\n{'='*70}")
            print(f"Tour de l'IA ({ai_algorithm.upper()})...")
            
            # Mesurer le temps d'exécution
            start_time = time.time()
            
            # Choisir l'algorithme
            if ai_algorithm == 'minimax':
                col, score, stats = find_best_move_minimax(game, search_depth)
                last_ai_pruned = 0  # Min-Max n'a pas d'élagage
            else:  # alphabeta
                col, score, stats = find_best_move_alphabeta(game, search_depth)
                last_ai_pruned = stats.get('nodes_pruned', 0)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Sauvegarder les statistiques
            last_ai_time = execution_time
            last_ai_nodes = stats['nodes_explored']
            
            # Afficher les statistiques
            print(f"Colonne choisie : {col}")
            print(f"Score évalué : {score}")
            print(f"Temps d'exécution : {execution_time:.3f} secondes")
            print(f"Nœuds explorés : {stats['nodes_explored']}")
            if ai_algorithm == 'alphabeta':
                print(f"Nœuds élagués : {stats['nodes_pruned']}")
                efficiency = (stats['nodes_pruned'] / stats['nodes_explored'] * 100) if stats['nodes_explored'] > 0 else 0
                print(f"Efficacité élagage : {efficiency:.1f}%")
            print(f"{'='*70}\n")
            
            # Jouer le coup
            if game.is_valid_location(col):
                row = game.get_next_open_row(col)
                game.drop_piece(row, col, PLAYER_2)
                
                if game.check_win(PLAYER_2):
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                    label = font_large.render("L'IA gagne!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game.game_over = True
                    end_message = "IA GAGNE !"
                    end_message_color = YELLOW
                    winning_tokens = game.get_winning_sequence(PLAYER_2)
                    print("\n🤖 VICTOIRE DE L'IA ! 🤖\n")
                
                game.turn = PLAYER_1
                draw_board(screen, game, winning_tokens)
        
        # Vérification match nul
        if len(game.get_valid_locations()) == 0 and not game.game_over:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            label = font_large.render("Match nul!", 1, WHITE)
            screen.blit(label, (80, 10))
            game.game_over = True
            end_message = "MATCH NUL !"
            end_message_color = WHITE
            print("\n🤝 MATCH NUL ! 🤝\n")
    
    # Afficher les statistiques finales et le message de fin
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
    
    if end_message:
        label = font_large.render(end_message, 1, end_message_color)
        label_rect = label.get_rect(center=(WIDTH//2, SQUARE_SIZE//2))
        screen.blit(label, label_rect)
        
    if last_ai_nodes > 0:
        display_stats(screen, font_small, ai_algorithm.upper(), 
                    last_ai_time, last_ai_nodes, 
                    last_ai_pruned if ai_algorithm == 'alphabeta' else None)
    pygame.display.update()
    
    # Attendre 5 secondes avant de fermer
    pygame.time.wait(5000)


def main():
    """Fonction principale"""
    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Afficher le menu de configuration
    ai_algorithm, search_depth = show_menu(screen)
    
    # Si l'utilisateur a fermé le menu
    if ai_algorithm is None:
        pygame.quit()
        sys.exit()
    
    # Lancer la partie
    play_game(ai_algorithm, search_depth)
    
    pygame.quit()


if __name__ == "__main__":
    main()