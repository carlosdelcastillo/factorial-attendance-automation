"""Automate Factorial timesheet autofill via Selenium.

Loads credentials from environment variables, logs into Factorial, and triggers
the automatic attendance fill for the current month. Designed to run headless
by default while providing structured logging for observability.
"""

import os
import sys
import logging
import time
from typing import Optional
from dataclasses import dataclass
from functools import wraps
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables from .env file
load_dotenv()

# Configure structured logging with emoji support
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Application configuration."""

    email: str
    password: str
    show_browser: bool
    login_url: str = (
        "https://api.factorialhr.com/en/users/sign_in"
        "?&return_to=https%3A%2F%2Fapp.factorialhr.com%2Fdashboard"
    )

    # Timeouts (in seconds)
    default_timeout: int = 10
    long_timeout: int = 15
    animation_wait: float = 2.0

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        email = os.getenv("FACTORIAL_EMAIL")
        password = os.getenv("FACTORIAL_PASSWORD")

        if not email or not password:
            raise ValueError(
                "FACTORIAL_EMAIL and FACTORIAL_PASSWORD must be set in .env file"
            )

        show_browser = os.getenv("SHOW_BROWSER", "false").lower() == "true"
        return cls(email=email, password=password, show_browser=show_browser)


@dataclass
class Selectors:
    """UI element selectors."""

    email_input: tuple = (By.ID, "user_email")
    password_input: tuple = (By.ID, "user_password")
    login_submit: tuple = (By.XPATH, '//*[@id="new_user"]/input[4]')
    timesheet_button: tuple = (By.LINK_TEXT, "Mi control horario")
    fill_hours_button: tuple = (
        By.XPATH,
        (
            "//button[contains(.//text(), "
            "'Rellenar automáticamente las hojas de fichajes')]"
        ),
    )
    autofill_popup_button: tuple = (
        By.XPATH,
        "//button[span[normalize-space()='Rellenar automáticamente']]",
    )
    previous_month_arrow: tuple = (By.CSS_SELECTOR, '[data-testid="arrow-left-icon"]')
    next_month_arrow: tuple = (By.CSS_SELECTOR, '[data-testid="arrow-right-icon"]')


def retry_on_failure(max_retries: int = 3, backoff_factor: float = 1.0):
    """Decorator to retry a function on failure with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (TimeoutException, NoSuchElementException) as e:
                    if attempt == max_retries:
                        logger.error(
                            "❌ Failed after %d attempts in %s: %s",
                            max_retries,
                            func.__name__,
                            e
                        )
                        raise
                    wait_time = backoff_factor * (2 ** (attempt - 1))
                    logger.warning(
                        "⏳ Attempt %d/%d failed in %s. Retrying in %.1fs...",
                        attempt,
                        max_retries,
                        func.__name__,
                        wait_time
                    )
                    time.sleep(wait_time)
        return wrapper
    return decorator


