# AI Chat-Bot for Latoken

Welcome to the AI Chat-Bot project! This bot is designed to provide users with information about Latoken, including details about the company, its hackathons, and its business culture. The bot scrapes relevant information from the official Latoken website and uses a built-in artificial conversational model to generate appropriate responses to user queries.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Code Overview](#code-overview)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Information Retrieval**: Scrapes data from the official Latoken website.
- **Conversational AI**: Engages users in conversation using an AI model.
- **Clarifying Questions**: Asks follow-up questions to ensure users understand key concepts.
- **User-Friendly Interface**: Interacts with users through Telegram.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository
2. Install the required dependencies
3. 
3. Set up your Telegram bot token:
   - Create a new bot on Telegram via [BotFather](https://core.telegram.org/bots#botfather).
   - Replace YOUR_TELEGRAM_BOT_TOKEN in the code with your bot token.
4. Run the bot
## Usage

Once the bot is running, you can interact with it through Telegram. Simply send your queries related to Latoken, and the bot will respond with relevant information.

### Example Queries
- "Tell me about Latoken's hackathons."
- "What is the business culture at Latoken?"

## How It Works

1. **Web Scraping**: The bot scrapes data from the official Latoken website to gather information about the company and its culture.
2. **Data Storage**: Collected data is stored in separate text files for efficient access.
3. **Conversational Model**: The chat-bot uses an AI model to interpret user queries and generate responses based on scraped data.
4. **Clarification Process**: After providing information, the bot engages users with clarifying questions to check their understanding of key concepts.

## Code Overview

Here’s a brief overview of the main components of the code:

- **Web Scraping**: The latoken_info() function uses Selenium to scrape information from the Latoken website.
- **Telegram Bot**: The bot is set up using the telegram library, handling commands and messages from users.
- **Response Handling**: The bot processes user messages and generates responses based on the collected information.



   

   

