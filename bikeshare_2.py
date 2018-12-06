#%%
#import sys
#from itertools import permutations, combinations, product
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
#%%
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze\n
        (str) month - name of the month to filter by, or "all" to apply no month filter\n
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    city = custom_input('Select a City among these: (1 to 3)',
                       cities, 'City' , get_all=False)
    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = custom_input('Select a Month among these: (1 to 6) (0 for all)',
                       months, 'Month')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = custom_input('Select a Day among these: (1 to 7) (0 for all)',
                       days, 'Day')
    #print('Day {} is Selected.'.format(day))


    print('-'*40)
    print('get_filters done :')
    print((city, month, day))
    print('-'*40)
    return city, month, day
#%%

def custom_input(input_desc:str, item_list:list , context:str , get_all=True) :
    """
    Custom function to take input

    """
    print('\n'+input_desc+'\n'+' | '.join(item_list).capitalize())
    while True:
        ask_str = '(1 to '+str(len(item_list))+')'
        if get_all:
            ask_str += ' (0 for all) : '
        else:
            ask_str += ' : '
        value = input(ask_str)
        try:
            value = int(value)
        except ValueError:
            continue
        if get_all :
            if 0<=value<=len(item_list):
                break
        elif 0<value<=len(item_list):
            break
    if value==0 and get_all:
        value = 'all'
    else:
        value = item_list[value-1]
    print('{} \'{}\' is Selected.'.format(context, value))
    return value


#%%
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze\n
        (str) month - name of the month to filter by, or "all" to apply no month filter\n
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #path = ''
    path = 'Sources/bikeshare-2/'
    filepath = path + CITY_DATA[city]
    df = pd.read_csv(filepath)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'],format='%Y-%m-%d',exact=False )
    df['End Time'] = pd.to_datetime(df['End Time'],format='%Y-%m-%d',exact=False )
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour



    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}
        # filter by month to create the new dataframe
        df = df[df['month'] == months[month]]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6}
        df = df[df['day_of_week'] == days[day]]


    return df
#%%

def time_stats(df,all_months=True,all_days=True):
    """Displays statistics on the most frequent times of travel."""

    print('\nCALCULATING THE MOST FREQUENT TIMES OF TRAVEL...\n')
    start_time = time.time()

    # display the most common month

    popular_month = ''
    if all_months:
        month_counts = df.groupby('month').groups
        month_counts = pd.Series(np.array([len(value) for value in month_counts.values()]), index=month_counts.keys())
        #print('month counts : \n',month_counts)
        popular_month = month_counts.idxmax() - 1
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        print('Popular month : ' + months[popular_month])

    # display the most common day of week
    popular_day = ''
    if all_days:
        days_counts = df.groupby('day_of_week').groups
        days_counts = pd.Series(np.array([len(value) for value in days_counts.values()]), index=days_counts.keys())
        #print('day counts : \n', days_counts)
        popular_day = days_counts.idxmax()
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        print('Popular day : ' + days[popular_day])

    # display the most common start hour
    hours_counts = df.groupby('hour').groups
    hours_counts = pd.Series(np.array([len(value) for value in hours_counts.values()]), index=hours_counts.keys())
    popular_hour = hours_counts.idxmax()
    print('Popular hour : ', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#%%


#%%

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCALCULATING The Most POPULAR STATIONS and TRIP...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations =  df.groupby('Start Station').groups
    start_station_counts = pd.Series(np.array([len(group) for group in start_stations.values()]), index = start_stations.keys())
    print('Popular Start Station : ', start_station_counts.idxmax(), ' with ', start_station_counts.max(), ' uses.')

    # display most commonly used end station
    end_stations =  df.groupby('End Station').groups
    end_station_counts = pd.Series(np.array([len(group) for group in end_stations.values()]), index = end_stations.keys())
    print('Popular End Station : ', end_station_counts.idxmax(), ' with ', end_station_counts.max(), ' uses.')


    # display most frequent combination of start station and end station trip
    path_counts = trip_path_counter(df)
    print('The most frequent path is : \n')
    print(path_counts.loc[[path_counts['Count'].idxmax()]] )

    # Additional statistics
    print('\n\n Additional Station Statistics')
    print('-'*20)
    print('The most frequent casual ride path is : (i.e. start station = end station)')
    casual_path_counts = path_counts[path_counts['Start Station']==path_counts['End Station']].filter(['Start Station', 'Count']).rename({'Start Station': 'Station'}, axis='columns')
    print(casual_path_counts.loc[[casual_path_counts['Count'].idxmax()]])
    print('Stations with no incoming trips : ')
    print(start_stations.keys() - (start_stations.keys() & end_stations.keys()))
    print('\nStations with no outgoing trips :')
    print(end_stations.keys() - (start_stations.keys() & end_stations.keys()))

    #print(len(start_stations.keys()))


    print("\nstation_stats() took %s seconds." % (time.time() - start_time))
    print('-'*40)

#%%
def trip_path_counter(df: pd.DataFrame):

    # Only Includes the trip paths take in the dataset. (Not all the possible paths that could be taken)
    trip_paths = df[['Start Station', 'End Station']]
    #unique_trip_paths = trip_paths.drop_duplicates()

    # path counts : unique paths and number of records on that path
    path_counts = trip_paths.groupby(['Start Station', 'End Station']).size().reset_index(name = 'Count')
    # casual path counts : unique paths where the start and end station is the same and the number of records for each of such path
    #print(type(path_counts))
    #print(path_counts.loc[path_counts['Count'].idxmax()])

    return path_counts

#%%

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCALCULATING TRIP DURATION...\n')
    start_time = time.time()

    # display total travel time
    print('Total duration:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean duration:', df['Trip Duration'].mean())

    print("\ntrip_duration_stats() took %s seconds." % (time.time() - start_time))
    print('-'*40)

#%%

def user_stats(df: pd.DataFrame):
    """Displays statistics on bikeshare users."""

    print('\nCALCULATING USER STATS...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df.groupby(['User Type']).size().reset_index(name = 'Count')
    print('User Type counts: ')
    print(user_type_counts)
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df.groupby(['Gender']).size().reset_index(name = 'Count')
        unspecified_count = len(df.index) - gender_counts['Count'].sum()
        gender_counts = gender_counts.append({'Gender': 'Unspecified', 'Count': unspecified_count},ignore_index=True)
        print('\nGender counts: ')
        print(gender_counts)
    else:
        print('\nGender data not given')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest Year : ',df['Birth Year'].min())
        print('Latest Year : ',df['Birth Year'].max())
        birth_year_counts = df.groupby('Birth Year').size().reset_index(name = 'Count')
        print('Most common year of birth: ',
              birth_year_counts.iloc[birth_year_counts['Count'].idxmax()]['Birth Year'])
    else:
        print('\nBirth Year data not given')

    print("\nuser_stats() took %s seconds." % (time.time() - start_time))
    print('-'*40)

#%%

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month=month, day=day)
        time_stats(df,all_months=month=='all',all_days=day=='all')
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ('yes','y'):
            break


if __name__ == "__main__":
    main()
