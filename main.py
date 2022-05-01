from flask import * 
from wtforms import *
import json
from flask import Flask, request, jsonify,render_template
from flask_mongoengine import MongoEngine
import requests
from flask import * 
from flask_mail import * 
from random import *
app = Flask(__name__)

app.config["MAIL_SERVER"]='smtp.gmail.com' 
app.config["MAIL_PORT"] = 465 
app.config["MAIL_USERNAME"] = 'hemgowda777@gmail.com' 
app.config['MAIL_PASSWORD'] = 'Hemgowda@123' 
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True 
 
mail = Mail(app) 
otp = randint(000000,999999)


app.config['MONGODB_SETTINGS'] = {
 'db': 'cake_order',
'host': 'localhost',
'port': 27017
}
db = MongoEngine()
db.init_app(app)
class Cakes(db.Document):
 cake_occasion=db.StringField()
 cake_name = db.StringField()
 cake_type = db.StringField()
 cake_weight=db.IntField()
 cake_shape=db.StringField()
 cake_text=db.StringField()
 def to_json(self):
    return {
         "cake_occasion":self.cake_occasion,
         "cake_name": self.cake_name,
         "cake_type": self.cake_type,
         "cake_weight":self.cake_weight,
         "cake_shape":self.cake_shape,
         'cake_text':self.cake_text
         }

 
@app.route('/login',methods = ['GET','POST']) 
def login():
 if request.method=="POST":
    uname=request.form['uname'] 
    passwrd=request.form['pass'] 
    if uname=="abc" and passwrd=="xyz": 
        return  redirect(url_for('add')) 
    else:
        return "<h1 style=color:red>Invalid user</h1>"
 else:
    return render_template("login.html")

@app.route('/', methods=['POST'])
def create_record():
 record = json.loads(request.data)
 c = Cakes(
    cake_occasion=record["cake_occasion"],
    cake_name=record['cake_name'],
    cake_type=record['cake_type'],
    cake_weight=record['cake_weight'],
    cake_shape=record["cake_shape"],
    cake_text=record['cake_text'])
 c.save()
 
 return jsonify(c.to_json())

@app.route('/add',methods=['GET','POST'])
def add():
 if request.method=="GET":
    return render_template("add.html")
 else:
      x={
        "cake_occasion":request.form["cake_occasion"],
        "cake_name":request.form['cake_name'],
        "cake_type":request.form['cake_type'],
        "cake_weight":int(request.form['cake_weight']),
         "cake_shape":request.form['cake_shape'],
         'cake_text':request.form["cake_text"]
      }
      x=json.dumps(x)
      response = requests.post(url="http://127.0.0.1:5000/",data=x)
      loaded_json = json.loads(x)
      
      return render_template('x.html',a=loaded_json)
      

@app.route('/verify',methods = ["POST"]) 
def verify(): 
 email = request.form["email"] 
 
 
 msg = Message('OTP',sender = 'hemgowda777@gmail.com', recipients = [email]) 
 msg.body = str(otp)
 mail.send(msg) 
 return render_template('verify.html') 
@app.route('/validate',methods=["POST"]) 
def validate(): 
 user_otp = request.form['otp'] 
 if otp == int(user_otp): 
    return "<h3>Order successfully</h3>"
 return "<h3>failure</h3>"

 
 
if __name__ == '__main__': 
 app.run(debug = True) 