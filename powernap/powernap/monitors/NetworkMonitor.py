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
from logging import error, debug, info, warn

class NetworkMonitor():

    # Initialise
    def __init__(self, config):
        print("NetworkMonitor starting...")
        self._type = config['monitor']
        self._name = config['name']
        self._absent_seconds = 0
        self._bwin = int(config['bwin'])
        self._bwout = int(config['bwout'])
        self._iface = config['iface']

    # Check for connections
    def active(self):
        ps = subprocess.getoutput("bwm-ng -o csv -c 1 -t 1000").splitlines()
        for line in ps:
            columns = line.split(";")
            
            iface = columns[1]
            if iface != self._iface: 
                continue

            bw_out = float(columns[2]) / 1024 / 1024 * 8
            bw_in = float(columns[3]) / 1024 / 1024 * 8
            if bw_in > self._bwin or bw_out > self._bwout:
                return True
        return False

    def start(self):
        pass

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
