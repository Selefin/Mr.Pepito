# Discord Bot Documentation

## Introduction
This documentation provides an overview of Mr.Pepito, a Discord bot built in Python.

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/makesse24/Mr.Pepito.git
   cd Mr.Pepito
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the bot, run this command in a shell:
```bash
python bot.py
```

## Commands
- **`/commands`:** List all available commands
- **`/ping`:** Check the bot's latency
- **`/disconnect`:** Disconnect the bot from Discord
- **`/roulette`:** Play a game of Russian roulette
- **`/blackjack`:** Play a hand of blackjack
- **`/bomb`:** Plant a bomb for a user to defuse
- **`/clear`:** Clear a specified number of messages

## Other Features
- **Role saving and loading:** Saves roles of users when the bot starts in case someone leaves the server.