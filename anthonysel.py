from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from tinydb import TinyDB
from db import users, helpers

options = Options()
#options.add_argument("--headless")  # optional
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Use a temporary user data directory
options.add_argument("--user-data-dir=/tmp/selenium_temp_profile")


driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:5005/loginscreen")
    time.sleep(2)
    
    print("== Starting Test ==")
################## Basic Test #################################
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type = 'submit'][value = 'Login']")
    delete_button = driver.find_element(By.CSS_SELECTOR, "input[type = 'submit'][value = 'Delete']")
    create_button = driver.find_element(By.CSS_SELECTOR, "input[type = 'submit'][value = 'Create']")
    if delete_button:
        print("[PASSED] - Delete Button Exists.")
    else:
        print("[FAILED] - Delete button not found.")
    if login_button:
        print("[PASSED] - Login Button Exists.")
    else:
        print("[FAILED] - Login button not found.")
    if create_button:
        print("[PASSED] - Create Button Exists.")
    else:
        print("[Failed] - Create button not found.")
###############################################################
############## Create, Logout, Delete User Test #########################
    test_name = 'abccc'
    test_pass = 'ISAH84l2nh-33'
    db = helpers.load_db() 
### creates user, sending name and pass
    users.delete_user(db, test_name, str(test_pass))  # ensure user does not exist before creation
    driver.find_element(By.NAME, "username").send_keys(test_name)
    driver.find_element(By.NAME, "password").send_keys(test_pass)
    create_button.click()
    time.sleep(1)
### checks for success message
    if "User" in driver.page_source and "created successfully" in driver.page_source:
        print("[PASSED] - User created successfully")
    else:
        print("[FAILED] - User creation failed, next test will also fail")
###check badges page
    try:
        toggler = driver.find_element(By.CSS_SELECTOR, ".navbar-toggler")
        if toggler.is_displayed():
            toggler.click()
            time.sleep(0.5)  # give animation time to finish
    except:
        pass  # if toggler not found, menu is probably already expanded
    badges_link = driver.find_element(By.CSS_SELECTOR, "[name='badges']")
    badges_link.click()
    time.sleep(1)
    if "Badges" in driver.page_source:
        print("[PASSED] - Badges page loaded successfully")
    else:
        print("[FAILED] - Badges page failed to load")
### check for home link
    try:
        toggler = driver.find_element(By.CSS_SELECTOR, ".navbar-toggler")
        if toggler.is_displayed():
            toggler.click()
            time.sleep(0.5)  # give animation time to finish
    except:
        pass  # if toggler not found, menu is probably already expanded
    home_link = driver.find_element(By.CSS_SELECTOR, "[name='home']")
    home_link.click()
    time.sleep(1)
    if "GeoCaching Ducks" in driver.page_source:
        print("[PASSED] - Home link works successfully")
    else:
        print("[FAILED] - Home link failed to work")
### check for friends link
    try:
        toggler = driver.find_element(By.CSS_SELECTOR, ".navbar-toggler")
        if toggler.is_displayed():
            toggler.click()
            time.sleep(0.5)  # give animation time to finish
    except:
        pass  # if toggler not found, menu is probably already expanded
    friends_link = driver.find_element(By.CSS_SELECTOR, "[name='friends']")
    friends_link.click()
    time.sleep(1)
    if "Friends" in driver.page_source:
        print("[PASSED] - Friends page loaded successfully")
    else:
        print("[FAILED] - Friends page failed to load")
### Home link again
    home_link = driver.find_element(By.CSS_SELECTOR, "[name='home']")
    home_link.click()
    time.sleep(1)
    if "GeoCaching Ducks" in driver.page_source:
        print("[PASSED] - Home link works successfully")
    else:
        print("[FAILED] - Home link failed to work")


### Logout
    time.sleep(1)
    try:
        toggler = driver.find_element(By.CSS_SELECTOR, ".navbar-toggler")
        if toggler.is_displayed():
            toggler.click()
            time.sleep(0.5)  # give animation time to finish
    except:
        pass  # if toggler not found, menu is probably already expanded
    logout_button = driver.find_element(By.NAME, "logout")
    logout_button.click()
### checks for logout message
    time.sleep(1)
    try:
        login_button_after_logout = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
        print("[PASSED] - User logged out successfully")
    except:
        print("[FAILED] - User logout failed")
### deletes user just 
    delete_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Delete']")
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "username").send_keys(test_name)
    driver.find_element(By.NAME, "password").send_keys(test_pass)
    delete_button.click()
    time.sleep(1)
### checks for delete message
    users.delete_user(db, test_name, str(test_pass))  # ensure user does not exist after test
    if "deleted successfully" in driver.page_source:
        print("[PASSED] - User deleted successfully")
    else:
        print("[FAILED] - User deletion failed")
##################################################################

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