class FactorialAutomationBot:
    """Main bot for Factorial attendance automation."""

    def __init__(self, config: Config, selectors: Optional[Selectors] = None):
        """
        Initialize the automation bot.

        Args:
            config: Application configuration
            selectors: UI element selectors (uses defaults if None)
        """
        self.config = config
        self.selectors = selectors or Selectors()
        self.driver: Optional[webdriver.Chrome] = None

    def _initialize_driver(self) -> webdriver.Chrome:
        """
        Initialize and configure the Chrome WebDriver.

        Returns:
            Configured webdriver.Chrome instance
        """
        logger.info("🚀 Initializing WebDriver...")

        chrome_options = ChromeOptions()

        if not self.config.show_browser:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--window-size=1920,1080")
            logger.info("🔒 Running in headless mode")
        else:
            chrome_options.add_argument("--start-maximized")
            logger.info("👁️  Running in visible mode")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(self.config.default_timeout)

        logger.info("✅ WebDriver initialized successfully")
        return driver

    @retry_on_failure(max_retries=2)
    def login(self) -> None:
        """
        Navigate to Factorial and authenticate user.

        Raises:
            TimeoutException: If login elements are not found
            ValueError: If credentials are missing
        """
        logger.info("🌐 Navigating to login page: %s", self.config.login_url)
        self.driver.get(self.config.login_url)

        try:
            logger.debug("⏳ Waiting for email input field...")
            email_element = WebDriverWait(
                self.driver, self.config.default_timeout
            ).until(EC.presence_of_element_located(self.selectors.email_input))
            email_element.send_keys(self.config.email)
            logger.debug("✉️  Email entered")

            logger.debug("⏳ Waiting for password input field...")
            password_element = WebDriverWait(
                self.driver, self.config.default_timeout
            ).until(EC.presence_of_element_located(self.selectors.password_input))
            password_element.send_keys(self.config.password)
            logger.debug("🔑 Password entered")

            logger.debug("⏳ Waiting for login submit button...")
            submit_button = WebDriverWait(
                self.driver, self.config.default_timeout
            ).until(EC.element_to_be_clickable(self.selectors.login_submit))
            submit_button.click()
            logger.info("📝 Login form submitted")

            logger.debug("⏳ Waiting for dashboard to load...")
            WebDriverWait(
                self.driver, self.config.long_timeout
            ).until(EC.presence_of_element_located(self.selectors.timesheet_button))
            logger.info("✅ Dashboard loaded successfully")

        except TimeoutException:
            logger.error(
                "❌ Timeout waiting for login elements. "
                "Check selectors or network connectivity."
            )
            raise
        except NoSuchElementException as e:
            logger.error("❌ Element not found during login: %s", e)
            raise
        except WebDriverException as e:
            logger.error("❌ WebDriver error during login: %s", e)
            raise

    @retry_on_failure(max_retries=2)
    def fill_attendance_for_current_month(self) -> None:
        """
        Navigate to timesheet and trigger autofill for current month.

        Raises:
            TimeoutException: If timesheet elements are not found
        """
        try:
            logger.info("📄 Navigating to timesheet page...")
            timesheet_button = WebDriverWait(
                self.driver, self.config.long_timeout
            ).until(EC.element_to_be_clickable(self.selectors.timesheet_button))
            timesheet_button.click()
            logger.info("✅ Timesheet page loaded")

            logger.info("🔍 Looking for autofill button...")
            fill_button = WebDriverWait(
                self.driver, self.config.long_timeout
            ).until(EC.element_to_be_clickable(self.selectors.fill_hours_button))
            fill_button.click()
            logger.info("💬 Autofill dialog opened")

            logger.info("✏️  Confirming autofill action...")
            confirm_button = WebDriverWait(
                self.driver, self.config.default_timeout
            ).until(EC.element_to_be_clickable(self.selectors.autofill_popup_button))
            confirm_button.click()
            logger.info("✅ Autofill triggered successfully")

            time.sleep(self.config.animation_wait)

        except TimeoutException:
            logger.error("❌ Timeout waiting for timesheet elements. UI may have changed.")
            raise
        except NoSuchElementException as e:
            logger.error("❌ Element not found during attendance filling: %s", e)
            raise
        except WebDriverException as e:
            logger.error("❌ WebDriver error during attendance filling: %s", e)
            raise

    def run(self) -> None:
        """
        Execute the complete automation workflow.
        """
        try:
            self.driver = self._initialize_driver()
            self.login()
            self.fill_attendance_for_current_month()
            logger.info("🎉 Automation completed successfully")

        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            logger.error("❌ Automation failed: %s", e)
            sys.exit(1)
        except Exception as e:
            logger.error(
                "❌ Unexpected error in automation: %s: %s",
                type(e).__name__,
                e,
            )
            sys.exit(1)

        finally:
            self._cleanup()

    def _cleanup(self) -> None:
        """Clean up resources."""
        if self.driver:
            logger.info("👋 Closing browser...")
            try:
                self.driver.quit()
            except WebDriverException as e:
                logger.warning("⚠️  Error closing browser: %s", e)


_CLOUDFLARE_BLOCK_MESSAGE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        THIS TOOL IS BROKEN                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Factorial HR has deployed Cloudflare Turnstile bot protection on their     ║
║  login page. Headless browser automation is blocked at the login step and   ║
║  there is no technical workaround available.                                 ║
║                                                                              ║
║  This project is archived. No fix is planned.                                ║
║                                                                              ║
║  Note: only native email/password login was ever supported.                  ║
║  SSO (Google, Microsoft, SAML) was never implemented.                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


def main() -> None:
    """Main entry point for the Factorial automation script."""
    logger.error(_CLOUDFLARE_BLOCK_MESSAGE)
    sys.exit(1)

    try:
        config = Config.from_env()
        bot = FactorialAutomationBot(config)
        bot.run()

    except ValueError as e:
        logger.error("⚙️  Configuration error: %s", e)
        sys.exit(1)
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error("❌ Automation error: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.error(
            "❌ Unexpected error: %s: %s",
            type(e).__name__,
            e,
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
