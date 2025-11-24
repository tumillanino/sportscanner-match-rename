### Overview

This is a very specific script to my personal use case, but can easily be modified for Kodi or whatever else.
Some things like the directory are hardcoded, so adjust them where necessary.

The watcher.py listens for new files to be added to the subfolders in '/data/downloads/sports/'.
When a new file is added, it triggers match-rename.py to run, which takes the name, which from sports-video.org.ua is normally formatted like 'Team A vs Team B dd.mm.yyyy.mkv' or 'Team at Team B dd.mm.yyyy in 40.mkv' and it will format it based on the folder it is in, and with syntax matching required by the SportScanner Plex plugin to read the SportsDB website.

For example: You add 'New England Patriots at Tampa Bay Buccaneers 09.11.2025.mkv.' to '/data/downloads/sports/NFL/Season 2025-2026'. The watcher recognizes that a new file has been added, and triggers match-rename.py to run. Then match-rename.py updates the name to 'NFL.2025.11.09.New-England-Patriots.vs.Tampa-Bay-Buccaneers.mkv'

### After downloading

First make and add files to the /data file path (unless you are planning to update the scripts).

You can either run watcher.py manually or set up a service in systemd or openrc to have it always listening. The command it needs to execute is:

```bash
python3 /data/watcher.py '/data/downloads/sports' '/data/match-rename.py'
```

To add this as a systemd service, create a file called something like sports-rename.service in /etc/systemd/system/
then add:

```toml
[Unit]
Description=Folder watcher that triggers match-rename.py to run
After=network.target

[Service]
Type=simple
User=<your username>
ExecStart=/usr/bin/python3 /data/watcher.py /data/downloads/sports /data/match-rename.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

You can also run match-rename manually each time you add a file, if you prefer that for whatever reason. You just run the script with python and then the path the new file is in. For example:

```bash
python3 /data/match-rename.py '/data/downloads/sports/NFL/Season 2025-2026'
```

### Still to be done

This fits my specific use case, but anyone that wants to take the scripts and expand on them is welcome to do so. I can see adding data tables of teams so that the scripts know which leagues to attach them to without needing to read 2 folders up in the directory, or testing and expanding for things like Formula One, or adding Kodi compatibility.
