#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""

from fabric.api import local, env, run
from datetime import datetime

env.hosts = ['107.21.38.215', '54.164.170.176']


def do_clean(number=0):
    """
    Deletes out-of-date archives.
    """
    try:
        number = int(number)
        if number < 0:
            number = 0

        # List all archives in the versions folder
        archives = local("ls -1t versions", capture=True).split("\n")

        # Keep the most recent 'number' archives, delete the rest
        archives_to_keep = archives[:number]
        archives_to_delete = archives[number:]

        for archive in archives_to_delete:
            local("rm versions/{}".format(archive))

        # List all releases in the /data/web_static/releases folder
        releases = run("ls -1t /data/web_static/releases").split("\n")

        # Keep the most recent 'number' releases, delete the rest
        releases_to_keep = releases[:number]
        releases_to_delete = releases[number:]

        for release in releases_to_delete:
            run("rm -rf /data/web_static/releases/{}".format(release))

        print("Deleted {} out-of-date archives/releases".format(
            len(archives_to_delete)))

    except ValueError:
        pass
