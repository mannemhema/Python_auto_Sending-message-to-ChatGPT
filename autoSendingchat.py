from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

print("Ask anything! I know everything Ha Ha")

input_String = input()
credential_Array = []

with open('credential/loginForGPT.txt') as f:
    lines = f.readlines()
    for line in lines:
        credential = line.split("\n")[0].split("=")[1]
        # print(credential)
        credential_Array.append(credential)

mail = credential_Array[0]
password = credential_Array[1]

# Replace with the path to your ChromeDriver
# Start a webdriver instance and open ChatGPT
driver = webdriver.Chrome()
driver.get('https://chat.openai.com')

# Wait for the page to load
time.sleep(5)       

# Find the input field and send a question
wait = WebDriverWait(driver, 10)
textarea = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-id='root'")))
textarea.send_keys(input_String)

# Press "Enter" to send the message
textarea.send_keys(Keys.RETURN)

# Find the response and save it to a file
response = driver.find_element_by_class_name('markdown').text

# Close the browser after some time (optional)
time.sleep(10)
driver.quit()
