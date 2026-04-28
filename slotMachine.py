import random
import time
from constants import MAX_BET, MIN_BET, MAX_LINES, ROWS, symbols_value


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

def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a valid number.")
    
    return lines

def get_bet():
    while True:
        amount = input("Enter the amount you would like to bet: $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid number.")
    
    return amount

def continue_to_deposit(balance):
    while True:
        wants_to_deposit = input("Would you like to deposit more? (y/n): ")
        if wants_to_deposit == 'y':
            balance += deposit()
            break
        elif wants_to_deposit == 'n':
            print("ending session ...")
            time.sleep(1.5)
            exit()
        else:
            print("Answer the question correctly")
    
    return balance


###### SLOT ENGINE ######
def get_symbols(symbols):
    all_symbols = []
    for symbol in symbols.keys():
        all_symbols.append(symbol)
    
    return all_symbols

def get_slot_spin(rows, cols, symbols):
    all_symbols = get_symbols(symbols)

    slot = []
    for _ in range(cols):
        row = []
        for _ in range(rows):
            value = random.choice(all_symbols)
            row.append(value)
        
        slot.append(row)

    return slot

def check_winnings(slot, bet, symbols):
    prize = 0
    for row in slot:
        dif = 0
        init_symb = row[0]
        multiplier = 0
        for i in row:
            if i != init_symb:
                dif = 1
                break
        
        if dif != 1:
            for symb, symb_val in symbols.items():
                if symb == init_symb:
                    multiplier = symb_val
                    prize += bet * multiplier
                    break
    
    print(f"You won ${prize}\n")
    return prize
        

###### SLOT TO STRING ######
def print_slot_machine(slot):
    for col in slot:
        for i in range(len(col)):
            symbol = f"{col[i]:^3}"
            if i != len(col) - 1: 
                print(symbol, end=" | ") 
            else: 
                print(symbol, end="")
        print()


###### Verifications ######
def is_valid_bet(total_bet, balance):
    if total_bet > balance:
        return False
    return True


def session(balance):
    while True:
        lines = get_number_of_lines()
        bet = get_bet()
        total_bet = bet * lines

        if is_valid_bet(total_bet, balance):
            balance = balance - total_bet 
            break
        else:
            print(f"You don't have enough balance. Your current balance is ${balance}")
            balance = continue_to_deposit(balance)

    print("--------------------------------------\n")
    print(f"Total bet is: ${total_bet}.\nYou have ${balance} left on your balance\n")

    slots = get_slot_spin(ROWS, lines, symbols_value)
    print_slot_machine(slots)
    prize = check_winnings(slots, bet, symbols_value)
    total_balance = prize + balance

    return total_balance


def main():
    balance = deposit()
    while True:
        print(f"Current balance: ${balance}")
        balance = session(balance)
        if balance <= 10:
            balance = continue_to_deposit(balance)

if __name__ == "__main__":
    main()