from flask import Flask, render_template, request, send_from_directory
from prediction import load_and_classify, recommendation
from flask_mysqldb import MySQL

app = Flask('_name_', template_folder='Front-end', static_folder='Front-end', static_url_path='/Front-end/Assets')

#database connection detail
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'grow_wise'
app.config['MYSQL_PASSWORD'] = 'Test.12345'
app.config['MYSQL_DB'] = 'grow_wise_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#model list
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

# route for homepage
@app.route('/')
def index():
    return render_template('index.html')

#route for disease identification page
@app.route('/disease_identification', methods = ['GET', 'POST'])
def disease_identification():
    #getting  the crop name from user input and checking if it exists in our models dictionary
    if request.method == 'POST':
        selected_plant = request.form.get('plants')
        uploaded_image = request.files['file-input']
        model_name = models_list.get(selected_plant)
        image_path = 'uploaded images/' + uploaded_image.filename
        uploaded_image.save(image_path)
        #calling the prediction function with the given parameters
        if model_name:
            class_label = load_and_classify(model_name, image_path)
            #checking  which label was returned by the model and redirecting to corresponding result pages
            if class_label != 'Healthy':
                cursor = mysql.connection.cursor()
                query = f"SELECT * FROM  diseaseidentification where plant_name = '{selected_plant}' and disease_name = '{class_label}'"
                cursor.execute(query, )
                identification_data = cursor.fetchone()
                cursor.close()
                return render_template('identification result.html', identification_data = identification_data, result = class_label, usr_image=uploaded_image.filename)
            else:
                cursor = mysql.connection.cursor()
                query = f"SELECT diseases_susceptibility FROM plantinformation WHERE name='{selected_plant}'"
                cursor.execute(query, )
                common_disease = cursor.fetchone()
                cursor.close()
                return render_template('identification result.html', common_disease=common_disease, result=class_label, usr_image=uploaded_image.filename)

    return render_template('disease_identification.html')

#showing user uploaded  image on results page
@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory('uploaded images', filename, mimetype='image/jpeg')


#rout for Crop Recommender page
@app.route('/crop_recommender', methods=['POST', 'GET'])
def crop_recommender():
        if request.method == 'POST':
            cursor = mysql.connection.cursor()
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
            cursor.execute(insert_query, (N, P, K, temperature, humidity, PH, rain_fall, output))
            mysql.connection.commit()

          # Fetch data from the CropTable1
            select_query = "SELECT * from plantinformation WHERE name = %s"
            cursor.execute(select_query, (output, ))
            crop_data = cursor.fetchone()

            # Close the cursor
            cursor.close()

            # Render the output page with the output
            return render_template('recommend_output.html', output=output, crop_data=crop_data)
        else:
            return render_template('crop_recommender.html')
#route for plant_information page
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
#route for about us page
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

#route for contact  us page
@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(debug=True)
