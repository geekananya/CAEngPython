from database import credentials, rides
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def check_credentials(user, passw):
    # from database import credentials
    for cred in credentials:
        # print(cred)
        if cred['username'] == user and cred['password'] == passw:
            if cred['username'] == 'admin':
                return 'admin'
            else:
                return 'user'
    return False

@app.route('/', methods=['GET'])
def index():
    print('on root route')
    return redirect('/login', 302)

@app.route('/login', methods=['GET', 'POST'])       # to tell which methods this route will respond to (by default, only GET)
def login():
    error = None
    if request.method == 'POST':
        res = check_credentials(request.form.get('username'), request.form.get('password'))
        if res:
            return redirect(f'/home/{res}')
        else:
            error = 'Invalid username/password'

    return render_template('login.html', error=error)

@app.route('/home/<usertype>', methods=['GET', 'POST'])
def home(usertype):

    # if usertype == 'admin':
    #     if request.method == 'POST':
    #
    #     return render_template('/admin_dashboard.html')

    if request.method == 'POST':
        age = int(request.form['age'])
        height = int(request.form['height'])

        # Filtering rides based on age and height
        available_rides = []
        total_price = 0

        for ride in rides:
            if age >= ride["age_limit"] and (ride["height_limit"] == 0 or height >= ride["height_limit"]):
                available_rides.append(ride)
                total_price += ride["price"]

        return render_template('result.html', available_rides=available_rides, total_price=total_price, age=age, height=height)

    return render_template('index.html',rides=rides, usertype=usertype)

if __name__ == "__main__":
    app.run(debug=True)