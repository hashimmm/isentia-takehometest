# cmdline news watcher

Copy `.env.example` to `.env`, and then `docker-compose up` should run the watcher.

`src/watcher.py` is the entrypoint to the application.

Currently runs for ABC news, easy enough to extend for others. Also, checks headlines at the moment, but checking description as well would be trivial.

The logic right now is link based. Items are considered added or removed if they are new/removed links, and updated if the text for the same link changed.

`src/test.py` contains the only relevant test.

Adding new news scanners would involve implementing the interface and adding it to the list in `src/watcher.py`.
