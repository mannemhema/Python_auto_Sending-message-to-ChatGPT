from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from LoginHandle import LoginHandle

# Start a webdriver instance and open ChatGPT
options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
driver.get('https://chat.openai.com')

login_handle = LoginHandle(driver)
login_handle.login()

try:
    print("Question:")
    input_String = input()
    i = 0
    while input_String != "exit":
        prompt_textarea = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "prompt-textarea")))
        input_textarea = driver.find_element(By.ID, "prompt-textarea").send_keys(input_String)
        prompt_textarea.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'(//div[contains(@class, \'markdown\')])[{i+1}]')))
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.result-streaming')))

        outer_response = driver.find_elements(By.CLASS_NAME, "markdown")

        # Get children of outer_responset
        children = outer_response[i].find_elements(By.XPATH, '*')
        # Itertae over the children
        for child in children:
            print("\n")
            print("Answer:")
            print(child.get_attribute('innerHTML'))
        i += 1
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("\n")
        print("Question:")
        input_String = input()
except TimeoutError:
    print("Network error")

# delete before exit
WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='p-1 hover:text-white'][2]"))).click()
WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete')]"))).click()

driver.quit()
