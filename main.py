from flask import Flask,render_template,request,jsonify
import pandas as pd 
import pickle

app = Flask(__name__)
data = pd.read_csv('final_dataset.csv')
pipe = pickle.load(open("RidgeModel.pkl", 'rb'))

@app.route('/')
def index():
    bedrooms = sorted(data['beds'].unique())
    bathrooms = sorted(data['baths'].unique())
    sizes = sorted(data['size'].unique())
    zip_codes = sorted(data['zip_code'].unique())

    return render_template('index.html', bedrooms=bedrooms, bathrooms=bathrooms, sizes=sizes, zip_codes=zip_codes)

@app.route('/predict', methods=['POST'])
def predict():
    bedrooms = request.form.get('beds')
    bathrooms = request.form.get('baths')
    size = request.form.get('size')
    zipcodes = request.form.get('zip_codes')

    # create a Dataframe with the input data
    input_data = pd.DataFrame([[bedrooms,bathrooms,size,zipcodes]],columns=['beds','baths','size','zip_codes'])

    print("Input Data:")
    print(input_data)   

    #Handle unknown categories in the input data
    for column in input_data.columns:
        unknown_categories = set(input_data[column])-set(data[column].unique())
        if unknown_categories:
            # handle unknown categories (e.g. replace with a default value)
            input_data[column] = input_data[column].replace(unknown_categories,data[column].mode()[0])

    print("Processed Input data:")
    print(input_data)

    # Predict the price
    prediction = pipe.predict(input_data)[0]

    return str(prediction)

from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('final_dataset.csv')
pipe = pickle.load(open("RidgeModel.pkl", 'rb'))

@app.route('/')
def index():
    bedrooms = sorted(data['beds'].unique())
    bathrooms = sorted(data['baths'].unique())
    sizes = sorted(data['size'].unique())
    zip_codes = sorted(data['zip_code'].unique()) 

    return render_template('index.html', bedrooms=bedrooms, bathrooms=bathrooms, sizes=sizes, zip_codes=zip_codes)

@app.route('/predict', methods=['POST'])
def predict():
    bedrooms = request.form.get('beds')
    bathrooms = request.form.get('baths')
    size = request.form.get('size')
    zipcodes = request.form.get('zip_codes')

    # create a Dataframe with the input data
    input_data = pd.DataFrame([[bedrooms,bathrooms,size,zipcodes]],columns=['beds','baths','size','zip_codes'])

    print("Input Data:")
    print(input_data)   

    #convet 'baths' column to numeric with errors='coerce'
    input_data['baths'] = pd.to_numeric(input_data['baths'],errors='coerce')

    #convert input data to numeric types
    input_data = input_data.astype({'beds':int, 'baths':float, 'size':float, 'zip_code':int})

    # Handle unknown categories in the input data
    for column in input_data.columns:
        unknown_categories = set(input_data[column])- set(data[column].unique())
        if unknown_categories:
            print(f"unknown categories in {column}:{unknown_categories}")
            # Handle unknown categories
            input_data[column] = input_data[column].replace(unknown_categories,data[column].mode()[0])


    print("Processed Input Data:")
    print(input_data)

    #Predict the price 
    prediction = pipe.predict(input_data)[0]

    return str(prediction)

if __name__ == "__main__":
    app.run(debug=True,port=5000)

if __name__ == "__main__":
    app.run(debug=True,port=5000)

