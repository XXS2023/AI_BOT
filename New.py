import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Define a function to scrape Latoken information
def latoken_info():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment for headless mode

    # Initialize the WebDriver for Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    URL = "https://latoken.me"
    driver.get(URL)

    # Locate the element by its class name
    elements = driver.find_elements(By.CLASS_NAME, "UiR3cpYj.zUKiXyE3.EI9jU84Z.R23Ln2cO.kr-span")
    # Loop through the elements and print their text content
    with open('why.txt', 'w', encoding='utf-8') as f:
        for element in elements[5:]:
            f.write(element.text)
            f.write('n')
    why = open('why.txt').read()

    URL = "https://latoken.me/culture-139"
    driver.get(URL)

    # Locate the element by its class name
    parts = driver.find_elements(By.CLASS_NAME, "UiR3cpYj.zUKiXyE3.EI9jU84Z.R23Ln2cO.kr-span")
    # Loop through the elements and print their text content
    with open('culture.txt', 'w', encoding='utf-8') as f:
        for part in parts[5:50]:
            f.write(part.text)
            f.write('n')
    culture = open('culture.txt').read()

    return {
        "why_latoken": why,
        "hackathon": '''A hackathon is an event where people engage in rapid and collaborative engineering over a relatively short period of time such as 24 or 48 hours...''',
        "culture": culture,
    }


latoken_data = latoken_info()

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    # Check if the user is asking a specific question
    if "?" in user_message:
        answer = get_answer(user_message)
        response = answer if answer else "I'm not sure about that."
    else:
        if "?" in user_message and "latoken" in user_message:
            response = latoken_data['why_latoken']
        elif "?" in user_message and "hackathon" in user_message:
            response = latoken_data['hackathon']
        elif "?" in user_message and "culture" in user_message:
            response = latoken_data['culture']
        else:
            response = "I'm not sure about that. Can you ask something else?"

    update.message.reply_text(response)



def main():
    updater = Updater("7992584492:AAHtpam1xIi3qOPUNKTZhDIs8cKrURTETGI")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


# Load the question-answering model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Combine all scraped data for context
combined_context = latoken_data['why_latoken'] + " " + latoken_data['hackathon'] + " " + latoken_data['culture']

# Example questions to check user memory
memory_questions = {
    "why_latoken": "What is one reason to choose LATOKEN?",
    "hackathon": "What is the purpose of the LATOKEN hackathon?",
    "culture": "Can you describe an aspect of LATOKEN's culture?"
}


def get_answer(question):
    result = qa_pipeline(question=question, context=combined_context)
    return result['answer'] if result['score'] > 0.1 else None  # Check if confidence score is above a threshold


def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    # Check if the user is asking a specific question
    if "?" in user_message:
        answer = get_answer(user_message)

        if answer:
            response = f"Here's what I found: {answer}"
            update.message.reply_text(response)
        else:
            response = "I'm not sure about that. Can you provide more details?"
            update.message.reply_text(response)

            # Ask for clarification if the answer was not satisfactory
            clarification_question = "Could you please specify what you are looking for?"
            update.message.reply_text(clarification_question)

        # After answering, ask a memory question
        memory_question = memory_questions.get(user_message.split()[0], None)  # Use first keyword for simplicity
        if memory_question:
            update.message.reply_text(memory_question)
        return

    # Handle keyword-based responses
    if "latoken" in user_message:
        response = latoken_data['why_latoken']
    elif "hackathon" in user_message:
        response = latoken_data['hackathon']
    elif "culture" in user_message:
        response = latoken_data['culture']
    else:
        response = "I'm not sure about that. Can you ask something else?"

    update.message.reply_text(response)

    # After providing information, ask a clarifying question
    clarification_question = "Does this answer your question, or would you like to know more?"
    update.message.reply_text(clarification_question)

    # Ask a memory question based on the provided information
    if "latoken" in user_message:
        memory_question = memory_questions["why_latoken"]
    elif "hackathon" in user_message:
        memory_question = memory_questions["hackathon"]
    elif "culture" in user_message:
        memory_question = memory_questions["culture"]

        if memory_question:
            update.message.reply_text(memory_question)


if __name__ == "__main__":
    main()
