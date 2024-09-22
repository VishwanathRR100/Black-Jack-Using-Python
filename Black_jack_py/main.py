import sys,random
#sys -> It allows operating on the interpreter as it provides access to the variables and functions that interact strongly with the interpreter
# visit https://www.geeksforgeeks.org/python-sys-module/ for overview of sys includes sys.argv,sys.exit(),sys.stdin,sys.stdout,sys.stderr
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'backside'

print("Welcome to BlackJack")
money = 5000

# get bet
def getBet(maxBet):
    '''Ask the player how much to bet'''
    while(True):
        print(f"How much do you want to bet? (1-{maxBet}, or QUIT)")
        bet = input("> ").upper().strip()
        if bet == "QUIT":
            print("Thanks for playing!")
            sys.exit()
        if not bet.isdecimal():
            print("Please enter a number! or QUIT!")
            continue
        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet
            sys.exit()
        
# get Deck
def getDeck():
    '''Create a standard deck of 52 cards'''
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def displayCards(cards):
    '''Display all the cards in the cards list'''
    rows = ['','','','','']
    for card in cards:
        rows[0] += " ___ "
        if(card == BACKSIDE):
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '| ##| '
        else:
            rank , suit = card
            rows[1] += '|{} |'.format(rank.ljust(2))
            rows[2] += '| {} |'.format(suit)
            rows[3] += '|_{}|'.format(rank.rjust(2,"_"))
    for row in rows:
        print(row)

def get_hand_value(cards):
    value = 0
    number_aces = 0
    for card in cards:
        rank = card[0]
        if(rank == "A"):
            number_aces += 1
        elif rank in ('K','J',"Q"):
            value += 10
        else:
            value += int(rank)
    value += number_aces
    for i in range(number_aces):
        if(value+10 <= 21):
            value += 10
    return value    

def display_hands(player_hand, dealer_hand, show_dealer_hand):
    print()
    if show_dealer_hand:
        print("DEALER:", get_hand_value(dealer_hand))
        displayCards(dealer_hand)
    else:
        print("DEALER: ???")
        displayCards([BACKSIDE] + dealer_hand[1:])

    print("PLAYER:", get_hand_value(player_hand))
    displayCards(player_hand)

def get_move(player_hand, money):
    while True:
        move = ["(H)it", "(S)tand"]
        if len(player_hand) == 2 and money > 0:
            move.append("(D)ouble down")

        move_prompt = ", ".join(move) + "> "
        moves = input(move_prompt).upper()
        if moves in ("H", "S"):
            return moves
        elif moves == "D" and "(D)ouble down" in move:
            return "D"

while True:
    if money <= 0:
        print("You're broke!")
        print("Good game. Thanks for playing")
        sys.exit()
    print(f"You have ${money}")
    bet = getBet(money)
    deck = getDeck()
    dealerHand = [deck.pop(), deck.pop()]
    playerHand = [deck.pop(), deck.pop()]
    print("Bet is ${}".format(bet))
    while True:
        display_hands(playerHand, dealerHand, False)
        player_val = get_hand_value(playerHand)
        move = get_move(playerHand, money - bet)

        if move == "D":
            additionalBet = input("Enter your additional bet : > ").strip()
            if(additionalBet.isdecimal()):
                bet += int(additionalBet)
                playerHand.append(deck.pop())
                display_hands(playerHand, dealerHand, False)
                print(f"Bet increased to ${bet}")
                print("Bet is ${}".format(bet))
                continue
            else:
                print("Please enter a number!")
                continue

        if player_val > 21:
            print("You busted!")
            money -= bet
            break

        if move == "H":
            playerHand.append(deck.pop())
            continue

        if move == "S":
            while(True):
                display_hands(playerHand, dealerHand, True)
                if get_hand_value(dealerHand) < 17:
                    dealerHand.append(deck.pop())
                    continue
                elif get_hand_value(dealerHand) > 21:
                    print("Dealer busts! You won ${}".format(bet))
                    money += bet
                    break
                elif get_hand_value(dealerHand) > get_hand_value(playerHand):
                    print("Dealer won ! You lost ${}".format(bet))
                    money -= bet
                    break
                elif get_hand_value(dealerHand) < get_hand_value(playerHand):
                    print("You won ${}".format(bet))
                    money += bet
                    break
                else:
                    print("It's a tie!")
                    break
            break



    


