import random

FLAG = 'flag{8615f3bda99aaec71dd605d982b22fc7}'

INTRO = f"""
+----------+
| WHAMAZON |
+----------+
"""

class Article:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Item:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        
    def __repr__(self):
        return f" {self.name}: {self.number}"

ARTICLES = [
    Article("Apple", 2),
    Article("Orange", 3),
    Article("Video Game", 20),
    Article("Game console", 100),
    Article("Television", 500),
    Article("House", 450000),
    Article("The Flag", 100000000),
]

WALLET = 50

INVENTORY = []

def rps():
    print("Wait a second Whammy... you wanna buy THE FLAG???")
    print("This is our most valued item! I won't give it up without an intense game of")
    print("ROCK PAPER SCISSORS!")
    print()
    print("You know how to play, right? A player can pick just one of three choices!")
    print("... Rock beats Scissors")
    print("... Scissors beats Paper")
    print("... Paper beats Rock")
    print("Let's play! First, here are some jedi-mind game tricks to throw you off...")
    
    CHOICES = ["Rock", "Paper", "Scissors"]
    while True:
        opponent = random.choice(CHOICES)
        not_choice = random.choice(CHOICES)
        while not_choice == opponent:
            not_choice = random.choice(CHOICES)
        print(f"\"I, your opponent, will NOT choose {not_choice}!!\"")
        print("?? What is your choice ??")
        print(" 1. Rock")
        print(" 2. Paper")
        print(" 3. Scissors")
        print(" 4. \"Nevermind, I don't wanna play\"")
        choice = input("> ")
        
        if choice not in ["1", "2", "3"]: return False
        
        if opponent == CHOICES[int(choice)-1]:
            print("...DRAW...")
            print("Let's start again")
            print()
        elif (opponent == "Rock" and CHOICES[int(choice)-1] == "Scissors") or \
            (opponent == "Paper" and CHOICES[int(choice)-1] == "Rock") or \
            (opponent == "Scissors" and CHOICES[int(choice)-1] == "Paper"):
            print("...YOU LOOSE...")
            print("I won't give you THE FLAG")
            return False
        else:
            print("...YOU WIN...")
            print("You can have THE FLAG")
            return True
        

def show_inventory():
    print(f"This is your inventory")
    print()
    for i in INVENTORY:
        print(i)
    print()
        
def add_or_update_item(name, number):
    if name == "The Flag": number = FLAG
        
    for item in INVENTORY:
        if item.name == "The Flag":
            return
        if item.name == name:
            item.number += number
            return
    
    # Si aucun Item n'a été trouvé, en ajouter un nouveau
    INVENTORY.append(Item(name, number))
    
def second_menu():
    print("What do you want to buy?")
    global WALLET
    while True:
        print()
        print(f"!! You have: {WALLET} dollars in your wallet !!")
        print()
        
        for i in range(len(ARTICLES)):
            print(f" {i+1}. {ARTICLES[i].name}")
        print(f" {len(ARTICLES)+1}. \"Nothing, I want to leave\"")
            
        choice = input("> ")
        print()
        if choice == str(len(ARTICLES)+1):
            break
        
        choices = [str(x+1) for x in range(len(ARTICLES))]
        if choice not in choices:
            break
        
        print(f"The '{ARTICLES[int(choice)-1].name}' item costs {ARTICLES[int(choice)-1].price} dollars.")
        print(f"How many of the '{ARTICLES[int(choice)-1].name}' items would you like?")
        second_choice = input("> ")
        print()
        try:
            amount = int(second_choice)
            total = amount * ARTICLES[int(choice)-1].price
            if total <= WALLET:
                WALLET = WALLET - (amount * ARTICLES[int(choice)-1].price)
                if ARTICLES[int(choice)-1].name == "The Flag":
                    result = rps()
                    if result:
                        add_or_update_item(ARTICLES[int(choice)-1].name, amount)
                else:
                    add_or_update_item(ARTICLES[int(choice)-1].name, amount)
                    print("Crunching the numbers...")
                    print(f"  {ARTICLES[int(choice)-1].price} dollars x {amount} = {total} subtracted from your wallet!")
        except:
            pass

def first_menu():
    while True:
        print("What do you want to do?")
        print()
        print(" 1. Examine your inventory")
        print(" 2. Buy from Whamazon")
        print(" 3. Quit")
        choice = input("> ")
        print()
        
        match choice:
            case "1":
                show_inventory()
            case "2":
                second_menu()
            case "3":
                break
                
        

print(INTRO)
first_menu()

