from flask import Flask, render_template, request
from prediction import load_and_classify, recommendation
from flask_mysqldb import MySQL

app = Flask('_name_', template_folder = 'Front-end', static_folder='Front-end', static_url_path='/Front-end/Assets')

#database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'grow_wise'
app.config['MYSQL_PASSWORD'] = 'Test.12345'
app.config['MYSQL_DB'] = 'grow_wise_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

models_list={
    'apple':'apple_model',
    'banana': 'banana_model',
    'cherry': 'cherry_model',
    'cotton': 'cotton_model',
    'grape':'grape_model',
    'mango': 'mango_model',
    'maize': 'maize_model',
    'peach': 'peach_model',
    'potato':'potato_model',
    'pepper': 'pepper_model',
    'rice': 'rice_model',
    'soybean': 'soybean_model',
    'strawberry': 'strawberry_model',
    'tomato':'tomato_model',
    'wheat':'wheat_model'
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disease_identification', methods = ['GET', 'POST'])
def disease_identification():
    if request.method == 'POST':
        selected_plant = request.form.get('plants')
        uploaded_image = request.files['file-input']
        model_name = models_list.get(selected_plant)
        image_path = 'uploaded images/' + uploaded_image.filename
        uploaded_image.save(image_path) 
        if model_name:
            class_label = load_and_classify(model_name, image_path)
            if class_label != 'Healthy':
                cursor = mysql.connection.cursor()
                query = f"SELECT * FROM  diseaseidentification where plant_name = '{selected_plant}' and disease_name = '{class_label}'"
                cursor.execute(query)
                identification_data = cursor.fetchone()
        return render_template('identification result.html', identification_data = identification_data, result = class_label)
    return render_template('disease_identification.html')


#Crop Recommender page
@app.route('/crop_recommender', methods=['POST', 'GET'])
def crop_recommender():
        if request.method == 'POST':
            cur = mysql.connection.cursor()
            N = float(request.form['nitrogen'])
            P = float(request.form['phosphorous'])
            K = float(request.form['k'])
            temperature = float(request.form['temperature'])
            humidity = float(request.form['Humidity'])
            PH = float(request.form['PH'])
            rain_fall = float(request.form['rain_fall'])

            output = recommendation(N, P, K, temperature, humidity, PH, rain_fall)

            # Insert data into the table
            insert_query = "INSERT INTO user_input_data (N, P, K, temperature, humidity, ph, rainfall, crop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(insert_query, (N, P, K, temperature, humidity, PH, rain_fall, output))
            mysql.connection.commit()

            # Fetch data from the CropTable1
            select_query = "SELECT * from plantinformation WHERE name = %s"
            cur.execute(select_query, (output, ))
            crop_data = cur.fetchone()

            # Close the cursor
            cur.close()

            # Render the output page with the output
            print("Output Value:", output)
            return render_template('recommend_output.html', output=output, crop_data=crop_data)
        else:
            return render_template('crop_recomender.html')
        return render_template('crop_recommender.html')




@app.route('/plant_information', methods=['GET', 'POST'])
def plant_information():
    if request.method == 'POST':
        # Acquiring the query from search bar
        query = request.form['searchInput']
        cur = mysql.connection.cursor()
        
        # Searching for the relevent data
        select_query = "SELECT * from PlantInformation WHERE name = %s"
        cur.execute(select_query, (query, ))
        data = cur.fetchone()

        cur.close()

        return render_template('plant_information.html', data=data)

    # Add a return statement for the case when the request method is 'GET'
    return render_template('plant_information.html',data=None)

#disease identifer part
if __name__ == '__main__':
    app.run(debug=True)
