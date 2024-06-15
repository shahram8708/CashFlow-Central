from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from flask_login import current_user
from io import BytesIO
import base64
import pandas as pd
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)  

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    budget = db.Column(db.Float, default=0.0)
    savings_goal = db.Column(db.Float, default=0.0)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('Username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    item = StringField('Item', validators=[InputRequired(), Length(max=100)])
    amount = FloatField('Amount', validators=[InputRequired()])
    date = StringField('Date (YYYY-MM-DD)', validators=[InputRequired()])
    submit = SubmitField('Add')

class BudgetForm(FlaskForm):
    budget = FloatField('Monthly Budget', validators=[InputRequired()])
    submit = SubmitField('Set')

class SavingsForm(FlaskForm):
    savings_goal = FloatField('Savings Goal', validators=[InputRequired()])
    submit = SubmitField('Set')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def generate_plot(user_id):
    expenses = Expense.query.filter_by(user_id=user_id).all()
    if expenses:
        df = pd.DataFrame([(e.date, e.amount) for e in expenses], columns=['Date', 'Amount'])
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df['Amount'], marker='o')
        plt.title('Expense Over Time')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.grid(True)
        plt.tight_layout()

        plt.savefig('static/plot_{}.png'.format(user_id))
        plt.close()  

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    expense_form = ExpenseForm()
    budget_form = BudgetForm()
    savings_form = SavingsForm()

    if expense_form.validate_on_submit():
        item = expense_form.item.data
        amount = expense_form.amount.data
        date = expense_form.date.data
        new_expense = Expense(item=item, amount=amount, date=date, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        generate_plot(current_user.id)  
        return redirect(url_for('index'))

    if budget_form.validate_on_submit():
        current_user.budget = budget_form.budget.data
        db.session.commit()
        flash('Budget updated successfully!', 'success')
        return redirect(url_for('index'))

    if savings_form.validate_on_submit():
        current_user.savings_goal = savings_form.savings_goal.data
        db.session.commit()
        flash('Savings goal updated successfully!', 'success')
        return redirect(url_for('index'))

    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total_expense = sum(exp.amount for exp in expenses)
    budget_left = current_user.budget - total_expense

    return render_template('index.html', expense_form=expense_form, budget_form=budget_form,
                           savings_form=savings_form, expenses=expenses, total_expense=total_expense,
                           budget_left=budget_left, savings_goal=current_user.savings_goal,
                           plot_url=url_for('static', filename='plot_{}.png'.format(current_user.id)))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
