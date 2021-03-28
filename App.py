from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    id = db.Column(db.Integer)
    marks = db.Column(db.Integer)

    def __init__(self, name, idnum, marks):
        self.name = name
        self.id = idnum
        self.marks = marks


@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", students = all_data)

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        idnum = request.form['idnum']
        marks = request.form['marks']

        my_data = Data(name, idnum, marks)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('Index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('uid'))

        print(request.form)
        print(my_data)
        my_data.name = request.form['name']
        my_data.id = request.form['idnum']
        my_data.marks = request.form['marks']

        db.session.commit()

        return redirect(url_for('Index'))

@app.route('/delete/<uid>/', methods=['GET', 'POST'])
def delete(uid):
    my_data = Data.query.get(uid)
    print(uid)
    print(my_data)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
