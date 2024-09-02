import ssl
import urllib.request
import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.tip_calculator_page import TipCalculatorPage

@pytest.fixture
def driver():
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
    driver = webdriver.Chrome(options=opt)

    yield driver

    # Close the browser after the test is done
    driver.quit()

def test_tip_calculation(driver):
    # Initialize the page object
    tip_calculator_page = TipCalculatorPage(driver)

    # Load the tip calculator page
    tip_calculator_page.load()

    # Wait for the bill amount input to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "billamt")))

    # Interact with the page
    tip_calculator_page.enter_bill_amount("100")
    tip_calculator_page.select_service_quality("0.2")
    tip_calculator_page.enter_people_amount("4")
    tip_calculator_page.click_calculate()

    # Verify the tip result
    tip_result = tip_calculator_page.get_tip_result()
    assert tip_result == "5.00", f"Expected tip to be $5.00, but got ${tip_result}"

if __name__ == "__main__":
    pytest.main()
