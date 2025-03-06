import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def before_all(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    context.driver.maximize_window()
    time.sleep(3)
    context.driver.find_element(By.XPATH, "//input[@name='username']").send_keys("Admin")
    context.driver.find_element(By.XPATH, "//input[@name='password']").send_keys("admin123")
    context.driver.find_element(By.CSS_SELECTOR, ".orangehrm-login-button").click()
    time.sleep(5)
    print(context.driver.current_url)
    assert "dashboard" in context.driver.current_url, "Login Failed"

def after_all(context):
    context.driver.quit()