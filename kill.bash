#!/bin/bash
ps aux | grep powernapd | grep -v grep | awk '{print $2}' | xargs sudo kill -9