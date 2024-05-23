import streamlit as st
import pandas as pd
from helper import clean, cleanwc, country_year, wccountry_year, hostco, cwise, winyear, posiinfo
import plotly.express as px

wc = pd.read_csv('worldcups.csv')
wc = cleanwc(wc)

wcmatch = pd.read_csv('wcmatches.csv')
wcmatch = clean(wcmatch)

mergedf = wc.merge(wcmatch, on='year')

sidebar = st.sidebar.radio('Select an option',
                 ('Host Country', 'Country wise', 'Position wise', 'Overall analysis', 'Charts'))

countries = wccountry_year(wc)
countries1, years1 = country_year(wcmatch)
wyear = winyear(mergedf)
posimerge = mergedf[['year', 'winner', 'second', 'third', 'fourth']]
posimerge = posimerge.drop_duplicates()

if sidebar == 'Host Country':
    wcc = st.sidebar.selectbox('Select Country', countries)
    st.table(hostco(wcc, wc, wcmatch))


if sidebar == 'Country wise':
    wcmatchc = st.sidebar.selectbox('Select Country', countries1)
    wcmatchy = st.sidebar.selectbox('Select Year', years1)
    st.table(cwise(wcmatchc, wcmatchy, wcmatch))

if sidebar == 'Position wise':
    posiyear = st.sidebar.selectbox('Select Year', wyear)
    posivalue = posimerge[posimerge['year'] == posiyear]
    posivalue = posivalue.values
    mg = mergedf[mergedf['year'] == posiyear]

    w, s, t, f, mw, mw1, mw2, mw3, ml, ml1, ml2, ml3 = posiinfo(mg)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.title('Winning Team')
        st.header(posivalue[0, 1])
        st.title('Total Goals')
        st.header(w.values[0])
        st.title('Matches won')
        st.header(mw.iloc[0])
        st.title('Matches lost')
        st.header(ml[0])

    with col2:
        st.title('Second Team')
        st.header(posivalue[0, 2])
        st.title('Total Goals')
        st.header(s.values[0])
        st.title('Matches won')
        st.header(mw1.iloc[0])
        st.title('Matches lost')
        st.header(ml1[0])

    with col3:
        st.title('Third Team')
        st.header(posivalue[0, 3])
        st.title('Total Goals')
        st.header(t.values[0])
        st.title('Matches won')
        st.header(mw2.iloc[0])
        st.title('Matches lost')
        st.header(ml2[0])

    with col4:
        st.title('Fourth Team')
        st.header(posivalue[0, 4])
        st.title('Total Goals')
        st.header(f.values[0])
        st.title('Matches won')
        st.header(mw3.iloc[0])
        st.title('Matches lost')
        st.header(ml3[0])

if sidebar == 'Overall analysis':
    overyear = st.sidebar.selectbox('Select Year', wyear)
    overvalue = wc[wc['year'] == overyear]
    overall = overvalue[['goals_scored', 'teams', 'games']]
    ov = overall.values
    st.title('Total Goals Scored')
    st.header(ov[0, 0])
    st.title('Total teams')
    st.header(ov[0, 1])
    st.title('Total games played')
    st.header(ov[0, 2])

if sidebar == 'Charts':
    fig = px.line(wc, x = 'year', y = wc.columns[6:9], title = 'stats over years')
    st.plotly_chart(fig)