from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import mysql.connector as msql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session and flash messages

CSV_FILE = 'users.csv'

# Database connection
def connect_db():
    return msql.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="canteen_alpha"
    )

# Check if user exists in CSV
def user_exists(username):
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    return row
    except FileNotFoundError:
        return None
    return None

# Login/Signup page
@app.route('/')
def login_signup():
    return render_template('login_signup.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = user_exists(username)
    if user and user['password'] == password:
        session['username'] = username  # Store username in session
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password!', 'error')
        return redirect(url_for('login_signup'))

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if user_exists(username):
        flash('Username already exists!', 'error')
        return redirect(url_for('login_signup'))
    else:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['username', 'password'])
            if file.tell() == 0:  # Write header if file is empty
                writer.writeheader()
            writer.writerow({'username': username, 'password': password})
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login_signup'))

# Menu page
@app.route('/index')
def index():
    if 'username' not in session:
        flash('Please log in first!', 'error')
        return redirect(url_for('login_signup'))

    db = connect_db()
    mycursor = db.cursor(dictionary=True)
    mycursor.execute('SELECT * FROM menu')
    menu = mycursor.fetchall()
    db.close()
    return render_template('index.html', menu=menu, username=session['username'])

# Bill page
@app.route('/bill', methods=['POST'])
def bill():
    if 'username' not in session:
        flash('Please log in first!', 'error')
        return redirect(url_for('login_signup'))

    username = session['username']
    item_nos = request.form.getlist('item_no')  # Get selected item numbers

    items = []
    total_cost = 0
    for item_no in item_nos:
        quantity = request.form.get(f'quantity_{item_no}')  # Get quantity for selected item
        db = connect_db()
        mycursor = db.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM menu WHERE Sno = %s', (item_no,))
        item = mycursor.fetchone()
        
        if item:
            total_cost += item['Price'] * int(quantity)
            items.append({
                'Itemname': item['Itemname'],
                'Quantity': quantity,
                'Price': item['Price'],
                'Total': item['Price'] * int(quantity)
            })
        db.close()

    return render_template('bill.html', username=username, items=items, total_cost=total_cost)

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login_signup'))

if __name__ == "__main__":
    app.run(debug=True)
