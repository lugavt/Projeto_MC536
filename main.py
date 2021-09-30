import pandas as pd
import numpy as np

IDH_data = pd.read_csv("data/Human Development Index.csv")
IDH_data.drop( ["2017"], axis = 1, inplace = True ) #retiramos a coluna de 2017 pois ela não será usada na análise


def handleIndicators(indicator):

    proper_indicators = ["Proportion of population practising open defecation", "Proportion of population using at least basic drinking water services", "Proportion of population using at least basic sanitation services","Proportion of population using safely managed drinking water services", "Proportion of population using safely managed sanitation services", "Proportion of population with a handwashing facility with soap and water available at home" ]

    for ele in proper_indicators:
        if (ele in indicator):
            return (ele)

def handleCountryName(country):
    return country[5:]


sanitation_data = pd.read_csv('data/sanitation_data_2000-2016.csv')
sanitation_data["REF_AREA:Geographic area"] = sanitation_data["REF_AREA:Geographic area"].map(handleCountryName)
sanitation_data["INDICATOR:Indicator"] = sanitation_data["INDICATOR:Indicator"].map(handleIndicators)
print(sanitation_data)

mortality_data = pd.read_excel('data/global_mortality.xlsx')

mortality_data["IDH"] = np.nan
mortality_data["Proportion of population practising open defecation"] = np.nan
mortality_data["Proportion of population using at least basic drinking water services"] = np.nan
mortality_data["Proportion of population using at least basic sanitation services"] = np.nan
mortality_data["Proportion of population using safely managed drinking water services"] = np.nan
mortality_data["Proportion of population using safely managed sanitation services"] = np.nan
mortality_data["Proportion of population with a handwashing facility with soap and water available at home"] = np.nan

print(mortality_data)


for country in IDH_data["Country"]:
    
    mortality_country = country[1:] #retiramos o espaço vazio que há antes do nome do país
    filtered_df = mortality_data.loc[mortality_data["country"] == mortality_country]
    
    
    for year in filtered_df["year"]:
        
        
        element = IDH_data.loc[IDH_data["Country"] == country]
        IDH_value = element[str(year)].iloc[0]
        

        mortality_data.loc[(mortality_data.country == mortality_country) & (mortality_data.year == year) , "IDH"] = IDH_value
        



for idh_country in IDH_data["Country"]:

    country = idh_country[1:]
    country_filtered_df = sanitation_data.loc[sanitation_data["REF_AREA:Geographic area"] == country]
    print(country)

    for year in country_filtered_df["TIME_PERIOD:Time period"]:

        year_filtered_df = country_filtered_df.loc[country_filtered_df["TIME_PERIOD:Time period"] == year]

        for indicator in year_filtered_df["INDICATOR:Indicator"]:
            
            element = year_filtered_df.loc[year_filtered_df["INDICATOR:Indicator"] == indicator]
            sanitation_value = element["OBS_VALUE:Observation Value"].iloc[0]

            
            mortality_data.loc[(mortality_data.country == country) & (mortality_data.year == year), str(indicator)] = sanitation_value


print(mortality_data)
mortality_data.to_csv(r'./data/new_data.csv')