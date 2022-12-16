# -*- coding: utf-8 -*-
"""
Created on Tue May  3 08:38:23 2022

@author: Owner
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()