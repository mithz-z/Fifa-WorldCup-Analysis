import pandas as pd
import streamlit as st

def clean(wcmatch):
    # No need of win conditions, outcome or month
    wcmatch.drop(['win_conditions', 'outcome', 'month'], inplace=True, axis=1)
    # Tied matches are nan values
    wcmatch = wcmatch.fillna('tie')

    # Correcting historical inaccuracy
    wcmatch['home_team'] = wcmatch['home_team'].str.replace('Soviet Union', 'Russia')
    wcmatch['away_team'] = wcmatch['away_team'].str.replace('Soviet Union', 'Russia')
    wcmatch['winning_team'] = wcmatch['winning_team'].str.replace('Soviet Union', 'Russia')

    wcmatch['home_team'] = wcmatch['home_team'].str.replace('East Germany', 'Germany')
    wcmatch['away_team'] = wcmatch['away_team'].str.replace('East Germany', 'Germany')
    wcmatch['winning_team'] = wcmatch['winning_team'].str.replace('East Germany', 'Germany')

    wcmatch['home_team'] = wcmatch['home_team'].str.replace('West Germany', 'Germany')
    wcmatch['away_team'] = wcmatch['away_team'].str.replace('West Germany', 'Germany')
    wcmatch['winning_team'] = wcmatch['winning_team'].str.replace('West Germany', 'Germany')

    wcmatch['home_team'] = wcmatch['home_team'].str.replace('Northern Ireland', 'Ireland')
    wcmatch['away_team'] = wcmatch['away_team'].str.replace('Northern Ireland', 'Ireland')
    wcmatch['winning_team'] = wcmatch['winning_team'].str.replace('Northern Ireland', 'Ireland')

    wcmatch['home_team'] = wcmatch['home_team'].str.replace('Republic of Ireland', 'Ireland')
    wcmatch['away_team'] = wcmatch['away_team'].str.replace('Republic of Ireland', 'Ireland')
    wcmatch['winning_team'] = wcmatch['winning_team'].str.replace('Republic of Ireland', 'Ireland')

    wcmatch['home_team'] = wcmatch['home_team'].str.replace('FR Yugoslavia', 'Yugoslavia')
    wcmatch['away_team'] = wcmatch['away_team'].str.replace('FR Yugoslavia', 'Yugoslavia')
    wcmatch['winning_team'] = wcmatch['winning_team'].str.replace('FR Yugoslavia', 'Yugoslavia')

    return wcmatch

def cleanwc(wc):
    # Correcting historical inaccuracies
    wc['winner'] = wc['winner'].str.replace('West Germany', 'Germany')
    wc['second'] = wc['second'].str.replace('West Germany', 'Germany')
    wc['third'] = wc['third'].str.replace('West Germany', 'Germany')
    wc['fourth'] = wc['fourth'].str.replace('West Germany', 'Germany')

    wc['host'] = wc['host'].str.replace('USA', 'United States')
    wc['third'] = wc['third'].str.replace('USA', 'United States')

    # Japan and South Korea hosted a year together, some matches were in japan and some were in south korea
    wc['host'] = wc['host'].str.replace('Japan, South Korea', 'Japan')

    # Adding south korea as a separate row
    row = pd.DataFrame({'year':2002, 'host':'South Korea', 'winner':'Brazil', 'second':'Germany',
                        'third':'Turkey', 'fourth':'South Korea', 'goals_scored':161, 'teams':32, 'games':64, 'attendance':2724604},  index = [16.5])
    wc = pd.concat([wc.iloc[:16], row, wc.iloc[16:]]).reset_index(drop=True)
    wc

    return wc

