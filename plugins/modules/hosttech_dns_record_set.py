#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2021 Felix Fontein
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: hosttech_dns_record_set

short_description: Add or delete record sets in Hosttech DNS service

version_added: 2.0.0

description:
  - Creates and deletes DNS record sets in Hosttech DNS service.
  - This module replaces C(hosttech_dns_record) from felixfontein.antsibull_nox_playground before 2.0.0.
extends_documentation_fragment:
  - felixfontein.antsibull_nox_playground.hosttech
  - felixfontein.antsibull_nox_playground.hosttech.record_default_ttl
  - felixfontein.antsibull_nox_playground.hosttech.record_notes
  - felixfontein.antsibull_nox_playground.hosttech.record_type_choices
  - felixfontein.antsibull_nox_playground.hosttech.record_type_seealso
  - felixfontein.antsibull_nox_playground.hosttech.zone_id_type
  - felixfontein.antsibull_nox_playground.module_record_set
  - felixfontein.antsibull_nox_playground.options.record_transformation
  - felixfontein.antsibull_nox_playground.attributes
  - felixfontein.antsibull_nox_playground.attributes.actiongroup_hosttech

attributes:
  action_group:
    version_added: 2.4.0

author:
  - Felix Fontein (@felixfontein)
"""

EXAMPLES = r"""
- name: Add new.foo.com as an A record with 3 IPs
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.com
    record: new.foo.com
    type: A
    ttl: 7200
    value: 1.1.1.1,2.2.2.2,3.3.3.3
    hosttech_token: access_token

- name: Update new.foo.com as an A record with a list of 3 IPs
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.com
    record: new.foo.com
    type: A
    ttl: 7200
    value:
      - 1.1.1.1
      - 2.2.2.2
      - 3.3.3.3
    hosttech_token: access_token

- name: Retrieve the details for new.foo.com
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set_info:
    zone_name: foo.com
    record: new.foo.com
    type: A
    hosttech_username: foo
    hosttech_password: bar
  register: rec

- name: Delete new.foo.com A record using the results from the facts retrieval command
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: absent
    zone_name: foo.com
    record: "{{ rec.set.record }}"
    ttl: "{{ rec.set.ttl }}"
    type: "{{ rec.set.type }}"
    value: "{{ rec.set.value }}"
    hosttech_username: foo
    hosttech_password: bar

- name: Add an AAAA record
  # Note that because there are colons in the value that the IPv6 address must be quoted!
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.com
    record: localhost.foo.com
    type: AAAA
    ttl: 7200
    value: "::1"
    hosttech_token: access_token

- name: Add a TXT record
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.com
    record: localhost.foo.com
    type: TXT
    ttl: 7200
    value: 'bar'
    hosttech_username: foo
    hosttech_password: bar

- name: Remove the TXT record
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: absent
    zone_name: foo.com
    record: localhost.foo.com
    type: TXT
    ttl: 7200
    value: 'bar'
    hosttech_username: foo
    hosttech_password: bar

- name: Add a CAA record
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.com
    record: foo.com
    type: CAA
    ttl: 3600
    value:
      - '128 issue "letsencrypt.org"'
      - '128 iodef "mailto:webmaster@foo.com"'
    hosttech_token: access_token

- name: Add an MX record
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.com
    record: foo.com
    type: MX
    ttl: 3600
    value:
      - "10 mail.foo.com"
    hosttech_token: access_token

- name: Add a CNAME record
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: bla.foo.com
    record: foo.com
    type: CNAME
    ttl: 3600
    value:
      - foo.foo.com
    hosttech_username: foo
    hosttech_password: bar

- name: Add a PTR record
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.foo.com
    record: foo.com
    type: PTR
    ttl: 3600
    value:
      - foo.foo.com
    hosttech_token: access_token

- name: Add an SPF record
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.com
    record: foo.com
    type: SPF
    ttl: 3600
    value:
      - "v=spf1 a mx ~all"
    hosttech_username: foo
    hosttech_password: bar

- name: Add a PTR record
  felixfontein.antsibull_nox_playground.hosttech_dns_record_set:
    state: present
    zone_name: foo.com
    record: foo.com
    type: PTR
    ttl: 3600
    value:
      - "10 100 3333 service.foo.com"
    hosttech_token: access_token
"""

RETURN = r"""
zone_id:
  description: The ID of the zone.
  type: int
  returned: success
  sample: 23
  version_added: 0.2.0
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.felixfontein.antsibull_nox_playground.plugins.module_utils.argspec import (
    ModuleOptionProvider,
)
from ansible_collections.felixfontein.antsibull_nox_playground.plugins.module_utils.hosttech.api import (
    create_hosttech_api,
    create_hosttech_argument_spec,
    create_hosttech_provider_information,
)
from ansible_collections.felixfontein.antsibull_nox_playground.plugins.module_utils.http import ModuleHTTPHelper
from ansible_collections.felixfontein.antsibull_nox_playground.plugins.module_utils.module.record_set import (
    create_module_argument_spec,
    run_module,
)


def main():
    provider_information = create_hosttech_provider_information()
    argument_spec = create_hosttech_argument_spec()
    argument_spec.merge(create_module_argument_spec(provider_information=provider_information))
    module = AnsibleModule(supports_check_mode=True, **argument_spec.to_kwargs())
    run_module(module, lambda: create_hosttech_api(ModuleOptionProvider(module), ModuleHTTPHelper(module)), provider_information=provider_information)


if __name__ == '__main__':
    main()
