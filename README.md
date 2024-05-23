# Discord Bot Documentation

## Introduction
**Mr. Pepito - A Discord Bot**

Mr. Pepito is a multifunctional Discord bot designed to enhance your server experience with fun and utility commands. This documentation provides a comprehensive guide to install, configure, and use Mr. Pepito.

## Features
### Commands
- **`/commands`:** List all available commands
- **`/ping`:** Check the bot's latency
- **`/disconnect`:** Disconnect the bot from Discord
- **`/roulette`:** Play a game of Russian roulette
- **`/blackjack`:** Play a hand of blackjack
- **`/bomb`:** Plant a bomb for a user to defuse
- **`/clear`:** Clear a specified number of messages

### Other Features
**Roles Management:** Automatically assigns roles to new members based on their previous roles.

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/makesse24/Mr.Pepito.git
   cd Mr.Pepito
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
3. **Create a `.env` file:**
    Create a `.env` file in the root directory of the project and add the following environment variables:
    ```env
    TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
    OWNER_ID=YOUR_DISCORD_USER_ID_HERE
    ```
   
4. **Run the bot:**
    ```bash
    python bot.py
    ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for more information.