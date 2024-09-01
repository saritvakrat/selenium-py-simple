import ssl
import urllib.request
import chromedriver_autoinstaller
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TipCalculatorTest(unittest.TestCase):

    def setUp(self):
        # Create an unverified SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Apply this context to urllib requests
        https_handler = urllib.request.HTTPSHandler(context=ssl_context)
        opener = urllib.request.build_opener(https_handler)
        urllib.request.install_opener(opener)

        # WebDriver setup
        opt = webdriver.ChromeOptions()
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome(options=opt)

        # Construct the file path to the HTML file
        base_path = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(base_path, 'index.html')  # Directly reference 'index.html'
        constructed_path = f'file://{file_path}'

        print(f"Constructed path: {constructed_path}")
        self.driver.get(constructed_path)

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

    def test_tip_calculation(self):
        # Wait for the element to be present before interacting with it
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "billamt")))

        # Test steps
        bill_amt_input = self.driver.find_element(By.ID, "billamt")
        bill_amt_input.send_keys("100")

        service_qual_select = Select(self.driver.find_element(By.ID, "serviceQual"))
        service_qual_select.select_by_value("0.2")

        people_amt_input = self.driver.find_element(By.ID, "peopleamt")
        people_amt_input.send_keys("4")

        calculate_btn = self.driver.find_element(By.ID, "calculate")
        calculate_btn.click()

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "tip"), "5.00")
        )

        tip_result = self.driver.find_element(By.ID, "tip").text
        self.assertEqual(tip_result, "5.00", f"Expected tip to be $5.00, but got ${tip_result}")

if __name__ == "__main__":
    unittest.main()
