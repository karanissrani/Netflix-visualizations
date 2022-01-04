import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from matplotlib import gridspec

option = st.sidebar.radio(
 "Select the dashboard",
('Viz 1', 'Viz 2', 'Viz 3', 'Viz 4'))

if option == 'Viz 2':
#karan
    karan_data = pd.read_csv('netflix_titles.csv')
    karan_data = karan_data.fillna('NULL')
    karan_data['year_added'] = karan_data['date_added'].apply(lambda x :  x.split(',')[-1])
    karan_data['year_added'] = karan_data['year_added'].apply(lambda x : x if x != 'NULL' else '2020')
    karan_data['year_added'] = karan_data['year_added'].apply(int)

    movie = karan_data[karan_data['type'] == 'Movie']
    tv_show = karan_data[karan_data['type'] == 'TV Show']


    country_data = karan_data['country']
    country_data
    country_counting = pd.Series(dict(Counter(','.join(country_data).replace(' ,',',').replace(', ',',').split(',')))).sort_values(ascending=False)
    country_counting.drop(['NULL'], axis=0, inplace=True)


    tot = sum(country_counting)
    top20 = sum(country_counting[:20]) 

    top20_country = country_counting[:20]

    fig = plt.figure(figsize=(20, 6))
    gs = gridspec.GridSpec(nrows=1, ncols=2,
                        height_ratios=[7], 
                        width_ratios=[15, 8])

    ax = plt.subplot(gs[0])
    sns.barplot(top20_country.index, top20_country, ax=ax, palette="RdGy")
    ax.set_xticklabels(top20_country.index, rotation='90')
    ax.set_title('Top 20 producing countries', fontsize=15, fontweight='bold')

    explode = [0 for _ in range(20)]
    explode[0] = 0.06

    ax2 = plt.subplot(gs[1])
    ax2.pie(top20_country, labels=top20_country.index,
            shadow=True, startangle=0, explode=explode,
            colors=sns.color_palette("RdGy", n_colors=20)
        )
    ax2.axis('equal') 

    st.pyplot(fig)

elif option == 'Viz 1':
#Sneha
    data = pd.read_csv('Comparison.csv')
    df = pd.DataFrame(data)

    X = list(df.iloc[:, 0])
    Y = list(df.iloc[:, 1])
    plt.bar(X, Y, color='g')
    plt.title("Number of movies in topmost streaming platform")
    plt.xlabel("Streaming Platform")
    plt.ylabel("Movies")
    st.pyplot(plt)

    X = list(df.iloc[:, 0])
    Y = list(df.iloc[:, 1])
    plt.plot(X, Y, color='b')
    plt.title("Number of shows in topmost streaming platform")
    plt.xlabel("Streaming Platform")
    plt.ylabel("Shows")
    plt.grid(True)
    st.pyplot(plt)

elif option == 'Viz 4':
    #Ajinkya
    netflix_data = pd.read_csv('netflix_titles.csv')
    ratings_ages= {
        'TV-PG': 'Child(TV-PG)',
        'TV-MA': 'Adult(TV-MA)',
        'TV-Y7-FV': 'Child(TV-Y7-FV)',
        'TV-Y7': 'Child(TV-Y7)',
        'TV-14': 'Adolesent(TV-14)',
        'R': 'Adolecent(R)',
        'TV-Y': 'Infant(TV-Y)',
        'NR': 'Adult(NR)',
        'PG-13': 'Teen(PG-13)',
        'TV-G': 'Infant(TV-G)',
        'PG': 'Child(PG)',
        'G': 'Infant(G)',
        'UR': 'Adult(UR)',
        'NC-17': 'Adult(NC-17)'}
    netflix_data["ratings_ages"] = netflix_data['rating'].replace(ratings_ages)
    value_counts = netflix_data['ratings_ages'].value_counts()

    # converting to df and assigning new names to the columns
    df_value_counts = pd.DataFrame(value_counts)
    df_value_counts = df_value_counts.reset_index()
    df_value_counts.columns = ['rating', 'count'] # change column names

    age_rating = alt.Chart(df_value_counts).mark_bar().encode(
        x='rating',
        y='count'
    ).properties(
        title='Quantitative comparison between rating and number of titles',
        width=600,
        height=500,
    )
    st.write(age_rating)

else:
    #Numbers data
    netflix_numbers = pd.read_csv('netflix_numbers.csv')
    columns = ['Revenue', 'Profit', 'Subscribers']
    value_type = st.sidebar.selectbox('Parameters', columns)

    attribute = ''
    title = ''
    chart_title = ''
    if value_type == 'Revenue':
        attribute = 'revenue'
        title = 'Revenue in billions'
        chart_title = 'Revenue over years'
    elif value_type == 'Profit':
        attribute = 'profit'
        title = 'Profit in Millions'
        chart_title = 'Profit over years'
    elif value_type == 'Subscribers':
        attribute = 'subscribers'
        title = 'Subscribers in Millions'
        chart_title = 'Subscribers over years'
    else:
        attribute = 'revenue'
        title = 'Revenue in billions'
        chart_title = 'Revenue over years'

    ch = alt.Chart(netflix_numbers).mark_line(point = True).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y(attribute+':Q', title=title)
    ).properties(
        title=chart_title,
        width=600,
        height=500,
    )

    st.write(ch)