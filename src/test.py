import os
import hashlib
import unittest
import requests
import sqlalchemy as sa

from abcnews import ABCScanner
from db import ensure_table


class _MockRequest:
    text: str
    status_code: int


def _cached_request(url: str) -> _MockRequest:
    url_hash = hashlib.md5()
    url_hash.update(url.encode('utf8'))
    url_hash_hex = url_hash.hexdigest()
    cache_file_path = f'test_data/{url_hash_hex}'
    if not os.path.exists(cache_file_path):
        with open(cache_file_path, 'w') as f:
            f.write(requests.get(url).text)
    with open(cache_file_path, 'r') as f:
        content = f.read()
    resp = _MockRequest()
    resp.text = content
    resp.status_code = 200
    return resp


def archived_url_getter(urls):
    while True:
        for url in urls:
            yield _cached_request(url)


test_db_engine = sa.engine.create_engine("sqlite:///:memory:", future=True)
ensure_table(test_db_engine)
test_db_connector = test_db_engine.connect


def make_news_getter():
    urls = [
        "https://web.archive.org/web/20210411000809/https://www.abc.net.au/",
        "https://web.archive.org/web/20210413013911/https://www.abc.net.au/",
        "https://web.archive.org/web/20210413013911/https://www.abc.net.au/", # same as the last
        "https://web.archive.org/web/20210414182235/https://www.abc.net.au/",
    ]
    f = archived_url_getter(urls)
    return lambda _: next(f)


class ABCNewsTestCase(unittest.TestCase):
    def test_news_changes(self):
        abc_scanner = ABCScanner(get_url=make_news_getter(), connector=test_db_connector)
        self.assertFalse(bool(abc_scanner.get_last_content()))
        changes1 = abc_scanner.detect_changes()
        self.assertGreater(len(changes1), 0)
        changes2 = abc_scanner.detect_changes()
        self.assertGreater(len(changes2), len(changes1))
        changes3 = abc_scanner.detect_changes()
        self.assertEqual(len(changes3), 0)
        changes4 = abc_scanner.detect_changes()
        self.assertGreater(len(changes4), len(changes1))
        # print(changes1)
        # print(changes2)
        # print(changes3)
        # print(changes4)
        # print(len(changes1))
        # print(len(changes2))
        # print(len(changes3))
        # print(len(changes4))


if __name__ == '__main__':
    unittest.main()
