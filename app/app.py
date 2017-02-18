#!/usr/bin/python
from flask import Flask, redirect, url_for, request, render_template, make_response
import sqlite3 as sql
import database

app = Flask(__name__)
if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
