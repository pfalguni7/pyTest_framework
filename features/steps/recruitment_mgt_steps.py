import os.path
import time

import pyautogui
from behave import given, when, then
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from functions.functions_lib_bdd_framework_recruit_mgt import select_dropdown_option

#Background steps
@given('I am on the OrangeHRM login page')
def step_orangehrm_login_page(context): #context is mandatory  - same like Self in class
    # context.driver = webdriver.Chrome()
    # context.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    # context.driver.maximize_window()
    # time.sleep(3)
    pass

@when('I enter valid credentials "{username}" and "{password}"')
def step_enter_cred(context,username, password): # using context we can access anything within this file
    # context.driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    # context.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    pass

@when('I click on the login button')
def step_click_login_btn(context):
    # context.driver.find_element(By.CSS_SELECTOR,".orangehrm-login-button").click()
    # time.sleep(5)
    pass

@then('I should be redirected to the OrangeHRM dashboard')
def step_verify_dashboard(context):
    # print(context.driver.current_url)
    # assert "dashboard" in context.driver.current_url, "Login Failed"
    pass

@then('I navigate to the "Recruitment" tab')
def step_click_recruitment_tab(context):
    context.driver.find_element(By.CSS_SELECTOR,"ul.oxd-main-menu li:nth-child(5)").click()
    time.sleep(3)

# Scenario Step
# Scenario 1: Add a New Candidate
@given('I click on the "Candidates" section')
def step_click_candidate_section(context):
    context.driver.find_element(By.XPATH,"//a[text()='Candidates']").click()
    time.sleep(2)

    # Assert Page header_name: Candidates
    page_header = context.driver.find_element(By.TAG_NAME, "h5")
    print(f"Page header: {page_header.text}")
    assert "Candidates" in page_header.text, "Invalid page header"

@when('I click on the "Add" button')
def step_click_add_button(context):
    context.driver.find_element(By.CSS_SELECTOR,"div.orangehrm-header-container button.oxd-button.oxd-button--medium.oxd-button--secondary").click()
    time.sleep(2)
#I enter the candidate's first name "John"
@when("I enter the candidate\'s first name {f_name}")
def step_candidate_fname(context,f_name):
    context.driver.find_element(By.CSS_SELECTOR,"input[name='firstName']").send_keys(f_name)

@when("I enter the candidate's last name {l_name}")
def step_candidate_lname(context,l_name):
    context.driver.find_element(By.NAME,"lastName").send_keys(l_name)

@when("I enter the candidate's email {email_id}")
def step_candidate_email(context, email_id):
    context.driver.find_element(By.XPATH,"(//input[@placeholder='Type here'])[1]").send_keys(email_id)

@when('I select a job vacancy "{job_vacancy}"')
def step_select_job_vacancy(context,job_vacancy ):
    '''Step to select job vacancy from dropdown using generic function
    :param context: Behave context object
    :param job_vacancy: "Software engineer" to select (passed from feature file)
    '''
    # define locators from dropdown & its options
    dropdown_locator = (By.XPATH,"//div[@class='oxd-select-text oxd-select-text--active']")
    options_locator = (By.XPATH,"//div[@class='oxd-select-dropdown --positon-bottom']/div")
    select_dropdown_option(context.driver,dropdown_locator, options_locator,job_vacancy)
    time.sleep(4)
    print('Dropdown option "Software Engineer" selected successfully')

    # verify that correct value is selected
    selected_value = context.driver.find_element(*dropdown_locator).text
    assert selected_value == job_vacancy, f"Dropdown selection failed. Expected: '{job_vacancy}', Found: '{selected_value}'"

    print(f'Dropdown option "{job_vacancy}" selected successfully and verified.')
    time.sleep(4)
    context.driver.save_screenshot("dropdown_debug.png")

@when('I upload the candidate\'s resume from "{file_path}"')
def step_upload_candidate_resume(context, file_path): # file_path from feature file
    absolute_path = os.path.expanduser(file_path)

    # Verify if file exist
    assert os.path.exists(absolute_path), f"File not found: {absolute_path}"

    # try with action class & pyautogui
    #pdf_file_path = r"C:\\path\\to\\your\\cv.pdf"

    # Locate file input element and upload file
    file_input = context.driver.find_element(By.XPATH,"//div/input[@type='file']")
    file_input.send_keys(absolute_path)
    print(f"Uploaded resume from: {absolute_path}")

    #verify file path
    print(f"Resolved absolute path: {absolute_path}")
    print(f"File exists: {os.path.exists(absolute_path)}")  # Should return True if the file exists
    context.driver.save_screenshot("upload_error.png")
    time.sleep(4)

@when('I click on the "Save" button')
def step_click_save(context):
    context.driver.find_element(By.CSS_SELECTOR,"button.oxd-button.oxd-button--medium.oxd-button--secondary.orangehrm-left-space").click()
    time.sleep(5)

