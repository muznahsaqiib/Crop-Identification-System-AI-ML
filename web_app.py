import numpy as np
from flask import Flask,request,render_template,jsonify,url_for,redirect
import pickle

import requests

app=Flask(__name__)


loaded_model=pickle.load(open('D:/Flask_App/Flask_App/model.pkl','rb'))

@app.route('/')
def home():
    return render_template('frontend.html')


@app.route('/Crop',methods=['POST'])
def Crop():
    float_features=[float(x) for x in request.form.values()]
    features=[np.array(float_features)]
    prediction=loaded_model.predict(features)
    print(prediction)
    if(prediction[0]==2): 
        return render_template ('frontend.html',htmlvariable= " Corn{}".format(prediction))
    elif(prediction[0]==3):
        return render_template ('frontend.html',htmlvariable= " Cotton{}".format(prediction))
    elif(prediction[0]==4):
        return render_template ('frontend.html',htmlvariable= " Soy{}".format(prediction))
    elif(prediction[0]==5):
        return render_template ('frontend.html',htmlvariable= " Spring Wheat{}".format(prediction))
    elif(prediction[0]==6):
        return render_template ('frontend.html',htmlvariable= " winter wheat{}".format(prediction))
    else:
        return render_template ('frontend.html',htmlvariable= " Barley{}".format(prediction))
    # return render_template ('frontend.html',htmlvariable= " {}".format(prediction))

@app.route('/get_features', methods=['GET'])
def get_features():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    print(f"Received coordinates: Latitude={lat}, Longitude={lon}")  # Debugging log

    try:
        # Fetch weather data
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=24bd28a9556b844caf9f902567ee99d9"
        weather_response = requests.get(weather_url)

        if weather_response.status_code != 200:
            print(f"Weather API Error: {weather_response.status_code}, {weather_response.text}")
            return jsonify({'error': 'Failed to fetch weather data'}), 500

        weather_data = weather_response.json()

        # Process the response
        ndvi = 0.5  # Example static NDVI value
        max_temp = weather_data['main']['temp_max']
        avg_temp = weather_data['main']['temp']
        min_temp = weather_data['main']['temp_min']
        avg_humidity = weather_data['main']['humidity']
        rainfall = weather_data.get('rain', {}).get('1h', 0)

        return jsonify({
            'ndvi': ndvi,
            'max_temp': max_temp,
            'avg_temp': avg_temp,
            'min_temp': min_temp,
            'avg_humidity': avg_humidity,
            'rainfall': rainfall,
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# #creating a function for prediction
# def Crop_types(input_value):
#     #making a predictive system
#     #this input values is in the form of list so first we convert the list of data into numpy array
#     #using function "asarray"
#     updated_input_value=np.asarray(input_value)
#     # as we know we not take last target value, so we reshape the numpy array
#     reshaped_input_value=updated_input_value.reshape(1,-1)

#     # for prediction
#     prediction=loaded_model.predict(reshaped_input_value)
#     print(prediction)

#     # take condition if prediction is R then it is Rock other wise Mine
#     # we take prediction[0] because it is in list form so we take first index 0 that this is equal to R or M
#     if(prediction[0]==2): 
#       return("This is Corn")
#     elif(prediction[0]==3):
#       return("This is Cotton")
#     elif(prediction[0]==4):
#       return("This is Soy")
#     elif(prediction[0]==5):
#       return("This is Spring Wheat")
#     elif(prediction[0]==6):
#       return("This is winter wheat")
#     else:
#       return("This is Barley")

# def main():
#     #Giving the title
#     st.title('Smart Agrico System Manually')

#     #Getting the data from user


#     longitude=st.text_input('Longitude of place')
#     latitude=st.text_input('Latitude of place')
#     NDVI=st.text_input('NDVI of Crop')
#     MaxTemp=st.text_input('MaxTemp of Crop')
#     AveTemp=st.text_input('AveTemp of Crop')
#     MinTemp=st.text_input('MinTemp of Crop')
#     AveHumidity=st.text_input('AveHumidity of place')
#     Rainfall=st.text_input('Rainfall of place')


#     #code for prediction
#     Classification = ''

#     #creating a button for prediction

#     if st.button('Name of crop'):
#         Classification=Crop_types([longitude,latitude,NDVI,MaxTemp,AveTemp,MinTemp,AveHumidity,Rainfall])

#     st.success(Classification)


if __name__ == '__main__':
      app.run(debug=True)
    

