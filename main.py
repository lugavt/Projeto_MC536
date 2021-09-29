import pandas as pd
import numpy as np

IDH_data = pd.read_csv("data/Human Development Index.csv")
IDH_data.drop( ["2017"], axis = 1, inplace = True ) #retiramos a coluna de 2017 pois ela não será usada na análise

mortality_data = pd.read_excel('data/global_mortality.xlsx')

mortality_data["IDH"] = np.nan


for country in IDH_data["Country"]:
    
    mortality_country = country[1:] #retiramos o espaço vazio que há antes do nome do país
    filtered_df = mortality_data.loc[mortality_data["country"] == mortality_country]
    
    
    for year in filtered_df["year"]:
        
        
        element = IDH_data.loc[IDH_data["Country"] == country]
        IDH_value = element[str(year)].iloc[0]
        
        
        mortality_year = f'{int(year):,}'

        mortality_data.loc[(mortality_data.country == mortality_country) & (mortality_data.year == year) , "IDH"] = IDH_value
        

mortality_data.to_csv(r'./data/new_data.csv')