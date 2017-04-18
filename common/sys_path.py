#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

__current_file__ = __file__
__current_abs_path__ = os.path.abspath(__current_file__)
__current_dir__ = os.path.dirname(__current_abs_path__)
__parent_dir__ = os.path.dirname(__current_dir__)
__grandfather_dir__ = os.path.dirname(__parent_dir__)

append_dir_list = [__current_dir__, __parent_dir__, __grandfather_dir__]
sys.path += append_dir_list
