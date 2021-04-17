import time
import sys
from db import ensure_table, engine
from scanner import NewsScannerInterface, Change
from abcnews import ABCScanner


SLEEP_DURATION_SECS = 7


def scan_news(scanners: list[NewsScannerInterface]) -> list[list[Change]]:
    changes = [scanner.detect_changes() for scanner in scanners]
    return changes


def print_changes(changes: list[Change]):
    print([str(change) for change in changes])


def main(scanners: list[NewsScannerInterface], sleeper=time.sleep, engine=engine):
    ensure_table(engine)
    while True:
        all_changes = scan_news(scanners)
        for change_set in all_changes:
            if change_set:
                print_changes(change_set)
            elif 'debug' in sys.argv:
                print("No changes")
        sleeper(SLEEP_DURATION_SECS)


if __name__ == '__main__':
    print("Watcher running. Press Ctrl+C to stop.")
    try:
        news_scanners: list[NewsScannerInterface]
        news_scanners = [ABCScanner()]
        main(news_scanners)
    except KeyboardInterrupt:
        print("Stopping...")
        exit(0)
