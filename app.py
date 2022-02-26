from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == '__main__':
        app.run()

@app.route('/product/<name>')
def get_product(shoes):
    return "The product is " + str(name)

if __name__ == '__main__':
        app.run()