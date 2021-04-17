from bs4.element import Tag
import requests
from bs4 import BeautifulSoup
from scanner import NewsScannerInterface, Change


class ABCScanner(NewsScannerInterface):
    url = "https://www.abc.net.au/"
    org = 'abc'
    get_url = None

    def __init__(self, **kwargs):
        # This way get_url is mockable.
        if kwargs.get('get_url'):
            self.get_url = kwargs.pop('get_url')
        else:
            self.get_url = requests.get
        super().__init__(**kwargs)

    def get_content(self) -> dict[str, str]:
        """Get a mapping of links to headlines."""
        resp = self.get_url(self.url)
        soup = BeautifulSoup(resp.text, features='html.parser')
        # all headlines have this class on them.
        elements = [x for x in soup.select("._7fOxm")]
        headlines: list[str]
        links: list[str]
        links = [x.find_parent('a')['href'] for x in elements]
        headlines = [x.text for x in elements]
        return {
            link: headline for link, headline in zip(links, headlines)
        }

    def detect_changes(self) -> list[Change]:
        content_now = self.get_content()
        last_content = self.get_last_content() or {}
        assert isinstance(last_content, dict)
        now_link_set = set(content_now.keys())
        last_link_set = set(last_content.keys())
        new_links = now_link_set - last_link_set
        removed_links = last_link_set - now_link_set
        same_links = last_link_set.intersection(now_link_set)
        added = [
            Change("+", content_now[link]) for link in new_links
        ]
        removed = [
            Change("-", last_content[link]) for link in removed_links
        ]
        updated = [
            Change("~", f"Was: {last_content[link]}\nNow:{content_now[link]}") for link in same_links
            if last_content[link] != content_now[link]
        ]
        if any([added, removed, updated]):
            self.save_content(content_now)
        return added + removed + updated
