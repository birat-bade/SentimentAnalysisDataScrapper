import unittest

from src.main.base.ApplicationSetup import ApplicationSetup
from src.pages.EKantipur import EKantipur


class Implementation(ApplicationSetup):
    def test_scrape(self):
        self.driver.get('http://www.ekantipur.com/eng/nepal')
        ek = EKantipur(self.driver)
        ek.scrape()


if __name__ == '__main__':
    unittest.main()
