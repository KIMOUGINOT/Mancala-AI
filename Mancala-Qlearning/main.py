from Qlearning import *

# Créer une instance de MancalaQLearning
mancala_ai = MancalaQLearning()

# Entraîner l'IA avec un certain nombre d'épisodes
mancala_ai.train(num_episodes=100)

# # Sauvegarder le modèle entraîné dans un fichier
mancala_ai.save_model('q_learning_model.pkl')

# Utiliser l'agent chargé pour jouer au Mancala
# cpt = 0
# for _ in range (100) :
#     if not(player_aivsai()) :
#         cpt+=1
#         print(cpt)
