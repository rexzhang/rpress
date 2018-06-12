#!/usr/bin/env python
# coding=utf-8


import os

from werkzeug import secure_filename
from flask import Blueprint, request
from flask_login import login_required

from rpress.database import db
from rpress.helpers.template.common import render_template
from rpress.helpers.mulit_site import get_current_request_site
from rpress.helpers.data_init import import_data_from_wordpress_xml


UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['xml', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

site_tools = Blueprint('site_tools', __name__)


@site_tools.route('', methods=['GET'])
@login_required
def index():
    """"""
    return render_template("rp/site_tools/index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@site_tools.route('/import_wp_xml', methods=['GET', 'POST'])
@login_required
def import_wordpress_xml():
    """导入 wordpress xml 文件"""
    site = get_current_request_site()
    if site is None:
        return 'site binding error'

    if request.method != 'POST':
        return render_template('rp/site_tools/upload_wordpress_xml.html')

    file = request.files['file']
    if file is None or not allowed_file(file.filename):
        return 'upload file error!'

    filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filename)

    response_msg = import_data_from_wordpress_xml(
        db_session=db.session,
        site=site,
        disable_convert_code_tag=False,
        filename=filename,
        is_cli_mode=False,
        is_skip_unknow_author=False
    )
    db.session.commit()

    return response_msg
