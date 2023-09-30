import time
import pandas as pd
import numpy as np

print("Hello! Let's explore some US bikeshare data!")
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    while True:
        cities = ["chicago", "new york city", "washington"]
        city = input(
            "\nWhich city would you like to analyze? (Chicago, New York City, or Washington): "
        ).lower()
        if city in cities:
            break
        else:
            print("\nError! Please select one of the provided city names.")

    while True:
        months = ["january", "february", "march", "april", "may", "june", "all"]
        month = input(
            "\nPlease select one of the following months to apply the filter: January, February, March, April, May, June or type 'all' to view all months: "
        ).lower()
        if month in months:
            break
        else:
            print("\nError! Please select one of the provided months.")

    while True:
        days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "all",
        ]
        day = input(
            "\nPlease select one of the days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or type 'all' to view all days: "
        ).lower()
        if day in days:
            break
        else:
            print("\nError! Please select a day.")

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df["Start Time"] = pd.to_datetime(df["Start Time"])

    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.strftime("%A").str.lower()

    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        df = df[df["month"] == month]

    if day != "all":
        df = df[df["day_of_week"] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    MCM = df["month"].mode()[0]
    print("Most Common Month:", MCM)

    MCD = df["day_of_week"].mode()[0]
    print("Most Common Day of the Week:", MCD)

    df["hour"] = df["Start Time"].dt.hour
    MCH = df["hour"].mode()[0]
    print("Most Common Start Hour:", MCH)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    Start_Station = df["Start Station"].mode()[0]
    print("Most Commonly Used Start Station:", Start_Station)

    End_Station = df["End Station"].mode()[0]
    print("Most Commonly Used End Station:", End_Station)

    popular_combination = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print(
        "Most Commonly Used Combination of Start and End Stations:", popular_combination
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    TTT = df["Trip Duration"].sum()
    print("Total Travel Time:", TTT / 86400, "Days")

    MTT = df["Trip Duration"].mean()
    print("Mean Travel Time:", MTT / 60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    UT = df["User Type"].value_counts()
    print("User Types:", UT)

    if city in ["chicago", "new york city"]:
        if "Gender" in df.columns:
            GC = df["Gender"].value_counts()
            print("The total count of gender is:", GC)
        else:
            print("Gender information is not available in this dataset.")
    else:
        print("Gender information is not available for Washington.")

    if city in ["chicago", "new york city"]:
        if "Birth Year" in df.columns:
            earliest_YOB = int(df["Birth Year"].min())
            print("The oldest user was born in", earliest_YOB)
            most_recent_YOB = int(df["Birth Year"].max())
            print("The youngest user was born in", most_recent_YOB)
            common_YOB = int(df["Birth Year"].mode()[0])
            print("Most users are born in", common_YOB)
        else:
            print("Birth Year information is not available in this dataset.")
    else:
        print("Birth Year information is not available for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def display_data(df):
    """Displays data upon user request."""
    start_loc = 0
    while True:
        view_data = input(
            "Would you like to view 5 rows of individual trip data? Enter yes or no: "
        )
        if view_data.lower() != "yes":
            break
        print(df.iloc[start_loc : start_loc + 5])
        start_loc += 5


def main():
    """Combining all the functions above into one and executing it."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
