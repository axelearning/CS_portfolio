'''
INPUT: datasource: https://github.com/CSSEGISandData/COVID-19
GOAL:
 	- load the data about the COVID19
	- clean the data
 	- Reshaping and merging the table in one 
 	- Keeping only the data about Reunion Island
OUTPUT:
	- csv file
	- google sheet 
'''
import pandas as pd

# Load the data
url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

df_confirmed = pd.read_csv(url_confirmed, error_bad_lines=False)
df_death = pd.read_csv(url_death, error_bad_lines=False)
df_recovered = pd.read_csv(url_recovered, error_bad_lines=False)


# Fill the NaN
df_confirmed['Province/State'].fillna(df_confirmed['Country/Region'], inplace=True)
df_death['Province/State'].fillna(df_death['Country/Region'], inplace=True)
df_recovered['Province/State'].fillna(df_recovered['Country/Region'], inplace=True)

# Reshape
def reshape_df(df, state = 'Confirmed'):
    df.set_index(['Province/State','Country/Region','Lat','Long'], inplace=True)
    df = df.stack().reset_index(drop=False)
    df.rename(columns={'level_4':'Date',0:state},inplace=True)
    return df

df_confirmed = df_confirmed.pipe(reshape_df,'Confirmed')
df_death = df_death.pipe(reshape_df,'Death')
df_recovered = df_recovered.pipe(reshape_df,'Recovered')


# temporary fix
df_confirmed['Date'] = df_confirmed['Date'].astype('datetime64[ns]')
df_death['Date'] = df_death['Date'].astype('datetime64[ns]')
df_recovered['Date'] = df_recovered['Date'].astype('datetime64[ns]')

# Merge
database = pd.merge(df_confirmed, df_death)
database = pd.merge(database,df_recovered, how='left')

# Convert type
database['Date'] = database['Date'].astype('datetime64[ns]')

# # Keeping only data fromm Reunion island
# database = database[database['Province/State'] == 'Reunion']

# # cleaning before saving
# database = database.drop_duplicates('Date')
# database.reset_index(drop=True, inplace=True)

# Update the google sheet 
# really long in global case ...
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/Users/axel/Google_Drive/Folder/02_CARRER/01_Startup/COVID_19/drive_key.json', scope)
gc = gspread.authorize(credentials)

spreadsheet_key = '1uZrsUXXBHcwLJu5kg3wY39T_5sudX_keCRtpXvTRQGo'
wks_name = 'Master'
d2g.upload(database, spreadsheet_key, wks_name, credentials=credentials, row_names=True)





