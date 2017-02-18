from flask import Flask, render_template

from app import app

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run('localhost', 8000)
