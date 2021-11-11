import pandas as pd
import requests
import io

def getSanitationData():

    url = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,WASH_HOUSEHOLDS,1.0/.WS_PPL_H-B+WS_PPL_S-ALB+WS_PPL_S-SM+WS_PPL_W-ALB+WS_PPL_W-SM+WS_PPS_S-OD..._T?format=csv&labels=both"
    data = requests.get(url).content
    csv = pd.read_csv(io.StringIO(data.decode("utf-8")))
    csv.to_csv(r"../data/external/sanitation_data")

    return csv