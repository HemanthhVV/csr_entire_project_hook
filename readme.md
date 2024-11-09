
---

# Prediction of Dialysis in Patients with Early Kidney Disease

This is a CSR-Initiative project with Madurai Meenakshi Mission Hospital in order to analyse the patients with Chronic Kidney Disease(CKD), It comprises of data analytics, understanding and building the model.

This repo contains the application built with the analysis made,The entire application is built with python, DB used - MySQL for the backend, and the frontend is developed with streamlit.The forms to add patient data is built with HTML,CSS,JS,Flask.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
├── sql_test        ## Forms to add data
│   ├── app.py
│   └── templates
│       ├── additional.htm
│       ├── dosage.htm
│       ├── index.htm
│       └── styles.css
└── webapp          ## Streamlit Application
    ├── 01_ForeCaster-[Old Patients].py
    ├── helpers
    │   ├── functions.py
    │   ├── __init__.py
    │   ├── Pipeline.py
    │   └── __pycache__
    ├── pages
    │   ├── 02_Recommender-[Old Patients].py
    │   ├── 03_Predictor-[New Patients].py
    │   ├── 04_Suggester-[New Patients].py
    │   ├── 05_Graphs-[Old Patients].py
    │   ├── 06_Data_Visits.py
    │   ├── Medicinal_Analysis.py
```

## Features

- **Data Processing and Analysis**: Perform statistical and machine learning analysis on patient data.
- **Forecasting and Recommending**: Modules to generate patient-specific forecasts and recommendations.
- **SQL Integration**: Includes SQL functionality for additional data queries and template rendering.
- **Interactive Web Application**: Visualizes data and displays recommendations.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/HemanthhVV/csr_entire_project_hook.git
    cd csr_entire_project_hook
    ```
2. Install required packages (if not installed):
    ```bash
    pip install -r requirements.txt
    ```
3. Setup the MySQL server in your local or cloud:
    `add the credentials to the app`
4. Start the SQL server.
5. Start the forms application by:
    ```bash
    cd sql_test ##It is a flask application
    python app.py
    ```

6. Start the web application:
    ```bash
    ## Note : Create a .streamlit/secrets.toml
    ## To detail about DB crendentials
    ## Refer https://docs.streamlit.io/develop/api-reference/connections/st.connection
    cd webapp
    streamlit run 01_ForeCaster-[Old Patients].py
    ```

## Usage
### DB

Here, There were two applications, sql_test(put the data to DB) is used for the forms and streamlit app(get the data from DB) is used to inferences, Both the apps were connected to the same DB - MySQL

### Forms Application(sql_test)

To add the patients data as form, navigate to the `sql_test` folder and start the server which will store the data in mysql:
```bash
python app.py
```
Open a browser and access the application via the URL displayed in the terminal.

### Streamlit Application(webapp)

To use the full web application, navigate to the `webapp` folder and run
```bash
streamlit run 01_ForeCaster-[Old Patients].py
```
which will run the modules for forecasting, recommending, and suggesting outcomes.

## File Descriptions

### Data Files (`data` folder)
- `Final_Detected_Params.csv`, `for_new_patient.csv`, and `Whatif_training.csv`:

        Source datasets for training and testing, Which we derived from preprocessing and analytical inferences from raw patient data.

### SQL Test Application (`sql_test` folder)
- `app.py`: Which connects to the mysql DB used to get patient data from the user.
- `templates`: Contains HTML templates for displaying data, including:
  - `index.htm`: Main page
  - `dosage.htm`: To add dosage types,name. eg. Paracetamol,Tablet
  - `additional.htm`: Additional information regarding the patients conditions. eg.hobbist,etc

### Web Application (`webapp` folder)
- `01_ForeCaster-[Old Patients].py`: Forecasting module for admitted patient data which runs on ARIMA to forecast next two steps.
- `02_Recommender-[Old Patients].py`: Recommender system for admitted patients based on their adminstrative data (patients' bp,sugar,etc).
- `03_Predictor-[New Patients].py`: Prediction module for new patient data, On time predictions for by input of patients health conditions.
- `04_Suggester-[New Patients].py`: Suggestions for new patients to improve their current condition.
- `05_Graphs-[Old Patients].py`: In terms to easy understanding, created graphs BP,BMI,Creatine of each patients here.
- `06_Data_Visits.py`: Tracks and analyzes data visits based on the forms, where it can be downloaded as structural data.

### Helpers (`webapp/helpers` folder)
- `functions.py`, `Pipeline.py`: Utility functions and data pipelines.


## License

This project is licensed under the Apache 2.0 License.

