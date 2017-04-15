# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from builtins import object, bytes
from collections import namedtuple
from datetime import datetime, timedelta

from sqlalchemy import (
    Column, Integer, String, DateTime, Text, Boolean, ForeignKey, PickleType,
    Index, Float)
from sqlalchemy import func, or_, and_
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import reconstructor, relationship, synonym

import sys_path
Base = declarative_base()

#########################################
class Chart(Base):
    # table name
    __tablename__ = "chart"

    # table struct
    id = Column(Integer, primary_key=True)
    label = Column(String(200))
    conn_id = Column(String(ID_LEN), nullable=False)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=True)
    chart_type = Column(String(100), default="line")
    sql_layout = Column(String(50), default="series")
    sql = Column(Text, default="SELECT series, x, y FROM table")
    y_log_scale = Column(Boolean)
    show_datatable = Column(Boolean)
    show_sql = Column(Boolean, default=True)
    height = Column(Integer, default=600)
    default_params = Column(String(5000), default="{}")
    owner = relationship("User", cascade=False, cascade_backrefs=False, backref='charts')
    x_is_date = Column(Boolean, default=True)
    iteration_no = Column(Integer, default=0)
    last_modified = Column(DateTime, default=func.now())

#########################################
class KnownEvent(Base):
    # table name
    __tablename__ = "known_event"

    # table struct
    id = Column(Integer, primary_key=True)
    label = Column(String(200))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    user_id = Column(Integer(), ForeignKey('users.id'),)
    known_event_type_id = Column(Integer(), ForeignKey('known_event_type.id'),)
    reported_by = relationship("User", cascade=False, cascade_backrefs=False, backref='known_events')
    event_type = relationship("KnownEventType", cascade=False, cascade_backrefs=False, backref='known_events')
    description = Column(Text)

#########################################
class SlaMiss(Base):
    """
    Model that stores a history of the SLA that have been missed.
    It is used to keep track of SLA failures over time and to avoid double
    triggering alert emails.
    """
    # table name
    __tablename__ = "sla_miss"

    # table struct
    task_id = Column(String(ID_LEN), primary_key=True)
    dag_id = Column(String(ID_LEN), primary_key=True)
    execution_date = Column(DateTime, primary_key=True)
    email_sent = Column(Boolean, default=False)
    timestamp = Column(DateTime)
    description = Column(Text)
    notification_sent = Column(Boolean, default=False)

