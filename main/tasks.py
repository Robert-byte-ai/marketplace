from board.celery import app


@app.task
def supper_sum(x, y):
    return x + y


@app.task
def hello():
    return 'Hello, world'
