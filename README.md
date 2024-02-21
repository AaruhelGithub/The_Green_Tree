# The_Green_Tree
The Green Tree is a Django based website which provieds names of plants and trees that can be planted in an area which will help reduce air pollution specific to it. It also provides projections of CO2 emissions of different sectors both of which can help in building sustainable cities.
The backend is based on Python and the frontend is made from HTML and CSS.
The runtime of the website is pretty long (around 2 minutes) because of the Polynomial Regression Machine Learning Model used for CO2 estimation.
The datasets used in the model are added to the repository. They can be downloaded and their paths can be changed in order to run the website
The dataset used in the views.py predict_emissions function is co-emissions-by-sector.csv.
The dataset used in the views.py process_input function is AQI and Lat Long of Countries.csv.
Work is being done on making ML model a trained model in order to decrease the runtime and on taking in account the climate of the city in order to suggest more specific plants and trees.
ChatGPT 3.5 was used to simplify and modify the code. 
