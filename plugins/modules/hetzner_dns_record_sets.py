#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Felix Fontein
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: hetzner_dns_record_sets

short_description: Bulk synchronize DNS record sets in Hetzner DNS service

version_added: 2.0.0

description:
  - Bulk synchronize DNS record sets in Hetzner DNS service.
extends_documentation_fragment:
  - felixfontein.antsibull_nox_playground.hetzner
  - felixfontein.antsibull_nox_playground.hetzner.record_notes
  - felixfontein.antsibull_nox_playground.hetzner.record_type_choices_record_sets_module
  - felixfontein.antsibull_nox_playground.hetzner.record_type_seealso
  - felixfontein.antsibull_nox_playground.hetzner.zone_id_type
  - felixfontein.antsibull_nox_playground.module_record_sets
  - felixfontein.antsibull_nox_playground.options.bulk_operations
  - felixfontein.antsibull_nox_playground.options.record_transformation
  - felixfontein.antsibull_nox_playground.attributes
  - felixfontein.antsibull_nox_playground.attributes.actiongroup_hetzner

attributes:
  action_group:
    version_added: 2.4.0

author:
  - Markus Bergholz (@markuman) <markuman+spambelongstogoogle@gmail.com>
  - Felix Fontein (@felixfontein)
"""

EXAMPLES = r"""
- name: Make sure some records exist and have the expected values
  felixfontein.antsibull_nox_playground.hetzner_dns_record_sets:
    zone: foo.com
    records:
      - prefix: new
        type: A
        ttl: 7200
        value:
          - 1.1.1.1
          - 2.2.2.2
      - prefix: new
        type: AAAA
        ttl: 7200
        value:
          - "::1"
      - record: foo.com
        type: TXT
        value:
          - test
    hetzner_token: access_token

- name: Synchronize DNS zone with a fixed set of records
  # If a record exists that is not mentioned here, it will be deleted
  felixfontein.antsibull_nox_playground.hetzner_dns_record_sets:
    zone_id: 23
    purge: true
    records:
      - prefix: ''
        type: A
        value: 127.0.0.1
      - prefix: ''
        type: AAAA
        value: "::1"
      - prefix: ''
        type: NS
        value:
          - ns-1.hoster.com
          - ns-2.hoster.com
          - ns-3.hoster.com
    hetzner_token: access_token
"""

RETURN = r"""
zone_id:
  description: The ID of the zone.
  type: str
  returned: success
  sample: 23
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.felixfontein.antsibull_nox_playground.plugins.module_utils.argspec import (
    ModuleOptionProvider,
)
from ansible_collections.felixfontein.antsibull_nox_playground.plugins.module_utils.hetzner.api import (
    create_hetzner_api,
    create_hetzner_argument_spec,
    create_hetzner_provider_information,
)
from ansible_collections.felixfontein.antsibull_nox_playground.plugins.module_utils.http import ModuleHTTPHelper
from ansible_collections.felixfontein.antsibull_nox_playground.plugins.module_utils.module.record_sets import (
    create_module_argument_spec,
    run_module,
)


def main():
    provider_information = create_hetzner_provider_information()
    argument_spec = create_hetzner_argument_spec()
    argument_spec.merge(create_module_argument_spec(provider_information=provider_information))
    module = AnsibleModule(supports_check_mode=True, **argument_spec.to_kwargs())
    option_provider = ModuleOptionProvider(module)
    run_module(
        module,
        lambda: create_hetzner_api(option_provider, ModuleHTTPHelper(module)),
        provider_information=create_hetzner_provider_information(option_provider=option_provider),
    )


if __name__ == '__main__':
    main()
