#    Copyright 2015, Ericsson AB
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

import os
import six.moves.urllib.parse as urlparse

from oslo_db.sqlalchemy import models
from oslo_db import options as db_options
from oslo_config import cfg
from sqlalchemy import schema
from sqlalchemy import (Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from gluon.common.particleGenerator import generator as particel_generator
from gluon.common import paths

sql_opts = [
    cfg.StrOpt('mysql_engine',
               default='InnoDB',
               help='MySQL engine to use.'),

]

# (enikher): for unittests
_DEFAULT_SQL_CONNECTION = ('sqlite:///' +
                           paths.state_path_def('gluon.sqlite'))

cfg.CONF.register_opts(sql_opts, 'database')
db_options.set_defaults(cfg.CONF, _DEFAULT_SQL_CONNECTION, 'gluon.sqlite')


class GluonBase(models.TimestampMixin, models.ModelBase):

    @classmethod
    def get_primary_key_type(cls):
        return cls._primary_key

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d

    def save(self, session=None):
        import gluon.db.sqlalchemy.api as db_api

        if session is None:
            session = db_api.get_session()

        super(GluonBase, self).save(session)


Base = declarative_base(cls=GluonBase)

particel_generator.build_sql_models(Base)
