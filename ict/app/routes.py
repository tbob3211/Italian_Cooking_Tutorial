from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, EditProfileForm
from datetime import datetime

@app.route('/')
def tester():
    return render_template('Theme.html')
    
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        #return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/Theme')
def test(): 
     return render_template('Theme.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/Assessment', methods=['GET', 'POST'])
@login_required
def Assessment():
    return render_template('Assignment.html', title='Assignment')


# @app.route('/feedback')
# def feedback():
#     @login_required 
#     #post = Post(body=request.form['answers'], score=request.form['score'])
#     db.session.add(post)
#     db.session.commit()
#     count = db.session.execute('select count(*) from Post where score <=' + request.form['score'] + '')
#     total = db.session.execute('select * from Post')
#     percentage = 100*count/total
#     return jsonify({'answers':request.form['answers']}),
#     #return render_template('feedback.html')
    


@app.route('/Statistic', methods=['GET', 'POST'])
@login_required
def Statistic():
    count = {}
    count1 = db.session.execute('select count(*) from Post where score <= 25')
    count2 = db.session.execute('select count(*) from Post where score <= 50')
    count3 = db.session.execute('select count(*) from Post where score <= 75')
    count4 = db.session.execute('select count(*) from Post where score <= 100')
    count["25"] = count1
    count["50"] = count2
    count["75"] = count3
    count["100"] = count4
    UP = db.session.execute('SELECT COUNT(*) FROM USER')
    GP = db.session.execute('SELECT COUNT(*) FROM POST')
    return jsonify({'count':count, 'Usercount':UP, 'Gradcount':GP}),render_template('Statistic.html', title='Feedback')

@app.route('/pizza')
def pizza(): 
     return render_template('Pizza.html', title='Pizza')

@app.route('/risotto')
def risotto(): 
     return render_template('Risotto.html', title='Risotto')

@app.route('/pasta')
def pasta(): 
     return render_template('sausage_pasta.html', title='Pasta')

@app.route('/minestrone_soup')
def minestrone_soup(): 
     return render_template('Minestrone_Soup.html', title='Minestrone_soup')

@app.route('/tiramisu')
def tiramisu(): 
     return render_template('Tiramisu.html', title='Tiramisu')

@app.route('/entree')
def entree(): 
     return render_template('arancini.html', title='Entree')
