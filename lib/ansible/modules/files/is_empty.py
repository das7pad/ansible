#!/usr/bin/python

from __future__ import absolute_import
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: is_empty
version_added: "2.9"
short_description: Retrieve empty status of a directory
description:
     - Lightweight sibling for the find module.
options:
  path:
    description:
      - The full path of the directory to get the facts of.
    type: path
    required: true
  ignore_missing:
    description:
      - Flag missing directories as empty
      - Set to C(false) to raise an error
    type: bool
    default: true
seealso:
- module: find
author: Jakob Ackermann (@das7pad)
'''

EXAMPLES = r'''
# Check for existing postgres data.
- is_empty:
    path: /var/lib/postgresql/data/
  register: db_data_dir
- debug:
    msg: "Schedule database init"
  when: not db_data_dir.is_empty
'''

RETURN = r'''
is_empty:
    description: boolean of the empty status
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
            ignore_missing=dict(type='bool', default=True),
        ),
        supports_check_mode=True,
    )

    path = module.params.get('path')
    b_path = to_bytes(path, errors='surrogate_or_strict')

    def handler(err):
        if err.errno == errno.ENOENT and module.params.get('ignore_missing'):
            module.exit_json(changed=False, is_empty=True)

        module.fail_json(msg=err.strerror)

    items = tuple(os.walk(b_path, onerror=handler))
    is_empty = items == ((b_path, [], []),)

    module.exit_json(changed=False, is_empty=is_empty)


if __name__ == '__main__':
    main()
