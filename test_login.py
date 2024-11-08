import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import get_driver

def get_last_registered_user():
    """Function to read the last registered user's data from users.json."""
    try:
        with open('users.json') as file:
            users = json.load(file)["users"]
            return users[-1]  
    except FileNotFoundError:
        print("Error: The 'users.json' file was not found.")
        return None
    except KeyError:
        print("Error: Incorrect JSON structure.")
        return None
    except json.JSONDecodeError:
        print("Error: JSON file is not properly formatted.")
        return None

def test_login(driver=None,close=False):
    
    user = get_last_registered_user()
    if not user:
        print("No user data available for login.")
        return
    if driver is None: 

        driver = get_driver()
    driver.get("https://www.xampro.org/login")

    try:
        
        wait = WebDriverWait(driver, 10)
        
       
        wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(user["email"])
        driver.find_element(By.ID, "password").send_keys(user["password"])
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div/div/div[1]/form/div[4]/div/button').click()

        
        if wait.until(EC.url_contains("/dashboard")):
            print(f"Login successful for user: {user['email']}")
            if close: driver.quit()
            return True
        
        raise Exception(f"Login failed for user: {user['email']}")
    

    except Exception as e:
        print(f"An error occurred during login: {e}")

        if close: driver.quit()
        
        return False
    

if __name__ == "__main__":

    
    test_login(True)
