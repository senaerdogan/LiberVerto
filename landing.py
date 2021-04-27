from initialization import cnx, cur
from flask import  render_template, url_for, redirect, request, session, Blueprint


landing = Blueprint('landing', __name__)

def signup(name, address, phonenumber, email, password):
    try:
        sql = '''INSERT INTO user_ (name_, email, password_, phone_number, address) values (%s, %s, %s, %s, %s)'''
        values = (name, email, password, phonenumber, address)
        cur.execute(sql, values)
        cnx.commit()
        return "successful"
    except Exception as e:
        return "error"

    # exception for too long entries
    except Exception as e:
        return "exception occured"

def login(email, password):
    try:
        sql = '''SELECT * FROM user_ WHERE email = %s and password_ = %s'''
        values = (email, password)
        cur.execute(sql, values)
        account = cur.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['name_']
            return (1, account['name_'])
        else:
            return (0, 'incorrect email or password')

    except Exception as e:
        return (0, e)

@landing.route("/", methods=['GET', 'POST'])
def landingpage():
    err_message = ''
    name= ''
    if request.method == 'POST':
        if request.form['access_system_btn'] == 'signup_btn':
            try:
                return_message = signup(request.form['name'], request.form['address'],
                                        request.form['phonenumber'], request.form['email'], request.form['password'])
                if (return_message == "successful"):
                    err_message = "new user created succesfully, you can login now"
                elif (return_message == "phone_number"):
                    err_message= "this phone number is being used by somebody else"
                elif (return_message == "email"):
                    err_message = "this email is being used by somebody else"
                else:
                    err_message= "exception occured"
            except Exception as e:
                print("exception occured in sign up form")

        elif request.form["access_system_btn"] == 'login_btn':
            try:
                email = request.form['email']
                password = request.form['password']
                name = login(email, password)
                if name[0] == 1:
                    name = name[1]
                    return redirect(url_for('main.mainpage'))
                else:
                    err_message = 'Invalid login credentials'

            except Exception as e:
                print(e)
                err_message = "exception occured login form"

    return render_template('landingpage.html', err_message=err_message)

@landing.route("/signout")
def signout():
    session.pop('username')
    return redirect( url_for('.landingpage'))