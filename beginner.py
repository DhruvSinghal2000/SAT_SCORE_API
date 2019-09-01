from flask import Flask as f

app = f(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello World'


s = "hello"


def hello_world():
    return 'hello world'


@app.route('/hello/<name>')
def withName(name):
    return "Hello {0}".format(name)


app.add_url_rule('/hello', s, hello_world)

if __name__ == '__main__':
    app.run(debug=True)
