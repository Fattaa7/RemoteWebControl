from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service =  Service(executable_path=r"C:\Users\ahmed\Desktop\Plyaer\pyt\geckodriver.exe")

driver = webdriver.Firefox(service=service)
#driver.get('https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F/')
driver.get('http://52.54.176.49:8080/')
    
#/html/body/div/div/div/div[3]/svg[2]

driver.implicitly_wait(6)

driver.find_element(By.CLASS_NAME, "btn_action_pp").click()


# driver.find_element(By.ID, 'login-username').send_keys("ahmed1999fattah@gmail.com")
# driver.find_element(By.ID, 'login-password').send_keys("onepiece12")

# driver.find_element(By.ID, 'login-button').click()

# elem = WebDriverWait(driver, 30).until(
# EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]/div")) #This is a dummy element
# )
# driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/nav/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]/ul/div/div[2]/li[1]/div").click()



# elem = WebDriverWait(driver, 30).until(
# EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button/span")) #This is a dummy element
# )
# driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button/span").click()


