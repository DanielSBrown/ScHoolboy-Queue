from app import app


@app.route('/health/')
def healthcheck():
    return 'Healthy\n', 200
