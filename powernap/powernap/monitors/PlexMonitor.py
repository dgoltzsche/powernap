#    powernapd plugin - Monitors plex clients
#
#    Copyright (C) 2011 Canonical Ltd.
#
#    Authors: Stefan Brenner <stefan@fam-brenner.eu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, re, subprocess
import threading 
import time
import logging
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound

class PlexMonitor():

    # Initialise
    def __init__(self, config):
        self._type = config['monitor']
        self._name = config['name']
        self._token = config['token']
        self._baseurl = config['baseurl']
        self._absent_seconds = 0
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("plexapi").setLevel(logging.WARNING)
        print(logging.Logger.manager.loggerDict)

    # Check for plex clients
    def active(self):
        try:
            plex = PlexServer(self._baseurl, self._token)
        except NotFound:
            return False
        for client in plex.clients():
            if client.isPlayingMedia():
                return True
        return False

    def start(self):
        pass

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
