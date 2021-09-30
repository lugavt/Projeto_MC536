import pandas as pd

def handleIndicators(indicator):

    proper_indicators = ["Proportion of population practising open defecation", "Proportion of population using at least basic drinking water services", "Proportion of population using at least basic sanitation services","Proportion of population using safely managed drinking water services", "Proportion of population using safely managed sanitation services", "Proportion of population with a handwashing facility with soap and water available at home" ]

    for ele in proper_indicators:
        if (ele in indicator):
            return (ele)

def handleCountryNameSanitation(country):
    return country[5:]

def handleCountryNameIDH(country):
    return country[1:]


IDH_data = pd.read_csv("data/Human Development Index.csv")
IDH_data.drop( ["2017"], axis = 1, inplace = True ) #retiramos a coluna de 2017 pois ela não será usada na análise
IDH_data["Country"] = IDH_data["Country"].map(handleCountryNameIDH)
IDH_data.rename({'Country':'country'}, axis=1, inplace=True)

sanitation_data = pd.read_csv('data/sanitation_data_2000-2016.csv')
sanitation_data["REF_AREA:Geographic area"] = sanitation_data["REF_AREA:Geographic area"].map(handleCountryNameSanitation)
sanitation_data["INDICATOR:Indicator"] = sanitation_data["INDICATOR:Indicator"].map(handleIndicators)
sanitation_data.drop( ["DATAFLOW", "SEX:Sex"], axis = 1, inplace = True )
sanitation_data = sanitation_data.loc[:, 'REF_AREA:Geographic area':'OBS_VALUE:Observation Value']
sanitation_data.rename({'REF_AREA:Geographic area': 'country', 'INDICATOR:Indicator':'Indicator', 'TIME_PERIOD:Time period':'year', 'OBS_VALUE:Observation Value':'OBS_VALUE'}, axis=1, inplace=True)

mortality_data = pd.read_excel('data/global_mortality.xlsx')

for country in IDH_data["country"]:
     
    if (country not in mortality_data["country"].unique()):
        
        filtered_data = IDH_data["country"] != country
        IDH_data = IDH_data[filtered_data]
        

for country in sanitation_data["country"].unique():
    
    if (country not in mortality_data["country"].unique()):
    
        filtered_data = sanitation_data["country"] != country
        sanitation_data = sanitation_data[filtered_data]

sanitation_data.to_csv(r'./new_data/sanitation_data.csv')

IDH_data.to_csv(r'./new_data/IDH_data.csv')

mortality_data.to_csv(r'./new_data/mortality_data.csv')