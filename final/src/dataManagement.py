import pandas as pd
import numpy as np
from apiRequest import getSanitationData

sanitation_data = getSanitationData()

def handleCountryNameIDH(country):
    return country[1:]

def handleCountryNameCountry(country):
    return country[:-1]

country_data = pd.read_csv('../data/external/countries of the world.csv')
country_data = country_data[['Country','Region','Climate']]
country_data["Country"] = country_data["Country"].map(handleCountryNameCountry)
country_data.to_csv(r'../data/interim/country_data.csv')

IDH_data = pd.read_csv("../data/external/Human Development Index.csv")
IDH_data.drop( ["2017"], axis = 1, inplace = True )
IDH_data["Country"] = IDH_data["Country"].map(handleCountryNameIDH)
IDH_data.rename({'Country':'country', 'HDI Rank':'HDIRank'}, axis=1, inplace=True)
IDH_data.to_csv(r'../data/interim/IDH_data.csv')

sanitation_data.rename({'Geographic area': 'country', 'TIME_PERIOD':'year', 'Service Type':'ServiceType', 'Unit of measure':'UnitOfMeasure'}, axis=1, inplace=True)
sanitation_data = sanitation_data[['REF_AREA','country','INDICATOR','Indicator','ServiceType','year', 'UnitOfMeasure', 'OBS_VALUE']]
sanitation_data.drop(sanitation_data[sanitation_data.year > 2016].index, inplace=True)
sanitation_data.to_csv(r"../data/interim/sanitation_data.csv")

mortality_data = pd.read_excel('../data/external/global_mortality.xlsx')

mortality_data.rename(columns=lambda x: x.replace(' (%)', ''), inplace=True)
mortality_data.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

#filtramos os dados, para verificar a chave externa para a tabela de países 
for country in IDH_data["country"]:
    
    if (country not in country_data["Country"].to_numpy()):

        filtered_data = IDH_data["country"] != country
        IDH_data = IDH_data[filtered_data]
        
for country in sanitation_data["country"].unique():
    
    if (country not in country_data["Country"].to_numpy()):
    
        filtered_data = sanitation_data["country"] != country
        sanitation_data = sanitation_data[filtered_data]

for country in mortality_data["country"].unique():

    if (country not in country_data["Country"].to_numpy()):

        filtered_data = mortality_data["country"] != country
        mortality_data = mortality_data[filtered_data]

#criar uma coluna year e transformar as informações de IDH para esse modelo
newIDH_data = pd.melt(IDH_data.reset_index(), id_vars=['HDIRank', 'country'], var_name='year', value_name='HDI_VALUE')
IDH_data = newIDH_data[newIDH_data.year.str.contains("index") == False]

IDH_data.dropna(subset = ["HDI_VALUE"], inplace=True)

sanitation_data.to_csv(r'../data/processed/sanitation_data.csv')

IDH_data.to_csv(r'../data/processed/IDH_data.csv')

mortality_data.to_csv(r'../data/processed/mortality_data.csv')

country_data.to_csv(r'../data/processed/countries_data.csv')