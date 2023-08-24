from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

COOKIES_FILE_PATH = 'credential/cookies.txt'
CREDENTIAL_FILE_PATH = 'credential/loginForGPT.txt'

class LoginHandle:
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        is_logged_in = self.loginWithCookies()
        if not is_logged_in:
            print('trying to login with username and password')
            self.loginWithUserNamePassword()

    def getUserNamePassword(self):
        credential_Array = []
        with open(CREDENTIAL_FILE_PATH) as f:
            lines = f.readlines()
            for line in lines:
                credential = line.split("\n")[0].split("=")[1]
                credential_Array.append(credential)
        return credential_Array
    
    def loginWithUserNamePassword(self):
        creds = self.getUserNamePassword()
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Log in"]'))).click()
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(creds[0])
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="Continue"]'))).click()
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(creds[1])
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "_button-login-password"))).click()
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), 'Okay, let’s go')]"))).click()
        self.storeCookies()

    def loginWithCookies(self):
        self.loadCookies()
        # Refresh the page to apply the cookies
        self.driver.get('https://chat.openai.com/')
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), 'Okay, let’s go')]"))).click()
            print('login success with cookies')
            return True
        except:
            print('login did not work with cookies')
            return False
    
    def storeCookies(self):
         # Get the cookies from the driver
        cookies = self.driver.get_cookies()
        # Write cookies to the output file
        with open(COOKIES_FILE_PATH, 'w') as f:
            for cookie in cookies:
                f.write(json.dumps(cookie) + "\n")

    def loadCookies(self):
        if not os.path.exists(COOKIES_FILE_PATH):
            return
         # Read cookies from the input file
        with open(COOKIES_FILE_PATH, 'r') as f:
            cookies = f.read().splitlines()
    
         # Add each cookie to the driver's session
        for cookie_str in cookies:
            cookie = json.loads(cookie_str)
            try:
                self.driver.add_cookie(cookie)
            except:
                # ignore cookies that cannot be added
                pass

