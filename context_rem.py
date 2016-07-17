#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys
import json
from resources.lib._json import read_json, write_json

loglevel = 1
xbmc.log('plugin.video.bookmark - init context rem', loglevel)

addonID = "plugin.video.bookmark"
addon = xbmcaddon.Addon(id=addonID)
home = addon.getAddonInfo('path').decode('utf-8')
userdataDir = xbmc.translatePath(addon.getAddonInfo('profile'))
path = xbmc.getInfoLabel("ListItem.Path")
fanart = ''
log_msg = 'plugin.video.bookmark - '

if addon.getSetting('auto_rem_db') == 'true': auto_rem_db = True

addon_id = xbmc.getInfoLabel("ListItem.Writer")
name = xbmc.getInfoLabel("ListItem.Title")


def main():
    db_file = userdataDir + addon_id + '.json'
    delete_from_db(name, db_file)


def delete_from_db(name, db_file):
    xbmc.log(log_msg + '!DELETE FROM DB!', loglevel)
    xbmc.log(log_msg + 'File: '+db_file, loglevel)
    db_data = read_json(db_file)
    for i in db_data:
        if name == db_data[i]['name'].encode("utf-8"):
            del db_data[i]
            write_json(db_file, db_data)
            break       #no need to keep searching
    else:
        xbmc.log(log_msg + 'Episode not found in data', loglevel)
    if auto_rem_db:
        if not db_data:
            xbmc.log(log_msg + 'File empty, delete it', loglevel)
            xbmcvfs.remove(db_file)


if __name__ == '__main__':
    main()
