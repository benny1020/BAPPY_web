from flask import Flask,session,request
from flask.templating import render_template
import app
import json
from router import sign.py


app = Flask(__name__)
app.secret_key='abcde'
app.register_blueprint(register.bp)

#app.config['db_ip']="18.118.131.221"
#app.config['db_ip']="127.0.0.1"


@app.route('/')
def init():
    return render_template("signup.html")



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        print(request.form.get('password'))
        print(request.form['id'])
        print(request.form.get('ch1'))
        print(request.form.get('character_3')) #None
        print(request.form.get('int_2')) # on



        return "true"
    #return render_template("signup.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        jsonData = request.get_json()
        print(jsonData)
        print(jsonData["password"])
        print(request.form)
        print(request.form["password"])
        return "true"
@app.route('/hangout')
def hangout():
    return render_template("hangout.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2222, debug=True)
