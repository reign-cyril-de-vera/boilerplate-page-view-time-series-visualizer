import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np
from calendar import month_name
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value']<=df['value'].quantile(0.975)) &
        (df['value']>=df['value'].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index.values, df['value'].values, color='firebrick')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['months'] = pd.Categorical(df_bar.index.strftime('%B'), categories=month_name[1:], ordered=True)
    df_bar = df_bar.groupby(['year', 'months'])['value'].sum().reset_index()
    df_bar = df_bar.pivot(columns='months', index='year', values='value')

    # Draw bar plot
    fig = df_bar.plot.bar(figsize=(10,10)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')  
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['year'] = df.index.year
    df_box['month'] = pd.Categorical(df_box.index.strftime('%B').str.slice(0, 3), 
                                     categories=list(map(lambda month: month[:3], 
                                                         month_name[1:])),
                                     ordered=True)
    # df_box['month'] = df_box['month'].str.slice(0, 3)
    df_box.reset_index(inplace=True)

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2, figsize=(24, 8))

    sns.boxplot(ax=axs[0], data=df_box, x='year', y='value')
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')
    
    sns.boxplot(ax=axs[1], data=df_box, x='month', y='value')
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')
    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
