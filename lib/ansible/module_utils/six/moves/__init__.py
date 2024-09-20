from ansible.module_utils.six import _importer
from ansible.module_utils.six import *

__DEBUG = False

for key, value in _importer.known_modules.items():
    if key == 'ansible.module_utils.six.moves':
        for key2 in dir(value):
            try:
                locals()[key2] = getattr(value, key2)
                if __DEBUG: print(key2, locals()[key2])
            except:
                if __DEBUG: print(key2)
    if key.find('ansible.module_utils.six.moves.') != 0: continue
    key = key.replace('ansible.module_utils.six.moves.', '')
    try:
        locals()[key] = value._resolve()
        if __DEBUG: print(key, locals()[key])
    except:
        if __DEBUG: print(key)
