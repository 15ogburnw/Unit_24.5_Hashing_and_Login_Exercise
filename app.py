
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.route('/')
def redirect_to_register():

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_new_user():

    form = RegisterUserForm()

    if form.validate_on_submit():
        user = {
            'username': form.data['username'],
            'password': form.data['password'],
            'email': form.data['email'],
            'first_name': form.data['first_name'],
            'last_name': form.data['last_name']
        }

        user = User.register(**user)

        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        return redirect(f'/users/{user.username}')

    if 'username' in session:
        session_user = session['username']
        flash('Please logout first!', 'danger')
        return redirect(f'/users/{session_user}')

    return render_template('register-user-form.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginUserForm()

    if form.validate_on_submit():

        username = form.data['username']
        password = form.data['password']

        user = User.authenticate(username=username, password=password)

        if user:
            session['username'] = user.username
            flash(f'Welcome back {user.username}!', 'success')
            return redirect(f'/users/{user.username}')

        else:
            form.password.errors.append(
                'Incorrect Username/Password! Please try again')

    if 'username' in session:
        session_user = session['username']
        flash('You are already logged in!', 'danger')
        return redirect(f'/users/{session_user}')

    return render_template('login-form.html', form=form)


@app.route('/logout')
def logout():

    if 'username' in session:
        session.pop('username')
        flash('Successfully logged out!', 'success')
        return redirect('/login')

    flash('You are not logged in', 'info')
    return redirect('/login')


@app.route('/users/<username>')
def show_user_page(username):

    if 'username' not in session:
        flash('You are not authorized to view that page! Please login first', 'danger')
        return redirect('/login')

    user = User.query.get_or_404(username)
    feedback = user.feedback

    return render_template('user-info.html', user=user, feedback=feedback)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):

    if 'username' in session and session['username'] == username:

        user = User.query.get_or_404(username)

        db.session.delete(user)
        db.session.commit()
        session.pop('username')

        flash('User Profile successfully deleted!', 'success')
        return redirect('/login')

    flash('You do not have permission do perform that action!')
    return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):

    form = FeedbackForm()
    user = User.query.get_or_404(username)

    if 'username' in session and session['username'] == username:

        if form.validate_on_submit():

            title = form.data['title']
            content = form.data['content']

            new_feedback = Feedback(
                title=title, content=content, username=username)

            db.session.add(new_feedback)
            db.session.commit()

            flash('Feedback successfully posted!', 'success')
            return redirect(f'/users/{username}')

        return render_template('feedback-form.html', form=form, user=user)

    elif 'username' in session and session['username'] != username:

        session_user = session['username']
        flash('You cannot add feedback for another user!', 'danger')
        return redirect(f'/users/{session_user}')

    flash('Please login!', 'danger')
    return redirect('/login')


@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)

    form = FeedbackForm(obj=feedback)
    user = feedback.user

    if 'username' in session and session['username'] == user.username:

        if form.validate_on_submit():

            title = form.data['title']
            content = form.data['content']

            feedback.title = title
            feedback.content = content

            db.session.add(feedback)
            db.session.commit()

            flash('Feedback successfully updated!', 'success')
            return redirect(f'/users/{user.username}')

        return render_template('feedback-form.html', form=form, user=user)

    elif 'username' in session and session['username'] != user.username:

        session_user = session['username']
        flash("You cannot update another user's feedback!", 'danger')
        return redirect(f'/users/{session_user}')

    flash('Please login!', 'danger')
    return redirect('/login')


@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.user

    if 'username' in session and session['username'] == user.username:

        db.session.delete(feedback)
        db.session.commit()

        flash('Feedback successfully deleted!', 'success')
        return redirect(f'/users/{user.username}')

    elif 'username' in session and session['username'] != user.username:
        session_user = session['username']
        flash("You cannot delete another user's feedback", 'danger')
        return redirect(f'users/{session_user}')

    flash('Please login!', 'danger')
    return redirect('/login')
