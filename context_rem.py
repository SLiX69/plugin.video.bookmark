#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys, os, io
import simplejson as json
from resources.lib._json import read_json, write_json

xbmc.log('plugin.video.bookmarks - init context rem')

addonID = "plugin.video.bookmark"
addon = xbmcaddon.Addon(id=addonID)
home = addon.getAddonInfo('path').decode('utf-8')
resourcesDir = os.path.join(home, 'resources') + '/'
path = xbmc.getInfoLabel("ListItem.Path")
fanart = ''
log_msg = 'plugin.video.bookmark - '

addon_id = xbmc.getInfoLabel("ListItem.Writer")
name = xbmc.getInfoLabel("ListItem.Title")


def main():
    db_file = resourcesDir + addon_id + '.json'
    delete_from_db(name, db_file)


def delete_from_db(name, db_file):
    xbmc.log(log_msg + '!DELETE FROM DB!', 1)
    xbmc.log(log_msg + 'File: '+db_file, 1)
    db_data = read_json(db_file)
    for i in db_data:
        if name == db_data[i]['name'].encode("utf-8"):
            del db_data[i]
            write_json(db_file, db_data)
            break
    else:
        xbmc.log(log_msg + 'Episode not found in data', 1)


if __name__ == '__main__':
    main()
