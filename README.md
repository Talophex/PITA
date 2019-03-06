# PITA
PredictIt Tracking and Analysis  
primary language: Python 2.7

# Features  
Current:  
-Polls the predictit.org API every minute to retrieve current pricing data as a JSON object  
-Inserts data into SQLite3 database using SQLAlchemy ORM  
-Processes requests for historical prices and outputs data as .csv  

Future:  
-Train LSTM neural network to predict price movement  


# Installation
Clone the directory:  
```bash

git clone https://github.com/Talophex/PITA.git

```  


Install [pip](https://pip.pypa.io/en/stable/).  
  
Install dependencies:  

```bash

pip install -r requirements.txt

```

Create the SQLite3 database to store data:
```bash

python CreateDatabase.py

```  
Add cron job to poll API once per minute:
```bash

python CronScheduler.py

```
