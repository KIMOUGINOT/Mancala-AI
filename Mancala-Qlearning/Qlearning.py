import random
import pickle
import matplotlib.pyplot as plt
import numpy as np
import copy
from Mancala import *


class QLearningAgent:
    def __init__(self, alpha=0.3, gamma=0.99, epsilon=0.3, epsilon_decay=0.999):
        self.Q = {}  # Dictionnary to stock Q value
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # Initial exploration rate
        self.epsilon_decay = epsilon_decay  # Decreasing of epsilon

    def get_Q_value(self, state, action):
        return self.Q.get((state, action), 0.0)

    def update_Q_value(self, state, action, reward, next_state, next_actions):
        if next_actions:
            max_next_Q = max([self.get_Q_value(next_state, a) for a in next_actions])
        else:
            max_next_Q = 0.0  # maybe choose a more appropriate value

        current_Q = self.get_Q_value(state, action)
        new_Q = current_Q + self.alpha * (reward + self.gamma * max_next_Q - current_Q)
        self.Q[(state, action)] = new_Q

    def choose_action(self, state, possible_actions):
        if random.random() < self.epsilon:
            return random.choice(possible_actions)
        else:
            max_Q = max([self.get_Q_value(state, a) for a in possible_actions])
            best_actions = [a for a in possible_actions if self.get_Q_value(state, a) == max_Q]
            return random.choice(best_actions)

    def decay_epsilon(self):
        self.epsilon *= self.epsilon_decay

