#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

################ tables ##################
T_USER_INFO = 'user_info'
T_PROJECT_INFO = 'project_info'
T_DAG_INFO = 'dag_info'
T_TASK_INFO = 'task_info'
T_MACHINE_INFO = 'machine_info'
T_DAG_RUN_HISTORY = 'dag_run_history'
T_TASK_RUN_HISTORY = 'task_run_history'
T_TASK_PENDING_QUEUE = 'task_pending_queue'

################ structs ##################
class UserInfo():
    '''
    @id: primary key
    @user_name: user name
    @user_password_hash: user password hash value
    @user_email: user email
    @register_time: register time
    '''

    ID = 'id'
    UserName = 'user_name'
    UserPasswordHash = 'user_password_hash'
    UserEmail = 'user_email'
    RegisterTime = 'register_time'

class ProjectInfo():
    '''
    @id: primary key
    @project_name: project name
    @create_user_id: create user id
    @create_time: create time
    @project_desc: project description
    @permission_users: has permission users list
    '''

    ID = 'id'
    ProjectName = 'project_name'
    CreateUserId = 'create_user_id'
    CreateTime = 'create_time'
    ProjectDesc = 'project_desc'
    PermissionUsers = 'permission_users'

class DagInfo():
    '''
    @id: primary key
    @dag_id: dag id
    @dag_name: dag name
    @valid: 1: dag is valid
            0: dag is invalid
    @project_name: dag project name
    @create_user_id: create user id
    @create_time: dag create time
    @expire_time: dag expire time
    @scheduler_interval: dag scheduler interval
    @skip_failed: 1: skip
                  0: no skip
    @modify_time: dag modify time
    @dag_status: Not Running
                 Running
                 Failed
                 Terminated
    @next_start_time: dag next start time
    @dag_json: dag json
    '''

    ID = 'id'
    DagId = 'dag_id'
    DagName = 'dag_name'
    Valid = 'valid'
    ProjectName = 'project_name'
    CreateUserId = 'create_user_id'
    CreateTime = 'create_time'
    ExpireTime = 'expire_time'
    SchedulerInterval = 'scheduler_interval'
    SkipFailed = 'skip_failed'
    ModifyTime = 'modify_time'
    DagStatus = 'dag_status'
    NextStartTime = 'next_start_time'
    DagJson = 'dag_json'

class TaskInfo():
    '''
    @id: task id
    @dag_id: task dag id
    @task_id: task id
    @task_name: task name
    @run_machine: task run machine iP address
    @run_user: task run user
    @run_dir: task run work directory
    @run_command: task run shell command
    @run_timeout: task run timeout
    @retry_times: task run retry times
    @task_status: Not Running
                  Running
                  Failed
                  Terminated
    @modify_time: task modify time
    '''

    ID = 'id'
    DagId = 'dag_id'
    TaskId = 'task_id'
    TaskName = 'task_name'
    RunMachine = 'run_machine'
    RunUser = 'run_user'
    RunDir = 'run_dir'
    RunCommand = 'run_command'
    RunTimeout = 'run_timeout'
    RetryTimes = 'retry_times'
    TaskStatus = 'task_status'
    ModifyTime = 'modifyTime'

class MachineInfo():
    '''
    @id: primary key
    @machine_name: machine name
    @machine_ip: machine ip
    '''

    ID = 'id'
    MachineName = 'machine_name'
    MachineIP = 'machine_ip'

class DagRunHistory():
    '''
    @id: dag history id
    @dag_id: dag id
    @start_time: dag start time
    @end_time: dag end time
    @status: dag status
             Failed
             Terminated
    '''

    ID = 'id'
    DagId = 'dag_id'
    StartTime = 'start_time'
    EndTime = 'end_time'
    Status = 'status'

class TaskRunHisgory():
    '''
    @id: primark key
    @task_id: task id
    @start_time: task start time
    @end_time: task end time
    @status: task status
             Failed
             Terminated
    @stdout: task stdout
    @stderr: task stderr
    '''

    ID = 'id'
    TaskId = 'task_id'
    StartTime = 'start_time'
    EndTime = 'end_time'
    Status = 'status'
    Stdout = 'stdout'
    Stderr = 'stderr'

class TaskPendingQueue():
    '''
    @task_id: task id
    @machine_ip: machine ip, machine group
    '''

    TaskId = 'task_id'
    MachineIp = 'machine_ip'
