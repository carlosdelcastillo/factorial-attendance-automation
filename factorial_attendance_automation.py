import os
import time
import sys
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()

# Credentials
FACTORIAL_EMAIL = os.getenv("FACTORIAL_EMAIL")
FACTORIAL_PASSWORD = os.getenv("FACTORIAL_PASSWORD")

# Browser visibility
SHOW_BROWSER = os.getenv("SHOW_BROWSER", "false").lower() == "true"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

# URLs
LOGIN_URL = "https://api.factorialhr.com/en/users/sign_in?&return_to=https%3A%2F%2Fapp.factorialhr.com%2Fdashboard"

# Selectors
EMAIL_INPUT = (By.XPATH, '//*[@id="user_email"]')
PASSWORD_INPUT = (By.XPATH, '//*[@id="user_password"]')
LOGIN_SUBMIT_BUTTON = (By.XPATH, '//*[@id="new_user"]/input[4]')
TIMESHEET_BUTTON = (By.LINK_TEXT, "Mi control horario")
FILL_HOURS_BUTTON = (
    By.XPATH,
    "//button[.//text()[contains(., 'Rellenar automáticamente las hojas de fichajes')]]",
)
AUTOFILL_POPUP_BUTTON = (
    By.XPATH,
    "//button[span[normalize-space(text())='Rellenar automáticamente']]",
)
PREVIOUS_MONTH_ARROW = (
    By.XPATH,
    '//*[@id="content"]/div/div[2]/div/section/div/div/div[2]/div[2]/div/div/div[1]',
)
NEXT_MONTH_ARROW = (By.CSS_SELECTOR, '[data-testid="arrow-right-icon"]')


def login(driver: webdriver.Chrome):
    """
    Navigates to the Factorial login page and logs in the user.

    Args:
        driver: The Selenium WebDriver instance.
    """
    logging.info(f"🌐 Navigating to login page: {LOGIN_URL}")
    driver.get(LOGIN_URL)

    logging.info("🔑 Entering credentials...")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(EMAIL_INPUT)
        ).send_keys(FACTORIAL_EMAIL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(PASSWORD_INPUT)
        ).send_keys(FACTORIAL_PASSWORD)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(LOGIN_SUBMIT_BUTTON)
        ).click()
        logging.info("📝 Login form submitted. Waiting for dashboard to load...")
        # It's better to wait for a specific element on the dashboard
        # but for now, a sleep will do.
        time.sleep(5)
    except TimeoutException:
        logging.error("❌ Timed out waiting for login elements. Check your selectors or network.")
        raise
    except Exception as e:
        logging.error(f"❌ An unexpected error occurred during login: {e}")
        raise


def fill_attendance_for_current_month(driver: webdriver.Chrome):
    """
    Navigates to the timesheet page and triggers the autofill for the current month.

    Args:
        driver: The Selenium WebDriver instance.
    """
    try:
        logging.info("⏳ Waiting for sidebar menu to load...")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(TIMESHEET_BUTTON))
        logging.info("🖱️ Clicking on timesheet button...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(TIMESHEET_BUTTON)
        ).click()
        logging.info("✅ Timesheet page loaded.")

        logging.info("⏳ Waiting for fill hours button to load...")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(FILL_HOURS_BUTTON))
        logging.info("🖱️ Clicking on fill hours button...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(FILL_HOURS_BUTTON)
        ).click()

        logging.info("⏳ Waiting for fill popup hours button to load...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(AUTOFILL_POPUP_BUTTON)
        )
        logging.info("🖱️ Clicking on fill hours popup button...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(AUTOFILL_POPUP_BUTTON)
        ).click()

        time.sleep(2)  # Allow animations/data loading
        logging.info("✅ Attendance autofill triggered successfully.")
    except TimeoutException:
        logging.error("❌ Timed out waiting for timesheet elements. The UI might have changed.")
        raise
    except Exception as e:
        logging.error(f"❌ An unexpected error occurred during attendance filling: {e}")
        raise


def main():
    """
    Main function to run the Factorial attendance automation bot.
    """
    if not FACTORIAL_EMAIL or not FACTORIAL_PASSWORD:
        logging.error(
            "❌ Error: FACTORIAL_EMAIL and FACTORIAL_PASSWORD must be set in the .env file."
        )
        sys.exit(1)

    driver = None
    try:
        logging.info("🚀 Initializing WebDriver...")
        chrome_options = webdriver.ChromeOptions()
        if not SHOW_BROWSER:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--window-size=1920,1080")
        else:
            chrome_options.add_argument("--start-maximized")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(5)

        login(driver)
        fill_attendance_for_current_month(driver)

        logging.info("🎉 Automation complete!")

    except Exception as e:
        logging.error(f"❌ An error occurred during automation: {e}")
    finally:
        if driver:
            logging.info("👋 Closing the browser...")
            driver.quit()


# --- Main Automation Script ---
if __name__ == "__main__":
    main()
