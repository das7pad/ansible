from ansible.module_utils.six import _importer

__DEBUG = False

for key, value in _importer.known_modules.items():
    if key == __name__:
        for key2 in dir(value):
            try:
                locals()[key2] = getattr(value, key2)
                if __DEBUG: print(key2, locals()[key2])
            except:
                if __DEBUG: print(key2)
    if key.find(__name__ + '.') != 0: continue
    key = key.replace(__name__ + '.', '')
    try:
        locals()[key] = value._resolve()
        if __DEBUG: print(key, locals()[key])
    except:
        if __DEBUG: print(key)
