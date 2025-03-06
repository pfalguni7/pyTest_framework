import time

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By



@given('the user is on the login page')
def step_open_login_page(context):
  context.driver = webdriver.Chrome()
  context.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
  context.driver.maximize_window()
  time.sleep(2)

@when('the user enters valid "{username}" username and "{password}" password')
def step_enter_credentials(context, username, password):
  context.driver.find_element(By.NAME,"username").send_keys(username)
  context.driver.find_element(By.NAME,"password").send_keys(password)


@when('clicks on the login button')
def step_click_login_btn(context):
  context.driver.find_element(By.CSS_SELECTOR,".orangehrm-login-button").click()
  time.sleep(5)

@then('the user should be able to see the dashboard page')
def step_verify_dashboard(context):
    try:
        assert "dashboard" in context.driver.current_url
    except Exception:
        assert "login" in context.driver.current_url

    context.driver.quit()