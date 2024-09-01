from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class TipCalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        # Construct the correct file path to the HTML file
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, 'index.html')  # Navigate to the index.html file
        self.url = f'file://{file_path}'  # Use the file:// protocol


        self.bill_amount_input_locator = (By.ID, "billamt")
        self.service_quality_select_locator = (By.ID, "serviceQual")
        self.people_amount_input_locator = (By.ID, "peopleamt")
        self.calculate_button_locator = (By.ID, "calculate")
        self.tip_result_locator = (By.ID, "tip")

    def load(self):
        self.driver.get(self.url)

    def enter_bill_amount(self, amount):
        bill_amt_input = self.driver.find_element(*self.bill_amount_input_locator)
        bill_amt_input.send_keys(amount)

    def select_service_quality(self, quality_value):
        service_qual_select = Select(self.driver.find_element(*self.service_quality_select_locator))
        service_qual_select.select_by_value(quality_value)

    def enter_people_amount(self, amount):
        people_amt_input = self.driver.find_element(*self.people_amount_input_locator)
        people_amt_input.send_keys(amount)

    def click_calculate(self):
        calculate_btn = self.driver.find_element(*self.calculate_button_locator)
        calculate_btn.click()

    def get_tip_result(self):
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(self.tip_result_locator, "5.00")
        )
        return self.driver.find_element(*self.tip_result_locator).text
