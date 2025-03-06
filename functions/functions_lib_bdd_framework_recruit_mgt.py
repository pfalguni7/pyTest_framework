from selenium.common import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def select_dropdown_option(driver, dropdown_locator, options_locator, value_to_select):
    '''

        :param driver: Chrome Webdriver instance
        :param dropdown_locator: locator for dropdown element
        :param options_locator: locator for dropdown options
        :param value_to_select: Text of option to select
        :return: None
        '''
    try:
        # Click on the dropdown to open options
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(dropdown_locator)).click()

        # Wait for dropdown options to be visible
        options = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located(options_locator)
        )

        # Iterate through options and select the desired one
        for option in options:
            try:
                if option.text == value_to_select:
                    option.click()
                    print(f"Option '{value_to_select}' clicked successfully.")
                    break
            except StaleElementReferenceException:
                print("Option became stale. Retrying....")

                # Re-locate options dynamically if stale
                options = WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_all_elements_located(options_locator)
                )

        # Verify if correct value is selected (optional)
        selected_value = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located(dropdown_locator)
        ).text

        if selected_value == value_to_select:
            print(f"Dropdown selection successful: {selected_value}")
        else:
            print(f"Dropdown selection failed. Expected: {value_to_select}, Found: {selected_value}")

    except Exception as e:
        print(f"Error occurred during dropdown selection: {e}")

