from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, tinydb
from db import helpers
from handlers import leaderboard

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:5005/loginscreen")
    time.sleep(2)
    
    #be on test user U:test PW:test
    print("--= Beginning Duck Code Tests =--")


    #logged in to right user:
    login_username = driver.find_element(By.CSS_SELECTOR, "input[name = 'username']")
    login_username.send_keys('test')

    login_pw= driver.find_element(By.CSS_SELECTOR, "input[name = 'password']")
    login_pw.send_keys('test')
   
    submit = driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
    submit.click()
    time.sleep(2)
    if(driver.current_url == "http://localhost:5005/"):
        print("[PASSED] - Logged in.")
    else:
        print("[Failed] - Log in failed")
    user= driver.find_element(By.CSS_SELECTOR, "h1[id='welcome']").text
    if user == 'Welcome, test!':
        print("[PASSED] - Correct user.")
    else:
        print("[FAILED] - Incorrect user. Username was: ", str(user))



    #access data for checks
    leaders = leaderboard.get_leaderboard()
    db = helpers.load_db()
    users = db.table('users')
    User = tinydb.Query()
    user = users.get(User.username == 'test')
    #ensure that previous entries don't affect entering score
    if 'Duck1' in user['ducks']:
        user['ducks'].remove('Duck1')
        user['points'] -= 100
        print("--- Removed Duck1 from test user ----")
        User = tinydb.Query()
        users.update({'ducks': user['ducks'], 'points': user['points']}, User.username == 'test')

    #check leaderboard exists and displays correct data
    leader = driver.find_element(By.CSS_SELECTOR, "div.leaders.no1 h4").text
    if(leader != ''):
        print("[PASSED] - Leaderboard exists.")
    else:
        print("[FAILED] - No leaderboard data found.")
    top_score = driver.find_element(By.CSS_SELECTOR, "div.leaders.no1 h4[class='score']").text
    if(top_score != ''):
        print("[PASSED] - Scores display.")
    else:
        print("[FAILED] - No scores found.")
    
    if(leader == leaders[0]['name']):
        print("[PASSED] - Correct user in #1 spot.")
    else:
        print("[FAILED] - Incorrect user in #1 spot.")
    if(int(top_score) == leaders[0]['score']):
        print("[PASSED] - Correct score in #1 spot.")
    else:
        print("[FAILED] - Incorrect score in #1 spot.")
        print(top_score)
        print(leaders[0]['score'])


   

except Exception as e:
    print("Error:", e)


try:
     #enter a code
    enter_code = driver.find_element(By.CSS_SELECTOR, "textarea[name = 'code']")
    print("[PASSED] - Enter code element exists.")
    enter_code.send_keys('12345')
    user = users.get(User.username == 'test')
    old_score = user['points']
    enter = driver.find_element(By.CSS_SELECTOR, "button[id='enter']")
    enter.click()
    time.sleep(2)
    user = users.get(User.username == 'test')
    new_score = user['points']
    if(new_score == old_score + 100):
        print('[PASSED] - User score updated correctly.')
    else:
        print('[FAILED] - User score updated incorrectly.')
    if('Duck1' in user['ducks']):
        print('[PASSED] - Duck was added to test user.')
    else:
        print('[FAILED] - Duck failed to add to test user.')


    #same process but without deleting duck to ensure more points don't get added
    enter_code = driver.find_element(By.CSS_SELECTOR, "textarea[name = 'code']")
    enter_code.send_keys('12345')
    user = users.get(User.username == 'test')
    old_score = user['points']
    enter = driver.find_element(By.CSS_SELECTOR, "button[id='enter']")
    enter.click()
    time.sleep(2)
    user = users.get(User.username == 'test')
    new_score = user['points']
    if(new_score == old_score):
        print('[PASSED] - User score did not add if duck was already found.')
    else:
        print('[FAILED] - User score added score even if the duck was found prior.')
except NoSuchElementException:
    print('[FAILED] - Enter code is missing 1 or more elements')

finally:
    print("--= Ending Tests =--")
    driver.quit()
