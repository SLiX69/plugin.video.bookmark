#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys, os, io
import json
from urllib import quote, unquote_plus, unquote, urlencode, quote_plus, urlretrieve
from resources.lib._json import read_json

xbmc.log('plugin.video.bookmark - init video addon')

addonID = "plugin.video.bookmark"
addon = xbmcaddon.Addon(id=addonID)
home = addon.getAddonInfo('path').decode('utf-8')
resourcesDir = os.path.join(home, 'resources') + '/'
fanart = ''
#view_mode_id = int('503')
pluginhandle = int(sys.argv[1])
loglevel = 1
log_msg = 'plugin.video.bookmark - '

skip_root = False
if addon.getSetting('skip_root') == 'true': skip_root = True


def root():
    addDir('Addons', '', 'addons', '')


def get_episodes(name):
    xbmc.log(log_msg + '!GET EPISODES!', loglevel)
    xbmc.log(log_msg + 'from addon: ' +name, loglevel)
    addon_id = name
    db_file = resourcesDir + addon_id + '.json'
    db_all = read_json(db_file)
    name = get_addon_name(addon_id)
    addDir(get_translation(30011)+' '+name, addon_id, 'to_addon', '')
    for i in db_all:
        try:
            name = db_all[i]['name']
            url = db_all[i]['link']
            plot = db_all[i]['plot']
            iconimage = db_all[i]['icon']
            duration = db_all[i]['dura']
            date_added = db_all[i]['date']
            addLink(name, url, 'play', iconimage, plot, duration, addon_id, date_added)
        except KeyError:
            pass


def get_addons():
    xbmc.log(log_msg + '!GET ADDONS!', loglevel)
    addons = []
    path = resourcesDir
    xbmc.log(log_msg + 'path: ' + path, loglevel)
    for subdir, dirs, files in os.walk(path):
        for db_file in files:
            filepath = subdir + os.sep + db_file
            if filepath.endswith(".json"):
                name = db_file[:db_file.rfind(".json")]
                addons.append(name)
    for name in addons:
        addon_id = name  # url = addon_id
        name = get_addon_name(addon_id)
        addDir(name, addon_id, 'episodes', '')


def change_addon(addon_id):
    xbmc.log(log_msg + '!CHANGE ADDON!', loglevel)
    xbmc.log(log_msg + 'AddonID: ' + addon_id, loglevel)
    xbmc.executebuiltin("ActivateWindow(10024,plugin://%s/)" % addon_id)


def addLink(name, url, mode, iconimage, desc, duration, addon_id, date):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode)
    ok = True
    item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    item.setInfo(type="Video", infoLabels={'Genre': ' test ', "Title": name, "Plot": desc, "Duration": duration, "Writer": addon_id, "dateadded": date})
    item.setProperty('IsPlayable', 'true')
    menu = []
    menu.append((get_translation(30022), 'XBMC.RunPlugin(%s?mode=delete)' % (sys.argv[0])))
    item.addContextMenuItems(items=menu, replaceItems=False)
    item.setProperty('fanart_image', fanart)
    #xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=item)
    xbmc.executebuiltin("Container.SetSortMethod(7)")


def play(url):
    try:
        video_url = url
        listitem = xbmcgui.ListItem(path=video_url)
        xbmcplugin.setResolvedUrl(pluginhandle, succeeded=True, listitem=listitem)
    except ValueError:
        pass


def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name)
    ok = True
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    item.setInfo(type="Video", infoLabels={"Title": name})
    item.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=item, isFolder=True)


def get_translation(string_id):
    return addon.getLocalizedString(string_id)


def get_addon_name(addon_id):
    return xbmcaddon.Addon(addon_id).getAddonInfo('name')


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


params = parameters_string_to_dict(sys.argv[2])
mode = params.get('mode')
url = params.get('url')
if type(url) == type(str()):
    url = unquote_plus(url)


if mode == 'addons':
    get_addons()
elif mode == 'episodes':
    get_episodes(url)
elif mode == 'play':
    play(url)
elif mode == 'to_addon':
    change_addon(url)
elif mode == 'delete':
    xbmc.log(log_msg + '!DELETE!', loglevel)
    xbmc.executebuiltin("XBMC.RunScript(%s\context_rem.py)" % home)
    xbmc.executebuiltin("Container.Refresh")
else:
    if not skip_root:
        root()
    else:
        get_addons()



xbmcplugin.endOfDirectory(pluginhandle)
