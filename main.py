from flask import Flask, request, redirect
import os
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader
(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route('/', methods=['POST'])
def validate_inputs():
    
    user_name = request.form['user_name']
    password = request.form['password']
    password2 = request.form['password2']

    username_error = ''
    password_error = ''
    password2_error = ''
    blank_field_error = ''

    
    if not user_name.isalnum():
        username_error = 'Username must use alpha-numeric characters.'
        password = ''
        password2 = ''
    else:
        if len(user_name) > 20 or len(user_name) < 3:
            username_error = 'Username length must be (3-20) characters'
    
    if not password.isalnum():
        password_error = 'Password must use alpha-numeric characters.'
        password = ''
        password2 = ''
    else:
        if len(password) > 20 or len(password) < 3:
            password_error = 'Password length must be (3-20) characters'

    if password2 != password:
        password2_error = 'Passwords do not match'
        password = ''
        password2 = ''
    
    if user_name == '' or password == '' or password2 == '':
        blank_field_error = 'Please complete form'
        password = ''
        password2 = ''
    
    if not username_error and not password_error and not password2_error:
        return redirect('/welcome?user_name={0}'.format(user_name))
    else:
        template = jinja_env.get_template('index.html')
        return template.render(blank_field_error=blank_field_error,password_error=password_error,password2_error=password2_error,
               username_error=username_error,user_name=user_name,password=password,password2=password2)

@app.route('/welcome')
def welcome():
    user_name = request.args.get('user_name')
    template = jinja_env.get_template('welcome.html')
    return template.render(user_name=user_name)


app.run()