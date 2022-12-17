import itertools
import random
import ast

# Global variable: scores
total_scores = {'bot1': 0, 'bot2': 0, 'bot3': 0, 'user': 0}
# 10 is taken as one as we are checking the second character
weights = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, '1': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}


# Function to generate random cards for each player
def generate_random(p, all_poss_pairs):
    for i in range(13):
        rand_card = random.choice(all_poss_pairs)
        p.append(rand_card[0] + rand_card[1])
        all_poss_pairs.remove(rand_card)


# Function to randomly distribute the cards among the players
def distribute_cards(b1, b2, b3, user):
    l = list()
    suits = ['S', 'H', 'D', 'C']  # Spades, Hearts, Diamonds and Clubs
    cards = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    distribute = list((itertools.product(suits, cards)))

    # Shuffle the cards
    random.shuffle(distribute)

    generate_random(b1, distribute)
    generate_random(b2, distribute)
    generate_random(b3, distribute)
    generate_random(user, distribute)

    l.extend([b1, b2, b3, user])
    return l


# Function to generate the bot calls
def generate_bot_call(bot):
    count = 0
    for val in bot:
        if val[-1] in ('A', 'K', 'Q', 'J'):
            count += 1
    return count


# Function to make the first call in each turn
def first_call(first_player, random_dist, cards_selected):
    x = 3
    max_card = ""
    max_weight = 0
    global weights
    if first_player == 'b1' or first_player == 'b2' or first_player == 'b3':
        if first_player == 'b1':
            x = 0
        elif first_player == 'b2':
            x = 1
        elif first_player == 'b3':
            x = 2
        for card in random_dist[x]:
            if weights[card[1]] > max_weight:
                max_card = ""
                max_weight = weights[card[1]]
                max_card += card
        random_dist[x].remove(max_card)
        cards_selected[first_player] = max_card
        print(f'bot{x + 1}:{max_card}')
        return max_card
    else:
        print(f'Your cards are: {random_dist[3]}')
        user_card = str(input('Select Card: '))
        random_dist[x].remove(user_card)
        cards_selected[first_player] = user_card
        print(f'player:{user_card}')
        return user_card


# Function to make the calls for the next three players
def call(next_player, random_dist, cards_selected):
    x = 3
    max_card = ""
    min_card = ""
    max_weight = weights[cards_selected[first_player][1]]
    min_weight = weights[cards_selected[first_player][1]]
    first_card_reel = []
    if next_player == 'b1' or next_player == 'b2' or next_player == 'b3':
        if next_player == 'b1':
            x = 0
        elif next_player == 'b2':
            x = 1
        elif next_player == 'b3':
            x = 2
        for card in random_dist[x]:
            if card[0] in cards_selected[first_player][0]:
                first_card_reel.append(card)
        if len(first_card_reel) != 0:
            for i in first_card_reel:
                if weights[i[1]] > max_weight:
                    max_card = ""
                    max_weight = weights[i[1]]
                    max_card += i
            if len(max_card) != 0:
                random_dist[x].remove(max_card)
                cards_selected[next_player] = max_card
                print(f'bot{x + 1}:{max_card}')
                return max_card
            else:
                for i in first_card_reel:
                    if weights[i[1]] < min_weight:
                        min_card = ""
                        min_weight = weights[i[1]]
                        min_card += i
                random_dist[x].remove(min_card)
                cards_selected[next_player] = min_card
                print(f'bot{x + 1}:{min_card}')
                return min_card
        else:
            min_weight = 13
            for card in random_dist[x]:
                if weights[card[1]] <= min_weight:
                    min_card = ""
                    min_weight = weights[card[1]]
                    min_card += card
            random_dist[x].remove(min_card)
            cards_selected[next_player] = min_card
            print(f'bot{x + 1}:{min_card}')
            return min_card
    else:
        print(f'Your cards are: {random_dist[3]}')
        user_card = str(input('Select Card: '))
        random_dist[x].remove(user_card)
        cards_selected[next_player] = user_card
        print(f'player:{user_card}')
        return user_card


# Function to make the calls in a circular manner
def calls_in_each_turn(random_dist, cards_selected):
    l = ['b1', 'b2', 'b3', 'user']
    index = l.index(first_player)
    i = index
    while i <= index:
        if i == index - 1:
            next_card = call(l[i], random_dist, cards_selected)
            break
        elif i + 1 == len(l):
            i = 0
            next_card = call(l[i], random_dist, cards_selected)
        else:
            if index == 3:
                for j in range(i + 1, len(l) - 1):
                    next_card = call(l[j], random_dist, cards_selected)
                break
            elif index == 0:
                for j in range(i + 1, len(l)):
                    next_card = call(l[j], random_dist, cards_selected)
                break
            elif index == 2:
                for j in range(i + 1, len(l)):
                    next_card = call(l[j], random_dist, cards_selected)
                next_card = call(l[0], random_dist, cards_selected)
                i = 1
            else:
                for j in range(i + 1, len(l)):
                    next_card = call(l[j], random_dist, cards_selected)
                i = 0


