from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def scrape_latoken_info():
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
    for element in elements[5:]:
        print(element.text)

    URL = "https://latoken.me/culture-139"
    driver.get(URL)

    # Locate the element by its class name
    parts = driver.find_elements(By.CLASS_NAME, "UiR3cpYj.zUKiXyE3.EI9jU84Z.R23Ln2cO.kr-span")
    # Loop through the elements and print their text content
    for part in parts:
        print(part.text)

print(scrape_latoken_info())