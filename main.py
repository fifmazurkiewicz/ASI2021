import datetime
import os
import pickle
import random

import pandas as pd
from flask import Flask, flash, render_template, request, session

from pogoda import pobierzpogode
from register import User, Grade, return_sqlalchemysession

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static',
)

app.secret_key = os.urandom(12)


@app.route("/predict", methods=["POST", "GET"])
def predict_prize():
    encoder_dict = pickle.load(open("labels.pkl", "rb"))
    xgb_model_loaded = pickle.load(open("xgb_depth10.pkl", "rb"))
    Vehicle_brand = request.args.get('Vehicle_brand')
    try:
        if Vehicle_brand:
            Production_year = request.args.get('Production_year')
            Mileage_km = request.args.get('Mileage_km')
            Power_HP = request.args.get('Power_HP')
            Displacement_cm3 = request.args.get('Displacement_cm3')
            Doors_number = request.args.get('Doors_number')
            Condition = request.args.get('Condition').lower()
            Vehicle_brand = request.args.get('Vehicle_brand').lower()
            Vehicle_model = request.args.get('Vehicle_model').lower()
            Drive = request.args.get('Drive').lower()
            Transmission = request.args.get('Transmission').lower()
            Type = request.args.get('Type').lower()
            new_pred = {
                "row": [Production_year, Mileage_km, Power_HP, Displacement_cm3, Doors_number, Condition, Vehicle_brand,
                        Vehicle_model, Drive, Transmission, Type]}
            new_pred = pd.DataFrame.from_dict(new_pred, orient='index',
                                              columns=['Production_year', 'Mileage_km', 'Power_HP', 'Displacement_cm3',
                                                       'Doors_number', 'Condition', 'Vehicle_brand',
                                                       'Vehicle_model', 'Drive', 'Transmission', 'Type'])
            new_pred = new_pred.replace(to_replace={"": 0})
            new_data_prediction = new_pred.replace(encoder_dict)
            result = round(xgb_model_loaded.predict(new_data_prediction.values)[0],2)
            return render_template("price_car.html", result=result)
        else:
            flash("Enter at least brand name", 'danger')
            return render_template('price_car.html')
    except Exception as exp:
        print(exp)
        flash("Please try again", 'danger')
        return render_template('price_car.html')


@app.route('/test_bootstrap')
def testujemy_base():
    return render_template('base_front.html', title='ASI2021')


@app.route('/')
def home():
    if not session.get('logged_in'):
        print(session)
        return render_template('logowanie.html', session=session)
    else:
        return render_template('base_front.html', session=session)


# Z formularza z template logowanie, POST
@app.route('/login', methods=["POST"])
def login_user():
    pepper = 'UEPxD'
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password']) + pepper
    sqlsession = return_sqlalchemysession()
    query = sqlsession.query(User).filter(User.username.in_([POST_USERNAME]))
    try:
        user = query.first()
        if user:
            logged = user.check_password(POST_PASSWORD)
            if logged:
                session['logged_in'] = True
                return home()
            else:
                flash('No user or wrong password provided',"danger")
                return render_template('logowanie.html')
        else:
            flash('No user or wrong password provided',"danger")
            return render_template('logowanie.html')
    except AttributeError as e:
        flash('No user or wrong password provided',"danger")
    return home()


@app.route('/wyloguj')
def wyloguj():
    session['logged_in'] = False
    return home()


@app.route('/register', methods=['POST', 'GET'])
def do_register():
    pepper = "UEPxD"
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password']) + pepper
    sqlsession = return_sqlalchemysession()
    # hashed_password = generate_password_hash(POST_PASSWORD)
    user = User(username=POST_USERNAME, password=POST_PASSWORD)
    try:
        query = sqlsession.query(User).filter(User.username.in_([POST_USERNAME]))
        # jezeli istnieje juz taka sama nazwa uzytkownika w bazie, blokujemy rejestracje
        query = query.first()
        if query:
            flash('Wybierz inną  nazwę użytkownika', "danger")
            return return_registrationpage()
        else:
            sqlsession.add(user)
            sqlsession.commit()
            sqlsession.close()
            return home()
    except Exception as exp:
        flash('Wybierz inną nazwę użytkownika', "danger")
    return return_registrationpage()


@app.route('/signup', methods=["GET"])
def return_registrationpage():
    return render_template('signup.html')


@app.route("/weather", methods=["POST", "GET"])
def showweather():
    search = request.args.get('search')
    try:
        if search:
            temp, humid, weathertype, rain, city, country = pobierzpogode(search)
            return render_template("weather.html", temp=temp, humid=humid, weathertype=weathertype, rain=rain,
                                   city=city,
                                   country=country)
        else:
            return render_template('weather.html')
    except:
        flash("Enter the name of the city", 'danger')
        return render_template('weather.html')


@app.route('/grades', methods=['GET'])
def return_grades():
    sqlsession = return_sqlalchemysession()
    grades = sqlsession.query(Grade).all()
    return render_template("grades.html", grades=grades)


## Dodawanie nowych ocen (patrz na dol tabelki)
@app.route('/addgrade', methods=['GET'])
def grades():
    if not session.get('logged_in'):
        return render_template('logowanie.html')
    else:
        gradeval = random.choice(['2', '3', '3.5', '4', '4.5', '5'])
        user_id = 99
        added_date = datetime.date.today()
        grade = Grade(gradeval, added_date, user_id)
        sqlsession = return_sqlalchemysession()
        sqlsession.add(grade)
        sqlsession.commit()
        return return_grades()


if __name__ == "__main__":
  # app.run(
  #   host='0.0.0.0',
  #   port=8080, debug=True)
    app.run()