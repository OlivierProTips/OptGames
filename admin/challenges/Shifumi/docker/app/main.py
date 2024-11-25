import random
import signal

MAX_GAMES = 100
TIMEOUT = 90

def timeout_handler(signum, frame):
    print("\n\nTROP LENT !!!")
    exit(0)

FLAG = "opt{Well_Done}"

INTRO = f"""
+---------+
| SHIFUMI |
+---------+
C'est un jeu de pierre / feuille / ciseaux
Le but est de gagner plusieurs fois
PIERRE gagne sur CISEAUX
CISEAUX gagne sur FEUILLE
FEUILLE gagne sur PIERRE

Vous avez {TIMEOUT} secondes
"""

class Symbol:
    def __init__(self, name, winner):
        self.name = name
        self.winner = winner

SYMBOLS = [
    Symbol("PIERRE", "FEUILLE"),
    Symbol("FEUILLE", "CISEAUX"),
    Symbol("CISEAUX", "PIERRE")
]

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(TIMEOUT)

print(INTRO)

for i in range(MAX_GAMES):
    print(f'ROUND {i+1}')
    mySymbol = random.choice(SYMBOLS)
    print(f'MOI JE JOUE: {mySymbol.name}')
    rep = input('VOTRE CHOIX: ')

    if not rep.strip().casefold() == mySymbol.winner.casefold():
        print('\nYOU LOOSE!!!')
        exit(0)
    else:
        print('YOU WIN.')

print(FLAG)
