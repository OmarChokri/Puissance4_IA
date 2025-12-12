"""
main.py
Version mise à jour :
- menu Pygame pour choisir l'algorithme (minimax / alphabeta)
- menu pour choisir l'heuristique (si disponible dans heuristic.py)
- tentative automatique de passer l'heuristique aux fonctions find_best_move_...
  si leur signature le permet (utilise inspect pour la détection)
"""

import pygame
import sys
import time
import inspect

from game import Connect4, ROWS, COLS, PLAYER_1, PLAYER_2, EMPTY
from minimax import find_best_move_minimax
from alphabeta import find_best_move_alphabeta

# importer le module heuristic (présent dans votre repo)
import heuristic as heuristic_module

# Constantes UI
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

# Profondeur par défaut
SEARCH_DEPTH = 5


# ---------- Utils pour détecter si on peut passer une heuristique ----------
def choose_heuristic_function():
    """
    Cherche dans heuristic_module une fonction utilisable.
    Retourne (callable, name) ou (None, "Default") si rien trouvé.
    """
    candidates = ["evaluate", "heuristic", "score_position", "score", "eval"]
    for name in candidates:
        if hasattr(heuristic_module, name):
            fn = getattr(heuristic_module, name)
            if callable(fn):
                return fn, name
    # fallback : chercher toute fonction callable exportée
    for attr in dir(heuristic_module):
        if not attr.startswith("_"):
            fn = getattr(heuristic_module, attr)
            if callable(fn):
                return fn, attr
    return None, "Default"


def can_pass_heuristic_to(fn):
    """
    Inspecte la signature de fn pour savoir si on peut lui passer un paramètre
    keyword 'heuristic' ou 'eval_fn' ou si la fonction accepte >=4 positional args.
    """
    try:
        sig = inspect.signature(fn)
        params = sig.parameters
        # accepte keyword 'heuristic' ou 'eval_fn' ?
        if "heuristic" in params or "eval_fn" in params:
            return "kw"
        # accepte >=4 positional-only or positional-or-keyword params ?
        pos_count = sum(1 for p in params.values()
                        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD))
        if pos_count >= 4:
            return "pos"
    except Exception:
        pass
    return None


