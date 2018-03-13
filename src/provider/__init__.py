# coding: utf-8

import time
import sys
import attr
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
    )
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@attr.s(slots=True)
class Provider(ABC):
    target = attr.ib()

    def __attrs_post_init__(self):
        # As using selenium api > 2.x, this call should block until
        # readyState is hit.
        self.driver_init()
        self.driver.get(self.target)
        self.providers = {}
        self._lookup_table = {}

    def driver_init(self):
        options = webdriver.ChromeOptions()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('--headless')
        options.add_argument('--window-size=1400x900')
        options.add_argument('--disable-gpu')
        options.add_argument('--lang=en_US')
        self.driver = webdriver.Chrome(chrome_options=options)

    def wait_for_clickable(self, element, timeout=90):
        time.sleep(2)  # Hack, when element is clicked, it remains active for a
        # small period on the DOM before beeing staled.
        try:
            WebDriverWait(self.driver,
                          timeout,
                          poll_frequency=2,
                          ignored_exceptions=(StaleElementReferenceException)
                          ).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, element))
            )
        except TimeoutException as ex:
            print("Timeout in finding element {} from DOM, reason: {}"
                  .format(element, str(ex))
                  )
            raise
        except Exception:
            print("Unexpected error occured:", sys.exc_info()[0])
            raise

    def get_provider(self, cls):
        found = []
        if type(cls) is str:
            cls = self._class_from_string(cls)

    def _class_from_string(self, string):
        if type(string) is str:
            try:
                return self._lookup_table[string]
            except KeyError:
                raise KeyError("No such provider found")

    @abstractmethod
    def cleanup(self, errno=0):
        raise "Should be implemented in daughter class"

    @abstractmethod
    def run(self):
        raise "Should be implemented in daughter class"

    @abstractmethod
    def parseResults(self):
        raise "Should be implemented in daughter class"
