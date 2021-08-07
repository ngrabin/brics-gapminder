#%%

# import all the data

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import imageio

# reading in files
fert = pd.read_csv('./data/gapminder_total_fertility.csv', index_col=0)
life = pd.read_excel('./data/gapminder_lifeexpectancy.xlsx', index_col=0, nrows=260)
population = pd.read_excel('./data/gapminder_population.xlsx', index_col=0, nrows=260)

# definitions and functions
data = [fert, life]
fert.name = "fertility_rate"
life.name = "life_expectancy"
population.name = "population"


def columns_as_int():
    """coverts columns values into integers"""
    for df in data:
        df.columns = df.columns.astype(int)

def df_meltconv(df):

    df.index.name = 'country'
    df.reset_index(inplace=True)
    df = df.melt(id_vars='country', var_name='year', value_name=df.name)
    return df
       

# making sure that all column values are integers
columns_as_int()

# converting the DataFrames
life_melted = df_meltconv(life)
fert_melted = df_meltconv(fert)
population_melted = df_meltconv(population)

# merging the DataFrames
dataframe_fp = fert_melted.merge(population_melted)
dataframe = dataframe_fp.merge(life_melted)
dataframe

# Main loop for createing the plots for the gif 

for year in range(1960, 2016):
    
    an = dataframe.loc[dataframe['year'].isin([year])] 

    dataframe_subset_an = an.loc[an['country'].isin([
    'Brazil', 'Russia', 'India', 'China', 'South Africa'])
    ]
    # creating moveble textfields
    brazil = an.loc[an['country'].isin(['Brazil'])]
    russia = an.loc[an['country'].isin(['Russia'])]
    india = an.loc[an['country'].isin(['India'])]
    china = an.loc[an['country'].isin(['China'])]
    south_africa = an.loc[an['country'].isin(['South Africa'])]

    font1 = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 36,
        }

    font2 = {'family': 'serif',
        'color':  'darkred',
        'weight': 'light',
        'size': 20,
        }

    font3 = {'family': 'serif',
        'color':  'darkred',
        'weight': 'light',
        'size': 12,
        }
     
    # styling the graph
    plt.figure(figsize=(12, 8), dpi=150)
    plt.style.use('seaborn-dark-palette')
    plt.axis((0, 8, 25, 85))
    plt.grid(True)
    plt.title('BRICS countries', fontdict=font2)
    plt.xlabel('fertility rate', fontdict=font3)
    plt.ylabel('life expectancy in years', fontdict=font3)
    plt.text(1, 35, str(year),fontdict=font1)

    # applying textfields to each year
    plt.text(china['fertility_rate'], china['life_expectancy'], 'China')
    plt.text(russia['fertility_rate'], russia['life_expectancy'], 'Russia')
    plt.text(india['fertility_rate'], india['life_expectancy'], 'India')
    plt.text(brazil['fertility_rate'], brazil['life_expectancy'], 'Brazil')
    plt.text(south_africa['fertility_rate'], south_africa['life_expectancy'], 'South Africa')

    # plotting a scatterplot for each data subset
    sns.scatterplot(x='fertility_rate', y='life_expectancy', hue='country',
            data=dataframe_subset_an, alpha=0.5, size='population', sizes=(500,5000), legend=False)
    
    # saving plot for each year
    plt.savefig('./PNGs/lexp_' + str(year) + '.png')
    plt.close()


# creating an animated scatterplot (gif)
images = []

for i in range(1960, 2016):
    filename = './PNGs/lexp_{}.png'.format(i)
    images.append(imageio.imread(filename))

imageio.mimsave('output.gif', images, fps=20)



