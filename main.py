# Bogdanov :D

import datetime
import os
from random import randint
from time import sleep
from colorama import *
init()

lastMessage = ["", ""]
message = ["", ""]

stepsSurvived = 0
playerHealth = 10
playerAccuracy = 60
playerDamage = 2
playerFood = 2
playersStep = True
isFriends = False

enemyHealth = 4
enemyDamage = 1
enemyFriendliness = 20
enemyAccuracy = 20
enemyIsAngry = False

def step():
    global lastMessage
    global message
    
    global stepsSurvived
    global playerHealth 
    global playerAccuracy 
    global playerDamage
    global playerFood
    global playersStep
    global isFriends

    global enemyHealth
    global enemyDamage
    global enemyFriendliness 
    global enemyAccuracy 
    global enemyIsAngry 
    
    os.system("cls")

    stepsSurvived += 1

    # Title
    print(Fore.CYAN + "> PITON by BOGDANOV <")
    print(f"{ stepsSurvived } steps survived")
    print(Fore.RESET)

    # Stats
    print(f"{ Fore.RESET }You - { Fore.GREEN }Health { playerHealth } { Fore.RED }Damage { playerDamage } { Fore.WHITE }Accuracy { playerAccuracy }% { Fore.GREEN }Food { playerFood }")
    print(f"{ Fore.RESET }Enemy - { Fore.GREEN }Health { enemyHealth } { Fore.RED }Damage { enemyDamage } { Fore.WHITE }Accuracy { enemyAccuracy }% { Fore.BLUE }Friendliness { enemyFriendliness }%")
    
    print(Fore.BLUE + "          {}       {}           ".format("+" if playersStep else " ", "+" if not playersStep else " "))
    print(Fore.RESET         + "          @      {}{}           ".format(
        "$" if isFriends else " ",
        "&" if enemyHealth > 0 else " "
    ))
    print(Fore.LIGHTBLACK_EX + "==============================")
    print("")
    renderMessages()
    print("")
    
    # Actions
    buttons = [
        f'{ Back.RED }[(1) ATTACK]',
        f'{ Back.BLUE }[(2) REST]',
        f'{ Back.GREEN }[(3) MERCY]',
        f'{ Back.GREEN }[(4) EAT]' if playerFood > 0 else ""
    ]
    print(f"{ Fore.RESET }Actions: { f'{ Back.RESET } '.join(str(btn) for btn in buttons) }{ Back.RESET }")

    if playersStep: # Player walks
        action = int(input(f"{ Back.RESET }Choose an action: { Fore.LIGHTYELLOW_EX }") or 0)

        putMessage("")
        playersStep = False

        # Attack
        if action == 1:
            enemyIsAngry = True
            
            if randint(0, 100) <= playerAccuracy:
                # Hit
                hitEnemy(playerDamage)
                
            else:
                # Miss
                putMessage(f"You've missed the enemy...")
                
        # Rest
        elif action == 2:
            putMessage("Rest")
        # Mercy
        elif action == 3:
            if randint(0, 100) <= enemyFriendliness and not enemyIsAngry:
                buffIndex = randint(0, 3)
                isFriends = True

                # Heal
                if buffIndex == 0:
                    playerHealth += 10
                    putMessage(f"{ Fore.YELLOW }Now you are friends! +10 health")
                # Damage up
                elif buffIndex == 1:
                    dmg = randint(1, 3)
                    playerDamage += dmg
                    putMessage(f"{ Fore.YELLOW }Now you are friends! +{ dmg } damage")
                # Accuracy up
                elif buffIndex == 2 and playerAccuracy < 100:
                    acc = randint(5, 10)
                    playerAccuracy += acc
                    putMessage(f"{ Fore.YELLOW }Now you are friends! +{ acc } accuracy")
                # Food
                elif buffIndex == 3:
                    playerFood += 2
                    putMessage(f"{ Fore.YELLOW }Now you are friends! +3 food")
                
                step()
                nextEnemy()
            else:
                enemyIsAngry = True
                putMessage(f"{ Fore.RED }Enemy don't want to be friends with you")
        # Heal
        elif action == 4 and playerFood > 0:
            playerFood -= 1
            playerHealth += 5
            putMessage(f"{ Fore.YELLOW }+5 health")
        else:
            putMessage(f"Wrong action")
            playersStep = True
        
        step()
    else: # Enemy walks
        print(f"{ Back.RESET+Fore.LIGHTBLACK_EX }Choose an action{ Fore.RESET }")

        if enemyHealth > 0 and not isFriends:
            sleep(.5)

            if randint(0, 100) <= enemyAccuracy:
                # Hit
                playerHealth -= enemyDamage
                putMessage(f"{ Fore.RED }Enemy have hitted you! { Fore.YELLOW }{ enemyDamage }")
            else:
                # Miss
                putMessage("Enemy have missed you...")

            playersStep = True
            
            if playerHealth <= 0:
                killPlayer()
            else:
                step()

def killPlayer():
    global stepsSurvived
    
    os.system("cls")
    print(Back.RED, "> YOU LOSE <")
    print(Back.RESET, f"{ stepsSurvived } steps survived")

# Enemies
def hitEnemy(damage: int)-> bool:
    global enemyHealth
    
    enemyHealth -= damage
    putMessage(f"You've hitted the enemy! { Fore.YELLOW }{ damage }")

    if enemyHealth <= 0:
        killEnemy()
    
def killEnemy():
    global playersStep
    global playerHealth
    
    putMessage(f"{ Fore.YELLOW }You've defeated the enemy!")
    playersStep = False
    playerHealth += 2
    step()
    # sleep(1)
    nextEnemy()
    
def nextEnemy():
    sleep(1)
    
    global message
    global lastMessage
    global playersStep
    
    global enemyHealth
    global enemyDamage
    global enemyAccuracy
    global enemyFriendliness
    global isFriends
    global enemyIsAngry

    message = ["", ""]
    lastMessage = ["", ""]
    isFriends = False
    enemyIsAngry = False
    enemyHealth = randint(2, 8)
    enemyDamage = randint(2, 4)
    enemyFriendliness = randint(10, 90)
    enemyAccuracy = randint(20, 60)

    playersStep = True
    step()

# Messages
def putMessage(msg: str):
    global message
    global lastMessage

    time = datetime.datetime.now().time()

    if message[0]:
        lastMessage[0] = message[0]
        lastMessage[1] = message[1]
    message[0] = msg
    if msg:
        message[1] = f"{ Fore.LIGHTBLACK_EX }[{ time.hour }:{ time.minute }:{ time.second }]"
def renderMessages():
    # Last message
    print(f"{ Fore.LIGHTBLACK_EX }> { lastMessage[0] } { lastMessage[1] }{ Fore.RESET }")
    # Message
    print(f"{ Fore.RESET }> { message[0] } { message[1] }{ Fore.RESET }")
    
if __name__ == "__main__":
    os.system("title PITON by BOGDANOV")
    step()