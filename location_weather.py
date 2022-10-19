import requests

def destination_weather(city):
    url = "https://api.ipma.pt/open-data/distrits-islands.json"
    response = requests.get(url=url)
    ipma_loc =  pd.DataFrame(response.json())
    ipma_data = pd.json_normalize(ipma_loc["data"])
    ipma_df_loc = ipma_data[["globalIdLocal", "local"]]
    list_globalidloc = list(ipma_df_loc["globalIdLocal"].values)
    url2 = "http://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"
    ipma_dict = {}
    for idloc in list_globalidloc:
        url =  url2 + str(idloc) + ".json"
        response = requests.get(url = url)
        ipma_dict[idloc] = response.json()
    ipma_df = pd.DataFrame(ipma_dict).T
    ipma_df.reset_index(inplace=True)
    to_bread_df = pd.json_normalize(ipma_df["data"])
    for i in range(len(to_bread_df.columns)-2):
        temp = pd.json_normalize(to_bread_df[i])
        ipma_df = pd.concat([ipma_df, temp], axis=1)
    ipma_clear = ipma_df.drop(columns=["country","data","predWindDir","idWeatherType","classWindSpeed","classPrecInt","dataUpdate","longitude","latitude","index","owner"])
    hoje = ipma_clear.iloc[:,:5]
    amanha = ipma_clear.iloc[:,[0,5,6,7,8]]
    depois_de_amanha = ipma_clear.iloc[:,[0,9,10,11,12]]
    vertical_concat = pd.concat([hoje, amanha, depois_de_amanha], axis=0)
    all_columns = pd.merge(vertical_concat, ipma_df_loc)
    return all_columns.loc[all_columns['local'] == city]

destination_weather("Lisboa")