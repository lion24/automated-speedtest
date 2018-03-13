# coding: utf-8
import sys, attr
from provider import Provider

@attr.s
class Speedtest(Provider):
    """ Speedtest.net class handler"""
    target = attr.ib(init=False, default="http://beta.speedtest.net")

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def run(self):
        try:
            gobtn = self.driver.find_element_by_css_selector('a.js-start-test')
            gobtn.click()
            print("[+] running speedtest.net, please wait")
            # Block until Go btn is available again
            self.wait_for_clickable('a.js-start-test')
            print("[+] done, taking snapshot of the website results")
            self.driver.get_screenshot_as_file('speedtest-results.png')
        except Exception:
            print("An error occured, cleaning up...")
            self.cleanup(-1)

        self.cleanup()

    def cleanup(self, errno=0):
        self.driver.close()
        self.driver.quit()
        if errno:
            sys.exit(errno)

    def parseResults(self):
        pass
