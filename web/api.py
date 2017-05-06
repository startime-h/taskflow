""" HTTP API methods for Dagobah daemon. """

import StringIO
import json

from flask import request, abort, send_file
from flask_login import login_required

from app import app

@app.route('/api/jobs', methods=['GET'])
@login_required
@api_call
def get_jobs():
    return 'all'
