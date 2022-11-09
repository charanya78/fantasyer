"""
@author: Aswatth
"""
import streamlit as st
import pandas as pd
import numpy as np 
import os

def RemoveDuplicate(listToRemoveDuplicates):
    return list(set(listToRemoveDuplicates))

def TossTab(matchDataFrame):
    #Get venue list
    venueList = matchDataFrame['Venue']
    #Removing duplicates
    venueList = RemoveDuplicate(venueList)

    #Get team list
    teamList = matchDataFrame['Team1']
    #Remove duplicates
    teamList = RemoveDuplicate(teamList)

    #Get season list
    seasonList = matchDataFrame['Season']
    #Removin duplicates
    seasonList = RemoveDuplicate(seasonList)
    
    ##### Venue data calculation #####
    #st.dataframe(matchDataFrame)
    selectedVenue = st.selectbox('Venue',venueList)
    
    venue_subset = matchDataFrame[matchDataFrame['Venue'] == selectedVenue]

    total_games = len(venue_subset)
    toss_outcome = venue_subset[ venue_subset ["TossWinner"]== venue_subset["WinningTeam"] ] 
    toss_winners = len(toss_outcome)

    TossAndMatchWin_Percentage = toss_winners / total_games * 100
    TossWinAndFieldWin_Percentage = len(venue_subset [venue_subset["TossDecision"]=='field']) / total_games * 100

    # st.dataframe(venue_subset)
    st.markdown('In **'+ selectedVenue +'**:')
    st.markdown('Percentage of chances when team won the toss and match: '+ str(round(TossAndMatchWin_Percentage,2)) + '%')
    st.markdown('Percentage of chances when team chose to field: '+ str(round(TossWinAndFieldWin_Percentage,2)) + '%')
    # st.markdown('Matches won by **'+ selectedTeam2 +'** when they won the toss: '+str(41)+'%') #TODO: To be updated with calculated number
    # st.markdown('Time when **'+ selectedTeam1 +'** who won the toss and chose to bat: '+str(42)+'%') #TODO: To be updated with calculated number
    # st.markdown('Time when **'+ selectedTeam2 +'** who won the toss and chose to bat: '+str(42)+'%') #TODO: To be updated with calculated number

    ##### Season data calculation#####    
    selectedSeason = st.selectbox('Season', seasonList)
    season_subset = matchDataFrame[matchDataFrame['Season'] == selectedSeason]

    total_games = len(season_subset)

    season_trends = len(season_subset[ season_subset ["TossWinner"] == season_subset["WinningTeam"] ])
    TossAndMatchWin_Percentage = season_trends / total_games * 100
    TossWinAndFieldWin_Percentage = len(season_subset [season_subset["TossDecision"] =='field']) / total_games * 100

    st.markdown('In **'+ str(selectedSeason) +'**:')
    st.markdown('Percentage of chances when team won the toss and match: '+ str(round(TossAndMatchWin_Percentage,2)) + '%')
    st.markdown('Percentage of chances when team chose to field: '+ str(round(TossWinAndFieldWin_Percentage,2)) + '%')

    ##### Team data calculation #####
    selectedTeam1 = st.selectbox('Team 1',teamList)

    team_trends = matchDataFrame [ matchDataFrame ["Team1"] == selectedTeam1]
    team_trends2 = matchDataFrame [ matchDataFrame["Team2"] == selectedTeam1] 

    total = len(team_trends) + len(team_trends2)

    team = len(team_trends[ team_trends ["TossWinner"] == selectedTeam1])
    team = team + len(team_trends2 [team_trends2 ["TossWinner"] == selectedTeam1])

    total_toss_wins = team 
    toss_win_percentage = total_toss_wins / total * 100
    st.markdown(selectedTeam1 + ' won the toss ' + str(round(toss_win_percentage,2)) + '% of the time')

    team1 = team_trends[ team_trends ["TossWinner"] == selectedTeam1]
    team2 = team_trends2 [team_trends2 ["TossWinner"] == selectedTeam1]

    team_wins = len(team1 [team1 ["WinningTeam"] == selectedTeam1]) + len(team2 [team2 ["WinningTeam"] == selectedTeam1])

    match_win_percentage = team_wins / total_toss_wins * 100

    st.markdown(selectedTeam1 + ' won the match ' + str(round(match_win_percentage,2)) + '% of the time when they won toss')
    
    ##### Opposition Data calculation #####
    oppositionTeam = st.selectbox('Team 2',teamList)
    team_trends = matchDataFrame [ matchDataFrame ["Team1"] == oppositionTeam]
    team_wins_bat = len(team_trends [ team_trends[ "WinningTeam"] == oppositionTeam])

    team_trends2 = matchDataFrame [ matchDataFrame ["Team2"] == oppositionTeam]
    team_wins_bowl = len(team_trends [ team_trends[ "WinningTeam"] == oppositionTeam])

    total = team_wins_bat + team_wins_bowl

    bat_win_percentage = team_wins_bat / total * 100
    bowl_win_percentage = team_wins_bowl / total * 100

    st.markdown('Percentage of wins when '+ oppositionTeam + ' chose to bat: ' + str(round(bat_win_percentage,2)))
    st.markdown('Percentage of wins when '+ oppositionTeam + ' chose to bowl: ' + str(round(bowl_win_percentage,2)))

