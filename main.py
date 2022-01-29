from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# створення Flask
app = Flask(__name__)

# Додавання бази даних
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# Ініціалізація бази даних
db = SQLAlchemy(app)


# створення Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # повернення рядка після додавання user-а
    def __repr__(self):
        return '<Name %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    user_name = request.form['input_name']
    user_surname = request.form['input_surname']
    user_email = request.form['input_email']
    # User email validator:
    try:
        new_user = User(name=user_name, surname=user_surname, email=user_email)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        exist_user = User.query.filter_by(
            email=user_email).first()  # if email exist in DB return name and surname from DB (not from request form)
        return render_template('exist_member.html', user_data=new_user, exist_user=exist_user)
    return render_template('hello.html', user_data=new_user)


@app.route('/show_members', methods=['GET'])
def show_members():
    member = User.query.order_by(User.id)
    return render_template('members.html', members=member)


@app.route('/delete_members')
def delete_members():
    delete_all = User.query.delete()
    db.session.commit()
    return render_template('members.html')


if __name__ == '__main__':
    app.run(debug=True)
