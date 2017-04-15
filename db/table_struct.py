#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sys_path

class FlowUserInfo():
    '''
    @id: primary key
    @name: username
    '''

    ID = 'id'
    Name = 'name'

class FlowDag():
    '''
    @id: primary key
    @name: dag pipeline name
    @is_valid: 1: valid
               0: invalid
    @project: dag project
    @owner: create user
    @scheduler_interval: scheduler interval
    @create_time: dag create time
    @expire_time: dag expire time
    @skip_failed: 1: skip
                  0: no skip
    @status: dag status [Running/Terminated/Failed]
    @next_start_time: dag next start time
    @dag_json: dag json
    @last_modify_time: dag last modify time
    '''

    ID = 'id'
    Name = 'name'
    IsValid = 'is_valid'
    Project = 'project'
    Owner = 'owner'
    SchedulerInterval = 'scheduler_interval'
    CreateTime = 'create_time'
    ExpireTime = 'expire_time'
    SkipFailed = 'skip_failed'
    Status = 'status'
    NextStartTime = 'next_start_time'
    DagJson = 'dag_json'
    LastModifyTime = 'last_modify_time'

class FlowTask():
    '''
    @id: task id
    @dag_id: task dag id
    @name: task name
    @status: task status [Running/Terminated/Failed]
    @run_machine: task run machine hostname
    @run_user: task run user
    @run_dir: task run work directory
    @run_command: task run shell command
    @run_timeout: task run timeout
    @retry_times: task run retry times
    @last_modify_time: task last modify time
    '''

    ID = 'id'
    DagId = 'dag_id'
    Name = 'name'
    Status = 'status'
    RunMachine = 'run_machine'
    RunUser = 'run_user'
    RunDir = 'run_dir'
    RunCommand = 'run_command'
    RunTimeout = 'run_timeout'
    RetryTimes = 'retry_times'
    LastModifyTime = 'last_modify_time'

class FlowDagHistory():
    '''
    @id: dag history id
    @dag_id: dag id
    @start_time: dag start time
    @end_time: dag end time
    @status: dag run status [Running/Terminated/Failed]
    '''

    ID = 'id'
    DagId = 'dag_id'
    StartTime = 'start_time'
    EndTime = 'end_time'
    Stutus = 'status'