@then('I should see candidate\'s name {full_name} displayed on the redirected page')
def step_verify_record(context, full_name):
    try:
        time.sleep(3)
        # generate dynamic Xpath for candidate's name
        dynamic_xpath = f"(//div/p[normalize-space(text()='{full_name}')])[1]"

        print(f"Trying to locate candidate name using Xpath: {dynamic_xpath}")
        # Wait for the element containing the candidate's name to appear
        candidate_name = WebDriverWait(context.driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH,dynamic_xpath)))

        # Retrieve and validate the displayed name
        displayed_name = candidate_name.text.strip()
        print(f"Displayed Candidate's Name: {displayed_name}")

        assert full_name == displayed_name, f"Expected name: {full_name}, but found: {displayed_name}"
        time.sleep(4)

    except Exception as e:
        context.driver.save_screenshot("candidate name validation error.png")
        print(f"Current URL: {context.driver.current_url}")
        print(f"Dynamic xpath: {dynamic_xpath}")
        raise e


# Scenario 2: Search for a Candidate
@given('I am on the "Candidates" section')
def step_click_candidate_section(context):
    context.driver.find_element(By.CSS_SELECTOR,"ul li.oxd-topbar-body-nav-tab.--visited").click()
    time.sleep(4)

@when('I enter the candidate\'s name {full_name} in the search field')
def step_search_candidate_name(context, full_name):
    search_field = context.driver.find_element(By.XPATH,"//input[@placeholder='Type for hints...']")
    search_field.click()
    search_field.send_keys(full_name)
    print(f"Enter Candidate's name: {full_name}")
    time.sleep(3)

@when('I click on the "Search" button')
def step_click_search_btn(context):
    context.driver.find_element(By.XPATH,"//button[text()=' Search ']").click()
    time.sleep(3)

@then('I should see {full_name} listed in the search results')
def step_verify_record(context,full_name):
    try:

        # Wait for the candidate's name to appear in the search results table
        search_name = WebDriverWait(context.driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH,"//div[@class='oxd-table-cell oxd-padding-cell'][3]/div[text()='John  Doe']")))
        search_name_text = search_name.text.strip()
        print(f"Candidate name found: {search_name_text}")

        # Validate that the candidate's name matches
        assert full_name in search_name_text, f"Candidate_name not found"

    except Exception as e:
        context.driver.save_screenshot("verify_record_error.png")
        raise e

#Scenario 3: Delete a Candidate from the List
#  Scenario: Delete a candidate from the recruitment list
@when('I select the candidate from the search results')
def step_select_candidate_from_search(context):
    # select the first row of record
    candidate_row = context.driver.find_element(By.XPATH,"(//div[@class='oxd-table-row oxd-table-row--with-border'])[2]")
    time.sleep(3)

    # click on checkbox to select the candidate record
    checkbox = context.driver.find_element(By.XPATH,"(//div[@class='oxd-table-row oxd-table-row--with-border'])[2]/div[1]")
    checkbox.click()

@when('I click on the "Delete" button')
def step_click_delete(context):
    delete_icon = (context.driver.find_element(By.XPATH,"(//div[@class='oxd-table-row oxd-table-row--with-border'])[2]/div[7]/div/button[2]"))
    delete_icon.click()

    # Wait for modal to appear
    try:
        # check if the modal appears
        modal = WebDriverWait(context.driver,10).until(expected_conditions.presence_of_element_located((By.XPATH,"//div[@role='document']//div[@class='orangehrm-modal-header']")))

        assert "Are you Sure?" in modal.text, f"Modal does not appear"
    except TimeoutException:
        raise AssertionError("Modal did not appear after clicking delete")


@when('I confirm the deletion')
def step_confirm_delete(context):

    # Click on Delete button in modal
    del_btn = context.driver.find_element(By.XPATH,
                                          "//button[@class='oxd-button oxd-button--medium oxd-button--label-danger orangehrm-button-margin']")
    del_btn.click()
    time.sleep(3)


@then('I should see the table updated without Candidate {full_name}')
def step_table_update_after_deletion(context, full_name):
    # Find all rows in table
    table_rows = context.driver.find_elements(By.XPATH,"//div[@class='oxd-table-row oxd-table-row--with-border']")

    # Check if candidate's name is present in any row.
    for row in table_rows:
        assert full_name not in row.text, f"Candidate '{full_name}' is still present"

    # To validate deletion of that record, compare the delete count before & after.
    # Get record count before deletion
    # record_count_before = len(context.driver.find_elements(By.XPATH, "(//span[@class='oxd-text oxd-text--span'])[1]"))
    #
    # # confirm deletion
    # step_confirm_delete(context)
    #
    # # Get record count after deletion
    # record_count_after = len(context.driver.find_elements(By.XPATH, "(//span[@class='oxd-text oxd-text--span'])[1])"))
    #
    # # compare the number of records found
    # assert record_count_after == record_count_before - 1, f"Record count did not updated as per expected. Before {record_count_before}, After: {record_count_after}"

# Scenario 4: Validate Empty Candidate Submission
@given('I click on the "Candidates" section')
def step_click_candidate_section(context):
    step_click_candidate_section(context)

@when('I click on the "Add" button')
def step_click_add_btn(context)