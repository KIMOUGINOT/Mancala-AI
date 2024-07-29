import random

def generate_random_mancala():
    length = 14
    total = 48
    rand_list = [random.randint(0, 8) for _ in range(length)]
    current_sum = sum(rand_list)
    scale_factor = total / current_sum
    adjusted_list = [int(value * scale_factor) for value in rand_list]
    
    while sum(adjusted_list) != total:
        if sum(adjusted_list) < total:
            index = random.randint(0, length - 1)
            adjusted_list[index] += 1
        else:
            index = random.randint(0, length - 1)
            adjusted_list[index] -= 1
    
    return adjusted_list

if __name__ == "__main__":
    random_numbers = generate_random_mancala()
    print(random_numbers,sum(random_numbers))
