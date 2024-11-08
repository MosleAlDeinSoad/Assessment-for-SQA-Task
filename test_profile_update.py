import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from config import get_driver
import time

def load_json(file_path):
    """Load data from a JSON file."""
    try:
        with open(file_path) as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: '{file_path}' file not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: JSON file '{file_path}' is not properly formatted.")
        return None

def update_profile(driver):
    """Update the user profile with provided data."""
    profile_data = load_json('updated_profile.json')
    if not profile_data:
        print("Profile data not found.")
        return
    
    driver.get("https://www.xampro.org/profile")
    wait = WebDriverWait(driver, 10)

    try:
        
        full_name_field = wait.until(EC.presence_of_element_located((By.ID, "fullName")))
        full_name_field.clear()
        full_name_field.send_keys(profile_data["fullName"])

        
        phone_field = driver.find_element(By.ID, "phoneNumber")
        phone_field.clear()
        phone_field.send_keys(profile_data["phoneNumber"])

       
        dob_field = driver.find_element(By.ID, "dob")
        dob_field.clear()
        dob_field.send_keys(profile_data["dob"])

        
        gender_radio = wait.until(EC.element_to_be_clickable((By.ID, f"radio-gender-{profile_data['gender'].lower()}")))
        gender_radio.click()

        
        education_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "education"))))
        education_dropdown.select_by_visible_text(profile_data["education"])

       
        university_input = driver.find_element(By.CSS_SELECTOR, "#react-select-3-input")
        university_input.clear()
        university_input.send_keys(profile_data["university"])
        time.sleep(1)  
        university_input.send_keys(Keys.ENTER)  
        
        if profile_data.get("profilePicture"):
            profile_picture_input = driver.find_element(By.CSS_SELECTOR, ".profile-page-image-upload")
            profile_picture_input.send_keys(profile_data["profilePicture"])

       
        update_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div/div/div/form/div[8]/div/button')))
        
        
        if update_button.is_enabled():
            update_button.click()
            print("Profile updated successfully.")
        else:
            print("Update button is disabled. Please check the form inputs.")

    except Exception as e:
        print(f"An error occurred during profile update: {e}")

def main():
    """Main function to perform login and update profile."""
    driver = get_driver()
    
    try:
       
        from test_login import test_login 
        login_successful = test_login(driver=driver, close=False)  
        
        if login_successful:
            print("Proceeding to update profile...")
            
            
            update_profile(driver)
        else:
            print("Login failed. Profile update aborted.")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
