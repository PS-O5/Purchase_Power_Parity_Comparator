import pandas as pd
import matplotlib.pyplot as plt
import requests

# Function to fetch data from World Bank API
def fetch_world_bank_data(indicator, country_codes, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country_codes}/indicator/{indicator}?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    data = response.json()[1]  # The actual data is in the second element of the JSON response
    return data

# Function to process the fetched data into a DataFrame
def process_data(data, country_name):
    records = []
    for entry in data:
        if entry['value'] is not None:
            records.append({
                'Year': int(entry['date']),
                country_name: entry['value']
            })
    return pd.DataFrame(records)

# Define parameters
indicator = "NY.GDP.PCAP.PP.CD"  # GDP per capita, PPP (current international $)
countries = {"DEU": "Germany", "IND": "India"}  # Country codes for Germany and India
start_year = 2010
end_year = 2020

# Fetch and process data for each country
df_list = []
for country_code, country_name in countries.items():
    data = fetch_world_bank_data(indicator, country_code, start_year, end_year)
    df = process_data(data, country_name)
    df_list.append(df)

# Merge dataframes on 'Year'
df_final = df_list[0]
for df in df_list[1:]:
    df_final = pd.merge(df_final, df, on='Year', how='outer')

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df_final['Year'], df_final['Germany'], label='Germany', marker='o')
plt.plot(df_final['Year'], df_final['India'], label='India', marker='o')
plt.title('GDP per Capita (PPP) Comparison: Germany vs India')
plt.xlabel('Year')
plt.ylabel('GDP per Capita (PPP, current international $)')
plt.legend()
plt.grid(True)
plt.show()
