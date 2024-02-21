from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Define a function to predict emissions
def predict_emissions(specific_country):
    # Load and preprocess data
    df = pd.read_csv(r"C:\Users\arupe\Downloads\co-emissions-by-sector.csv", encoding="utf8")
    df.fillna(0, inplace=True)

    select_country = df.loc[df['Entity'] == specific_country].copy(deep=True)
    select_country.drop(select_country.columns[[0, 1]], axis=1, inplace=True)
    X = select_country.drop('Year', axis=1)
    y = select_country[select_country.columns[2]]
    # Define dictionary to store predicted emissions
    predictions = {}

    for i in range(1, 9):
        predictions_list = []

        for j in range(10):
            y = select_country[select_country.columns[i]]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

            # Define the degree of the polynomial
            degree = 1

            # Polynomial feature transformation
            poly = PolynomialFeatures(degree=degree)
            X_train_poly = poly.fit_transform(X_train)
            X_test_poly = poly.transform(X_test)

            # Define the linear regression model
            model = Sequential([
                Dense(1, input_shape=(X_train_poly.shape[1],))
            ])

            # Compile the model
            model.compile(optimizer='adam', loss='mse')

            # Train the model
            history = model.fit(X_train_poly, y_train, epochs=500, verbose=0)

            # Assuming X_test_poly contains the features for the year 2024
            y_pred_2024 = model.predict(X_test_poly)

            # Append prediction to the list
            predictions_list.append(y_pred_2024[0][0])

        # Compute mean prediction over multiple runs
        avg_prediction = np.mean(predictions_list)

        # Store the average prediction in the dictionary
        predictions[select_country.columns[i]] = avg_prediction

    return predictions

# Your view functions
def process_input(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data')
        input_data_2 = request.POST.get('input_data_2')
        # Process the input_data (e.g., perform some computation)

        import pandas as pd
        '''from google.colab import drive
        drive.mount("./content")'''
        dff = pd.read_csv(r"C:\Users\arupe\Downloads\AQI and Lat Long of Countries.csv", encoding="utf8")
        dff.fillna(0, inplace=True)

        # Get the city name from the user
        specific = input_data.title()

        if specific in dff['City'].values:
            select = dff.loc[dff['City'] == specific].copy(deep=True)
            bad_quality = []

            for i in range(3, 12, 2):
                if select.iloc[0, i] != 'Good':
                    bad_quality.append(select.columns[i])

            indoor = {
                'AQI Category':'Bird’s Nest Fern, Snake Plant, Succulents, Cacti',
                'CO AQI Category': 'Rubber Plant, Bamboo Palm',
                'NO2 AQI Category': 'Peace lily, Corn plant, Fern arum ',
                'PM2.5 AQI Category':'Snake Plant, Spider Plant, Areca Palm, Fiddle Fig.',
                'Ozone AQI Category':'Ficus, Calathia, Dieffenbachia, Golden Pothos'

            }

            outdoor = {
                'AQI Category': 'Mediterranean Hackberry Plant, Common Ivy Plant, Aster and Osmanthus Plants',
                'CO AQI Category': 'Honey Locust, Common Ivy Plant',
                'NO2 AQI Category': 'Lady’s Mantle Plant, English Oak, Eastern White Pine, Red Maple',
                'PM2.5 AQI Category': 'Honey Locust, Red Maple, Eastern White Pine, Green Ash, English Oak, Silver birch, Yew, Elder',
                'Ozone AQI Category':'Eastern White Pine,Green Ash,Red Maple'
            }

            ind_plt = [indoor.get(cat, '') for cat in bad_quality]
            out_plt = [outdoor.get(cat, '') for cat in bad_quality]

        else:
            ind_plt = ['We are sorry but your city is not in our database but you can always plant Bird’s Nest Fern, Snake Plant, Cacti']
            out_plt = ['You can never go wrong with planting common horse-chestnut, black Walnut, London plane, and American sweetgum tees in your neighbourhood to improve air quality.']

        # Call predict_emissions function
        specific_country = input_data_2.title()
        emissions_predictions = predict_emissions(specific_country)

        return render(request, 'Result.html', {'output1': "".join(ind_plt), 'output2': "".join(out_plt),'output3': emissions_predictions})
    else:
        return render(request, 'gdsc_view.html')

def input_page(request):
    # Render the loading page while processing
    return render(request, 'loading.html')

