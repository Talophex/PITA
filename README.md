# PITA
PredictIt Tracking and Analysis
language: Python 2.7

Current:  
-Polls the predictit.org API to retrieve current pricing data as a JSON object  
-Inserts data into SQL database using SQLAlchemy ORM  
-Processes requests for historical prices and outputs data as .csv  

Future:  
-Train LSTM neural network to predict price movement
