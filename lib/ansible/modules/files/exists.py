#!/usr/bin/python

from __future__ import absolute_import
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: exists
version_added: "2.9"
short_description: Retrieve file existence status
description:
     - Lightweight sibling for the stat module.
options:
  path:
    description:
      - The full path of the file/object to get the facts of.
    type: path
    required: true
  follow:
    description:
      - Whether to follow symlinks.
    type: bool
    default: no
seealso:
- module: stat
author: Jakob Ackermann (@das7pad)
'''

EXAMPLES = r'''
# Check for existing postgres data.
- exists:
    path: /var/lib/postgresql/data/PG_VERSION
  register: db_data
- debug:
    msg: "Schedule database init"
  when: not db_data.exists
'''

RETURN = r'''
exists:
    description: boolean of the existence status
    returned: success
    type: bool
    sample: True
'''

import errno
import os

from ansible.module_utils._text import to_bytes
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='path', required=True),
            follow=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    path = module.params.get('path')
    b_path = to_bytes(path, errors='surrogate_or_strict')
    follow = module.params.get('follow')

    exists = False
    try:
        if follow:
            os.stat(b_path)
        else:
            os.lstat(b_path)
    except OSError as err:
        if err.errno != errno.ENOENT:
            module.fail_json(msg=err.strerror)
    else:
        exists = True

    module.exit_json(changed=False, exists=exists)


if __name__ == '__main__':
    main()
