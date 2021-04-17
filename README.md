# cmdline news watcher

Copy `.env.example` to `.env`, and then `docker-compose up` should run the watcher.

Currently runs for ABC news, easy enough to extend for others. Also, checks headlines at the moment, but checking description as well would be trivial.

The logic right now is link based. Items are considered added or removed if they are new/removed links, and updated if the text for the same link changed.

`test.py` contains the only relevant test.
