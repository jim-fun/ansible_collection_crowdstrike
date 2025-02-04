#!/usr/bin/python
# -*- coding: utf-8 -*-

# Ansible info module used to query options for the CrowdStrike Falcon Sensor on Linux systems.
# Copyright: (c) 2021, CrowdStrike Inc.

# Unlicense (see LICENSE or https://www.unlicense.org)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: falconctl_info

short_description: Get values associated with Falcon sensor.

version_added: "1.0.0"

description:
  - Return value associated with the Falcon sensor options.
  - This module is similar to the GET option in falconctl cli.

options:
  name:
    description:
      - A list of falconctl GET options to query.
    choices: [
        'cid',
        'aid',
        'apd',
        'aph',
        'app',
        'trace',
        'feature',
        'metadata_query',
        'message_log',
        'billing',
        'tags',
        'provisioning_token'
        ]
    type: list
    elements: str

author:
  - Carlos Matos <matosc15@gmail.com>
  - Gabriel Alford <redhatrises@gmail.com>
'''

EXAMPLES = r'''
- name: Get all Falcon sensor options
  crowdstrike.falcon.falconctl_info:

- name: Get a subset of Falcon sensor options
  crowdstike.falcon.falconctl_info:
    name:
      - 'cid'
      - 'aid'
      - 'tags'
'''

RETURN = r'''
falconctl_info:
    description:
      - The dictionary containing values of requested Falcon sensor options.
      - Option values consist of strings, or null for options not set.
    type: dict
    returned: success
    sample: {
        'cid': '53abc1234c584115a46efc25dd831a2b',
        'provisioning_token': '1234567',
        'tags': null
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.crowdstrike.falcon.plugins.module_utils.falconctl_utils import FALCONCTL_GET_OPTIONS, get_options


class FalconCtlInfo(object):

    def __init__(self, module):
        self.module = module
        self.name = module.params['name']
        self.cs_path = "/opt/CrowdStrike"
        self.falconctl = self.module.get_bin_path(
            'falconctl', required=True, opt_dirs=[self.cs_path])

    def get_options(self):
        return get_options(self.name)


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='list', elements='str', required=False,
                  choices=FALCONCTL_GET_OPTIONS),
    )

    result = dict(
        changed=False,
        falconctl_info={}
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    falconctl_info = FalconCtlInfo(module)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['falconctl_info'] = falconctl_info.get_options()

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
