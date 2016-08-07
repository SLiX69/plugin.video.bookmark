#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys, os
import json
from urllib import quote, unquote_plus, unquote, urlencode, quote_plus, urlretrieve
from resources.lib._json import read_json

xbmc.log('plugin.video.bookmark - init video addon')

addonID = "plugin.video.bookmark"
addon = xbmcaddon.Addon(id=addonID)
home = addon.getAddonInfo('path').decode('utf-8')
userdataDir = xbmc.translatePath(addon.getAddonInfo('profile'))
resourcesDir = os.path.join(home, 'resources') + '/'
fanart = ''
#view_mode_id = int('503')
pluginhandle = int(sys.argv[1])
loglevel = 1
log_msg = 'plugin.video.bookmark - '

skip_root = False
enab_fana = False
if addon.getSetting('skip_root') == 'true': skip_root = True
if addon.getSetting('enab_fana') == 'true': enab_fana = True


def root():
    addDir('Addons', '', 'addons', '')


def get_addons():
    xbmc.log(log_msg + '!GET ADDONS!', loglevel)
    addons = []
    path = userdataDir
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
        addDir(name, addon_id, 'episodes', '', True)


def get_episodes(name):
    xbmc.log(log_msg + '!GET EPISODES!', loglevel)
    xbmc.log(log_msg + 'from addon: ' +name, loglevel)
    addon_id = name
    db_file = userdataDir + addon_id + '.json'
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
            fanart = ''
            if enab_fana:
                if 'fana' in db_all[i]:
                    fanart = db_all[i]['fana']
            addLink(name, url, 'play', iconimage, plot, duration, addon_id, date_added, fanart)
        except KeyError:
            pass


def change_addon(addon_id):
    xbmc.log(log_msg + '!CHANGE ADDON!', loglevel)
    xbmc.log(log_msg + 'AddonID: ' + addon_id, loglevel)
    xbmc.executebuiltin("ActivateWindow(10024,plugin://%s/)" % addon_id)


def addLink(name, url, mode, iconimage, desc, duration, addon_id, date, fanart):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode)
    ok = True
    item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    item.setInfo(type="Video", infoLabels={'Genre': ' test ', "Title": name, "Plot": desc, "Duration": duration, "Writer": addon_id, "dateadded": date})
    item.setProperty('IsPlayable', 'true')
    item.setProperty('fanart_image', fanart)
    menu = []
    menu.append((get_translation(30022), 'XBMC.RunPlugin(%s?mode=delete_entry)' % (sys.argv[0])))
    item.addContextMenuItems(items=menu, replaceItems=False)
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


def addDir(name, url, mode, iconimage, cm_del_addon=False):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name)
    ok = True
    item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    item.setInfo(type="Video", infoLabels={"Title": name})
    item.setProperty('fanart_image', fanart)
    if cm_del_addon:
        menu = []
        menu.append((get_translation(30023), 'XBMC.RunPlugin(%s?mode=delete_addon&url=%s)' % (sys.argv[0], url)))
        item.addContextMenuItems(items=menu, replaceItems=False)
    xbmcplugin.addDirectoryItem(pluginhandle, url=u, listitem=item, isFolder=True)


def check_for_old_dbs():
    dirs, files = xbmcvfs.listdir(resourcesDir)
    for file in files:
        if file.endswith('.json'):  # json file exists
            xbmc.log(log_msg + 'FOUND OLD DB!')
            move_dbs()  # move dbs to userdata
            break   # exit after file found and move_dbs


def move_dbs():
    dirs, files = xbmcvfs.listdir(resourcesDir)
    for file in files:
        if file.endswith('.json') and xbmcvfs.exists(xbmc.translatePath(resourcesDir + file)):  # file endswith json and exists
            db_file = xbmc.translatePath(resourcesDir + file)
            xbmcvfs.copy(db_file, db_file + '.backup')
            new_db_file = xbmc.translatePath(userdataDir + file)
            success = xbmcvfs.copy(db_file, new_db_file)
            if success == 1 and xbmcvfs.exists(new_db_file):
                delete = xbmcvfs.delete(xbmc.translatePath(resourcesDir + file))

# old move_dbs function
'''
def move_dbs():
    import fnmatch
    dirs, files = xbmcvfs.listdir(resourcesDir)
    for file in files:
        if fnmatch.fnmatch(file, '*.json'):
            success = xbmcvfs.copy(xbmc.translatePath(resourcesDir + file), xbmc.translatePath(userdataDir + file))
            if success == 1:
                delete = xbmcvfs.delete(xbmc.translatePath(resourcesDir + file))
'''


def get_translation(string_id):
    return addon.getLocalizedString(string_id)


def get_addon_name(addon_id):
    retval = 'unknown'
    try:
        retval = xbmcaddon.Addon(addon_id).getAddonInfo('name')
    except RuntimeError:
        pass
    return retval


def delete_entry():
    xbmc.log(log_msg + '!DELETE!', loglevel)
    xbmc.executebuiltin("XBMC.RunScript(%s\context_rem.py)" % home)
    xbmc.executebuiltin("Container.Refresh")


def delete_addon(addon_id):
    name = get_addon_name(addon_id)
    line1 = get_translation(30110) + ' (%s)' % name
    retval_rule = xbmcgui.Dialog().yesno("Bookmark Addon", line1)
    if retval_rule == 1:
        db_file = userdataDir + addon_id + '.json'
        xbmcvfs.delete(db_file)
    xbmc.executebuiltin("Container.Refresh")


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
elif mode == 'delete_entry':
    delete_entry()
elif mode == 'delete_addon':
    delete_addon(url)
else:
    if not skip_root:
        root()
    else:
        get_addons()


xbmcplugin.endOfDirectory(pluginhandle)

check_for_old_dbs()
