from flask import Flask,render_template, jsonify
app = Flask(__name__)
#namenya harus sama kaya nama filenya.


@app.route('/')
def index():
    return "hello world"
#define routenya   

if __name__ == '__main__':
    app.run(debug = True)