from Qlearning import *

# Créer une instance de MancalaQLearning
mancala_ai = MancalaQLearning()

# Entraîner l'IA avec un certain nombre d'épisodes
mancala_ai.train(num_episodes=5000)

# Sauvegarder le modèle entraîné dans un fichier
mancala_ai.save_model('q_learning_model.pkl')

# Utiliser l'agent chargé pour jouer au Mancala
# player_aibot()