# Function to calculate the score of each player
def calculate_score(calls_made_initial, no_of_wins, scores):
    global total_scores
    for key, value in scores.items():
        if calls_made_initial[key] > no_of_wins[key]:
            scores[key] = -1 * 10 * (calls_made_initial[key])
            total_scores[key] += scores[key]
        else:
            scores[key] = 10 * (calls_made_initial[key]) + (no_of_wins[key] - calls_made_initial[key])
            total_scores[key] += scores[key]
    return scores


# Function to declare winner after each game
def declare_winner(score_this_game):
    winner = sorted(score_this_game.items(), key=lambda x: x[1], reverse=True)
    print(f'\n {winner[0][0]} is the winner!!!!!! \n')


# Function to declare winner after each turn
def declare_winner_each_turn():
    global win
    max_weight = weights[cards_selected[first_player][1]]
    for key, value in cards_selected.items():
        if value[0] in cards_selected[first_player][0]:
            if weights[value[1]] >= max_weight:
                winner = ""
                max_weight = weights[value[1]]
                winner += key

    if winner == 'b1':
        win = 1
        no_of_wins['bot1'] += 1
        print(f'\n BOT1 wins \n')
    elif winner == 'b2':
        win = 2
        no_of_wins['bot2'] += 1
        print(f'\n BOT2 wins \n')
    elif winner == 'b3':
        win = 3
        no_of_wins['bot3'] += 1
        print(f'\n BOT3 wins \n')
    else:
        win = 4
        no_of_wins['user'] += 1
        print(f'\n USER wins \n')


# Function to ask for the type of input (Read from file or random distribution)
def type_of_input(ques):
    global b1, b2, b3, user
    while ques.lower() != '0':
        if ques.lower() == 'r':
            # Distribute the cards randomly among the players
            distribute = distribute_cards(b1, b2, b3, user)
            break

        elif ques.lower() == 'f':
            read = open("input.txt", 'r')
            distribute = list()
            for eachLine in read:
                line = ast.literal_eval(eachLine)
                distribute.append(line)

            b1 = distribute[0]
            b2 = distribute[1]
            b3 = distribute[2]
            user = distribute[3]

            break
        else:
            ques = input("Input either R or F (R for random input and F for file input): ")

    return distribute


if __name__ == '__main__':
    question = 'yes'
    b1 = list()
    b2 = list()
    b3 = list()
    user = list()

    while question.lower()[0] == 'y':
        no_of_games = 0

        # Scores for that particular game
        scores = {'bot1': 0, 'bot2': 0, 'bot3': 0, 'user': 0}

        ques = input("Do you want a random(R) input or file(F) input (R/F): ")

        # Make a function call to 'type_of_input' which returns a list of lists containing cards of each player
        random_dist = type_of_input(ques)

        # Show the cards of the player
        print(f'Your cards are: {random_dist[3]}')

        print('Calls of players: ')
        print(f'Bot 1: {generate_bot_call(b1)}')
        print(f'Bot 2: {generate_bot_call(b2)}')
        print(f'Bot 3: {generate_bot_call(b3)}')

        # Ask the player for his expected potential wins
        player_call = int(input('User: '))

        # Calls made by each of them initially is stored in this dict
        calls_made_initial = {'bot1': generate_bot_call(b1), 'bot2': generate_bot_call(b2),
                              'bot3': generate_bot_call(b3), 'user': player_call}

        # Choosing a random player to start with
        players = ['b1', 'b2', 'b3', 'user']
        first_player = random.choice(players)
        print(f'start from {first_player}')

        # Number of wins is stored here. increment its corresponding value whenever a win occurs
        no_of_wins = {'bot1': 0, 'bot2': 0, 'bot3': 0, 'user': 0}

        # Update win with 1 if b1 wins the previous turn and 2 if b2 and 3 if b3 and 4 if user
        win = 0

        while no_of_games != 13:
            print(f'Turn {no_of_games + 1}')

            cards_selected = {'b1': "", 'b2': "", 'b3': "", 'user': ""}

            # First call in every turn
            if win == 0:
                first_card = first_call(first_player, random_dist, cards_selected)
            else:
                first_player = players[win - 1]
                # From the turns 2 to 13 we have to start with the player who wins
                first_card = first_call(first_player, random_dist, cards_selected)

            # Make a function call to execute one complete turn
            calls_in_each_turn(random_dist, cards_selected)

            # Make a function call to declare a winner for each turn
            declare_winner_each_turn()

            no_of_games += 1
        if no_of_games == 13:
            score_this_game = calculate_score(calls_made_initial, no_of_wins, scores)
            print('\nThe scores for this game are: ')
            for key, value in score_this_game.items():
                print(f'{key}: {score_this_game[key]}')
            declare_winner(score_this_game)

            question = input('Do you want to continue?')

            # Clear the initial lists for the next game
            b1.clear()
            b2.clear()
            b3.clear()
            user.clear()

    # If the player doesn't want to continue, declare the winner
    if question.lower()[0] == 'n':
        print('\nThe final scores are: ')
        for key, value in total_scores.items():
            print(f'{key}: {total_scores[key]}')
        series_winner = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
        print(f'\033[1m {series_winner[0][0].upper()} WINS THE SERIES \033[0m')
