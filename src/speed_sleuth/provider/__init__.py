# coding: utf-8
# Disable broad-except for now, will refine later.
# pylint: disable=broad-except
"""Generic Provider class which provides an abstraction for the different
drivers we would like to use."""

import sys
from abc import ABC, abstractmethod

from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from speed_sleuth.browser import BrowserInterface


class Provider(ABC):
    """Each driver will be derive from this Abstract provider class.

    This class also contains generic methods which needs to be
    implemented in the concrete provider classes.

    """

    def __init__(self, browser: BrowserInterface):
        try:
            self.driver = browser.load_driver()
        except Exception as e:
            print("browser.load_driver() exception: ", e)

    def wait_to_be_visible(
        self, element: WebElement, timeout: int = 90
    ) -> bool:
        """Waits for the given element to become visible and interactable on
        the page.

        Args:
            element: The WebElement object representing the
                element to wait for.
            timeout: Maximum time to wait for the element to
                become visible, in seconds. Defaults to 90.

        Returns:
            bool: True if the element becomes visible within the specified
                timeout, False otherwise.
        """
        errors = [NoSuchElementException, ElementNotInteractableException]
        try:
            wait = WebDriverWait(
                self.driver,
                timeout=timeout,
                poll_frequency=0.2,
                ignored_exceptions=errors,
            )

            res = wait.until(lambda d: element.is_displayed() or False)
            print(f"res: {res}")
            return True
        except TimeoutException as e:
            print("wait_for_clickable timed out waiting: ", e)
            return False
        except Exception as e:
            print("wait_for_clickable expection occurred: ", e)
            return False

    def wait_for_element(
        self, locator: tuple[str, str], timeout: int = 120
    ) -> WebElement:
        """Wait for an element to be visible and returns it If not found,
        NoSuchElementException is raised.

        Args:
            locator: A tuple of (By, locator) to find the element.
            timeout: The amount for time to wait for the element pointed
                by the locator to be visible. Default to 120.

        Returns:
            WebElement: The element identified by locator

        Raises:
            NoSuchElementException: raised when no element was found under the
                specified locator.

        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException as e:
            raise NoSuchElementException(
                f"Element {locator} was not visible after {timeout} second"
            ) from e

    def wait_for_button_clickable(
        self, locator: tuple[str, str], timeout: int = 120
    ) -> WebElement:
        """Wait for a button to be visible and clickable If not found,
        NoSuchElementException is raised.

        Args:
            locator: A tuple of (By, locator) to find the element.
            timeout: The amount for time to wait for the element pointed
                by the locator to be visible. Default to 120.

        Returns:
            WebElement: The button identified by locator

        Raises:
            NoSuchElementException: raised when no element was found under the
                specified locator.

        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException as e:
            raise NoSuchElementException(
                f"Element {locator} was not clickable after {timeout} second"
            ) from e

    def cleanup(self, errno=0):
        """Cleanup every reserved resources."""
        if self.driver:
            self.driver.close()
            self.driver.quit()
            self.driver = None

        if errno:
            sys.exit(errno)

    @abstractmethod
    def run(self, filename):
        """Actual method that would trigger the test for the given provider."""
        raise NotImplementedError("Should be implemented in daughter class")

    @abstractmethod
    def parse_results(self):
        """Method that would gather results from the speedtest for the given
        provider."""
        raise NotImplementedError("Should be implemented in daughter class")
