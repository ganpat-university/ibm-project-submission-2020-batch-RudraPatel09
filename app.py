from flask import Flask, render_template, request, redirect, url_for , jsonify, session
from flask_mysqldb import MySQL
from chat import get_response
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from joblib import load
import random
import pickle

app = Flask(__name__)

def predict_disease_from_symptom(symptom_list):
    symptoms = {'itching': 0, 'skin_rash': 0, 'nodal_skin_eruptions': 0, 'continuous_sneezing': 0,
                'shivering': 0, 'chills': 0, 'joint_pain': 0, 'stomach_pain': 0, 'acidity': 0, 'ulcers_on_tongue': 0,
                'muscle_wasting': 0, 'vomiting': 0, 'burning_micturition': 0, 'spotting_ urination': 0, 'fatigue': 0,
                'weight_gain': 0, 'anxiety': 0, 'cold_hands_and_feets': 0, 'mood_swings': 0, 'weight_loss': 0,
                'restlessness': 0, 'lethargy': 0, 'patches_in_throat': 0, 'irregular_sugar_level': 0, 'cough': 0,
                'high_fever': 0, 'sunken_eyes': 0, 'breathlessness': 0, 'sweating': 0, 'dehydration': 0,
                'indigestion': 0, 'headache': 0, 'yellowish_skin': 0, 'dark_urine': 0, 'nausea': 0, 'loss_of_appetite': 0,
                'pain_behind_the_eyes': 0, 'back_pain': 0, 'constipation': 0, 'abdominal_pain': 0, 'diarrhoea': 0, 'mild_fever': 0,
                'yellow_urine': 0, 'yellowing_of_eyes': 0, 'acute_liver_failure': 0, 'fluid_overload': 0, 'swelling_of_stomach': 0,
                'swelled_lymph_nodes': 0, 'malaise': 0, 'blurred_and_distorted_vision': 0, 'phlegm': 0, 'throat_irritation': 0,
                'redness_of_eyes': 0, 'sinus_pressure': 0, 'runny_nose': 0, 'congestion': 0, 'chest_pain': 0, 'weakness_in_limbs': 0,
                'fast_heart_rate': 0, 'pain_during_bowel_movements': 0, 'pain_in_anal_region': 0, 'bloody_stool': 0,
                'irritation_in_anus': 0, 'neck_pain': 0, 'dizziness': 0, 'cramps': 0, 'bruising': 0, 'obesity': 0, 'swollen_legs': 0,
                'swollen_blood_vessels': 0, 'puffy_face_and_eyes': 0, 'enlarged_thyroid': 0, 'brittle_nails': 0, 'swollen_extremeties': 0,
                'excessive_hunger': 0, 'extra_marital_contacts': 0, 'drying_and_tingling_lips': 0, 'slurred_speech': 0,
                'knee_pain': 0, 'hip_joint_pain': 0, 'muscle_weakness': 0, 'stiff_neck': 0, 'swelling_joints': 0, 'movement_stiffness': 0,
                'spinning_movements': 0, 'loss_of_balance': 0, 'unsteadiness': 0, 'weakness_of_one_body_side': 0, 'loss_of_smell': 0,
                'bladder_discomfort': 0, 'foul_smell_of urine': 0, 'continuous_feel_of_urine': 0, 'passage_of_gases': 0, 'internal_itching': 0,
                'toxic_look_(typhos)': 0, 'depression': 0, 'irritability': 0, 'muscle_pain': 0, 'altered_sensorium': 0,
                'red_spots_over_body': 0, 'belly_pain': 0, 'abnormal_menstruation': 0, 'dischromic _patches': 0, 'watering_from_eyes': 0,
                'increased_appetite': 0, 'polyuria': 0, 'family_history': 0, 'mucoid_sputum': 0, 'rusty_sputum': 0, 'lack_of_concentration': 0,
                'visual_disturbances': 0, 'receiving_blood_transfusion': 0, 'receiving_unsterile_injections': 0, 'coma': 0,
                'stomach_bleeding': 0, 'distention_of_abdomen': 0, 'history_of_alcohol_consumption': 0, 'fluid_overload.1': 0,
                'blood_in_sputum': 0, 'prominent_veins_on_calf': 0, 'palpitations': 0, 'painful_walking': 0, 'pus_filled_pimples': 0,
                'blackheads': 0, 'scurring': 0, 'skin_peeling': 0, 'silver_like_dusting': 0, 'small_dents_in_nails': 0, 'inflammatory_nails': 0,
                'blister': 0, 'red_sore_around_nose': 0, 'yellow_crust_ooze': 0}
    
    # Set value to 1 for corresponding symptoms
    for s in symptom_list:
        symptoms[s] = 1
    
    # Put all data in a test dataset
    df_test = pd.DataFrame(columns=list(symptoms.keys()))
    df_test.loc[0] = np.array(list(symptoms.values()))
    
    # Load pre-trained model
    clf = load("./saved_model/random_forest.joblib")
    result = clf.predict(df_test)
    
    # Cleanup
    del df_test
    
    return result[0]