# ---------- Menu Pygame ----------
def choose_algorithm_and_heuristic(screen):
    font_title = pygame.font.SysFont("monospace", 40)
    font_btn = pygame.font.SysFont("monospace", 28)

    heur_fn, heur_name = choose_heuristic_function()

    while True:
        screen.fill(BLACK)

        title = font_title.render("Choisir l'algorithme et l'heuristique", True, WHITE)
        screen.blit(title, (WIDTH // 2 - 300, 40))

        # Boutons algos
        minimax_rect = pygame.Rect(WIDTH // 2 - 200, 120, 400, 60)
        alphabeta_rect = pygame.Rect(WIDTH // 2 - 200, 200, 400, 60)

        pygame.draw.rect(screen, BLUE, minimax_rect)
        pygame.draw.rect(screen, BLUE, alphabeta_rect)

        txt1 = font_btn.render("Minimax", True, WHITE)
        txt2 = font_btn.render("Alpha-Beta", True, WHITE)

        screen.blit(txt1, (minimax_rect.x + 30, minimax_rect.y + 12))
        screen.blit(txt2, (alphabeta_rect.x + 10, alphabeta_rect.y + 12))

        # Héuristique affichée (choisie automatiquement si trouvée)
        heur_text = font_btn.render(f"Heuristique détectée : {heur_name}", True, WHITE)
        screen.blit(heur_text, (WIDTH // 2 - 220, 300))

        hint = font_btn.render("Cliquez sur un algorithme pour démarrer", True, WHITE)
        screen.blit(hint, (WIDTH // 2 - 220, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if minimax_rect.collidepoint(mx, my):
                    return "minimax", heur_fn, heur_name
                if alphabeta_rect.collidepoint(mx, my):
                    return "alphabeta", heur_fn, heur_name


# ---------- Dessin plateau & stats (identique) ----------
def draw_board(screen, game):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE,
                             (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK,
                               (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                               RADIUS)

    for c in range(COLS):
        for r in range(ROWS):
            if game.board[r][c] == PLAYER_1:
                pygame.draw.circle(screen, RED,
                                   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                    HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            elif game.board[r][c] == PLAYER_2:
                pygame.draw.circle(screen, YELLOW,
                                   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                    HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
    pygame.display.update()


def display_stats(screen, font, algo_name, exec_time, nodes, pruned=None, heur_name="Default"):
    y_offset = HEIGHT - 90
    text = font.render(f"Algo: {algo_name} | Heur: {heur_name}", True, WHITE)
    screen.blit(text, (10, y_offset))

    text = font.render(f"Temps: {exec_time:.3f}s", True, WHITE)
    screen.blit(text, (10, y_offset + 20))

    text = font.render(f"Noeuds: {nodes}", True, WHITE)
    screen.blit(text, (10, y_offset + 40))

    if pruned is not None:
        text = font.render(f"Elagages: {pruned}", True, GREEN)
        screen.blit(text, (10, y_offset + 60))

    pygame.display.update()


# ---------- Main ----------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puissance 4 - IA")

    # Choix menu : algo + heuristique (heur_fn peut être None)
    AI_ALGORITHM, heur_fn, heur_name = choose_algorithm_and_heuristic(screen)
    pygame.display.set_caption(f"Puissance 4 - {AI_ALGORITHM.upper()} (Heur: {heur_name})")

    font_large = pygame.font.SysFont("monospace", 75)
    font_small = pygame.font.SysFont("monospace", 20)

    game = Connect4()
    draw_board(screen, game)

    last_ai_time = 0
    last_ai_nodes = 0
    last_ai_pruned = 0

    print(f"\n{'='*60}")
    print(f"PUISSANCE 4 - IA avec {AI_ALGORITHM.upper()} (Heur: {heur_name})")
    print(f"Profondeur de recherche : {SEARCH_DEPTH}")
    print(f"{'='*60}\n")

    # préparer infos sur signature des fonctions
    minimax_accept = can_pass_heuristic_to(find_best_move_minimax)
    alphabeta_accept = can_pass_heuristic_to(find_best_move_alphabeta)

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                if game.turn == PLAYER_1:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)

                if last_ai_nodes > 0:
                    display_stats(screen, font_small, AI_ALGORITHM.upper(),
                                  last_ai_time, last_ai_nodes,
                                  last_ai_pruned if AI_ALGORITHM == 'alphabeta' else None,
                                  heur_name)
                pygame.display.update()

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

                        game.turn = PLAYER_2
                        draw_board(screen, game)

        # Tour IA
        if game.turn == PLAYER_2 and not game.game_over:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            label = font_small.render("L'IA réfléchit...", 1, YELLOW)
            screen.blit(label, (WIDTH // 2 - 100, 10))
            pygame.display.update()

            start_time = time.time()

            # appel réfléchi : si la fonction accepte une heuristique, on la passe
            try:
                if AI_ALGORITHM == "minimax":
                    if heur_fn and minimax_accept:
                        if minimax_accept == "kw":
                            col, score, stats = find_best_move_minimax(game, SEARCH_DEPTH, heuristic=heur_fn)
                        else:
                            col, score, stats = find_best_move_minimax(game, SEARCH_DEPTH, heur_fn)
                    else:
                        col, score, stats = find_best_move_minimax(game, SEARCH_DEPTH)
                    last_ai_pruned = 0
                else:  # alphabeta
                    if heur_fn and alphabeta_accept:
                        if alphabeta_accept == "kw":
                            col, score, stats = find_best_move_alphabeta(game, SEARCH_DEPTH, heuristic=heur_fn)
                        else:
                            col, score, stats = find_best_move_alphabeta(game, SEARCH_DEPTH, heur_fn)
                    else:
                        col, score, stats = find_best_move_alphabeta(game, SEARCH_DEPTH)
                    last_ai_pruned = stats.get("nodes_pruned", 0)
            except TypeError:
                # Si signature inattendue, fallback sans heuristique
                if AI_ALGORITHM == "minimax":
                    col, score, stats = find_best_move_minimax(game, SEARCH_DEPTH)
                    last_ai_pruned = 0
                else:
                    col, score, stats = find_best_move_alphabeta(game, SEARCH_DEPTH)
                    last_ai_pruned = stats.get("nodes_pruned", 0)

            execution_time = time.time() - start_time
            last_ai_time = execution_time
            last_ai_nodes = stats.get("nodes_explored", stats.get("nodes", 0))

            # logs console
            print(f"Colonne choisie : {col}")
            print(f"Score évalué : {score}")
            print(f"Temps d'exécution : {execution_time:.3f} secondes")
            print(f"Nœuds explorés : {last_ai_nodes}")
            if AI_ALGORITHM == "alphabeta":
                print(f"Nœuds élagués : {last_ai_pruned}")
            print(f"{'='*60}\n")

            # jouer le coup
            if game.is_valid_location(col):
                row = game.get_next_open_row(col)
                game.drop_piece(row, col, PLAYER_2)

                if game.check_win(PLAYER_2):
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                    label = font_large.render("L'IA gagne!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game.game_over = True

                game.turn = PLAYER_1
                draw_board(screen, game)

        # match nul
        if len(game.get_valid_locations()) == 0 and not game.game_over:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            label = font_large.render("Match nul!", 1, WHITE)
            screen.blit(label, (80, 10))
            game.game_over = True
            print("\n🤝 MATCH NUL ! 🤝\n")

    # fin : afficher stats
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
    if last_ai_nodes > 0:
        display_stats(screen, font_small, AI_ALGORITHM.upper(),
                      last_ai_time, last_ai_nodes,
                      last_ai_pruned if AI_ALGORITHM == "alphabeta" else None,
                      heur_name)
    pygame.display.update()

    pygame.time.wait(5000)


if __name__ == "__main__":
    main()
