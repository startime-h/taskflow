#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import sys_path

class AirflowException(Exception):
    pass

class AirflowConfigException(AirflowException):
    pass

class AirflowSensorTimeout(AirflowException):
    pass

class AirflowTaskTimeout(AirflowException):
    pass

class AirflowSkipException(AirflowException):
    pass
