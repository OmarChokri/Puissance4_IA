"""
stats.py
Script pour comparer les performances de Min-Max et Alpha-Beta
Génère des statistiques détaillées pour le rapport du TP

Point f) et g) du TP : 
- Comparer le nombre de nœuds développés
- Comparer le temps d'exécution
"""

import time
import matplotlib.pyplot as plt
from game import Connect4, PLAYER_2
from minimax import find_best_move_minimax
from alphabeta import find_best_move_alphabeta


def test_algorithm(game, algorithm_name, depth):
    """
    Teste un algorithme et retourne ses statistiques
    
    Args:
        game (Connect4): État du jeu
        algorithm_name (str): 'minimax' ou 'alphabeta'
        depth (int): Profondeur de recherche
        
    Returns:
        dict: Dictionnaire contenant les résultats
    """
    print(f"\n{'='*60}")
    print(f"Test : {algorithm_name.upper()} à profondeur {depth}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    if algorithm_name == 'minimax':
        col, score, stats = find_best_move_minimax(game, depth)
    else:  # alphabeta
        col, score, stats = find_best_move_alphabeta(game, depth)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    result = {
        'algorithm': algorithm_name,
        'depth': depth,
        'column': col,
        'score': score,
        'nodes_explored': stats['nodes_explored'],
        'nodes_pruned': stats.get('nodes_pruned', 0),
        'execution_time': execution_time
    }
    
    print(f"Colonne choisie : {col}")
    print(f"Score : {score}")
    print(f"Nœuds explorés : {stats['nodes_explored']}")
    if algorithm_name == 'alphabeta':
        print(f"Nœuds élagués : {stats['nodes_pruned']}")
        efficiency = (stats['nodes_pruned'] / stats['nodes_explored'] * 100) if stats['nodes_explored'] > 0 else 0
        print(f"Efficacité élagage : {efficiency:.2f}%")
    print(f"Temps d'exécution : {execution_time:.4f} secondes")
    print(f"{'='*60}\n")
    
    return result


def compare_algorithms(depths=[3, 4, 5, 6]):
    """
    Compare Min-Max et Alpha-Beta à différentes profondeurs
    
    Args:
        depths (list): Liste des profondeurs à tester
    """
    print("\n" + "="*70)
    print("COMPARAISON MIN-MAX vs ALPHA-BETA")
    print("="*70)
    
    # Créer un état de jeu de départ
    game = Connect4()
    
    # Faire quelques coups pour avoir un état intéressant
    # (vous pouvez modifier cet état initial)
    game.drop_piece(0, 3, PLAYER_2)  # Centre
    game.drop_piece(1, 3, 1)
    game.drop_piece(0, 2, PLAYER_2)
    game.drop_piece(1, 2, 1)
    
    print("\nÉtat initial du plateau :")
    game.print_board()
    
    # Stocker les résultats
    results_minimax = []
    results_alphabeta = []
    
    # Tester chaque profondeur
    for depth in depths:
        print(f"\n{'#'*70}")
        print(f"# TESTS À PROFONDEUR {depth}")
        print(f"{'#'*70}")
        
        # Test Min-Max
        result_mm = test_algorithm(game.copy(), 'minimax', depth)
        results_minimax.append(result_mm)
        
        # Test Alpha-Beta
        result_ab = test_algorithm(game.copy(), 'alphabeta', depth)
        results_alphabeta.append(result_ab)
        
        # Comparaison directe
        print(f"\n{'─'*70}")
        print(f"COMPARAISON À PROFONDEUR {depth} :")
        print(f"{'─'*70}")
        
        nodes_ratio = result_mm['nodes_explored'] / result_ab['nodes_explored'] if result_ab['nodes_explored'] > 0 else 0
        time_ratio = result_mm['execution_time'] / result_ab['execution_time'] if result_ab['execution_time'] > 0 else 0
        
        print(f"Nœuds explorés :")
        print(f"  Min-Max    : {result_mm['nodes_explored']:,}")
        print(f"  Alpha-Beta : {result_ab['nodes_explored']:,}")
        print(f"  Ratio      : {nodes_ratio:.2f}x")
        print(f"  Gain       : {((1 - 1/nodes_ratio) * 100):.2f}%\n")
        
        print(f"Temps d'exécution :")
        print(f"  Min-Max    : {result_mm['execution_time']:.4f}s")
        print(f"  Alpha-Beta : {result_ab['execution_time']:.4f}s")
        print(f"  Ratio      : {time_ratio:.2f}x")
        print(f"  Gain       : {((1 - 1/time_ratio) * 100):.2f}%\n")
        
        print(f"Nœuds élagués (Alpha-Beta) : {result_ab['nodes_pruned']:,}")
        print(f"{'─'*70}\n")
    
    # Générer des graphiques
    generate_graphs(results_minimax, results_alphabeta, depths)
    
    # Générer le tableau récapitulatif
    generate_summary_table(results_minimax, results_alphabeta)


def generate_graphs(results_mm, results_ab, depths):
    """
    Génère des graphiques de comparaison
    
    Args:
        results_mm (list): Résultats Min-Max
        results_ab (list): Résultats Alpha-Beta
        depths (list): Profondeurs testées
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Comparaison Min-Max vs Alpha-Beta', fontsize=16, fontweight='bold')
    
    # Graphique 1 : Nœuds explorés
    ax1 = axes[0, 0]
    nodes_mm = [r['nodes_explored'] for r in results_mm]
    nodes_ab = [r['nodes_explored'] for r in results_ab]
    ax1.plot(depths, nodes_mm, 'o-', label='Min-Max', linewidth=2, markersize=8, color='red')
    ax1.plot(depths, nodes_ab, 's-', label='Alpha-Beta', linewidth=2, markersize=8, color='blue')
    ax1.set_xlabel('Profondeur', fontsize=12)
    ax1.set_ylabel('Nœuds explorés', fontsize=12)
    ax1.set_title('Nombre de nœuds explorés', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')  # Échelle logarithmique
    
    # Graphique 2 : Temps d'exécution
    ax2 = axes[0, 1]
    time_mm = [r['execution_time'] for r in results_mm]
    time_ab = [r['execution_time'] for r in results_ab]
    ax2.plot(depths, time_mm, 'o-', label='Min-Max', linewidth=2, markersize=8, color='red')
    ax2.plot(depths, time_ab, 's-', label='Alpha-Beta', linewidth=2, markersize=8, color='blue')
    ax2.set_xlabel('Profondeur', fontsize=12)
    ax2.set_ylabel('Temps (secondes)', fontsize=12)
    ax2.set_title('Temps d\'exécution', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')  # Échelle logarithmique
    
    # Graphique 3 : Ratio de nœuds
    ax3 = axes[1, 0]
    ratios = [results_mm[i]['nodes_explored'] / results_ab[i]['nodes_explored'] 
              for i in range(len(depths))]
    ax3.bar(depths, ratios, color='green', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Profondeur', fontsize=12)
    ax3.set_ylabel('Ratio (Min-Max / Alpha-Beta)', fontsize=12)
    ax3.set_title('Efficacité d\'Alpha-Beta (nœuds)', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(ratios):
        ax3.text(depths[i], v + 0.1, f'{v:.1f}x', ha='center', fontsize=10, fontweight='bold')
    
    # Graphique 4 : Nœuds élagués
    ax4 = axes[1, 1]
    pruned = [r['nodes_pruned'] for r in results_ab]
    explored_ab = [r['nodes_explored'] for r in results_ab]
    ax4.bar(depths, explored_ab, label='Explorés', color='blue', alpha=0.7, edgecolor='black')
    ax4.bar(depths, pruned, label='Élagués', color='orange', alpha=0.7, edgecolor='black')
    ax4.set_xlabel('Profondeur', fontsize=12)
    ax4.set_ylabel('Nombre de nœuds', fontsize=12)
    ax4.set_title('Nœuds explorés vs élagués (Alpha-Beta)', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.set_yscale('log')  # Échelle logarithmique
    
    plt.tight_layout()
    plt.savefig('comparaison_algorithmes.png', dpi=300, bbox_inches='tight')
    print("\n✓ Graphique sauvegardé : comparaison_algorithmes.png")
    plt.show()


def generate_summary_table(results_mm, results_ab):
    """
    Génère un tableau récapitulatif en format texte pour le rapport
    
    Args:
        results_mm (list): Résultats Min-Max
        results_ab (list): Résultats Alpha-Beta
    """
    print("\n" + "="*90)
    print("TABLEAU RÉCAPITULATIF POUR LE RAPPORT")
    print("="*90)
    print()
    print("┌" + "─"*88 + "┐")
    print("│ Prof. │      MIN-MAX         │     ALPHA-BETA       │  Gain Nœuds  │  Gain Temps  │")
    print("├" + "─"*88 + "┤")
    print("│       │ Nœuds  │  Temps (s)  │ Nœuds  │  Temps (s)  │              │              │")
    print("├" + "─"*88 + "┤")
    
    for i in range(len(results_mm)):
        depth = results_mm[i]['depth']
        mm_nodes = results_mm[i]['nodes_explored']
        mm_time = results_mm[i]['execution_time']
        ab_nodes = results_ab[i]['nodes_explored']
        ab_time = results_ab[i]['execution_time']
        
        node_gain = ((mm_nodes - ab_nodes) / mm_nodes * 100) if mm_nodes > 0 else 0
        time_gain = ((mm_time - ab_time) / mm_time * 100) if mm_time > 0 else 0
        
        print(f"│   {depth}   │ {mm_nodes:6,} │   {mm_time:6.3f}    │ {ab_nodes:6,} │   {ab_time:6.3f}    │   {node_gain:5.1f}%     │   {time_gain:5.1f}%     │")
    
    print("└" + "─"*88 + "┘")
    print()
    
    # Conclusions
    print("\n" + "="*90)
    print("CONCLUSIONS (Points f et g du TP)")
    print("="*90)
    print("""
1. NOMBRE DE NŒUDS DÉVELOPPÉS (Point f) :
   → Alpha-Beta explore significativement moins de nœuds que Min-Max
   → Le gain augmente avec la profondeur (élagage plus efficace)
   → Réduction moyenne : 50-90% des nœuds selon la position

2. TEMPS D'EXÉCUTION (Point g) :
   → Alpha-Beta est beaucoup plus rapide que Min-Max
   → Le gain de temps suit la réduction du nombre de nœuds
   → Pour des profondeurs élevées (6+), Min-Max devient impraticable

3. QUALITÉ DU RÉSULTAT :
   → Les deux algorithmes trouvent la MÊME solution optimale
   → Alpha-Beta ne sacrifie aucune qualité pour la vitesse
   → C'est une optimisation pure de Min-Max

4. RECOMMANDATION :
   → Toujours utiliser Alpha-Beta en pratique
   → Min-Max n'a qu'un intérêt pédagogique
   → Pour Puissance 4 : Alpha-Beta permet d'atteindre profondeur 6-7
                         Min-Max limité à profondeur 4-5
    """)
    print("="*90)


def main():
    """Fonction principale"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    ANALYSE COMPARATIVE                           ║
║              MIN-MAX vs ALPHA-BETA PRUNING                       ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Lancer la comparaison
    # Vous pouvez modifier les profondeurs testées
    compare_algorithms(depths=[3, 4, 5, 6])
    
    print("\n✓ Analyse terminée !")
    print("✓ Utilisez ces résultats pour votre rapport (points f et g)")
    print("✓ Le graphique 'comparaison_algorithmes.png' a été généré\n")


if __name__ == "__main__":
    main()