def BatterVsGround(matchDataFrame, deliveriesDataFrame):
    #Get batman list
    batsmanList = deliveriesDataFrame['batter']
    #Remove duplicates
    batsmanList = RemoveDuplicate(batsmanList)

    #Get city list
    cityList = matchDataFrame["City"]
    #Remove duplicates
    cityList = RemoveDuplicate(cityList)

    selectedCity = st.selectbox('City', cityList)

    venue_subset = matchDataFrame[matchDataFrame["City"] == selectedCity]
    matchIdList = venue_subset["ID"].to_numpy()

    selectedBatter = st.selectbox('Batsmen',batsmanList,key='batter_venue')
    player_subset = deliveriesDataFrame[deliveriesDataFrame["batter"] == selectedBatter]

    final_df = []
    for i in range(len(player_subset)):
        if player_subset.iat[i,0] in matchIdList:
            final_df.append(player_subset.iloc[i])
    final_df = pd.DataFrame(final_df)
    # st.dataframe(final_df)

    if(len(final_df) == 0):
        st.markdown("Player not played at ground")
    else:
        ##### Overall #####
        total_runs = final_df["batsman_run"].sum()
        
        total_innings = len(pd.unique(final_df['ID']))
        
        total_outs = final_df[final_df["player_out"] == selectedBatter]
        
        average = 0
        if(len(total_outs) == 0):
            st.markdown("Player not yet dismissed at ground")
        else:
            average = total_runs / len(total_outs)
                    
        strike_rate = total_runs / len(final_df) * 100
        
        dots = final_df[final_df["batsman_run"] == 0]
        dot_percentage = len(dots)/len(final_df) * 100
        
        boundaries = final_df[final_df["batsman_run"] == 4]
        sixes =  final_df[final_df["batsman_run"] == 6]
        boundary_percentage = len(boundaries) + len(sixes) / len(final_df) * 100

        overallData = [[round(total_runs,2), round(total_innings,2), round(average,2), round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]

        ##### 1st innings #####
        firstInningData = [[]]
        
        final_df_1 = final_df[final_df["innings"]==1]

        if(len(final_df_1)==0):
            st.markdown("Player not played at ground in 1st innings")
        else:
            total_runs = final_df_1["batsman_run"].sum()

            total_innings = len(pd.unique(final_df_1['ID']))

            total_outs = final_df_1[final_df_1["player_out"] == selectedBatter]

            average=0
            if(len(total_outs)==0):
                st.markdown("Player not yer dismissed at ground")
            else:
                average = total_runs / len(total_outs)

            strike_rate = total_runs / len(final_df_1) * 100

            dots = final_df_1[final_df_1["batsman_run"] == 0]
            dot_percentage = len(dots)/len(final_df_1) * 100

            boundaries = final_df_1[final_df_1["batsman_run"] == 4]
            sixes =  final_df_1[final_df_1["batsman_run"] == 6]
            boundary_percentage = len(boundaries) + len(sixes) / len(final_df_1) * 100
            
            firstInningData = [[round(total_runs,2), round(total_innings,2), round(average,2), round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]

        ##### 2nd innings #####
        secondInningData = [[]]

        final_df_2 = final_df[final_df["innings"]==2]

        if(len(final_df_2)==0):
            st.markdown("Player not played at ground in 2nd innings")

        else:
            total_runs = final_df_2["batsman_run"].sum()

            total_innings = len(pd.unique(final_df_2['ID']))

            total_outs = final_df_2[final_df_2["player_out"] == selectedBatter]

            if(len(total_outs) == 0):
                st.markdown("Player not yer dismissed at ground")
            else:
                average = total_runs / len(total_outs)

            strike_rate = total_runs / len(final_df_2) * 100

            dots = final_df_2[final_df_2["batsman_run"] == 0]
            dot_percentage = len(dots)/len(final_df_2) * 100

            boundaries = final_df_2[final_df_2["batsman_run"] == 4]
            sixes =  final_df_2[final_df_2["batsman_run"] == 6]
            boundary_percentage = len(boundaries) + len(sixes) / len(final_df_2) * 100

            secondInningData = [[round(total_runs,2), round(total_innings,2), round(average,2), round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]

        data_to_display = [[]]

        if(any(overallData)):
            data_to_display = overallData
        if(any(firstInningData)):
            data_to_display = data_to_display + firstInningData
        if(any(secondInningData)):
            data_to_display = data_to_display + secondInningData

        if(any(data_to_display)):
            DF = pd.DataFrame(data_to_display, index=['Overall','1s Inning','2nd Inning'], columns=["Total runs", "Total innings", "Average", "Strike rate", "Dot %", "Boundary %"])
            st.dataframe(DF)
 
def BowlerVsGround(matchDataFrame, deliveriesDataFrame):
    #Get batman list
    bowlerList = deliveriesDataFrame['bowler']
    #Remove duplicates
    bowlerList = RemoveDuplicate(bowlerList)

    #Get city list
    cityList = matchDataFrame["City"]
    #Remove duplicates
    cityList = RemoveDuplicate(cityList)

    selectedCity = st.selectbox('City', cityList, key='City_bowler')

    venue_subset = matchDataFrame[matchDataFrame["City"] == selectedCity]
    matchIdList = venue_subset["ID"].to_numpy()

    selectedBowler = st.selectbox('Bowler',bowlerList,key='bowloer_venue')
    player_subset = deliveriesDataFrame[deliveriesDataFrame["bowler"] == selectedBowler]

    final_df = []
    for i in range(len(player_subset)):
        if player_subset.iat[i,0] in matchIdList:
            final_df.append(player_subset.iloc[i])
    final_df = pd.DataFrame(final_df)
    # st.dataframe(final_df)

    if(len(final_df) == 0):
        st.markdown("Player not played at ground")
    else:
        ##### Overall #####
        overallData = [[0,0,0,0,0,0,0]]
        extras_wides = final_df[final_df["extra_type"]=='wides'] 
        extras_noballs =  final_df[final_df["extra_type"]=='noballs']
        total_innings = len(pd.unique(final_df['ID']))
        total_runs = final_df["batsman_run"].sum() + extras_wides["total_run"].sum() + extras_noballs["total_run"].sum()
        total_outs = final_df["player_out"].isnull().sum()
        total_outs = len(final_df)-total_outs

        if(total_outs==0):
            st.markdown("Player has not taken any wickets at the ground")
        else:
            average = total_runs/total_outs
            
            strike_rate = len(final_df)/ total_outs

        economy = total_runs / (len(final_df)/6)
    
        overallData = [[round(total_runs,2), round(total_outs,2), round(average,2), round(strike_rate,2), round(economy,2)]]

        ##### 1st innings #####
        firstInningData = [[0,0,0,0,0,0,0]]
        
        final_df_1 = final_df[final_df["innings"]==1]

        if(len(final_df_1)==0):
            st.markdown("Player not played at ground in 1st innings")
        else:
            extras_wides = final_df_1[final_df_1["extra_type"]=='wides'] 
            extras_noballs =  final_df_1[final_df_1["extra_type"]=='noballs']

            # total_innings = len(pd.unique(final_df_1['ID']))

            total_runs = final_df_1["batsman_run"].sum() + extras_wides["total_run"].sum() + extras_noballs["total_run"].sum()

            total_outs = final_df_1["player_out"].isnull().sum()
            total_outs = len(final_df_1)-total_outs
            
            if(total_outs==0):
                st.markdown("Player has not taken any wickets at the ground")
            else:
                average = total_runs/total_outs
                print(average)

                strike_rate = len(final_df_1)/ total_outs
                print(strike_rate)

            economy = total_runs / (len(final_df_1)/6)
            
            firstInningData = [[round(total_runs,2), round(total_outs,2), round(average,2), round(strike_rate,2), round(economy,2)]]

        ##### 2nd innings #####
        secondInningData = [[0,0,0,0,0,0,0]]
        
        final_df_2 = final_df[final_df["innings"]==2]

        if(len(final_df_2)==0):
            st.markdown("Player not played at ground in 1st innings")
        else:
            extras_wides = final_df_2[final_df_2["extra_type"]=='wides'] 
            extras_noballs =  final_df_2[final_df_2["extra_type"]=='noballs']

            # total_innings = len(pd.unique(final_df_1['ID']))

            total_runs = final_df_2["batsman_run"].sum() + extras_wides["total_run"].sum() + extras_noballs["total_run"].sum()

            total_outs = final_df_2["player_out"].isnull().sum()
            total_outs = len(final_df_2)-total_outs
            
            if(total_outs==0):
                st.markdown("Player has not taken any wickets at the ground")
            else:
                average = total_runs/total_outs
                print(average)

                strike_rate = len(final_df_2)/ total_outs
                print(strike_rate)

            economy = total_runs / (len(final_df_2)/6)
            
            secondInningData = [[round(total_runs,2), round(total_outs,2), round(average,2), round(strike_rate,2), round(economy,2)]]

        data_to_display = [[]]

        if(any(overallData)):
            data_to_display = overallData
        if(any(firstInningData)):
            data_to_display = data_to_display + firstInningData
        if(any(secondInningData)):
            data_to_display = data_to_display + secondInningData

        if(any(data_to_display)):
            DF = pd.DataFrame(data_to_display, index=['Overall','1s Inning','2nd Inning'], columns=["Total runs", "Total outs", "Average", "Strike rate", "Economy"])
            st.dataframe(DF)

def BatterVsOpposition(matchDataFrame ,deliveriesDataFrame):
    #Get list of batsmen
    batsmanList = deliveriesDataFrame['batter']
    #Remove duplicates
    batsmanList = RemoveDuplicate(batsmanList)

    selectedBatsman = st.selectbox('Batsmen',batsmanList,key='batter_opposition')
    player_subset = deliveriesDataFrame[deliveriesDataFrame["batter"] == selectedBatsman]

    #Get list of teams
    teamList1 = matchDataFrame['Team1']
    #Remove duplicates
    teamList1 = RemoveDuplicate(teamList1)

    teamList2 = matchDataFrame['Team2']
    #Remove duplicates
    teamList2 = RemoveDuplicate(teamList2)

    selectedTeam1 = st.selectbox('Team 1', teamList1,key='batter_opposition_team1')
    # selectedTeam2 = st.selectbox('Team 2', teamList2,key='batter_opposition_team2')

    team_subset1 = matchDataFrame[matchDataFrame["Team2"] == selectedTeam1] 
    team_subset2 = matchDataFrame[matchDataFrame["Team1"] == selectedTeam1] 

    match_id_list_1 = team_subset1["ID"].to_numpy()
    match_id_list_2 = team_subset2["ID"].to_numpy()

    match_id_list = np.concatenate([match_id_list_1,match_id_list_2])

    player_subset = player_subset[player_subset['BattingTeam']!=selectedTeam1]

    final_df = []
    for i in range(len(player_subset)):
        if player_subset.iat[i,0] in match_id_list:
            final_df.append(player_subset.iloc[i])
    

    final_df = pd.DataFrame(final_df)

    #Overall
    overallData = [[]]
    hasPlayedInGround = True

    if(len(final_df)!=0):

        total_runs = final_df["batsman_run"].sum()

        total_innings = len(pd.unique(final_df['ID']))

        total_outs = final_df[final_df["player_out"] == selectedBatsman]

        average = 0
        if(len(total_outs)==0):
            average = "inf"
        
        else:
            average = total_runs / len(total_outs)

        strike_rate = total_runs / len(final_df) * 100

        dots = final_df[final_df["batsman_run"] == 0]
        dot_percentage = len(dots)/len(final_df) * 100

        boundaries = final_df[final_df["batsman_run"] == 4]
        sixes =  final_df[final_df["batsman_run"] == 6]
        boundary_percentage = len(boundaries) + len(sixes) / len(final_df) * 100

        if(average=="inf"):
            overallData = [[round(total_runs,2), round(total_innings,2), round(len(total_outs),2), "inf", round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]
        else:
            overallData = [[round(total_runs,2), round(total_innings,2), round(len(total_outs),2), round(average,2), round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]

    else:
        st.markdown("Player not played at ground")
        hasPlayedInGround = False

    #First Innings
    firstInningsData = [[]]
    final_df_1 = []
    if(hasPlayedInGround):
        final_df_1 = final_df[final_df["innings"]==1]

    if(len(final_df_1)!=0):

        total_runs = final_df_1["batsman_run"].sum()

        total_innings = len(pd.unique(final_df_1['ID']))

        total_outs = final_df_1[final_df_1["player_out"] == selectedBatsman]

        average=0
        if len(total_outs)==0:
            average = "inf"

        else:
            average = total_runs / len(total_outs)

        strike_rate = total_runs / len(final_df_1) * 100

        dots = final_df_1[final_df_1["batsman_run"] == 0]
        dot_percentage = len(dots)/len(final_df_1) * 100
        boundaries = final_df_1[final_df_1["batsman_run"] == 4]
        sixes =  final_df_1[final_df_1["batsman_run"] == 6]
        boundary_percentage = len(boundaries) + len(sixes) / len(final_df_1) * 100

        if(average=="inf"):
            firstInningsData = [[round(total_runs,2), round(total_innings,2), round(len(total_outs),2), "inf", round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]
        else:
            firstInningsData = [[round(total_runs,2), round(total_innings,2), round(len(total_outs),2), round(average,2), round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]

    else:
            st.markdown("Player not played at ground in 1st innings")
        
    
    #2nd_innings
    secondInningsData = [[]]
    final_df_2 = []
    if(hasPlayedInGround):
        final_df_2 = final_df[final_df["innings"]==2]
        
    if(len(final_df_2)!=0):
        total_runs = final_df_2["batsman_run"].sum()

        total_innings = len(pd.unique(final_df_2['ID']))

        total_outs = final_df_2[final_df_2["player_out"] == selectedBatsman]

        average=0
        if len(total_outs)==0:
                average= "inf"

        else:
            average = total_runs / len(total_outs)

        strike_rate = total_runs / len(final_df_2) * 100

        dots = final_df_2[final_df_2["batsman_run"] == 0]
        dot_percentage = len(dots)/len(final_df_2) * 100

        boundaries = final_df_2[final_df_2["batsman_run"] == 4]
        sixes =  final_df_2[final_df_2["batsman_run"] == 6]
        boundary_percentage = len(boundaries) + len(sixes) / len(final_df_2) * 100

        if(average=="inf"):
            secondInningsData = [[round(total_runs,2), round(total_innings,2), round(len(total_outs),2), "inf", round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]
        else:
            secondInningsData = [[round(total_runs,2), round(total_innings,2), round(len(total_outs),2), round(average,2), round(strike_rate,2), round(dot_percentage,2), round(boundary_percentage,2)]]
    else:
            st.markdown("Player not played at ground in 2nd innings")

    data_to_display = [[]]  

    if(any(overallData)):
        data_to_display = overallData
    if(any(firstInningsData)):
        data_to_display = data_to_display + firstInningsData
    if(any(secondInningsData)):
        data_to_display = data_to_display + secondInningsData

    if(any(data_to_display)):
        DF = pd.DataFrame(data_to_display, index=['Overall','1s Inning','2nd Inning'], columns=["Total runs", "Total innings", "Total outs", "Average", "Strike rate", "Dot %", "Boundary %"])
        st.dataframe(DF)

def BowlerVsOpposition(matchDataFrame, deliveriesDataFrame):
    #Get list of batsmen
    bowlerList = deliveriesDataFrame['bowler']
    #Remove duplicates
    bowlerList = RemoveDuplicate(bowlerList)

    selectedBowler = st.selectbox('Bowler',bowlerList,key='bowler_opposition')
    player_subset = deliveriesDataFrame[deliveriesDataFrame["bowler"] == selectedBowler]

    #Get list of teams
    teamList1 = matchDataFrame['Team1']
    #Remove duplicates
    teamList1 = RemoveDuplicate(teamList1)

    teamList2 = matchDataFrame['Team2']
    #Remove duplicates
    teamList2 = RemoveDuplicate(teamList2)

    selectedTeam1 = st.selectbox('Team 1', teamList1,key='bowler_opposition_team1')
    # selectedTeam2 = st.selectbox('Team 2', teamList2,key='ba_opposition_team2')

    team_subset1 = matchDataFrame[matchDataFrame["Team2"] == selectedTeam1] 
    team_subset2 = matchDataFrame[matchDataFrame["Team1"] == selectedTeam1] 

    match_id_list_1 = team_subset1["ID"].to_numpy()
    match_id_list_2 = team_subset2["ID"].to_numpy()

    match_id_list = np.concatenate([match_id_list_1,match_id_list_2])

    player_subset = player_subset[player_subset['BattingTeam']==selectedTeam1]

    final_df = []
    for i in range(len(player_subset)):
        if player_subset.iat[i,0] in match_id_list:
            final_df.append(player_subset.iloc[i])
    final_df = pd.DataFrame(final_df)
    # st.dataframe(final_df)

    hasPlayedInGround = True

    #Overall
    overallData = [[]]
    if len(final_df)!=0:
        
        extras_wides = final_df[final_df["extra_type"]=='wides'] 
        extras_noballs =  final_df[final_df["extra_type"]=='noballs']
        total_innings = len(pd.unique(final_df['ID']))

        total_runs = final_df["batsman_run"].sum() + extras_wides["total_run"].sum() + extras_noballs["total_run"].sum()

        total_outs = final_df["player_out"].isnull().sum()
        total_outs = len(final_df)-total_outs
        
        average = 0
        if total_outs==0:
            st.markdown("Player has not taken any wickets at the ground")
        
        else:
            average = total_runs/total_outs

            strike_rate = len(final_df)/ total_outs

        economy = total_runs / (len(final_df)/6)

        overallData = [[round(total_innings,2), round(total_outs,2), round(average,2), round(strike_rate,2), round(economy,2)]]

    else:
        st.markdown("Player not played at ground")
        hasPlayedInGround = False

    ##### 1st innings #####
    firstInningData = [[]]
    
    final_df_1 = []
    if(hasPlayedInGround):
        final_df_1 = final_df[final_df["innings"]==1]

    if len(final_df_1)!=0:
        extras_wides = final_df_1[final_df_1["extra_type"]=='wides'] 
        extras_noballs =  final_df_1[final_df_1["extra_type"]=='noballs']

        total_innings = len(pd.unique(final_df_1['ID']))

        total_runs = final_df_1["batsman_run"].sum() + extras_wides["total_run"].sum() + extras_noballs["total_run"].sum()

        total_outs = final_df_1["player_out"].isnull().sum()
        total_outs = len(final_df_1)-total_outs
        
        average = 0
        if total_outs==0:
            st.markdown("Player has not taken any wickets at the ground in 1st innings")

        else:
            average = total_runs/total_outs

            strike_rate = len(final_df_1)/ total_outs

        economy = total_runs / (len(final_df_1)/6)

        firstInningData = [[round(total_innings,2), round(total_outs,2), round(average,2), round(strike_rate,2), round(economy,2)]]
        
    else:
            st.markdown("Player not played at ground in 1st innings")    

    ##### 2nd innings #####
    secondInningData = [[]]
    
    final_df_2 = []
    if(hasPlayedInGround):
        final_df_2 = final_df[final_df["innings"]==2]
    
    if len(final_df_2)!=0:

        extras_wides = final_df_2[final_df_2["extra_type"]=='wides'] 
        extras_noballs =  final_df_2[final_df_2["extra_type"]=='noballs']

        total_innings = len(pd.unique(final_df_2['ID']))
        
        total_runs = final_df_2["batsman_run"].sum() + extras_wides["total_run"].sum() + extras_noballs["total_run"].sum()
        
        total_outs = final_df_2["player_out"].isnull().sum()
        total_outs = len(final_df_2)-total_outs
        
        if total_outs==0:
            st.markdown("Player has not taken any wickets at the ground in 2nd innings")

        else:
            average = total_runs/total_outs
           
        strike_rate = len(final_df_2)/ total_outs
        
        economy = total_runs / (len(final_df_2)/6)
        
        secondInningData = [[round(total_runs,2), round(total_outs,2), round(average,2), round(strike_rate,2), round(economy,2)]]

    else:
            st.markdown("Player not played at ground in 2nd innings")
    
    data_to_display = [[]]

    if(any(overallData)):
        data_to_display = overallData
    if(any(firstInningData)):
        data_to_display = data_to_display + firstInningData
    if(any(secondInningData)):
        data_to_display = data_to_display + secondInningData

    if(any(data_to_display)):
        DF = pd.DataFrame(data_to_display, index=['Overall','1s Inning','2nd Inning'], columns=["Total runs", "Total outs", "Average", "Strike rate", "Economy"])
        st.dataframe(DF)

def BatterMatchups(deliveriesDataFrame, bowlerTeamData):
    #Get list of batsmen
    batterList = deliveriesDataFrame['batter']
    #Remove duplicates
    batterList = RemoveDuplicate(batterList)

    selectedBatter = st.selectbox('Batter',batterList,key='batter_matchup')
    player_subset = deliveriesDataFrame[deliveriesDataFrame["batter"] == selectedBatter]

     #Get list of teams
    teamList = bowlerTeamData['Team']
    #Remove duplicates
    teamList = RemoveDuplicate(teamList)

    selectedTeam = st.selectbox('Team', teamList, key ='batter_mathcup_team')

    bowler_subset = bowlerTeamData[bowlerTeamData["Team"] == selectedTeam]
    bowler_subset = bowler_subset["Bowlers"].to_numpy()
    
    for bowler in bowler_subset:
        st.markdown(selectedBatter + " vs " + bowler)        
        
        temp = player_subset[player_subset["bowler"] == bowler]
        
        if len(temp)==0:
            st.markdown("Not yet faced")
            
        else:
            total_runs = temp["batsman_run"].sum()
            st.markdown("Total runs: \t"+str(total_runs))

            total_innings = len(pd.unique(temp['ID']))
            st.markdown("Total innings: \t"+str(total_innings) )

            total_outs = temp[temp["player_out"] == selectedBatter]
            st.markdown("Total outs: \t"+str(len(total_outs)))
            
            dots = temp[temp["batsman_run"] == 0]
            dot_percentage = len(dots)/len(temp) * 100
            st.markdown("Dot %: \t"+str(dot_percentage))

            boundaries = temp[temp["batsman_run"] == 4]
            sixes =  temp[temp["batsman_run"] == 6]
            boundary_percentage = len(boundaries) + len(sixes) / len(temp) * 100
            st.markdown("Boundary %: \t"+str(boundary_percentage))

            if len(total_outs)==0:
                st.markdown("Avg :\tinf")
            else:
                average = total_runs / len(total_outs)
                st.markdown("Average: \t"+str(average))

            strike_rate = total_runs / len(temp) * 100
            st.markdown("Strike rate: \t"+str(strike_rate))

def BowlerMatchups(deliveriesDataFrame, batterTeamData):
    #Get list of batsmen
    bowlerList = deliveriesDataFrame['batter']
    #Remove duplicates
    bowlerList = RemoveDuplicate(bowlerList)

    selectedBowler = st.selectbox('Batter',bowlerList,key='bowler_matchup')
    player_subset = deliveriesDataFrame[deliveriesDataFrame["bowler"] == selectedBowler]

     #Get list of teams
    teamList = batterTeamData['Team']
    #Remove duplicates
    teamList = RemoveDuplicate(teamList)

    selectedTeam = st.selectbox('Team', teamList, key ='bowler_mathcup_team')

    batter_subset = batterTeamData[batterTeamData["Team"] == selectedTeam]
    batter_subset = batter_subset["Batters"].to_numpy()

    for batter in batter_subset:
        st.markdown(selectedBowler + " vs " + batter)
        
        temp = player_subset[player_subset["batter"] == batter]
        
        if len(temp)==0:
            st.markdown("Not yet faced")
            
        else:
            extras_wides = temp[temp["extra_type"]=='wides'] 
            extras_noballs =  temp[temp["extra_type"]=='noballs']
            
            total_innings = len(pd.unique(temp['ID']))
            st.markdown("Total innings: \t"+str(total_innings))

            total_runs = temp["batsman_run"].sum() + extras_wides["total_run"].sum() + extras_noballs["total_run"].sum()

            total_outs = temp["player_out"].isnull().sum()
            total_outs = len(temp)-total_outs
            st.markdown("Total outs: \t"+str(total_outs))

            if total_outs == 0:
                st.markdown("Wicket not taken")
                
            else:
                average = total_runs/total_outs
                st.markdown("Average: \t"+str(average))
                
            if total_outs == 0:
                st.markdown("Wicket not taken")
            else:
                strike_rate = len(temp)/ total_outs
                st.markdown("Strike rate: \t"+str(strike_rate))

            economy = total_runs / (len(temp)/6)
            st.markdown("Economy: \t"+str(economy))

currentPath = os.getcwd()

dataPath = currentPath.replace(r'\StreamLit', r'\archive\IPL_Matches_2008_2022.csv')
matchDataFrame = pd.read_csv(dataPath)

dataPath = currentPath.replace(r'\StreamLit', r'\archive\IPL_Ball_by_Ball_2008_2022.csv')
deliveriesDataFrame = pd.read_csv(dataPath)

dataPath = currentPath.replace(r'\StreamLit', r'\archive\batter_team_data(2022).xlsx')
batterTeamData = pd.read_excel(dataPath)

dataPath = currentPath.replace(r'\StreamLit', r'\archive\bowler_team_data(2022).xlsx')
bowlerTeamData = pd.read_excel(dataPath)

tossTab, batterVsGround, bowlerVsGround, batterVsOpposition, bowlerVsOpposition, batterMatchups, bowlerMatchups = st.tabs(['Toss', 'Batter vs Ground', 'Bowler vs Ground', 'Batter vs Opposition', 'Bowler vs Opposition', 'Batter Matchups', 'Bowler Matchups'])

with tossTab:
    TossTab(matchDataFrame)

with batterVsGround:
    BatterVsGround(matchDataFrame, deliveriesDataFrame)

with bowlerVsGround:
    BowlerVsGround(matchDataFrame, deliveriesDataFrame)

with batterVsOpposition:
    BatterVsOpposition(matchDataFrame, deliveriesDataFrame)

with bowlerVsOpposition:
    BowlerVsOpposition(matchDataFrame, deliveriesDataFrame)

with batterMatchups:
    BatterMatchups(deliveriesDataFrame, bowlerTeamData)
with bowlerMatchups:
    BowlerMatchups(deliveriesDataFrame, batterTeamData)