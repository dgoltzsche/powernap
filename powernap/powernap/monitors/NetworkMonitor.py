#    powernapd plugin - Monitors network traffic
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
from logging import error, debug, info, warn

class NetworkMonitor():

    # Initialise
    def __init__(self, config):
        self._type = config['monitor']
        self._name = config['name']
        self._absent_seconds = 0
        self._bwin = int(config['bwin'])
        self._bwout = int(config['bwout'])
        self._iface = config['iface']
        # start background thread
        self._active = False
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self.thread_main)
        self._thread.start()

    def thread_main(self):
        while True:
            active = self.checkNetworkTraffic()
            self._lock.acquire()
            self._active = active
            self._lock.release()
            time.sleep(1)

    def checkNetworkTraffic(self):
        ps = subprocess.getoutput("bwm-ng -o csv -c 1 -t 3000").splitlines()
        for line in ps:
            columns = line.split(";")
            
            iface = columns[1]
            if iface != self._iface: 
                continue

            bw_out = float(columns[2]) / 1024 * 8
            bw_in = float(columns[3]) / 1024 * 8
            if bw_in > self._bwin or bw_out > self._bwout:
                return True
        return False

    # Check for connections
    def active(self):
        self._lock.acquire()
        active = self._active
        self._lock.release()
        return active

    def start(self):
        pass

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
