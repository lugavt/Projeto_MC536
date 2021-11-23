import numpy as np
import math
from sklearn import linear_model
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

IDH_data = pd.read_csv('./final/data/processed/IDH_data.csv')
sanitation_data = pd.read_csv('./final/data/processed/sanitation_data.csv')
country_data = pd.read_csv('./final/data/processed/countries_data.csv')
mortality_data = pd.read_csv('./final/data/processed/mortality_data.csv')

mortality_data = mortality_data.loc[mortality_data['year'] >= 2000]

IDH_data = IDH_data.loc[IDH_data['year'] >= 2000]

x = []
y = []

for country in country_data['Country']:

    m_data = mortality_data.loc[(mortality_data['country'] == country)]

    idh_data = IDH_data.loc[IDH_data['country'] == country]
    
    soap_data = sanitation_data.loc[(sanitation_data['country'] == country) & (sanitation_data['INDICATOR'] == 'WS_PPL_S-ALB')]
    #Proportion of population using at least basic sanitation services

    water_data = sanitation_data.loc[(sanitation_data['country'] == country) & (sanitation_data['INDICATOR'] == 'WS_PPL_W-ALB')]
    #Proportion of population using at least basic drinking water services

    validated_years = [] #vetor que salva os anos que contém valores de soap e water

    for year in m_data['year']:

        if ((year in soap_data['year'].to_numpy()) & (year in water_data['year'].to_numpy()) & (year in idh_data['year'].to_numpy())):

            validated_years.append(year)

    #print(validated_years)
    for year in validated_years:
        
        idh_value = idh_data.loc[idh_data['year'] == year]
        soap_value = soap_data.loc[soap_data['year'] == year]
        water_value = water_data.loc[water_data['year'] == year]

        row = [idh_value['HDI_VALUE'].values[0], soap_value['OBS_VALUE'].values[0]/100, water_value['OBS_VALUE'].values[0]/100]
        #dividimos por cem pois está em porcentagem
        x.append(row)

        mortality_value = m_data.loc[m_data['year'] == year] 
        y.append(mortality_value['Tuberculosis'].values[0])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

regr = linear_model.LinearRegression()
regr.fit(x_train, y_train)

print('Coeficientes: ', regr.coef_)
print('Intersecção: ', regr.intercept_)

print('Variância: ', regr.score(x_test, y_test))