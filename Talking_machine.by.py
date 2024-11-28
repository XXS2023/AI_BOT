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
import logging



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
            f.write('\n')
    why = open('why.txt').read()

    URL = "https://latoken.me/culture-139"
    driver.get(URL)

    # Locate the element by its class name
    parts = driver.find_elements(By.CLASS_NAME, "UiR3cpYj.zUKiXyE3.EI9jU84Z.R23Ln2cO.kr-span")
    # Loop through the elements and print their text content
    with open('culture.txt', 'w', encoding='utf-8') as f:
        for part in parts[5:60]:
            f.write(part.text)
            f.write('\n')
    culture = open('culture.txt').read()

    return {
        "why_latoken": why,
        "hackathon": '''A hackathon is an event where people engage in rapid and collaborative engineering over a relatively short period of time such as 24 or 48 hours. They are often run using agile software development practices, such as sprint-like design wherein computer programmers and others involved in software development, including graphic designers, interface designers, product managers, project managers, domain experts, and others collaborate intensively on engineering projects, such as software engineering.
The goal of a hackathon is to create functioning software or hardware by the end of the event. Hackathons tend to have a specific focus, which can include the programming language used, the operating system, an application, an API, or the subject and the demographic group of the programmers. In other cases, there is no restriction on the type of software being created or the design of the new system. Hakatons in Latoken company are held every Friday at 6 pm (Moskow)''',
        "culture": culture,
    }

latoken_data = latoken_info()

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome! Ask me about Latoken.')


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


# Load the question-answering model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


# Combine all scraped data for context
combined_context = latoken_data['why_latoken'] + " " + latoken_data['hackathon'] + " " + latoken_data['culture']


# Example questions and expected answers to check user memory
memory_questions = {
    "why_latoken": {
        "question": "What is one reason to choose LATOKEN?",
        "expected_answer": "LATOKEN is known for its liquidity and innovative solutions."
    },
    "hackathon": {
        "question": "What is the purpose of the LATOKEN hackathon?",
        "expected_answer": "To foster innovation and develop new blockchain solutions."
    },
    "culture": {
        "question": "Can you describe an aspect of LATOKEN's culture?",
        "expected_answer": "LATOKEN promotes a culture of collaboration and continuous learning."
    }
}


def get_answer(question):
    result = qa_pipeline(question=question, context=combined_context)
    return result['answer'] if result['score'] > 0.1 else None  # Check if confidence score is above a threshold


def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    # Check if the user is in answer-checking mode
    if context.user_data.get('waiting_for_answer'):
        current_question_key = context.user_data.get('current_memory_question')

        if current_question_key:
            expected_answer = memory_questions[current_question_key]['expected_answer'].lower()

            # Check user's answer against expected answer
            if expected_answer in user_message:
                response = "Correct! Great job remembering that!"
            else:
                response = f"That's not quite right. The expected answer was: '{memory_questions[current_question_key]['expected_answer']}'"

            # Clear the state after checking the answer
            context.user_data.clear()  # Clear all user data
            update.message.reply_text(response)
            return

    # If not answering a memory question, handle general queries
    if "?" in user_message:
        answer = get_answer(user_message)

        if answer:
            response = f"Here's what I found: {answer}"
            update.message.reply_text(response)

            # After answering, ask a memory question related to LATOKEN
            if "latoken" in user_message:
                memory_question_key = "why_latoken"
            elif "hackathon" in user_message:
                memory_question_key = "hackathon"
            elif "culture" in user_message:
                memory_question_key = "culture"
            else:
                response = "I'm not sure how that relates to LATOKEN. Can you ask something else?"
                update.message.reply_text(response)
                return

            # Ask the memory question
            update.message.reply_text(memory_questions[memory_question_key]['question'])

            # Set state to waiting for answer and store current question key
            context.user_data['waiting_for_answer'] = True
            context.user_data['current_memory_question'] = memory_question_key
        else:
            response = "I'm not sure about that. Can you provide more details?"
            update.message.reply_text(response)


def main():
    # Set up the bot with token and handlers...
    updater = Updater("7992584492:AAHtpam1xIi3qOPUNKTZhDIs8cKrURTETGI")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()