class MancalaQLearning:
    def __init__(self):
        self.agent = QLearningAgent()  

    def train(self, num_episodes):
        reward_table = []
        episodes_table = np.arange(num_episodes)

        for episode in range(num_episodes):
            mancala_game = Mancala_Board(None)  
            state = tuple(mancala_game.mancala)  
            done = False
            coup = 0
            repeat_turn = False
            current_player = 1
            while not done:
                coup += 1
                if current_player == 0:
                    possible_actions = [i for i in range(6) if mancala_game.mancala[i] > 0]
                else:
                    possible_actions = [i for i in range(7, 13) if mancala_game.mancala[i] > 0]

                action = self.agent.choose_action(state, possible_actions)
                repeat_turn = mancala_game.player_move(action)
                next_state = tuple(mancala_game.mancala)

                reward = mancala_game.husVal()  # hus based reward
                if mancala_game.isEnd():
                    done = True
                    reward = mancala_game.husVal(nb_coup=coup)  # Final reward
                    reward_table.append(reward)

                if not repeat_turn:
                    next_actions = possible_actions if not done else []
                    self.agent.update_Q_value(state, action, reward, next_state, next_actions)
                    state = next_state
                    current_player = not(current_player)

            self.agent.decay_epsilon()  # Decreasing after each episode

            if (episode + 1) % 1000 == 0:
                self.save_model(f'q_learning_model_{episode + 1}.pkl')
                plt.figure()
                plt.scatter(episodes_table[:episode+1], reward_table)
                plt.title('Training Rewards Over Episodes')
                plt.xlabel('Episodes')
                plt.ylabel('Rewards')
                plt.show()

        print(f"reward moyenne : {sum(reward_table)/len(reward_table)}")
        

    def save_model(self, filename):
        """Save Q-learning model

        Args:
            filename (_string_)
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.agent.Q, f)

    def load_model(self, filename):
        """Load Q-learning model

        Args:
            filename (_string_)
        """
        with open(filename, 'rb') as f:
            saved_Q = pickle.load(f)

        self.agent.Q = saved_Q

def player_aibot():
    j = Mancala_Board(None)
    
    mancala_ai = MancalaQLearning()
    
    try:
        mancala_ai.load_model('q_learning_model_10000.pkl')
        print("Model loaded")
    except FileNotFoundError:
        print("No pre-trained model found. Training new model...")
        mancala_ai.train(num_episodes=1000)
        mancala_ai.save_model('q_learning_model.pkl')

    j.print_mancala()

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
            
            print("AI-BOT TURN >>> ", end="")
            state = tuple(j.mancala)  # actual state of the game
            possible_actions = [i for i in range(7, 13) if j.mancala[i] > 0]  # Actions possibles pour l'AI-bot
            
            action = mancala_ai.agent.choose_action(state, possible_actions)
            print(action)
            t = j.player_move(action)
            j.print_mancala()
            if not t:
                break
    
    # Display the game state
    if j.mancala[6] < j.mancala[13]:
        print("AI-BOT WINS")
    else:
        print("YOU WIN")
    
    print('GAME ENDED')
    j.print_mancala()

def player_aivsai():
    """Make two Q-learning agent play each other
    """
    agent_main = MancalaQLearning()
    agent_opponent = MancalaQLearning()

    try:
        agent_main.load_model('q_learning_model_8000.pkl')
        print("1st Model Loaded")
    except FileNotFoundError:
        print("No pre-trained model found for the main agent. Training new model...")
        agent_main.train(num_episodes=200)
        agent_main.save_model('q_learning_model_main.pkl')

    try:
        agent_opponent.load_model('q_learning_model_2000.pkl')
        print("2nd Model Loaded")
    except FileNotFoundError:
        print("No pre-trained model found for the opponent agent. Training new model...")
        agent_opponent.train(num_episodes=50)
        agent_opponent.save_model('q_learning_model_opponent.pkl')


    j = Mancala_Board(None)
    j.print_mancala()

    while True:
        if j.isEnd():
            break
        
        while True:
            if j.isEnd():
                break
            
            print("MAIN AGENT TURN >>> ", end="")
            state = tuple(j.mancala)  
            possible_actions = [i for i in range(7, 13) if j.mancala[i] > 0]  # Actions possibles pour l'agent principal
            
            action = agent_main.agent.choose_action(state, possible_actions)
            print(action)
            t = j.player_move(action)
            j.print_mancala()
            if not t:
                break
        
        while True:
            if j.isEnd():
                break
            
            print("OPPONENT AGENT TURN >>> ", end="")
            state = tuple(j.mancala)
            possible_actions = [i for i in range(0, 6) if j.mancala[i] > 0]  # Actions possibles pour l'agent adversaire
            
            action = agent_opponent.agent.choose_action(state, possible_actions)
            print(action)
            t = j.player_move(action)
            j.print_mancala()
            if not t:
                break
    
    print('GAME ENDED')
    j.print_mancala()
    if j.mancala[6] < j.mancala[13]:
        print("MAIN AGENT WINS")
        return True
    else:
        print("OPPONENT AGENT WINS")
        return False
    
def player_aivsrandom():
    """Make the Q-learning agent play against a random-chooser player
    """
    agent_main = MancalaQLearning()

    try:
        agent_main.load_model('q_learning_model_10000.pkl')
        print("1st Model Loaded")
    except FileNotFoundError:
        print("No pre-trained model found for the main agent. Training new model...")
        agent_main.train(num_episodes=10000)
        agent_main.save_model('q_learning_model_10000.pkl')

    j = Mancala_Board(None)
    j.print_mancala()

    while True:
        if j.isEnd():
            break
        
        while True:
            if j.isEnd():
                break
            
            print("MAIN AGENT TURN >>> ", end="")
            state = tuple(j.mancala) 
            possible_actions = [i for i in range(7, 13) if j.mancala[i] > 0]  # Actions possibles pour l'agent principal
            
            action = agent_main.agent.choose_action(state, possible_actions)
            print(action)
            t = j.player_move(action)
            j.print_mancala()
            if not t:
                break
        
        while True:
            if j.isEnd():
                break
            
            print("OPPONENT AGENT TURN >>> ", end="")
            state = tuple(j.mancala)  
            possible_actions = [i for i in range(0, 6) if j.mancala[i] > 0]  # Actions possibles pour l'agent adversaire
            
            action = random.choice(possible_actions)
            print(action)
            t = j.player_move(action)
            j.print_mancala()
            if not t:
                break
    
    print('GAME ENDED')
    j.print_mancala()
    if j.mancala[6] < j.mancala[13]:
        print("MAIN AGENT WINS")
        return True
    else:
        print("OPPONENT AGENT WINS")
        return False

