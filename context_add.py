#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys, os, io, re
import simplejson as json
import time
import codecs
from resources.lib._json import read_json, write_json

loglevel = 1
xbmc.log('plugin.video.bookmark - init context add')

addonID = "plugin.video.bookmark"
addon = xbmcaddon.Addon(id=addonID)
home = addon.getAddonInfo('path').decode('utf-8')
resourcesDir = os.path.join(home, 'resources') + '/'
path = xbmc.getInfoLabel("ListItem.Path")
fanart = ''
log_msg = 'plugin.video.bookmark - '
time_now = time.strftime("%Y-%m-%d - %H:%M:%S")


def main():
    addon_id = get_addon_id(path)
    db_file = resourcesDir + addon_id + '.json'
    new_data = get_data_episode()
    add_to_db(new_data, db_file)


def get_data_episode():
    name = xbmc.getInfoLabel("ListItem.Title")
    link = xbmc.getInfoLabel("ListItem.FileNameAndPath")
    plot = xbmc.getInfoLabel("ListItem.Plot")
    dura = xbmc.getInfoLabel("ListItem.Duration")
    icon = xbmc.getInfoLabel("ListItem.Thumb")
    fana = xbmc.getInfoLabel("ListItem.Art(fanart)")
    date = time_now
    data = {name: {'name': name, 'link': link, 'icon': icon, 'fana': fana, 'plot': plot, 'dura': dura, 'date': date}}
    return data


def add_to_db(new_data, db_file):
    xbmc.log(log_msg + '!ADD TO DB!', loglevel)
    xbmc.log(log_msg + 'File: ' + db_file, loglevel)
    db_data = read_json(db_file)
    db_data.update(new_data)
    write_json(db_file, db_data)


def get_addon_id(path):
    xbmc.log(log_msg + '!GET ADDON ID!', loglevel)
    xbmc.log(log_msg + 'Path: ' + path, loglevel)
    import re
    addon_id = 'unknown'
    match = re.match(r'plugin://(.*?)\/', path)
    if match:
        addon_id = match.group(loglevel)
    xbmc.log(log_msg + 'AddonID: ' + addon_id, loglevel)
    return addon_id


if __name__ == '__main__':
    main()
