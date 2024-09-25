from flask import Flask, render_template, request

app = Flask(__name__)

rides = [
    {"name": "Roller Coaster", "age_limit": 12, "height_limit": 140, "price": 10},
    {"name": "Ferris Wheel", "age_limit": 0, "height_limit": 0, "price": 5},
    {"name": "Bumper Cars", "age_limit": 8, "height_limit": 120, "price": 7},
    {"name": "Haunted House", "age_limit": 10, "height_limit": 0, "price": 8},
    {"name": "Merry-Go-Round", "age_limit": 0, "height_limit": 0, "price": 4},
    {"name": "Water Slide", "age_limit": 5, "height_limit": 100, "price": 6},
    {"name": "Log Flume", "age_limit": 6, "height_limit": 110, "price": 7},
    {"name": "Swing Ride", "age_limit": 0, "height_limit": 0, "price": 5},
    {"name": "Drop Tower", "age_limit": 12, "height_limit": 130, "price": 9},
    {"name": "Go-Karts", "age_limit": 10, "height_limit": 130, "price": 15},
]

def check_credentials(user, passw):
    from database import credentials
    for cred in credentials:
        if cred.username == user and cred.password == passw:
            if cred.username == 'admin':
                return 'admin'
            else:
                return 'user'
    return False

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        res = check_credentials(request.form['username'], request.form['password'])
        if res:
            return render_template(index.html)
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

@app.route('/', methods=['GET', 'POST'])
def index():
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

    return render_template('index.html',rides=rides)

if __name__ == "__main__":
    app.run(debug=True)