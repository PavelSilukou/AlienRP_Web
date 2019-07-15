#!/usr/bin/python

from flask import render_template, request
from alienrp import app
from alienrp import babel
from config import LANGUAGES
import os

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/license')
def license():
    return render_template('license.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/source')
def source():
    #source_code_file = find_source_code_files()
    return render_template('source.html')

@app.route('/download')
def download():
    setup_files = find_last_setup_files()
    return render_template('download.html', setup32 = setup_files[0], setup64 = setup_files[1])

def find_last_setup_files():
    start_folder = '/h/alienrpcom/htdocs/alienrp'
    #start_folder = '/var/www/alienrp/alienrp'
    download_folder = 'static/download/'

    setup32 = ''
    setup64 = ''

    for file in os.listdir(os.path.join(start_folder, download_folder)):
        if 'x32' in file:
            setup32 = os.path.join(download_folder, file)
        if 'x64' in file:
            setup64 = os.path.join(download_folder, file)

    return (setup32, setup64)

def find_source_code_files():
    start_folder = '/h/alienrpcom/htdocs/alienrp'
    #start_folder = '/var/www/alienrp/alienrp'
    download_folder = 'static/download/'

    source_code_file = ''

    for file in os.listdir(os.path.join(start_folder, download_folder)):
        if 'source' in file:
            source_code_file = os.path.join(download_folder, file)

    return source_code_file
