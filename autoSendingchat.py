from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Get mail and password from .txt outside
credential_Array = []

with open('credential/loginForGPT.txt') as f:
    lines = f.readlines()
    for line in lines:
        credential = line.split("\n")[0].split("=")[1]
        # print(credential)
        credential_Array.append(credential)

mail = credential_Array[0]
password = credential_Array[1]

# Start a webdriver instance and open ChatGPT
driver = webdriver.Chrome()
driver.get('https://chat.openai.com')
  
try:
    driver.minimize_window()
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Log in"]')))
    
    login_button = driver.find_element(By.XPATH, '//div[text()="Log in"]').click()
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "username")))
    email = driver.find_element(By.ID, "username").send_keys(mail)

    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="Continue"]')))
    continue_button = driver.find_element(By.XPATH, '//button[text()="Continue"]').click()

    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "password")))
    password = driver.find_element(By.ID, "password").send_keys(password)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "_button-login-password")))
    continue_button_next = driver.find_element(By.CLASS_NAME, "_button-login-password").click()

    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Next"]')))
    next_button = driver.find_element(By.XPATH, '//div[text()="Next"]').click()
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Next"]')))
    next_button = driver.find_element(By.XPATH, '//div[text()="Next"]').click()
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Done"]')))
    next_button = driver.find_element(By.XPATH, '//div[text()="Done"]').click()

    print("Question:")
    input_String = input()
    while input_String != "exit":
        prompt_textarea = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "prompt-textarea")))
        input_textarea = driver.find_element(By.ID, "prompt-textarea").send_keys(input_String)
        prompt_textarea.send_keys(Keys.RETURN)

        time.sleep(5)
        outer_response = driver.find_element(By.CLASS_NAME, "markdown")

        # Get children of outer_response
        children = outer_response.find_elements(By.XPATH, '*')
        # Itertae over the children
        for child in children:
            print("\n")
            print("Answer:")
            print(child.get_attribute('innerHTML'))
        input_String = ""
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("\n")
        print("Click 'exit' to close chatting!")
        input_String = input()
except TimeoutError:
    print("Network error")
driver.quit()