def country_year(wcmatch):
    # Taking unique names of countries for selectbox
    ab = wcmatch['home_team'].unique()
    ba = wcmatch['away_team'].unique()

    ab.sort()
    ba.sort()

    country = list(set(ab) | set(ba))
    country.sort()
    country.insert(0, 'Overall')

    # Taking unique year values for selectbox
    year = wcmatch['year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    return country, year

def wccountry_year(wc):
    # Taking names of countries that hosted a tournament
    wccountry = wc['host'].unique().tolist()
    wccountry.sort()
    wccountry.insert(0, 'Overall')

    return wccountry

def hostco(c, wc ,wcmatch):
    # Takes country names as input and displays matches hosted in that country
    if c == 'Overall':
        temp_df = wc
    elif c != 'Overall':
        temp_df = wcmatch[wcmatch['country'] == c]
    return temp_df
    
def cwise(country, year, wcmatch):
    # Takes country names and year as input and displays which matches were played by which country in which year
    if country == 'Overall' and year == 'Overall':
        temp_df1 = wcmatch
    elif country != 'Overall' and year == 'Overall':
        temp_df1 = wcmatch[(wcmatch['home_team'] == country) | (wcmatch['away_team'] == country)]
    elif country == 'Overall' and year != 'Overall':
        temp_df1 = wcmatch[wcmatch['year'] == int(year)]
    elif country != 'Overall' and year != 'Overall':
        temp_df1 = wcmatch[((wcmatch['home_team'] == country) | (wcmatch['away_team'] == country)) & (wcmatch['year'] == int(year))]
    if temp_df1.empty:
        st.title('This country did not play this year')
    else:
        return temp_df1

def winyear(mergedf):
    # Gives unique value of year without adding overall
    wy = mergedf['year'].unique().tolist()
    wy.sort()
    return wy

def posiinfo(mg):
    # Gives number of goals the winning team have
    winnergoal = mg[mg['winner'] == mg['home_team']]
    winnergoal1 = mg[mg['winner'] == mg['away_team']]
    wg = winnergoal.groupby('winner')['home_score'].sum()
    wg1 = winnergoal1.groupby('winner')['away_score'].sum()
    w = wg.add(wg1, fill_value=0).astype('int')

    # Gives number of goals the second team have
    secondgoal = mg[mg['second'] == mg['home_team']]
    secondgoal1 = mg[mg['second'] == mg['away_team']]
    sg = secondgoal.groupby('second')['home_score'].sum()
    sg1 = secondgoal1.groupby('second')['away_score'].sum()
    s = sg.add(sg1, fill_value=0).astype('int')

    # Gives number of goals the third team have
    thirdgoal = mg[mg['third'] == mg['home_team']]
    thirdgoal1 = mg[mg['third'] == mg['away_team']]
    tg = thirdgoal.groupby('third')['home_score'].sum()
    tg1 = thirdgoal1.groupby('third')['away_score'].sum()
    t = tg.add(tg1, fill_value=0).astype('int')

    # Gives number of goals the fourth team have
    fourthgoal = mg[mg['third'] == mg['home_team']]
    fourthgoal1 = mg[mg['third'] == mg['away_team']]
    fg = fourthgoal.groupby('third')['home_score'].sum()
    fg1 = fourthgoal1.groupby('third')['away_score'].sum()
    f = fg.add(fg1, fill_value=0).astype('int')

    # Gives number of wins the winning team have
    matchwon = mg[mg['winner'] == mg['winning_team']]
    mw = matchwon['winning_team'].value_counts()

    # Gives number of wins the second team have
    matchwon1 = mg[mg['second'] == mg['winning_team']]
    mw1 = matchwon1['winning_team'].value_counts()
    
    # Gives number of wins the third team have
    matchwon2 = mg[mg['third'] == mg['winning_team']]
    mw2 = matchwon2['winning_team'].value_counts()

    # Gives number of wins the fourth team have
    matchwon3 = mg[mg['fourth'] == mg['winning_team']]
    mw3 = matchwon3['winning_team'].value_counts()

    # Gives number of losses the winning team have
    matchlos = mg[mg['winner'] == mg['losing_team']]
    ml = matchlos['losing_team'].value_counts().tolist()
    # Appending 0 because some are empty list and since in the selectbox we are using variable.values[0] empty list problem gets resolved
    ml.append(0)

    # Gives number of wins the second team have
    matchlos1 = mg[mg['second'] == mg['losing_team']]
    ml1 = matchlos1['losing_team'].value_counts().tolist()
    # Appending 0 because some are empty list and since in the selectbox we are using variable.values[0] empty list problem gets resolved
    ml1.append(0)

    # Gives number of wins the third team have
    matchlos2 = mg[mg['third'] == mg['losing_team']]
    ml2 = matchlos2['losing_team'].value_counts().tolist()
    # Appending 0 because some are empty list and since in the selectbox we are using variable.values[0] empty list problem gets resolved
    ml2.append(0)

    # Gives number of wins the fourth team have
    matchlos3 = mg[mg['fourth'] == mg['losing_team']]
    ml3 = matchlos3['losing_team'].value_counts().tolist()
    # Appending 0 because some are empty list and since in the selectbox we are using variable.values[0] empty list problem gets resolved
    ml3.append(0)

    return w, s, t, f, mw, mw1, mw2, mw3, ml, ml1, ml2, ml3