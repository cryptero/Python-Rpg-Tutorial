import sys 
import os
import random
import pickle

weapons = {"Great Sword":40}

class Player:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 100
        self.health = self.maxhealth
        self.base_attack = 10
        self.gold = 40
        self.pots = 0
        self.weap = ["Rusty Sword"]
        self.curweap = ["Rusty Sword"]
        
    @property 
    def attack(self):
        attack = self.base_attack
        if self.curweap == "Rusty Sword":
            attack += 5
        
        if self.curweap == "Great Sword":
            attack += 15
            
        return attack
        

class Goblin:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 50
        self.health = self.maxhealth
        self.attack = 5
        self.goldgain = 10
GoblinIG = Goblin("Goblin")

class Zombie:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 70
        self.health = self.maxhealth
        self.attack = 7
        self.goldgain = 15
ZombieIG = Zombie("Zombie")

def main():
    os.system('clear')
    print "Welcome to my game!\n"
    print "1.) Start"
    print "2.) Load"
    print "3.) Exit"
    option = raw_input("-> ")
    if option == "1":
        start()
    elif option == "2":
        if os.path.exists("savefile") == True:
            os.system('clear')
            with open('savefile', 'rb') as f:
                global PlayerIG
                PlayerIG = pickle.load(f)
            print "Loaded Save State..."
            option = raw_input(' ')
            start1()
        else:
            print "You have no save file for this game."
            option = raw_input(' ')
            main()
            
    elif option == "3":
        sys.exit()
    else:
        main()

def start():
    os.system('clear')
    print "Hello, what is your name?"
    option = raw_input("--> ")
    global PlayerIG
    PlayerIG = Player(option)
    start1()

def start1():
    os.system('clear')
    print "Name: %s" % PlayerIG.name
    print "Attack: %i" % PlayerIG.attack
    print "Gold: %d" % PlayerIG.gold
    print "Current Weapons: %s" % PlayerIG.curweap
    print "Potions: %d" % PlayerIG.pots
    print "Health: %i/%i\n" % (PlayerIG.health, PlayerIG.maxhealth)
    print "1.) Fight"
    print "2.) Store"
    print "3.) Save"
    print "4.) Exit"
    print "5.) Inventory"
    option = raw_input("--> ")
    if option == "1":
        prefight()
    elif option == "2":
        store()
    elif option == "3":
        os.system('clear')
        with open('savefile', 'wb') as f:
            pickle.dump(PlayerIG, f)
            print "\nGame has been saved!\n"
        option = raw_input(' ')
        start1()
    elif option == "4":
        sys.exit()
    elif option == "5":
        inventory()
    else:
        start1()

def inventory():
    os.system('clear')
    print "what do you want to do?"
    print "1.) Equip Weapon"
    print "b.) go back"
    option = raw_input(">>> ")
    if option == "1":
        equip()
    elif option == 'b':
        start1()

def equip():
    os.system('clear')
    print "What do you want to equip?"
    for weapon in PlayerIG.weap:
        print weapon
    print "b to go back"
    option = raw_input(">>> ")
    if option == PlayerIG.curweap:
        print "You already have that weapon equipped"
        option = raw_input(" ")
        equip()
    elif option == "b":
        inventory()
    elif option in PlayerIG.weap:
        PlayerIG.curweap = option
        print "You have equipped %s." % option
        option = raw_input(" ")
        equip()
    else:
        print "You don't have %s in your inventory" % option
    
    
    

def prefight():
    global enemy
    enemynum = random.randint(1, 2)
    if enemynum == 1:
        enemy = GoblinIG
    else:
        enemy = ZombieIG
    fight()
    
def fight():
    os.system('clear')
    print "%s     vs      %s" % (PlayerIG.name, enemy.name)
    print "%s's Health: %d/%d    %s's Health: %i/%i" % (PlayerIG.name, PlayerIG.health, PlayerIG.maxhealth, enemy.name, enemy.health, enemy.maxhealth)
    print "Potions %i\n" % PlayerIG.pots
    print "1.) Attack"
    print "2.) Drink Potion"
    print "3.) Run"
    option = raw_input(' ')
    if option == "1":
        attack()
    elif option == "2":
        drinkpot()
    elif option == "3":
        run()
    else:
        fight()

def attack():
    os.system('clear')
    PAttack = random.randint(PlayerIG.attack / 2, PlayerIG.attack)
    EAttack = random.randint(enemy.attack / 2, enemy.attack)
    if PAttack == PlayerIG.attack / 2:
        print "You miss!"
    else:
        enemy.health -= PAttack
        print "You deal %i damage!" % PAttack
    option = raw_input(' ')
    if enemy.health <=0:
        win()
    os.system('clear')
    if EAttack == enemy.attack/2:
        print "The enemy missed!"
    else:
        PlayerIG.health -= EAttack
        print "The enemy deals %i damage!" % EAttack
    option = raw_input(' ')
    if PlayerIG.health <= 0:
        dead()
    else:
        fight()
    
def drinkpot():
    os.system('clear')
    if PlayerIG.pots == 0:
        print "You don't have any potions!"
    else:
        PlayerIG.health += 50
        if PlayerIG.health > PlayerIG.maxhealth:
            PlayerIG.health = PlayerIG.maxhealth
        print "You drank a potion!"
    option = raw_input(' ')
    fight()

def run():
    os.system('clear')
    runnum = random.randint(1, 3)
    if runnum == 1:
        print "You have successfully ran away!"
        option = raw_input(' ')
        start1()
    else:
        print "You failed to get away!"
        option = raw_input(' ')
        os.system('clear')
        EAttack = random.randint(enemy.attack / 2, enemy.attack)
        if EAttack == enemy.attack/2:
            print "The enemy missed!"
        else:
            PlayerIG.health -= EAttack
            print "The enemy deals %i damage!" % EAttack
        option = raw_input(' ')
        if PlayerIG.health <= 0:
            dead()
        else:
            fight()

def win():
    os.system('clear')
    enemy.health = enemy.maxhealth
    PlayerIG.gold += enemy.goldgain
    print "You have defeated the %s" % enemy.name
    print "You found %i gold!" % enemy.goldgain
    option = raw_input(' ')
    start1()
    
def dead():
    os.system('clear')
    print "You have died"
    option = raw_input(' ')
    
def store():
    os.system('clear')
    print "Welcome to the shop!"
    print "\nWhat would you like to buy?\n"
    print "1.) Great Sword"
    print "back"
    print " "
    option = raw_input(' ')
    
    if option in weapons:
        if PlayerIG.gold >= weapons[option]:
            os.system('clear')
            PlayerIG.gold -= weapons[option]
            PlayerIG.weap.append(option)
            print "You have bought %s" % option
            option = raw_input(' ')
            store()
        
        else:
            os.system('clear')
            print "You don't have enough gold"
            option = raw_input(' ')
            store()
    
    elif option == "back":
        start1()
    
    else:
        os.system('clear')
        print "That item does not exist"
        option = raw_input(' ')
        store()
    
main()


