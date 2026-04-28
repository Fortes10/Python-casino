# Python Casino

A simple terminal casino project built with Python. Right now it includes a slot machine game and a blackjack game.

## Games

### Slot Machine

- Deposit money before starting a session
- Choose how many lines to bet on
- Choose the amount to bet
- Spin the slot machine and check your winnings
- Continue playing while you still have balance

#### Symbols

The slot machine currently uses four symbols with different payout values:

- Diamond: `8x`
- Cherry: `6x`
- Lemon: `4x`
- Bell: `2x`

#### How It Works

1. Deposit an initial balance
2. Choose the number of lines to bet on
3. Choose your bet amount
4. The slot machine spins
5. If all symbols in a row match, you win based on that symbol's value

### BlackJack

- Deposit money before starting a session
- Place a bet within the allowed minimum and maximum values
- Play with `Hit`, `Stay`, or `Double`
- Aces are adjusted automatically between `11` and `1`
- The dealer keeps drawing until reaching at least `17`
- The game calculates wins, losses, draws, and blackjack payout

#### How It Works

1. Deposit an initial balance
2. Place your bet
3. Receive your starting hand and see the dealer's hand
4. Choose `Hit`, `Stay`, or `Double`
5. The dealer finishes the round
6. The balance is updated based on the result

## Run The Project

Make sure you have Python installed, then run one of these:

```bash
python slotMachine.py
```

```bash
python blackJack.py
```

## Project Structure

- `slotMachine.py` - slot machine game logic
- `blackJack.py` - blackjack game logic
- `constants.py` - shared constants used by the games

## Author

Made as a Python practice project.
