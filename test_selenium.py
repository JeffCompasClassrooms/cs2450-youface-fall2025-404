from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
#options.add_argument("--headless")  # optional
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Use a temporary user data directory
options.add_argument("--user-data-dir=/tmp/selenium_temp_profile")


driver = webdriver.Chrome(options=options)
driver.get("https://isitchristmas.com")


#Find the element with id="answer"
answer = driver.find_element(By.ID, "answer")

print("Page title:", driver.title)
print("Answer text:", answer.text)

driver.quit()


