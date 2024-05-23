from flask import Flask, render_template, request, redirect, url_for , session
import pymysql
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL configuration
#db_config = {
#    'host': 'localhost',
#    'user': 'root',
#    'password': 'vvh@sql@07',
#    'database': 'new_schema',
#}
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:vvh@sql@07@localhost/new_schema'
# db = SQLAlchemy(app)
# class SelectedOption(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     option_name = db.Column(db.String(255), nullable=False)

# Function to establish a connection to MySQL
def get_mysql_connection():
    return pymysql.connect(**db_config)

# Route to display the form
@app.route('/')
def index():
    conn = get_mysql_connection()
    if conn.open:
        # Fetch medicines from the database
        cursor = conn.cursor()
        cursor.execute("SELECT dosage FROM new_table")
        medicines = [row[0] for row in cursor.fetchall()]

        # Close the connection
        cursor.close()
        conn.close()

        return render_template('index.htm', medicines=medicines)

@app.route('/dosage')
def dosage():
    return render_template('dosage.htm')

@app.route('/submit_dosage', methods=['GET', 'POST'])
def dosage_page():
    try:
        data={
            'dosage': request.form['dosage'],
            'dosage_type': request.form['dosage_type']
            }
        connection = get_mysql_connection()
        cursor = connection.cursor()

        columns = ', '.join(data.keys())
        values_template = ', '.join(['%s'] * len(data))

        insert_query = "INSERT INTO new_table ({columns}) VALUES ({values_template})"
        cursor.execute(insert_query, tuple(data.values()))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions, e.g., display an error page
        return f"Error: {str(e)}"

# @app.route('/submit_dosage', methods=['GET', 'POST'])
# def dosage_page():
#     print("hrllo")
    # if request.method == 'POST':
    #     # Handle dosage form submission (add your logic here)
    #     return redirect(url_for('index')) # Redirect to the main form page after submission
    # return render_template('dosage.htm')


# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        medicines_list = request.form.getlist('medicines')
        # print(medicines_list)
        medi_str = ""
        try:
            for medicine in medicines_list:
                medi_str+= str(medicine)
                medi_str+=','
        except Exception as e:
            return f"Heeeeello: {str(e)}"
        # print(medi_str)
        data = {
            'name': request.form['name'],
            'id': request.form['id'],
            'hospital_visited_date': request.form['hospital_visited_date'],
            'gender': request.form['gender'],
            'age': request.form['age'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'bp': request.form['bp'],
            'diabetes': request.form['diabetes'],
            'hypertension': request.form['hypertension'],
            'family_history': request.form['family_history'],
            'previous_kidney_disease': request.form['previous_kidney_disease'],
            'urine_albumin': request.form['urine_albumin'],
            'cardiovascular_disease': request.form['cardiovascular_disease'],
            'glomerular_filration': request.form['glomerular_filtration'],
            'serum_creatinine_level': request.form['serum_creatinine_level'],
            'haemoglobin_level': request.form['haemoglobin_level'],
            'urinary_tract_infection': request.form['urinary_tract_infection'],
            'kidney_stone': request.form['kidney_stone'],
            'kidney_injury_history': request.form['kidney_injury_history'],
            'total_water_intake': request.form['total_water_intake'],
            'living_area': request.form['living_area'],
            'total_count': request.form['total_count'],
            'random_blood_sugar': request.form['random_blood_sugar'],
            'urea': request.form['urea'],
            'pus_cells': request.form['pus_cells'],
            'worker': request.form['worker'],
            'diet': request.form['diet'],
            'other_medical_condition': request.form['other_medical_condition'],
            'medications':medi_str
        }
        # a =list(pipeline.cleaning(data))
        # print(a)
        # print(request.form.getlist('medicines'))
        # Insert data into the patient_data table
        connection = get_mysql_connection()
        cursor = connection.cursor()

        columns = ', '.join(data.keys())
        values_template = ', '.join(['%s'] * len(data))

        insert_query = f"INSERT INTO finaliti ({columns}) VALUES ({values_template})"
        cursor.execute(insert_query, tuple(data.values()))

        connection.commit()
        cursor.close()
        connection.close()

        # Set a flag to indicate success
        success = True

        return render_template('index.htm', success=success)

    except Exception as e:
        # Handle exceptions, e.g., display an error page
        return f"Error: {str(e)}"

# @app.route('/index')
# def index():
#     # Retrieve the success flag from session
#     success = session.pop('success', False)

#     return render_template('index.htm', success=success)

if __name__ == '__main__':
    app.run(debug=True)
