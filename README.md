# TelemetryNest
A real-time data platform for collecting, storing, and analyzing KPI and alarm data

## Install components

    pip install cassandra-driver pandas numpy scikit-learn

## Run for development
    
    uvicorn app.main:app --reload

## Generate KPIs
    
    python3 app/cli.py

## Routes:

- /user/login - Sign in and get access token (JWT)

  Dev Credentials:
 
  - email: tokernel@example.com
  - password: tokernel@example.com.p

- /profile - Access signed-in user profile data using token

- /kpis - Create KPIs

- /kpis/last - Get KPIs

- /predicted-alarms - Create Alarms
- /predicted-alarms/last - Get alarms
