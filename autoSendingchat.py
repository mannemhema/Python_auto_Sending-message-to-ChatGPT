from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from LoginHandle import LoginHandle

# Start a webdriver instance and open ChatGPT
options = Options()
options.add_argument('--headless=new')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36")
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

        # Get children of outer_response
        children = outer_response[i].find_elements(By.XPATH, '*')
        print("Answer:")
        # Iterate over the children
        for child in children:
            print("\n")
            print(child.get_attribute('innerHTML'))
        i += 1
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("\n")
        print("Question:")
        input_String = input()
    
    # delete before exit
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='p-1 hover:text-white'][2]"))).click()
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete')]"))).click()
except TimeoutError:
    print("Network error")
except TimeoutException:
    print('Possibly there is a captcha, uncomment headless and increase timeout after send_keys RETURN to solve the puzzle manually')

driver.quit()
