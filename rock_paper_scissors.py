import random

player_score = None
program_stop = False


def user_name_input():
    global player_score
    player = input('Enter your name: ')
    print(f'Hello, {player}')
    rating = open('rating.txt', 'r')
    a = rating.readlines()
    for i in a:
        if player in i:
            x = i.split(' ')
            player_score = int(x[1])
            break
    else:
        player_score = 0


def options():
    global program_stop, player_score
    items = ['fire', 'scissors', 'snake', 'human', 'tree',
             'wolf', 'sponge', 'paper', 'air', 'water',
             'dragon', 'devil', 'lightning', 'gun', 'rock',
             'spock', 'lizard']

    while True:
        try:
            options_type = input()
            if not options_type:
                print("Okay, let's start")
                return ['rock', 'paper', 'scissors']
            else:
                options_type = options_type.split(',')
            a = all(elem in items for elem in options_type)
            if a is False:
                print('Invalid input')
            elif a is True:
                print("Okay, let's start")
                return options_type
        except ValueError as exception:
            print(str(exception))


def user_input(opts):
    global program_stop
    while True:
        try:
            option = input()
            if option in opts:
                return option
            elif option == '!rating':
                print(f'Your rating: {player_score}')
                continue
            elif option == '!exit':
                program_stop = True
                break
            else:
                print('Invalid input')
        except ValueError as exception:
            print(str(exception))


def comp_input(opts):
    return opts[random.randint(0, len(opts) - 1)]


def evaluater(user_opt, comp_opt):
    def loss():
        print(f'Sorry, but computer chose {comp_opt}')

    def win():
        global player_score
        print(f'Well done. Computer chose {comp_opt} and failed')
        player_score += 100

    def draw():
        global player_score
        print(f'There is a draw ({comp_opt})')
        player_score += 50

    rules = {'rock': {'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors', 'fire', 'lizard'},
             'fire': {'paper', 'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors'},
             'scissors': {'air', 'paper', 'sponge', 'wolf', 'tree', 'human', 'snake', 'lizard'},
             'snake': {'water', 'air', 'paper', 'sponge', 'wolf', 'tree', 'human'},
             'human': {'dragon', 'water', 'air', 'paper', 'sponge', 'wolf', 'tree'},
             'tree': {'devil', 'dragon', 'water', 'air', 'paper', 'sponge', 'wolf'},
             'wolf': {'lightning', 'devil', 'dragon', 'water', 'air', 'paper', 'sponge'},
             'sponge': {'gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'paper'},
             'paper': {'rock', 'gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'spock'},
             'air': {'fire', 'rock', 'gun', 'lightning', 'devil', 'dragon', 'water'},
             'water': {'scissors', 'fire', 'rock', 'gun', 'lightning', 'devil', 'dragon'},
             'dragon': {'snake', 'scissors', 'fire', 'rock', 'gun', 'lightning', 'devil'},
             'devil': {'human', 'snake', 'scissors', 'fire', 'rock', 'gun', 'lightning'},
             'lightning': {'tree', 'human', 'snake', 'scissors', 'fire', 'rock', 'gun'},
             'gun': {'wolf', 'tree', 'human', 'snake', 'scissors', 'fire', 'rock'},
             'spock': {'rock', 'scissors'},
             'lizard': {'spock', 'paper'}
             }
    if user_opt == comp_opt:
        draw()
    elif user_opt in rules[comp_opt]:
        loss()
    elif comp_opt in rules[user_opt]:
        win()


def menu():
    user_name_input()
    option = options()
    while not program_stop:
        try:
            evaluater(user_input(option), comp_input(option))
        except KeyError:
            print('Bye!')


menu()
