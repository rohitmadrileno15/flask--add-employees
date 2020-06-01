from flask import Flask,redirect, url_for,render_template, request,session,flash,request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField,SubmitField
from wtforms.validators import DataRequired,Length, Email , EqualTo, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = '450933c08c5ab75e79619102eddf47dee813a9d6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(50), nullable = False)
    designation = db.Column(db.String(120), nullable = False)

    address = db.Column(db.String(160), nullable = False)
    phone = db.Column(db.String(60), nullable = False)



    def __repr__(self):
        return f"User('{self.name}','{self.designation}')"

class addform(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    designation = StringField('designation', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    submit = SubmitField('Add')

class searchForm(FlaskForm):
    data = StringField('data', validators=[DataRequired()])
    submit = SubmitField('Search')



@app.route("/",methods=['GET','POST'])
def home():
    posts =Employee.query.all()
    form = searchForm()
    if(request.method == 'POST'):
        if (form.validate_on_submit()):
            search_data = form.data.data
            form.data.data = None
            val = search(search_data)
            print(val)

            return render_template('search.html',posts = val)

    return render_template('home.html',posts = posts,form = form )




@app.route("/add", methods = ["GET" ,  "POST"] )
def add():
    form = addform()
    alert= "You can add new employee data here"
    if(request.method == 'POST'):
        if (form.validate_on_submit()):
            name_ = form.name.data
            form.name.data = None
            desig_ = form.designation.data
            form.designation.data=None
            address_ = form.address.data
            form.address.data= None
            phone_ = form.phone.data
            form.phone.data =None
            print("done")
            newFile = Employee(name = name_ , designation = desig_  ,address = address_, phone = phone_ )
            db.session.add(newFile)
            db.session.commit()

            return redirect(url_for('home'))

    return render_template('add.html',form = form,alert = alert)

def search(obj):
    data1 = Employee.query.filter_by(name = obj  ).all()
    data2 = Employee.query.filter_by(  designation = obj  ).all()
    data3 = Employee.query.filter_by( address = obj  ).all()
    data4 = Employee.query.filter_by(  phone = obj).all()
    data = []
    data.extend(data1)
    data.extend(data2)
    data.extend(data3)
    data.extend(data4)

    return data


if __name__ == "__main__":
    app.run(debug=True)