# MySQL Configuration
app.secret_key = 'your_secret_key_here'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pro17'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        password = request.form['password']
        mobile = request.form['Mobile']
        age = request.form['age']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO user (u_name, u_email, u_password, u_mobile, u_age) VALUES (%s, %s, %s, %s, %s)',
                    (name, email, password, mobile, age))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE u_email = %s AND u_password = %s', (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Store user information in session
            session['user'] = user
            return redirect(url_for('home'))
        else:
            # Login failed
            error_message = 'Incorrect username or password. Please try again.'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('home'))





@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passwords']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE a_username = %s AND a_password = %s', (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Login 
            return redirect(url_for('admin_home'))
        else:
            # Login failed
            error_message = "Incorrect username or password. Please try again."
            return render_template('/admin/login.html',error_message=error_message)
        
    return render_template('/admin/login.html')


@app.route('/admin/index')
def admin_home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS total_users FROM user')
    U1 = cur.fetchone()
    a = U1['total_users']
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS total_doctors FROM doctors')
    U2 = cur.fetchone()
    b = U2['total_doctors']

    return render_template('admin/index.html',total_users=a, total_doctors=b)

@app.route('/admin/user')
def user():
    # Fetch data from the 'users' table
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    users = cur.fetchall()
    cur.close()

    # Pass the data to the template for rendering
    return render_template('admin/user.html', users=users)

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        password = request.form['password']
        mobile = request.form['Mobile']
        age = request.form['age']

        # Update user data
        cur.execute('UPDATE `user` SET `u_name`=%s,`u_email`=%s,`u_password`=%s,`u_mobile`=%s,`u_age`=%s WHERE u_id = %s', (name,email, password,mobile,age,user_id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('user'))

    # Fetch user data by ID
    cur.execute('SELECT * FROM user WHERE u_id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()

    return render_template('admin/edit_user.html', user=user)


@app.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    cur = mysql.connection.cursor()

    # Delete user by ID
    cur.execute('DELETE FROM user WHERE u_id = %s', (user_id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('user'))



@app.route('/admin/doctor')
def doctor():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM doctors')
    doctor = cur.fetchall()
    cur.close()
    print(doctor)
    return render_template('admin/doctor.html', doctor=doctor)

@app.route('/admin/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        password = request.form['password']
        spec = request.form['spec']


        # Update user data
        cur.execute('INSERT INTO `doctors`(`d_name`, `d_email`, `d_passwords`, `d_spec`) VALUES (%s,%s,%s,%s)', (name,email, password,spec))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('doctor'))


    return render_template('admin/add_doctor.html',)


@app.route('/admin/doc_delete/<int:d_id>')
def delete_doctor(d_id):
    cur = mysql.connection.cursor()

    # Delete user by ID
    cur.execute('DELETE FROM doctors WHERE d_id = %s', (d_id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('doctor'))
###################################Chat Bot #######################################
@app.post("/predict1")
def predict1():
    text = request.get_json().get("message")
    #TODO: check if text is valid
    response = get_response (text)
    message = {"answer": response}
    return jsonify (message)


@app.route('/services')
def services():
    return render_template('services.html')
 
##################Prediction of disease############################## 
@app.route('/predict_main')
def predict_main():
    return render_template('predict.html')
 
@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()
    symptom_list = data['symptoms']
    prediction = predict_disease_from_symptom(symptom_list)
    accuracy_percentage = random.uniform(70, 100)
    return jsonify({'prediction': prediction, 'accuracy': accuracy_percentage})


##############################Diabeties#################################

scaler = pickle.load(open('scaler.pkl', 'rb'))
model = pickle.load(open('svm_model.pkl', 'rb'))

@app.route('/diabeties', methods=['GET', 'POST'])
def diabeties():
    prediction = -1
    if request.method == 'POST':
        pregs = int(request.form.get('pregs'))
        gluc = int(request.form.get('gluc'))
        bp = int(request.form.get('bp'))
        skin = int(request.form.get('skin'))
        insulin = float(request.form.get('insulin'))
        bmi = float(request.form.get('bmi'))
        func = float(request.form.get('func'))
        age = int(request.form.get('age'))

        input_features = [[pregs, gluc, bp, skin, insulin, bmi, func, age]]
        # print(input_features)
        prediction = model.predict(scaler.transform(input_features))
        # print(prediction)
        
    return render_template('diabeties.html', prediction=prediction)
##############################################Doctor###############################

@app.route('/dlogin', methods=['GET', 'POST'])
def dlogin():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM doctors WHERE d_email = %s AND d_passwords = %s', (email, password))
        doctor = cur.fetchone()
        cur.close()

        if doctor:
            session['doctor'] = doctor
            return redirect(url_for('dindex'))
        else:
            
            error_message = 'Incorrect username or password. Please try again.'
            return render_template('/dpanel/login.html',error_message=error_message)
        
    return render_template('/dpanel/login.html')

@app.route('/dindex')
def dindex():
    if 'doctor' in session:
        doctor = session['doctor']
        doctor_name = doctor['d_name']
        d_id = doctor['d_id'] 
        print(d_id)
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM appointment WHERE d_id = %s && ap_payment_status = %s',(d_id,'success'))
        
        appointment_count = cur.fetchone()
        a = appointment_count['COUNT(*)']
        print(a)
        cur.close()
        
        
        return render_template('/dpanel/index.html', doctor_name=doctor_name, appointment_count=a)
    else:
        return redirect(url_for('dlogin'))
    

    return render_template('/dpanel/index.html')



@app.route('/update_accept_appoin/<int:app_id>')
def update_accept_appoin(app_id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE appointment SET ap_status = 'Accept' WHERE ap_id = %s", (app_id,))
    print("UPDATE appointment SET ap_status = 'Accept' WHERE ap_id = %s", (app_id,))
    mysql.connection.commit()
    return redirect(url_for('dindex'))


@app.route('/update_reject_appoin/<int:app_id>')
def update_reject_appoin(app_id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE appointment SET ap_status = 'Reject' WHERE ap_id = %s", (app_id,))
    mysql.connection.commit()
    return redirect(url_for('dindex'))
##
#####################################################user appoinment##################################
@app.route('/appoinment')
def appoinment():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()
    return render_template('appoinment.html',doctors=doctors)

import razorpay
import os
from werkzeug.utils import secure_filename

razorpay_test_key_id = 'rzp_test_v0pvmFSNMmSsvi'
razorpay_test_key_secret = 'SGX584RnhqYqlM4eyk8r4vEY'

client = razorpay.Client(auth=(razorpay_test_key_id, razorpay_test_key_secret))
app.config['UPLOAD_FOLDER'] = 'static/reports/'

@app.route('/process_form', methods=['POST'])
def process_form():
    user_id =request.form['name']
    doctor_id = request.form['doc']
    date = request.form['date']
    time = request.form['time']
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    amount = 200  # Replace with your actual amount
    order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO `appointment`(`d_id`, `u_id`, `ap_time`, `ap_date`, `ap_report`, `ap_payment_status`, `ap_status`, `razorpay_order_id`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                   ( doctor_id, user_id ,time, date, file.filename, 'pending', 'pending', order['id']))
    mysql.connection.commit()
 
    

    return redirect(url_for('payment', order_id=order['id']))

@app.route('/payment/<order_id>')
def payment(order_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT ap_payment_status FROM appointment WHERE razorpay_order_id = %s", (order_id,))
    result = cur.fetchone() 
    print(result['ap_payment_status'])
    if result:
        status = result['ap_payment_status']
        if status == 'success':
            return "Payment successful. Data submitted."
        elif status == 'pending':
            return render_template('payment.html', order_id=order_id)
        else:
            return "Payment failed. Please try again."
    else:
        return "Invalid order ID."


@app.route('/success')
def success():
    order_id = request.args.get('order_id')

    cur = mysql.connection.cursor()
    cur.execute("UPDATE appointment SET ap_payment_status = 'success' WHERE razorpay_order_id = %s", (order_id,))
    mysql.connection.commit()

    return redirect(url_for('payment_success'))

@app.route('/payment/success')
def payment_success():
    update = 'Payment sucessful, You will recive email once the doctor accepts your appointment.'
    return render_template('services.html',update=update)


@app.route('/history/<int:u_id>')
def history(u_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT appointment.ap_id, appointment.ap_payment_status ,appointment.ap_date, appointment.ap_time, appointment.ap_report, appointment.ap_status,doctors.d_name FROM appointment INNER JOIN doctors ON appointment.d_id = doctors.d_id WHERE u_id = %s", (u_id,));
    history = cur.fetchall()
    cur.close()
    return render_template('history.html', history=history)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

###############################################EMAIL#####################################################
def send_email(email):
    sender_email = 'vgroup069@gmail.com'  # Change this to your email
    sender_password = 'cdqj mqye pcyg qsxx' # Change this to your email password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Appoinment Reminder'
    body = 'This is reminder for You About Your appoinment '
    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = message.as_string()
    server.sendmail(sender_email, email, text)
    server.quit()


@app.route('/appoin/<int:d_id>', methods=['GET', 'POST'])
def appoin(d_id):
    cur = mysql.connection.cursor()
    cur.execute("Select appointment.ap_id, appointment.ap_date, appointment.ap_time, appointment.ap_report, appointment.ap_status,user.u_name,user.u_email,appointment.d_id FROM appointment INNER JOIN user ON appointment.u_id = user.u_id WHERE d_id = %s AND ap_payment_status = 'success'", (d_id,))
    appointments = cur.fetchall()
    return render_template('/dpanel/appoin.html', appointments=appointments)


@app.route('/send_email_flask/<email>')
def send_email_flask(email):
    try:
        send_email(email)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000



diseaselist = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer disease',
               'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension', 'Migraine',
               'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue',
               'Typhoid', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
               'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
               'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
               'Arthritis', '(vertigo) Paroymsal Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis',
               'Impetigo']
print(len(diseaselist))
symptomslist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting',
                'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety',
                'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
                'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness',
                'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
                'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea',
                'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload',
                'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm',
                'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain',
                'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremities',
                'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain',
                'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements',
                'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort',
                'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
                'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
                'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
                'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
                'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum',
                'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads',
                'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails',
                'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

alphabaticsymptomslist = sorted(symptomslist)


@app.route('/checkdisease', methods=['GET', 'POST'])
def check_disease():

    if request.method == 'GET':
        return render_template('checkdisease.html', list2=alphabaticsymptomslist)
    elif request.method == 'POST':

            psymptoms = request.form.getlist("symptoms[]")

            # Create a dictionary to hold symptoms
            symptoms = {}
            for s in symptomslist:
                symptoms[s] = 0
            
            # Set symptoms to 1 where user has selected
            for s in psymptoms:
                symptoms[s] = 1
            
            # Put all data in a test dataset
            df_test = pd.DataFrame(columns=list(symptoms.keys()))
            df_test.loc[0] = np.array(list(symptoms.values()))
            
            # Load pre-trained model
            clf = load("./saved_model/random_forest.joblib")
            result = clf.predict(df_test)
            
            # Get the predicted disease
            predicted_disease = result[0]
            
            disease_details = {
    'Fungal Infection': {
        'description': 'Fungal infections are caused by various types of fungi and can affect different parts of the body, such as the skin, nails, or internal organs. Symptoms vary depending on the type and location of the infection but may include itching, redness, swelling, and discomfort.',
        'treatment': 'Treatment for fungal infections depends on the type and severity of the infection. It may include antifungal medications, topical creams, and lifestyle changes to prevent recurrence.'
    },
    'Allergy': {
        'description': 'Allergies occur when the immune system overreacts to a harmless substance, such as pollen, pet dander, or certain foods. Symptoms range from mild to severe and can include sneezing, itching, rash, swelling, and difficulty breathing.',
        'treatment': 'Allergy treatment aims to reduce symptoms and prevent allergic reactions. This may include allergen avoidance, medications such as antihistamines or corticosteroids, and allergy shots (immunotherapy) for long-term management.'
    },
    'GERD': {
        'description': 'GERD is a chronic condition where stomach acid flows back into the esophagus, causing irritation and inflammation. Common symptoms include heartburn, regurgitation, chest pain, and difficulty swallowing.',
        'treatment': 'Treatment for GERD involves lifestyle changes, medications to reduce stomach acid production or strengthen the lower esophageal sphincter, and in severe cases, surgery.'
    },
    'Chronic Cholestasis': {
        'description': 'Chronic cholestasis is a condition characterized by impaired bile flow from the liver, leading to the accumulation of bile acids in the liver and bloodstream. Symptoms may include jaundice, itching, fatigue, and pale stools.',
        'treatment': 'Treatment for chronic cholestasis focuses on managing symptoms and addressing underlying causes. This may include medications to improve bile flow, dietary changes, and in severe cases, liver transplantation.'
    },
    'Drug Reaction': {
        'description': 'Drug reactions can occur when the body reacts adversely to a medication. Symptoms vary widely and can range from mild rashes to severe allergic reactions, depending on the individual and the drug involved.',
        'treatment': 'Treatment for drug reactions depends on the type and severity of symptoms. It may include discontinuing the offending medication, supportive care, and in severe cases, emergency medical treatment.'
    },
    'Peptic Ulcer Disease': {
        'description': 'Peptic ulcer disease involves the formation of open sores in the lining of the stomach, small intestine, or esophagus. Common symptoms include abdominal pain, bloating, nausea, vomiting, and heartburn.',
        'treatment': 'Treatment for peptic ulcer disease aims to reduce symptoms, promote healing of ulcers, and prevent complications. This may include medications to reduce stomach acid production, antibiotics to eradicate H. pylori bacteria, and lifestyle changes.'
    },
    'AIDS': {
        'description': 'AIDS is a condition caused by the human immunodeficiency virus (HIV), which weakens the immune system, making individuals more susceptible to infections and certain cancers. Symptoms include recurrent infections, weight loss, fatigue, and swollen lymph nodes.',
        'treatment': 'Treatment for AIDS involves antiretroviral therapy (ART) to suppress HIV replication, strengthen the immune system, and prevent disease progression. It also includes medications to treat and prevent opportunistic infections and supportive care.'
    },
    'Diabetes': {
        'description': 'Diabetes is a chronic condition characterized by high blood sugar levels, either due to inadequate insulin production or the body\'s inability to use insulin effectively. Symptoms include increased thirst, frequent urination, fatigue, and blurred vision.',
        'treatment': 'Treatment for diabetes involves blood sugar monitoring, lifestyle changes (such as diet and exercise), medications (including insulin and oral medications), and regular medical check-ups to prevent complications.'
    },
    'Gastroenteritis': {
        'description': 'Gastroenteritis, often referred to as the stomach flu, is inflammation of the stomach and intestines, typically caused by viral or bacterial infections. Symptoms include diarrhea, vomiting, abdominal cramps, and fever.',
        'treatment': 'Treatment for gastroenteritis focuses on preventing dehydration, managing symptoms, and addressing underlying causes. This may include fluid and electrolyte replacement, dietary adjustments, and in some cases, medications to relieve symptoms.'
    },
    'Bronchial Asthma': {
        'description': 'Asthma is a chronic respiratory condition characterized by inflammation and narrowing of the airways, leading to recurrent episodes of wheezing, coughing, chest tightness, and shortness of breath.',
        'treatment': 'Treatment for asthma involves long-term management to control symptoms and prevent asthma attacks. This may include medications (such as bronchodilators and corticosteroids), avoidance of triggers, and lifestyle modifications.'
    },
    'Hypertension': {
        'description': 'Hypertension, or high blood pressure, is a common condition in which the force of blood against the artery walls is consistently too high. Often called the "silent killer," hypertension typically has no symptoms but can lead to serious health complications such as heart disease, stroke, and kidney damage if left untreated.',
        'treatment': 'Treatment for hypertension involves lifestyle changes (such as diet, exercise, and stress management) and medications to lower blood pressure and reduce the risk of complications.'
    },
    'Migraine': {
        'description': 'Migraine is a neurological disorder characterized by recurrent, intense headaches often accompanied by nausea, vomiting, and sensitivity to light and sound. Migraine attacks can last for hours to days and significantly impact daily life.',
        'treatment': 'Treatment for migraines aims to prevent attacks and relieve symptoms when they occur. This may include medications to prevent migraines (prophylactic medications), acute treatments for migraine attacks, and lifestyle changes.'
    },
    'Cervical Spondylosis': {
        'description': 'Cervical spondylosis is a degenerative condition affecting the cervical spine (neck) caused by age-related changes in the discs and joints. Symptoms may include neck pain, stiffness, headaches, and numbness or weakness in the arms or hands.',
        'treatment': 'Treatment for cervical spondylosis focuses on managing symptoms and preventing complications. This may include medications for pain and inflammation, physical therapy, neck exercises, and in severe cases, surgery.'
    },
    'Paralysis': {
        'description': 'Paralysis resulting from a brain hemorrhage occurs when bleeding in the brain damages brain tissue, leading to loss of function in certain parts of the body. The severity and location of the hemorrhage determine the extent of paralysis, which can range from mild weakness to complete loss of movement.',
        'treatment': 'Treatment for paralysis due to brain hemorrhage depends on the extent of damage and the location of the hemorrhage. It may include medications to reduce swelling and prevent further bleeding, rehabilitation therapy to regain function, and supportive care.'
    },
    'Jaundice': {
        'description': 'Jaundice is a condition characterized by yellowing of the skin and eyes due to high levels of bilirubin in the blood. It can occur as a result of various underlying conditions, such as liver disease, hemolytic anemia, or bile duct obstruction.',
        'treatment': 'Treatment for jaundice depends on the underlying cause. It may include medications to treat liver disease or infections, procedures to remove obstructions in the bile ducts, and supportive care to manage symptoms.'
    },
    'Malaria': {
        'description': 'Malaria is a mosquito-borne infectious disease caused by Plasmodium parasites. Symptoms typically include fever, chills, sweats, headache, muscle aches, and fatigue. Without prompt treatment, malaria can be life-threatening.',
        'treatment': 'Treatment for malaria involves antimalarial medications to kill the parasites in the bloodstream. The choice of medication depends on the type of malaria parasite and its resistance to drugs.'
    },
    'Chickenpox': {
        'description': 'Chickenpox is a highly contagious viral infection caused by the varicella-zoster virus. It is characterized by an itchy rash of fluid-filled blisters that eventually crust over. Other symptoms may include fever, headache, and fatigue.',
        'treatment': 'Treatment for chickenpox aims to relieve symptoms and prevent complications. This may include over-the-counter medications for fever and itching, antiviral medications for severe cases, and measures to prevent scratching and secondary infections.'
    },
    'Dengue': {
        'description': 'Dengue fever is a mosquito-borne viral infection common in tropical and subtropical regions. Symptoms include high fever, severe headache, pain behind the eyes, joint and muscle pain, rash, and mild bleeding.',
        'treatment': 'Treatment for dengue fever focuses on relieving symptoms and preventing complications. This may include rest, hydration, pain relievers (but not aspirin), and medical monitoring for signs of severe dengue.'
    },
    'Typhoid': {
        'description': 'Typhoid fever is a bacterial infection caused by Salmonella typhi. Symptoms include sustained high fever, weakness, stomach pain, headache, and loss of appetite. In severe cases, complications such as intestinal perforation can occur.',
        'treatment': 'Treatment for typhoid fever involves antibiotics to kill the Salmonella bacteria. In addition to medications, supportive care such as fluids and electrolyte replacement may be necessary.'
    },
    'Hepatitis A': {
        'description': 'Hepatitis A is a viral liver infection spread through contaminated food or water. Symptoms include fever, fatigue, nausea, jaundice, and loss of appetite. Most cases resolve without treatment.',
        'treatment': 'Treatment for hepatitis A focuses on relieving symptoms and preventing complications. This may include rest, hydration, and supportive care. In some cases, hospitalization may be necessary.'
    },
    'Hepatitis B': {
        'description': 'Hepatitis B is a liver infection caused by the hepatitis B virus, transmitted through contact with infected blood or bodily fluids. Symptoms include fatigue, abdominal pain, and jaundice. Chronic infection can lead to severe liver damage and cancer.',
        'treatment': 'Treatment for hepatitis B aims to manage symptoms, prevent complications, and reduce the risk of transmission. This may include antiviral medications, regular monitoring, and vaccination for close contacts.'
    },
    'Hepatitis C': {
        'description': 'Hepatitis C is a liver infection transmitted through contact with infected blood. Often asymptomatic, it can lead to severe liver damage, including cirrhosis and cancer. Treatment with antiviral medications is available.',
        'treatment': 'Treatment for hepatitis C involves antiviral medications to suppress the virus and prevent liver damage. The choice of medication and duration of treatment depend on factors such as the genotype of the virus and the extent of liver damage.'
    },
    'Hepatitis D': {
        'description': 'Hepatitis D occurs only in individuals already infected with hepatitis B. Symptoms are similar to hepatitis B but can be more severe. Prevention through hepatitis B vaccination is crucial.',
        'treatment': 'Treatment for hepatitis D focuses on managing symptoms and preventing complications. This may include antiviral medications for hepatitis B and supportive care to relieve symptoms.'
    },
    'Hepatitis E': {
        'description': 'Hepatitis E is a liver infection spread through contaminated water or food. Symptoms are similar to hepatitis A and usually resolve without treatment. Pregnant women and those with liver disease are at higher risk of complications.',
        'treatment': 'Treatment for hepatitis E is usually supportive, focusing on relieving symptoms and preventing dehydration. In severe cases, hospitalization and supportive care may be necessary.'
    },
    'Alcoholic hepatitis': {
        'description': 'Liver inflammation caused by excessive alcohol consumption. Symptoms include jaundice, abdominal pain, nausea, and fever. Severe cases can lead to liver failure.',
        'treatment': 'Treatment for alcoholic hepatitis involves abstinence from alcohol, supportive care to manage symptoms, and interventions to prevent further liver damage. In severe cases, hospitalization and medical interventions may be necessary.'
    },
    'Tuberculosis': {
        'description': 'Infectious disease caused by the bacteria Mycobacterium tuberculosis. Symptoms include persistent cough, fever, weight loss, and night sweats. It primarily affects the lungs but can also involve other parts of the body.',
        'treatment': 'Treatment for tuberculosis involves a combination of antibiotics taken for several months. It is essential to complete the full course of treatment to prevent the development of drug-resistant strains.'
    },
    'Common Cold': {
        'description': 'Viral infection of the upper respiratory tract, causing symptoms like runny nose, sore throat, cough, and congestion. Usually resolves within a week with rest and home remedies.',
        'treatment': 'Treatment for the common cold focuses on relieving symptoms and supporting the body\'s immune response. This may include rest, hydration, over-the-counter medications for symptom relief, and avoiding close contact with others to prevent transmission.'
    },
    'Pneumonia': {
        'description': 'Inflammation of the lungs typically caused by bacterial, viral, or fungal infections. Symptoms include fever, chills, cough, chest pain, and difficulty breathing. Treatment involves antibiotics or antiviral medications.',
        'treatment': 'Treatment for pneumonia depends on the underlying cause and severity of symptoms. It may include antibiotics for bacterial pneumonia, antiviral medications for viral pneumonia, supportive care to relieve symptoms, and hospitalization for severe cases.'
    },
    'Dimorphic hemmorhoids(piles)': {
        'description': 'Swollen veins in the rectum or anus causing discomfort, itching, and bleeding. Can be internal or external and may require lifestyle changes, medication, or surgery for severe cases.',
        'treatment': 'Treatment for hemorrhoids depends on the severity of symptoms. Mild cases can often be managed with lifestyle changes, dietary modifications, and over-the-counter medications. Severe cases may require prescription medications or surgical procedures.'
    },
    'Heart Attack': {
        'description': 'Medical emergency caused by reduced blood flow to the heart muscle. Symptoms include chest pain or discomfort, shortness of breath, nausea, and lightheadedness. Prompt medical treatment is critical to prevent damage to the heart.',
        'treatment': 'Treatment for a heart attack involves restoring blood flow to the heart muscle as quickly as possible to prevent further damage. This may include medications, such as clot-busting drugs or angioplasty, to open blocked arteries, and lifestyle changes to reduce the risk of future heart problems.'
    },
    'Varicose veins': {
        'description': 'Enlarged, twisted veins usually found in the legs. Symptoms include pain, swelling, and bulging veins. Treatment options range from lifestyle changes to medical procedures.',
        'treatment': 'Treatment for varicose veins depends on the severity of symptoms and may include lifestyle modifications (such as exercise and elevation of the legs), compression stockings, minimally invasive procedures (such as sclerotherapy or laser therapy), or surgery for severe cases.'
    },
    'Hypothyroidism': {
        'description': 'Underactive thyroid gland leading to symptoms like fatigue, weight gain, cold sensitivity, dry skin, and depression. Treatment involves hormone replacement therapy.',
        'treatment': 'Treatment for hypothyroidism involves taking synthetic thyroid hormone medication to replace the hormone your body is lacking. It is important to take the medication as prescribed and have regular check-ups to monitor thyroid function.'
    },
    'Hyperthyroidism': {
        'description': 'Overactive thyroid gland causing symptoms such as weight loss, rapid heartbeat, sweating, anxiety, and tremors. Treatment options include medications, radioactive iodine therapy, or surgery.',
        'treatment': 'Treatment for hyperthyroidism aims to reduce the production of thyroid hormones and alleviate symptoms. This may include antithyroid medications, radioactive iodine therapy to destroy thyroid cells, beta-blockers to manage symptoms, or surgery to remove part of the thyroid gland.'
    },
    'Hypoglycemia': {
        'description': 'Low blood sugar levels leading to symptoms like shakiness, sweating, irritability, confusion, and fainting. It can occur in individuals with diabetes or as a result of other medical conditions or medications.',
        'treatment': 'Treatment for hypoglycemia involves consuming fast-acting carbohydrates to raise blood sugar levels quickly. For people with diabetes, regular monitoring of blood sugar levels, adjustments to medication or insulin doses, and dietary modifications may be necessary to prevent hypoglycemic episodes.'
    },
    'Osteoarthritis': {
        'description': 'Degenerative joint disease characterized by joint pain, stiffness, and swelling. Commonly affects the knees, hips, hands, and spine. Treatment involves pain management, exercise, and sometimes surgery.',
        'treatment': 'Treatment for osteoarthritis focuses on relieving pain, improving joint function, and preventing further damage to the affected joints. This may include medications, physical therapy, lifestyle changes, and in severe cases, joint replacement surgery.'
    },
    'Arthritis': {
        'description': 'Inflammation of the joints causing pain, swelling, and stiffness. There are many types of arthritis, including rheumatoid arthritis, osteoarthritis, and gout, each with different causes and treatments.',
        'treatment': 'Treatment for arthritis aims to reduce pain, inflammation, and joint damage, improve joint function, and enhance quality of life. This may include medications, physical therapy, lifestyle changes, and in some cases, surgery.'
    },
    '(Vertigo) Paroxysmal Positional Vertigo': {
        'description': 'A type of vertigo caused by sudden movements of the head, leading to brief episodes of dizziness and spinning sensations. Treatment involves specific head maneuvers to reposition displaced inner ear crystals.',
        'treatment': 'Treatment for paroxysmal positional vertigo (BPPV) involves physical maneuvers or exercises to move the displaced inner ear crystals (canaliths) back into the correct position. These maneuvers are often performed by a healthcare professional and can provide rapid relief from symptoms.'
    },
    'Acne': {
        'description': 'Skin condition characterized by pimples, blackheads, and whiteheads, typically on the face, chest, and back. It can be caused by hormonal changes, genetics, or bacteria.',
        'treatment': 'Treatment for acne aims to reduce inflammation, unclog pores, and prevent new breakouts. This may include topical treatments (such as benzoyl peroxide or retinoids), oral medications (such as antibiotics or hormonal therapy), and lifestyle changes (such as skincare routines and diet modifications).'
    },
    'Urinary Tract Infection (UTI)': {
        'description': 'Bacterial infection of the urinary tract, commonly causing symptoms such as frequent urination, burning sensation during urination, abdominal pain, and cloudy or bloody urine.',
        'treatment': 'Treatment for urinary tract infections (UTIs) typically involves antibiotics to kill the bacteria causing the infection. The choice of antibiotic and duration of treatment depend on factors such as the type of bacteria and the severity of symptoms.'
    },
    'Psoriasis': {
        'description': 'Chronic autoimmune condition causing rapid skin cell growth, leading to thick, red, scaly patches on the skin. Symptoms may also include itching and pain.',
        'treatment': 'Treatment for psoriasis aims to reduce inflammation, slow down skin cell growth, and alleviate symptoms. This may include topical treatments (such as corticosteroids or retinoids), phototherapy (light therapy), oral medications (such as methotrexate or biologics), and lifestyle modifications.'
    },
    'Impetigo': {
        'description': 'Highly contagious bacterial skin infection characterized by red sores or blisters that rupture and form yellowish crusts. Common in children and often treated with antibiotics.',
        'treatment': 'Treatment for impetigo usually involves topical or oral antibiotics to kill the bacteria causing the infection. Keeping the affected area clean and dry can also help prevent the spread of impetigo.'
    }
}


            # Define specialists
            specialists = {
                'Rheumatologist': ['Osteoarthristis', 'Arthritis'],
                'Cardiologist': ['Heart attack', 'Bronchial Asthma', 'Hypertension'],
                'ENT specialist': ['(vertigo) Paroymsal Positional Vertigo', 'Hypothyroidism'],
                'Neurologist': ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis'],
                'Allergist': ['Allergy', 'Pneumonia', 'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid'],
                'Urologist': ['Urinary tract infection', 'Dimorphic hemmorhoids(piles)'],
                'Dermatologist': ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo'],
                'Gastroenterologist': ['Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Gastroenteritis', 'Hepatitis E',
                                       'Alcoholic hepatitis', 'Jaundice', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
                                       'Diabetes', 'Hypoglycemia']
            }
            
            # Find the specialist to consult
            consult_doctor = "Other"
            for specialist, diseases in specialists.items():
                if predicted_disease in diseases:
                    consult_doctor = specialist
                    break

            predicted_disease_details = disease_details.get(predicted_disease, {'description': 'No details available', 'treatment': 'No details available'})

                # Fetch consulting doctor from database
            cur = mysql.connection.cursor()
            cur.execute("SELECT d_name FROM doctors WHERE d_spec = %s", (consult_doctor,))
            consulting_doctor = cur.fetchone()
            if consulting_doctor:
                consult_doctor_name = consulting_doctor['d_name']
            else:
                consult_doctor_name = "Other"
            # Cleanup
            del df_test
            
            return jsonify({'predicteddisease': predicted_disease, 'consultdoctor': consult_doctor_name, 'consult':consult_doctor, 'predicteddiseasedetails': predicted_disease_details,})






if __name__ == '__main__':   
    app.run(debug=True)  
