#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Generate the archive filename
    # (web_static_<year><month><day><hour><minute><second>.tgz)
    archive_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(archive_time)

    # Compress the web_static folder into the archive
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.succeeded:
        print("web_static packed: {} -> {}Bytes"
              .format(archive_path, os.path.getsize(archive_path)))
        return (archive_path)
    else:
        return None