#########################################
class TaskInstance(Base):
    """
    Task instances store the state of a task instance. This table is the
    authority and single source of truth around what tasks have run and the
    state they are in.

    The SqlAlchemy model doesn't have a SqlAlchemy foreign key to the task or
    dag model deliberately to have more control over transactions.

    Database transactions on this table should insure double triggers and
    any confusion around what task instances are or aren't ready to run
    even while multiple schedulers may be firing task instances.
    """

    # table name
    __tablename__ = "task_instance"

    # table struct
    task_id = Column(String(ID_LEN), primary_key=True)
    dag_id = Column(String(ID_LEN), primary_key=True)
    execution_date = Column(DateTime, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    duration = Column(Float)
    state = Column(String(20))
    try_number = Column(Integer, default=0)
    hostname = Column(String(1000))
    unixname = Column(String(1000))
    job_id = Column(Integer)
    pool = Column(String(50))
    queue = Column(String(50))
    priority_weight = Column(Integer)
    operator = Column(String(1000))
    queued_dttm = Column(DateTime)
    pid = Column(Integer)

#########################################
class User(Base):
    # table name
    __tablename__ = "users"

    # table struct
    id = Column(Integer, primary_key=True)
    username = Column(String(ID_LEN), unique=True)
    email = Column(String(500))
    superuser = False

#########################################
class Connection(Base):
    """
    Placeholder to store information about different database instances
    connection information. The idea here is that scripts use references to
    database instances (conn_id) instead of hard coding hostname, logins and
    passwords when using operators or hooks.
    """
    # table name
    __tablename__ = "connection"

    # table struct
    id = Column(Integer(), primary_key=True)
    conn_id = Column(String(ID_LEN))
    conn_type = Column(String(500))
    host = Column(String(500))
    schema = Column(String(500))
    login = Column(String(500))
    _password = Column('password', String(5000))
    port = Column(Integer())
    is_encrypted = Column(Boolean, unique=False, default=False)
    is_extra_encrypted = Column(Boolean, unique=False, default=False)
    _extra = Column('extra', String(5000))

#########################################
class Log(Base):
    """
    Used to actively log events to the database
    """
    # table name
    __tablename__ = "log"

    # table struct
    id = Column(Integer, primary_key=True)
    dttm = Column(DateTime)
    dag_id = Column(String(ID_LEN))
    task_id = Column(String(ID_LEN))
    event = Column(String(30))
    execution_date = Column(DateTime)
    owner = Column(String(500))
    extra = Column(Text)

#########################################
class Pool(Base):
    # table name
    __tablename__ = "slot_pool"

    # table struct
    id = Column(Integer, primary_key=True)
    pool = Column(String(50), unique=True)
    slots = Column(Integer, default=0)
    description = Column(Text)

#########################################
class DagModel(Base):
    """
    These items are stored in the database for state related information
    """

    # table name
    __tablename__ = "dag"

    dag_id = Column(String(ID_LEN), primary_key=True)
    # A DAG can be paused from the UI / DB
    # Set this default value of is_paused based on a configuration value!
    is_paused_at_creation = configuration.getboolean('core',
                                                     'dags_are_paused_at_creation')
    is_paused = Column(Boolean, default=is_paused_at_creation)
    # Whether the DAG is a subdag
    is_subdag = Column(Boolean, default=False)
    # Whether that DAG was seen on the last DagBag load
    is_active = Column(Boolean, default=False)
    # Last time the scheduler started
    last_scheduler_run = Column(DateTime)
    # Last time this DAG was pickled
    last_pickled = Column(DateTime)
    # Time when the DAG last received a refresh signal
    # (e.g. the DAG's "refresh" button was clicked in the web UI)
    last_expired = Column(DateTime)
    # Whether (one  of) the scheduler is scheduling this DAG at the moment
    scheduler_lock = Column(Boolean)
    # Foreign key to the latest pickle_id
    pickle_id = Column(Integer)
    # The location of the file containing the DAG object
    fileloc = Column(String(2000))
    # String representing the owners
    owners = Column(String(2000))

#########################################
class Variable(Base):
    # table name
    __tablename__ = "variable"

    # table struct
    id = Column(Integer, primary_key=True)
    key = Column(String(ID_LEN), unique=True)
    _val = Column('val', Text)
    is_encrypted = Column(Boolean, unique=False, default=False)

#########################################
class XCom(Base):
    """
    Base class for XCom objects.
    """
    # table name
    __tablename__ = "xcom"

    # table struct
    id = Column(Integer, primary_key=True)
    key = Column(String(512))
    value = Column(PickleType(pickler=dill))
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    execution_date = Column(DateTime, nullable=False)
    # source information
    task_id = Column(String(ID_LEN), nullable=False)
    dag_id = Column(String(ID_LEN), nullable=False)

#########################################
class DagRun(Base):
    """
    DagRun describes an instance of a Dag. It can be created
    by the scheduler (for regular runs) or by an external trigger
    """
    # table name
    __tablename__ = "dag_run"

    # table struct
    id = Column(Integer, primary_key=True)
    dag_id = Column(String(ID_LEN))
    execution_date = Column(DateTime, default=func.now())
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    _state = Column('state', String(50), default=State.RUNNING)
    run_id = Column(String(ID_LEN))
    external_trigger = Column(Boolean, default=True)
    conf = Column(PickleType)
