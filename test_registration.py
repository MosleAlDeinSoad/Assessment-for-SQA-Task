import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import get_driver

def test_registration():
    driver = get_driver()
    driver.get("https://www.xampro.org/signup")

    # Load user data from JSON
    try:
        with open('users.json') as file:
            users = json.load(file)["users"]
    except FileNotFoundError:
        print("Error: The 'users.json' file was not found.")
        return

    try:
        for user in users:
            wait = WebDriverWait(driver, 10)

            # Fill in the registration form
            wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys(user["first_name"] + " " + user["last_name"])
            driver.find_element(By.ID, "email").send_keys(user["email"])
            driver.find_element(By.ID, "password").send_keys(user["password"])
            driver.find_element(By.ID, "confirmPassword").send_keys(user["password"])
            driver.find_element(By.ID, "phoneNumber").send_keys(user["phone"])

            
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div[3]/div/div[2]/form/div[6]/div/button').click()

            
            if wait.until(EC.url_contains("/check-email")):
                print(f"Registration successful for user: {user['email']}")
            else:
                print(f"Registration failed for user: {user['email']}")

    except Exception as e:
        print(f"An error occurred during registration: {e}")

    finally:
        driver.quit()

# Run the test
test_registration()
#UKndvTXVaVmvV8P