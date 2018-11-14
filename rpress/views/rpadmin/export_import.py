#!/usr/bin/env python
# coding=utf-8


import io

from flask import Blueprint, send_file
from flask_login import login_required

from rpress.runtimes.rpadmin.template import render_template, navbar
from rpress.runtimes.current_session import get_current_site
from rpress.runtimes.data_export_import_v1 import export_site_data_to_json_str

app = Blueprint('rpadmin_export_import', __name__)


@app.route('')
@login_required
@navbar(level1='export_import')
def index():
    return render_template('rpadmin/export_import.html')


@app.route('/export')
def export():
    site = get_current_site()
    json_str, filename = export_site_data_to_json_str(site_id=site.id)

    # convert str to string stream
    staging = io.StringIO(json_str)
    # Creating the byteIO object from the StringIO Object
    fp = io.BytesIO()
    fp.write(staging.getvalue().encode('utf-8'))
    # seeking was necessary. Python 3.7, Flask 1.0
    fp.seek(0)
    staging.close()

    return send_file(
        fp,
        mimetype='text/json',
        as_attachment=True,
        attachment_filename=filename
    )
