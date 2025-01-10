import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df.dropna(subset=['value'], inplace=True)

# Handle outliers
percentile_2_5 = df['value'].quantile(0.025)
percentile_97_5 = df['value'].quantile(0.975)

df = df[(df['value'] >= percentile_2_5) & (df['value'] <= percentile_97_5)]

# Ensure the 'value' column is a float (explicitly cast to float type)
df['value'] = df['value'].astype(float)  # Using Python's built-in float

# Function to draw a line plot
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='b', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    fig.savefig('line_plot.png')
    return fig

# Function to draw a bar plot
def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()  # Use month_name() to get full month names

    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Ensure months are in correct order
    df_bar_grouped = df_bar_grouped[['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']]

    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar_grouped.plot(kind='bar', ax=ax)
    ax.set_title("Average Monthly Page Views")
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    fig.savefig('bar_plot.png')
    return fig
# Function to draw a box plot
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Ensure months are ordered from Jan to Dec
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=months_order, ordered=True)

    # Convert 'value' to float explicitly (ensure no errors related to types)
    df_box['value'] = df_box['value'].astype('float64')  # Use np.float64 if necessary

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")  # Ensure this is "Year" with a capital 'Y'
    ax1.set_ylabel("Page Views")  # Ensure the y-axis label is "Page Views"

    sns.boxplot(x='month', y='value', data=df_box, ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")  # Ensure the x-axis label is "Month"
    ax2.set_ylabel("Page Views")  # Fix: change 'value' to 'Page Views'

    fig.savefig('box_plot.png')
    return fig
