import unittest
from selenium import webdriver
from selenium.webdriver import ChromeOptions


class ApplicationSetup(unittest.TestCase):
    def setUp(self):
        opts = ChromeOptions()
        opts.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(chrome_options=opts)

    def tearDown(self):
        print('...........')
        # self.driver.close()
