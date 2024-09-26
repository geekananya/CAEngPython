from xml.dom import NotFoundErr

from database import credentials, Rides, rides_data
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
ridesInstance = Rides()     #instantiate class for this session
ridesInstance.initialize_rides(rides_data)


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
    if usertype == 'admin':
        if request.method == 'POST':
            print('post')
        return render_template('/admin_dashboard.html', rides = ridesInstance.get_rides())

    if request.method == 'POST':
        age = int(request.form['age'])
        height = int(request.form['height'])

        # Filtering rides based on age and height
        available_rides = []
        total_price = 0

        for ride in ridesInstance.get_rides():
            if age >= ride.age_limit and (ride.height_limit == 0 or height >= ride.height_limit):
                available_rides.append(ride)
                total_price += ride.price

        return render_template('result.html', available_rides=available_rides, total_price=total_price, age=age, height=height)

    return render_template('index.html',rides=ridesInstance.get_rides(), usertype=usertype)


@app.route('/rides/add-ride', methods=['GET', 'POST'])
def add_ride():             # url-for looks for the function that handles itm and not the route.
    if request.method == 'POST':
        name = request.form.get('name')
        age_limit = int(request.form['age_limit'])
        height_limit = int(request.form['height_limit'])
        price = int(request.form.get('price'))

        ridesInstance.add_ride(name=name, age_limit=age_limit, height_limit=height_limit, price=price)

        print("added successfully")
        return redirect('/home/admin')

    return render_template('newride.html')

@app.route('/rides/remove-ride')
def remove_ride():
    try:
        ridesInstance.remove_ride(request.args.get('ride'))
    except NotFoundErr as nfe:
        print(nfe)
    finally:
        return redirect(url_for('home', usertype='admin'))
        # return render_template('admin_dashboard.html', rides = ridesInstance.get_rides())   # cant use redirect here because we are inside rides/

@app.route('/rides/update-ride')
def update_ride():
    name = request.args.get('ride')
    print(name)
    if request.method == 'POST':
        try:
            info = {}
            if request.form.get('age_limit') is not None:
                info['age_limit'] = request.form.get('age_limit')
            if request.form.get('height_limit') is not None:
                info['height_limit'] = request.form.get('height_limit')
            if request.form.get('price') is not None:
                info['price'] = request.form.get('price')
            ridesInstance.add_ride(name, info)

        except Exception as e:
            print(e)
        finally:
            return redirect('/home/admin')
    return render_template('editride.html', ride=name)

if __name__ == "__main__":
    app.run(debug=True)

