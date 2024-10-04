from flask import Flask, render_template, request, redirect, url_for
from xml.dom import NotFoundErr
import pymysql
# from dotenv import load_dotenv      #development purpose only
from database import credentials, Rides, rides_data
import os

app = Flask(__name__)
# load_dotenv()

# ridesInstance = Rides()     #instantiate class for this session
# ridesInstance.initialize_rides(rides_data)

# init db connection
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USERNAME'),
        password=os.environ.get('MYSQL_PASSWORD'),
        port=int(os.environ.get('MYSQL_PORT', 3306)),
        db=os.environ.get('MYSQL_DBNAME'),
        cursorclass=pymysql.cursors.DictCursor
    )


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

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rides")
        rides = cursor.fetchall()
    connection.close()

    if usertype == 'admin':
        if request.method == 'POST':
            print('post')
        return render_template('/admin_dashboard.html', rides=rides)

    if request.method == 'POST':
        age = int(request.form['age'])
        height = int(request.form['height'])

        total_price = 0
        # Filtering rides based on age and height
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * from rides where age_limit<={age} and height_limit<= {height}")
            available_rides = cursor.fetchall()
        connection.close()

        for ride in available_rides:
            total_price += ride.get('price')

        return render_template('result.html', available_rides=available_rides, total_price=total_price, age=age, height=height)

    return render_template('index.html',rides=rides, usertype=usertype)


@app.route('/rides/add-ride', methods=['GET', 'POST'])
def add_ride():             # url-for looks for the function that handles itm and not the route.
    if request.method == 'POST':
        name = request.form.get('name')
        age_limit = int(request.form['age_limit'])
        height_limit = int(request.form['height_limit'])
        price = int(request.form.get('price'))

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO rides (name, age_limit, height_limit, price) VALUES (%s, %s, %s, %s)",
                    (name, age_limit, height_limit, price)
                )
                connection.commit()
            print("Added successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()

        return redirect('/home/admin')

    return render_template('newride.html')

@app.route('/rides/remove-ride')
def remove_ride():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"DELETE from rides where name='{request.args.get('ride')}'"
            )
            connection.commit()
    except NotFoundErr as nfe:
        print(nfe)
    except Exception as e:
        print('db exception', e)
    finally:
        connection.close()
        return redirect(url_for('home', usertype='admin'))
        # return render_template('admin_dashboard.html', rides = ridesInstance.get_rides())   # cant use redirect here because we are inside rides/

@app.route('/rides/update-ride', methods=['GET', 'POST'])
def update_ride():
    name = request.args.get('ride')
    print(name)
    if request.method == 'POST':
        connection = get_db_connection()
        info = {}
        if len(request.form.get('age_limit')) :
            info['age_limit'] = request.form.get('age_limit')
        if len(request.form.get('height_limit')) :
            info['height_limit'] = request.form.get('height_limit')
        if len(request.form.get('price')) :
            info['price'] = request.form.get('price')

        set_clause = []
        for key, value in info.items():
            set_clause.append(f"{key} = %s")  # Using %s for parameterized queries

        set_clause_str = ', '.join(set_clause)
        try:
            with connection.cursor() as cursor:
                query = f"UPDATE rides SET {set_clause_str} WHERE name = %s"
                print('query', query)
                cursor.execute(query, (*info.values(), name))
                connection.commit()

        except Exception as e:
            print(e)
        finally:
            return redirect(url_for('home', usertype='admin'))
    return render_template('editride.html', ride=name)

if __name__ == "__main__":
    app.run(
        port=7340,
        debug=True,
        host="0.0.0.0"
    )

