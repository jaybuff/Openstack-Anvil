# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright (C) 2012 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from anvil import log as logging
from anvil import trace as tr
from anvil import type_utils as tu
from anvil import utils


LOG = logging.getLogger(__name__)


class Component(object):
    def __init__(self, name, subsystems, instances, options, siblings,  distro, passwords, **kwargs):

        # Subsystems this was requested with
        self.subsystems = subsystems
        
        # The component name (from config)
        self.name = name
        
        # Any component options
        self.options = options

        # All the other active instances
        self.instances = instances

        # All the other class names that can be used alongside this class
        self.siblings = siblings

        # The distribution 'interaction object'
        self.distro = distro

        # Turned on and off as phases get activated
        self.activated = False

        # How we get any passwords we need
        self.passwords = passwords

    def get_password(self, option, prompt_text, **kwargs):
        return self.passwords.get_password(option, prompt_text, **kwargs)

    def get_option(self, option, default_value=None):
        option_value = utils.get_from_path(self.options, option)
        if option_value is None:
            return default_value
        else:
            return option_value

    def get_bool_option(self, option, default_value=False):
        return tu.make_bool(self.get_option(option, default_value))

    def get_int_option(self, option, default_value=0):
        return int(self.get_option(option, default_value))

    @property
    def env_exports(self):
        return {}

    def verify(self):
        pass

    def __str__(self):
        return "%s@%s" % (tu.obj_name(self), self.name)

    @property
    def params(self):
        # Various params that are frequently accessed
        return {
            'APP_DIR': self.get_option('app_dir'),
            'COMPONENT_DIR': self.get_option('component_dir'),
            'CONFIG_DIR': self.get_option('cfg_dir'),
            'TRACE_DIR': self.get_option('trace_dir'),
        }

    @property
    def trace_files(self):
        trace_dir = self.get_option('trace_dir')
        return {
            'install': tr.trace_fn(trace_dir, "install"),
            'start': tr.trace_fn(trace_dir, "start"),
        }

    def warm_configs(self):
        # Before any actions occur you get the chance to 
        # warmup the configs u might use (ie for prompting for passwords
        # earlier rather than later)
        pass
