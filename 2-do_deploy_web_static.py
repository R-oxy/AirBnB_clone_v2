#!/usr/bin/python3
"""This module distributes an archive to your web servers"""

from fabric.api import local, put, run, env
from os.path import exists
from datetime import datetime

env.hosts = ['107.21.38.215', '54.164.170.176']


def do_deploy(archive_path):
    """ Distributes an archive to your web servers."""

    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/
        # <archive filename without extension>
        archive_filename = archive_path.split("/")[-1]
        release_folder = "/data/web_static/releases/{}".format(
            archive_filename[:-4])
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_folder))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the release folder to the current folder
        run("mv {}/web_static/* {}".format(release_folder, release_folder))

        # Remove the web_static folder from the release folder
        run("rm -rf {}/web_static".format(release_folder))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the latest release
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
