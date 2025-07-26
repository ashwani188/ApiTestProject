import pytest
from setup import init_browser

@pytest.mark.usefixtures("init_browser")
class TestBase:
    pass


class TestChild(TestBase):

    @pytest.mark.parametrize(
        "url,title",
        [
            ("https://www.google.com", "Google"),
            ("https://www.bing.com", "Search - Microsoft Bing")
        ]
    )
    def test_login(self,url,title):
        self.driver.get(url)
        assert self.driver.title == title

