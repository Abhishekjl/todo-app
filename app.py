from flask import Flask, render_template, request, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())

class ToDo(db.Model):
    __tablename__ = 'todos'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())


@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        ent_user_email = request.form['email']
        ent_user_pass = request.form['psw']
        data = Users.query.filter_by(user_email = ent_user_email).first()
        try: 
            if data.password == ent_user_pass:
                return redirect('/home')
            else:
                if data.password != ent_user_pass:
                    return render_template('login.html', alert = 'Password Incorrect')    
        except:
            return render_template('login.html', alert = 'User Not Registered')
    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['psw']
        data = Users.query.filter_by(user_email = email).first()
        try:
            if data.user_email == email:
                return render_template('register.html', alert = 'User Already Registered')
        except: 
            register = Users(username = username , user_email = email, password = password)
            db.session.add(register)
            db.session.commit()
            return render_template('register.html',alert = 'Succesfully Registered')
        # return redirect('/')
    return render_template('register.html')    

@app.route('/home', methods=['POST','GET'])
def todos():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title = title , desc = desc)
        db.session.add(todo)
        db.session.commit()
    allToDo = ToDo.query.all()
    # print(allToDo)
    return render_template('index.html', allToDo = allToDo)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/home')


    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo = todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/home')



if __name__ == '__main__':
    app.run(debug=True, port=8080)    