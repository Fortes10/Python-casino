from constants import MAX_RANK, MAX_BET, MIN_BET, RANKS, SUIT_EMOJIS
import random
import time


###### INPUTS ######
def deposit():
    while True:
        amount = input("Enter your deposit: $")
        print()
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a valid number.")

    return amount


def get_bet(balance):
    while True:
        amount = input("Enter your bet: $")
        if amount.isdigit():
            amount = int(amount)
            if amount < MIN_BET or amount > MAX_BET:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
            elif amount > balance:
                print(f"You don't have enough balance. Your current balance is ${balance}.")
            else:
                return amount
        else:
            print("Please enter a valid number.")


def continue_to_deposit(balance):
    while True:
        wants_to_deposit = input("Would you like to deposit more? (y/n): ").lower()
        if wants_to_deposit == "y":
            balance += deposit()
            break
        elif wants_to_deposit == "n":
            print("ending session ...")
            time.sleep(1.5)
            raise SystemExit
        else:
            print("Answer the question correctly")

    return balance


###### CARDS ######
def get_all_suits_and_cards():
    all_suits = []
    for suit in SUIT_EMOJIS.values():
        all_suits.append(suit)

    cards = []
    for card in RANKS.keys():
        cards.append(card)

    return all_suits, cards


def draw_card():
    suits, cards = get_all_suits_and_cards()
    rank = random.choice(cards)
    suit_emoji = random.choice(suits)
    return rank, suit_emoji


def print_card(rank, suit_emoji):
    print(rank + suit_emoji)


def add_card_to_hand(hand):
    rank, suit_emoji = draw_card()
    hand.append((rank, suit_emoji))
    return rank, suit_emoji


def get_hand_value(hand):
    value = 0
    aces = 0

    for rank, _ in hand:
        value += RANKS[rank]
        if rank == "A":
            aces += 1

    while value > MAX_RANK and aces > 0:
        value -= 10
        aces -= 1

    return value


def print_total(owner, hand):
    print(f"{owner} total: {get_hand_value(hand)}")


def print_hand(owner, hand):
    print(f"{owner}'s hand:")
    cards = [f"{rank}{suit_emoji}" for rank, suit_emoji in hand]
    print("  ".join(cards))
    print_total(owner, hand)
    print()


def print_hand_with_new_card(owner, hand, new_rank, new_suit):
    print(f"{owner}'s hand:")
    cards = [f"{rank}{suit_emoji}" for rank, suit_emoji in hand]
    print("  ".join(cards))
    print(f"new card: {new_rank}{new_suit}")
    print_total(owner, hand)
    print()


###### ROUND LOGIC ######
def deal_initial_hand(owner):
    hand = []
    if owner == 'Player':
        add_card_to_hand(hand)
    add_card_to_hand(hand)
    print_hand(owner, hand)
    return hand


def player_turn(player_hand, bet, balance):
    current_bet = bet

    while True:
        player_value = get_hand_value(player_hand)

        if player_value > MAX_RANK:
            print("You lost")
            return current_bet, player_value, "bust"

        if player_value == MAX_RANK:
            print("BLACK JACK!!")
            return current_bet, player_value, "blackjack"

        wants_card = input("Hit(H), Stay(S) or Double(D)? ").upper()
        if wants_card not in ("H", "S", "D"):
            print("Answer correctly")
            continue

        if wants_card == "S":
            return current_bet, player_value, "stay"

        if wants_card == "D":
            if current_bet * 2 > balance:
                print("You don't have enough balance to double.")
                continue

            current_bet *= 2
            print(f"Your bet: ${current_bet}")
            new_rank, new_suit = add_card_to_hand(player_hand)
            print_hand_with_new_card("Player", player_hand, new_rank, new_suit)

            player_value = get_hand_value(player_hand)
            if player_value > MAX_RANK:
                print("You lost")
                return current_bet, player_value, "bust"
            if player_value == MAX_RANK:
                print("BLACK JACK!!")
                return current_bet, player_value, "blackjack"
            return current_bet, player_value, "stay"

        new_rank, new_suit = add_card_to_hand(player_hand)
        print_hand_with_new_card("Player", player_hand, new_rank, new_suit)
        time.sleep(2)


def dealer_turn(dealer_hand):
    print("Dealer's turn:")
    print_hand("Dealer", dealer_hand)
    while get_hand_value(dealer_hand) < 17:
        time.sleep(5)
        add_card_to_hand(dealer_hand)
        print_hand("Dealer", dealer_hand)

    time.sleep(3)
    dealer_value = get_hand_value(dealer_hand)
    if dealer_value > MAX_RANK:
        print("Dealer busted")
    print()
    return dealer_value


def settle_round(balance, bet, player_value, dealer_value, outcome):
    balance -= bet

    if outcome == "bust":
        print("Round result: You lost")
        return balance

    if outcome == "blackjack":
        if dealer_value == MAX_RANK:
            print("Round result: Draw")
            return balance + bet

        print("Round result: BLACKJACK payout")
        return balance + int(bet * 2.5)

    if dealer_value > MAX_RANK or player_value > dealer_value:
        print("Round result: You won")
        return balance + bet * 2

    if player_value < dealer_value:
        print("Round result: You lost")
        return balance

    print("Round result: Draw")
    return balance + bet


def main():
    balance = deposit()

    while True:
        if balance < MIN_BET:
            print(f"You only have ${balance} left.")
            balance = continue_to_deposit(balance)

        print(f"Current balance: ${balance}")
        bet = get_bet(balance)
        print()

        player_hand = deal_initial_hand("Player")
        dealer_hand = deal_initial_hand("Dealer")

        bet, player_value, outcome = player_turn(player_hand, bet, balance)
        dealer_value = get_hand_value(dealer_hand)

        if outcome != "bust":
            dealer_value = dealer_turn(dealer_hand)

        balance = settle_round(balance, bet, player_value, dealer_value, outcome)
        print(f"Current balance: ${balance}")

        wants_to_continue = input("Do you want to continue? (y/n) ").upper()
        while wants_to_continue not in ("Y", "N"):
            print("Answer correctly")
            wants_to_continue = input("Do you want to continue? (y/n) ").upper()

        if wants_to_continue == "N":
            print("ending session ...")
            time.sleep(1.5)
            raise SystemExit

        print()


if __name__ == "__main__":
    main()
