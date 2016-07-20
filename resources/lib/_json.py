import simplejson as json
import io
import xbmc, xbmcvfs, xbmcaddon

addonID = "plugin.video.bookmark"
addon = xbmcaddon.Addon(id=addonID)
userdataDir = xbmc.translatePath(addon.getAddonInfo('profile'))

log_msg = 'plugin.video.bookmark - _json_lib -'

def read_json(db_file):
    xbmc.log(log_msg + '!READ JSON!', 1)
    xbmc.log(log_msg + 'File: '+db_file, 1)
    if xbmcvfs.exists(db_file):
        xbmc.log(log_msg+'File Exists', 1)
        with open(db_file) as f:
            try:
                data = json.load(f)
                f.close()
            except ValueError:
                data = {}
    else:
        xbmc.log(log_msg + 'File Not Exists', 1)
        data = {}
    return data



def write_json(db_file, data):
    xbmc.log(log_msg + '!WRITE JSON!', 1)
    xbmc.log(log_msg + 'File: ' + db_file, 1)
    check_dir()
    with io.open(db_file, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))
        f.close()


def check_dir():
    if not xbmcvfs.exists(userdataDir):
        xbmcvfs.mkdir(userdataDir)
