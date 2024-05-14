import random
import pickle
from Mancala import *

class QLearningAgent:
    def __init__(self, alpha=0.2, gamma=0.9, epsilon=0.1):
        self.Q = {}  # Dictionnaire pour stocker les valeurs Q
        self.alpha = alpha  # Taux d'apprentissage
        self.gamma = gamma  # Facteur de remise (discount factor)
        self.epsilon = epsilon  # Taux d'exploration initial

    def get_Q_value(self, state, action):
        return self.Q.get((state, action), 0.0)

    def update_Q_value(self, state, action, reward, next_state, next_actions):
        if next_actions:
            max_next_Q = max([self.get_Q_value(next_state, a) for a in next_actions])
        else:
            # Si next_actions est vide, assigner une valeur par défaut
            max_next_Q = 0.0  # Vous pouvez choisir une autre valeur appropriée ici

        current_Q = self.get_Q_value(state, action)
        new_Q = current_Q + self.alpha * (reward + self.gamma * max_next_Q - current_Q)
        self.Q[(state, action)] = new_Q


    def choose_action(self, state, possible_actions):
        if random.random() < self.epsilon:
            return random.choice(possible_actions)
        else:
            # Choix de l'action avec la plus grande valeur Q pour cet état
            max_Q = max([self.get_Q_value(state, a) for a in possible_actions])
            best_actions = [a for a in possible_actions if self.get_Q_value(state, a) == max_Q]
            return random.choice(best_actions)

class MancalaQLearning:
    def __init__(self):
        self.agent = QLearningAgent()  # Initialisation de l'agent Q-learning

    def train(self, num_episodes):
        mancala_game = Mancala_Board(None, True)  # Initialisation du jeu Mancala

        for episode in range(num_episodes):
            print(f"Episode : {episode}")
            state = tuple(mancala_game.mancala)  # État initial du jeu (configuration du plateau)
            done = False
            mancala_game.print_mancala()

            while not done:
                current_player = 0 if mancala_game.player_move == 0 else 1
                if current_player == 0:
                    possible_actions = [i for i in range(6) if mancala_game.mancala[i] > 0]
                else:
                    possible_actions = [i for i in range(7, 13) if mancala_game.mancala[i] > 0]

                action = self.agent.choose_action(state, possible_actions)
                repeat_turn = mancala_game.player_move(action)
                next_state = tuple(mancala_game.mancala)

                reward = mancala_game.husVal()  # Récompense basée sur la valeur hus
                print(f"reward :{reward}")
                if mancala_game.isEnd():
                    done = True
                    reward = mancala_game.husVal()  # Récompense finale à la fin du jeu

                if not repeat_turn:
                    # Mettre à jour la valeur Q
                    next_actions = possible_actions if not done else []
                    self.agent.update_Q_value(state, action, reward, next_state, next_actions)
                    state = next_state

            mancala_game = Mancala_Board(None,True)  # Réinitialisation du jeu pour un nouvel épisode

    def save_model(self, filename):
        # Sauvegarder le modèle Q-learning dans un fichier
        with open(filename, 'wb') as f:
            pickle.dump(self.agent.Q, f)

    def load_model(self, filename):
        # Charger le modèle Q-learning à partir du fichier
        with open(filename, 'rb') as f:
            saved_Q = pickle.load(f)

        # Assigner les valeurs Q sauvegardées à l'agent Q-learning
        self.agent.Q = saved_Q

def player_aibot():
    j = Mancala_Board(None)
    j.print_mancala()
    
    # Créer une instance de MancalaQLearning pour l'agent Q-learning
    mancala_ai = MancalaQLearning()
    
    # Charger le modèle Q-learning pré-entraîné (s'il existe)
    try:
        mancala_ai.load_model('q_learning_model.pkl')
    except FileNotFoundError:
        print("No pre-trained model found. Training new model...")
        # Entraîner un nouveau modèle Q-learning
        mancala_ai.train(num_episodes=1000)
        # Sauvegarder le modèle entraîné
        mancala_ai.save_model('q_learning_model.pkl')

    while True:
        if j.isEnd():
            break
        
        while True:
            if j.isEnd():
                break
            
            h = int(input("YOUR TURN >>> "))
            if h > 5 or j.mancala[h] == 0:
                print("You can't Play at this position. Choose another position")
                continue
            
            t = j.player_move(h)
            j.print_mancala()
            if not t:
                break
        
        while True:
            if j.isEnd():
                break
            
            print("AI-BOT TURN >>> \n", end="")
            state = tuple(j.mancala)  # État actuel du jeu
            possible_actions = [i for i in range(7, 13) if j.mancala[i] > 0]  # Actions possibles pour l'AI-bot
            
            # Faire choisir à l'agent Q-learning l'action à jouer
            action = mancala_ai.agent.choose_action(state, possible_actions)
            t = j.player_move(action)
            j.print_mancala()
            if not t:
                break
    
    # Afficher le résultat du jeu
    if j.mancala[0] < j.mancala[13]:
        print("AI-BOT WINS")
    else:
        print("YOU WIN")
    
    print('GAME ENDED')
    j.print_mancala()
