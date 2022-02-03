from flask import Flask,session,request,url_for,redirect
from flask.templating import render_template
import app
import json
from router import sign
from router import hangout
from router import admin


app = Flask(__name__)
app.secret_key='abcde'
app.register_blueprint(sign.bp)
app.register_blueprint(hangout.bp)
app.register_blueprint(admin.bp)

#app.config['db_ip']="18.118.131.221"
#app.config['db_ip']="127.0.0.1"

@app.route ('/test', methods=['GET','POST'])
def test():
    idx = request.form.get('index')
    print(idx)
    return redirect(url_for(hangout.bp.hangout_list))

@app.route('/logout',methods=['GET','POST'])
def logout():
    session['loggedin']=False
    return str(session['loggedin'])


@app.route('/home',methods=['GET','POST'])
def home():
    if "loggedin" in session and session["loggedin"]== True:
        session['loggedin']=False
        return redirect(url_for('hangout_bp.hangout_list'))
    else:
        return redirect(url_for('sign_bp.login'))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2222, debug=True)
