import random

def generate_random_mancala():
    length = 14
    total = 48
    rand_list = [random.randint(0, 8) for _ in range(length)]
    current_sum = sum(rand_list)
    scale_factor = total / current_sum
    adjusted_list = [int(value * scale_factor) for value in rand_list]
    
    # Correction des valeurs si nécessaire pour atteindre exactement 'total'
    while sum(adjusted_list) != total:
        if sum(adjusted_list) < total:
            # Ajouter la différence à un élément aléatoire
            index = random.randint(0, length - 1)
            adjusted_list[index] += 1
        else:
            # Soustraire la différence à un élément aléatoire
            index = random.randint(0, length - 1)
            adjusted_list[index] -= 1
    
    return adjusted_list

# Définir le nombre de termes et la somme totale désirée


# Générer la liste aléatoire avec la somme correcte
random_numbers = generate_random_mancala()

# Afficher la liste générée
print(random_numbers,sum(random_numbers))
