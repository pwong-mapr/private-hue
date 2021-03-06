#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import sys

from django.utils.translation import ugettext_lazy as _t, ugettext as _

from desktop.lib.conf import Config

from beeswax.settings import NICE_NAME



HIVE_SERVER_HOST = Config(
  key="hive_server_host",
  help=_t("Host where HiveServer2 server is running. If Kerberos security is enabled, "
         "the fully-qualified domain name (FQDN) is required"),
  default="localhost")

HIVE_SERVER_PORT = Config(
  key="hive_server_port",
  help=_t("Configure the port the HiveServer2 server runs on."),
  default=10000,
  type=int)

HIVE_CONF_DIR = Config(
  key='hive_conf_dir',
  help=_t('Hive configuration directory, where hive-site.xml is located.'),
  default=os.environ.get("HIVE_CONF_DIR", '/etc/hive/conf'))

HIVE_SERVER_BIN = Config(
  key="hive_server_bin",
  help=_t("Path to HiveServer2 start script"),
  default='/usr/lib/hive/bin/hiveserver2',
  private=True)

LOCAL_EXAMPLES_DATA_DIR = Config(
  key='local_examples_data_dir',
  default=os.path.join(os.path.dirname(__file__), "..", "..", "data"),
  help=_t('The local filesystem path containing the Hive examples.'))

SERVER_CONN_TIMEOUT = Config(
  key='server_conn_timeout',
  default=120,
  type=int,
  help=_t('Timeout in seconds for Thrift calls.'))

BROWSE_PARTITIONED_TABLE_LIMIT = Config(
  key='browse_partitioned_table_limit',
  default=250,
  type=int,
  help=_t('Set a LIMIT clause when browsing a partitioned table. A positive value will be set as the LIMIT. If 0 or negative, do not set any limit.'))


def config_validator(user):
  # dbms is dependent on beeswax.conf (this file)
  # import in method to avoid circular dependency
  from beeswax.server import dbms

  res = []
  try:
    if not 'test' in sys.argv: # Avoid tests hanging
      server = dbms.get(user)
      server.get_databases()
  except:
    res.append((NICE_NAME, _("The application won't work without a running HiveServer2.")))

  return res
