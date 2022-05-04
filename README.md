<p align="left"><img src="https://www.worldenergytrade.com/images/stories/news/energias_alternativas/electricidad/4024/La-demanda-de-energia-electrica-de-Espana-aumenta-en-julio.jpg"></p>

# electric-load-forecasting

## **🤔 Contex**

- In the **Day-ahead electricity market**, market agents sell and takeover bids for electrical energy for the twenty-four hours of the following day.
- Every day of the year at 12:00 CET is the day-ahead market session where prices and electrical energies are set.
- Knowing in advance next day information (price, demand, generation...) is quite valuable so market agents can use it for their strategists.
- Go to [OMIE](https://www.omie.es/) for more information.


## **🎯 Objectives**

The goal of this project is to provide a solution for predicting **the electricity demand** in Spain peninsule for the 24 hours of next day before the day-ahead market session:

- Predictions will be available everyday for the following day in hourly basis.
- For defining the solution, Baktesting tecnique is used. This technique is crucial for ensuring that a ML solution will be feasible in the future.
- The idea is reproducing the behaviour in the past so it's possible to test that final solution will have a good perforance in the future.

## **🎯 Objectives**

The goal of this project is to provide a solution for predicting **the electricity demand** in Spain peninsule for the 24 hours of next day before the day-ahead market session:

- Predictions will be available everyday for the following day in hourly basis.
- For defining the solution, Baktesting tecnique is used. This technique is crucial for ensuring that a ML solution will be feasible in the future.
- The idea is reproducing the behaviour in the past so it's possible to test that final solution will have a good perforance in the future.


Precictions are calculated using the following information in different regions of the country:

- **Temperature** 
- **Population**
- **Main Bank holidays** 
- **Month of the year**
- **Day of the week**
- **Hour of the day**

For the backtesting solution, data from 2015 to 2021 is included.

The prediction is done using:

- **Regression Supervised Learning** 
- **Prediction's accuracy** is meassured using **RMSE** (Root Mean Square Error).


## **👩🏻‍💻 Resources**

- Python 3.7 and libraries ([Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/index.html), [NumPy](https://numpy.org/doc/stable/user/index.html), [matplotlib](https://matplotlib.org/stable/users/index),[seaborn](https://seaborn.pydata.org/index.html), [xgboost](https://xgboost.readthedocs.io/en/stable/)).
- Specific libraries for exporting temperature information ([cdsapi](https://cds.climate.copernicus.eu/api-how-to) and [netCDF4](https://unidata.github.io/netcdf4-python/)).


## **📊 SOTs**

- **Bank holidays by region and year**: Information coming from [public source](https://administracion.gob.es/pag_Home/atencionCiudadana/calendarios/diasInhabiles.html#-b95725c1af8d).
- **2m dewpoint temperature	(K)**: Information exported from [ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview).
- **Popoulation**: Information coming from [INE](https://www.ine.es/jaxiT3/Datos.htm?t=2915).
- **Past demand**: Information coming from [public source](https://www.ree.es/es/apidatos).


## **🗄 Folder structure**

```
 └── project
    ├── .gitignore
    ├── requirements.txt
    ├── README.md
    ├── main_script.py   
    ├── modules
    │   ├── data_extraction
    │   │   └──data_extractor_bank_holidays.py
    │   │   └──data_extractor_electricity_demand.py
    │   │   └──data_extractor_population.py
    │   │   └──data_extractor_temperature.py
    │   └── data_transformation
    │   │   └──data_transformation.py    
    │   └── data_analytics
    │       └──ml_backtesting.py    
    ├── notebooks
    │   ├── data_extraction
    │   │   └──data_extractor_bank_holidays.ipynb
    │   │   └──data_extractor_electricity_demand.ipynb
    │   │   └──data_extractor_population.ipynb
    │   │   └──data_extractor_temperature.ipynb
    │   └── data_transformation
    │   │   └──data_transformation.ipynb  
    │   └── data_analytics
    │       └──eda.ipynb  
    │       └──ml_backtesting.ipynb  
    │       └──final_results.ipynb  
    └── data
        ├── SOTs
        ├── raw_data
        ├── intermediate_data
        └── final_results
       
 ```

 


