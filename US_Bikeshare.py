import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filter - the way that user choose to filter the data, its value can be month, day, both or none.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWhich city would you like to explore: chicago, new york city or washington?\n')
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        print('Sorry, there is no data for ', city, '.')
        city = input('\nPlease enter a valid city: ')

    # ask the user how he want to filter the data
    filter = input('\nWould you like to filter the data by month, day, both or not at all? Type none for no time filter.\n')

    if filter == 'month':
        day = 'all'
        # get user input for month (all, january, february, ... , june)
        month = input('\nWhich month would you like to analyze: January, February, March, April, May or June?\n')
        while months.index(month) + 1 > 6:
            print('Sorry, there is no data for ', month, '.')
            month = input('\nPlease enter a valid month: ')

    elif filter == 'day':
        month = 'all'
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('\nWhich day would you like to analyze: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n')

    elif filter == 'both':
        # get user input for month (all, january, february, ... , june)
        month = input('\nWhich month would you like to analyze: January, February, March, April, May or June?\n')
        while months.index(month) + 1 > 6:
            print('Sorry, there is no data for ', month, '.')
            month = input('\nPlease enter a valid month: ')
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('\nWhich day would you like to analyze: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n')

    else:
        month = 'all'
        day = 'all'

    return city, month, day, filter


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if filter != 'month' and filter != 'both':
        month_int = df['month'].value_counts().index[0]
        month_name = months[month_int-1]
        month_count = df['month'].value_counts().values[0]
        print('\nMost frequent month of Travel: ', month_name, ', Count: ', month_count, ', Filter: ', filter, '.')

    # display the most common day of week
    if filter != 'day' and filter != 'both':
        day_name = df['day_of_week'].value_counts().index[0]
        day_count = df['day_of_week'].value_counts().values[0]
        print('\nMost frequent day of Travel: ', day_name, ', Count: ', day_count, ', Filter: ', filter, '.')

    # display the most common start hour
    hour_int = df['hour'].value_counts().index[0]
    hour_count = df['hour'].value_counts().values[0]
    print('\nMost frequent hour of Travel: ', hour_int, ', Count: ', hour_count, ', Filter: ', filter, '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().index[0]
    counts_start = df['Start Station'].value_counts().values[0]
    print('\nMost popupar start station: ', popular_start, ', Count: ', counts_start, ', Filter: ', filter, '.')

    # display most commonly used end station
    popular_end = df['End Station'].value_counts().index[0]
    counts_end = df['End Station'].value_counts().values[0]
    print('\nMost popupar end station: ', popular_end, ', Count: ', counts_end, ', Filter: ', filter, '.')

    # check unique value of start stations and end stations
    # start_stations = df['Start Station'].unique()
    # end_stations = df['End Station'].unique()

    # check most frequent start stations and most frequent end stations
    start_stations = df['Start Station'].value_counts().index[:30]
    end_stations = df['End Station'].value_counts().index[:30]

    # check different combinations of start and end stations
    trips = []
    for startst in start_stations:
        for endst in end_stations:
            df_sub = df.loc[(df['Start Station'] == startst) & (df['End Station'] == endst)]
            trip_counts = len(df_sub)
            tmp = [startst, endst, trip_counts]
            trips.append(tmp)

    # create a new dataframe
    new_df = pd.DataFrame(data=trips, columns=['Start Station', 'End Station', 'Trip Counts'])

    # select the most popular trip combination
    tmp = new_df.loc[new_df['Trip Counts'].idxmax()]

    # display most frequent combination of start station and end station trip
    print("\nMost popular trip is:")
    print('\nStart from:', tmp['Start Station'])
    print('\nEnd at:', tmp['End Station'])
    print('\nCounts:', tmp['Trip Counts'], ', Filter:', filter, ".")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum(axis=0)
    timedelta_tt = str(datetime.timedelta(seconds=int(total_time)))
    print("\nTotal travel duration:", total_time, ", Timedelta:", timedelta_tt, " , Filter:", filter)

    # display mean travel time
    avg_time = df['Trip Duration'].mean(axis=0)
    timedelta_at = str(datetime.timedelta(seconds=int(avg_time)))
    print("\nAverage travel duration:", avg_time, ", Timedelta:", timedelta_at, " , Filter:", filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types = len(df['User Type'].value_counts())
    for i in range(types):
        print('\n', df['User Type'].value_counts().index[i], ':', df['User Type'].value_counts().values[i], '      Filter:', filter)

    # Display counts of gender
    if city != 'washington':
        types = len(df['Gender'].value_counts())
        for i in range(types):
            print('\n', df['Gender'].value_counts().index[i], ':', df['Gender'].value_counts().values[i], '      Filter:', filter)
    else:
        print('\nNo gender information.')

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        birth_year = int(df['Birth Year'].min())
        print('\nEarliest year of birth: ', birth_year, '      Filter:', filter)

        birth_year = int(df['Birth Year'].max())
        print('\nMost recent year of birth: ', birth_year, '      Filter:', filter)

        birth_year = int(df['Birth Year'].value_counts().index[0])
        print('\nMost common year of birth: ', birth_year, '      Filter:', filter)

    else:
        print('\nNo birth year information.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filter)
        station_stats(df, filter)
        trip_duration_stats(df, filter)
        user_stats(df, city, filter)

        view_individual = input('\nWould you like to view individual travel data?\n')
        if view_individual.lower() == 'yes':
            for i in range(len(df)):
                print(df.iloc[i])
                print('-'*40)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
