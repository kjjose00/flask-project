from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Hello World</h1>"

@app.route('/info')
def info():
    return render_template('sample.html')

@app.route('/user/<name>')
def friend(name):
    return "<h1>my friend name is {}</h1>".format(name)

if __name__=='__main__':
    app.run(debug=True)
