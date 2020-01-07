from info import create_app


app = create_app('development')


@app.route('/')
def hello():
    return 'hello'




if __name__ == '__main__':
    app.run()