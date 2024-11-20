import pandas as pd
import plotly.graph_objects as go
from django.shortcuts import render
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings

# Define the path to the CSV file
csv_path = os.path.join(settings.BASE_DIR, 'CAPS_app', 'data', 't20.csv')

# Read the CSV file
data = pd.read_csv(csv_path)
def team_stats(request):
    # Load the dataset
    teams = sorted(set(data['Bat First']).union(set(data['Bat Second'])))

    if request.method == 'POST':
        if 'team' in request.POST:  # Single team statistics
            team = request.POST.get('team')
            # Validate team input
            if team not in teams:
                return HttpResponse("Invalid team selection")
            
            # Calculate statistics for the selected team
            total_matches_played = data[(data['Bat First'] == team) | (data['Bat Second'] == team)].shape[0]
            total_wins = data[data['Winner'] == team]['Winner'].count()
            bat_first_wins = data[((data['Bat First'] == team) & (data['Winner'] == team)) | 
                                  ((data['Bat Second'] == team) & (data['Winner'] != team))].shape[0]
            bowl_first_wins = total_wins - bat_first_wins

            # Prepare data for Plotly graphs
            bat_first_data = [bat_first_wins, total_wins - bat_first_wins]
            bowl_first_data = [bowl_first_wins, total_wins - bowl_first_wins]

            # Create Plotly graphs
            fig_bat_first = go.Figure(data=[go.Pie(labels=['Batting First Wins', 'Other Wins'], values=bat_first_data)])
            fig_bat_first.update_traces(marker=dict(colors=['red', 'green']))
            fig_bat_first.update_layout(title='Batting First Wins')

            fig_bowl_first = go.Figure(data=[go.Pie(labels=['Bowling First Wins', 'Other Wins'], values=bowl_first_data)])
            fig_bowl_first.update_traces(marker=dict(colors=['blue', 'orange']))
            fig_bowl_first.update_layout(title='Bowling First Wins')

            # Total Wins Bar Graph
            fig_total_wins = go.Figure(data=[go.Bar(x=['Total Wins'], y=[total_wins], marker=dict(color='pink'))])
            fig_total_wins.update_layout(title='Total Wins')

            # Total Matches Played Bar Graph
            fig_total_matches = go.Figure(data=[go.Bar(x=['Total Matches Played'], y=[total_matches_played], marker=dict(color='yellow'))])
            fig_total_matches.update_layout(title='Total Matches Played')

            # Team wins at venues
            team_wins_at_venue = data[data['Winner'] == team]['Venue'].value_counts()
            fig_team_wins_venue = go.Figure(data=[go.Bar(x=team_wins_at_venue.index, y=team_wins_at_venue.values, marker=dict(color='purple'))])
            fig_team_wins_venue.update_layout(title=f'{team} Wins at Venues')

            # Prepare context to pass to template
            context = {
                'team': team,
                'total_matches_played': total_matches_played,
                'total_wins': total_wins,
                'bat_first_wins': bat_first_wins,
                'bowl_first_wins': bowl_first_wins,
                'fig_bat_first': fig_bat_first.to_html(full_html=False),
                'fig_bowl_first': fig_bowl_first.to_html(full_html=False),
                'fig_total_wins': fig_total_wins.to_html(full_html=False),
                'fig_total_matches': fig_total_matches.to_html(full_html=False),
                'fig_team_wins_venue': fig_team_wins_venue.to_html(full_html=False),
            }
            
            return render(request, 'teamstatst20.html', context)

        elif 'team1' in request.POST and 'team2' in request.POST:  # Head-to-head statistics
            team1 = request.POST.get('team1')
            team2 = request.POST.get('team2')
            # Validate team inputs
            if team1 not in teams or team2 not in teams:
                return HttpResponse("Invalid team selection")
            
            # Calculate statistics for the selected teams
            matches_team1_vs_team2 = data[((data['Bat First'] == team1) & (data['Bat Second'] == team2)) | 
                                          ((data['Bat First'] == team2) & (data['Bat Second'] == team1))]
            total_matches_played_team1_vs_team2 = matches_team1_vs_team2.shape[0]
            wins_team1_vs_team2 = matches_team1_vs_team2[matches_team1_vs_team2['Winner'] == team1].shape[0]
            wins_team2_vs_team1 = matches_team1_vs_team2[matches_team1_vs_team2['Winner'] == team2].shape[0]

            # Create Plotly graphs for wins against each other
            fig_wins_vs_each_other = go.Figure(data=[go.Bar(x=[team1, team2], y=[wins_team1_vs_team2, wins_team2_vs_team1], marker=dict(color=['pink', 'yellow']))])
            fig_wins_vs_each_other.update_layout(title='Wins Against Each Other')

            # Team vs Team wins at venues
            # Group matches by venue and count wins for each team at each venue
            venue_wins_data = matches_team1_vs_team2.groupby(['Venue', 'Winner']).size().unstack(fill_value=0)

# Plot the graph
            fig_team_vs_team_wins_venue = go.Figure()
            for team in [team1, team2]:
                    fig_team_vs_team_wins_venue.add_trace(go.Bar(x=venue_wins_data.index, y=venue_wins_data[team], name=team))

            fig_team_vs_team_wins_venue.update_layout(barmode='group', title=f'{team1} vs {team2} Wins at Venues', xaxis_title='Venue', yaxis_title='Number of Wins')
            # Count batting first wins for each team
            bat_first_wins_team1 = ((matches_team1_vs_team2['Bat First'] == team1) & (matches_team1_vs_team2['Winner'] == team1)).sum()
            bat_first_wins_team2 = ((matches_team1_vs_team2['Bat First'] == team2) & (matches_team1_vs_team2['Winner'] == team2)).sum()

# Count batting second wins for each team
            bat_second_wins_team1 = ((matches_team1_vs_team2['Bat Second'] == team1) & (matches_team1_vs_team2['Winner'] == team1)).sum()
            bat_second_wins_team2 = ((matches_team1_vs_team2['Bat Second'] == team2) & (matches_team1_vs_team2['Winner'] == team2)).sum()


            # Prepare context to pass to template
            context = {
                'team1': team1,
                'team2': team2,
                'total_matches_played_team1_vs_team2': total_matches_played_team1_vs_team2,
                'bat_first_wins_team1': bat_first_wins_team1,
                'bat_first_wins_team2': bat_first_wins_team2,
                'bat_second_wins_team1': bat_second_wins_team1,
                'bat_second_wins_team2': bat_second_wins_team2,
                'wins_team1_vs_team2': wins_team1_vs_team2,
                'wins_team2_vs_team1': wins_team2_vs_team1,
                'fig_wins_vs_each_other': fig_wins_vs_each_other.to_html(full_html=False),
                'fig_team_vs_team_wins_venue': fig_team_vs_team_wins_venue.to_html(full_html=False),
            }
            
            return render(request, 'team_vs_team_t20.html', context)

    # If not a POST request or invalid input, render the initial template
    return render(request, 'team_selectt20.html', {
        'teams': teams,
    })


def t20_analysis(request):

    # All Wins
    wins_counts = data['Winner'].value_counts().reset_index()
    wins_counts.columns = ['Team', 'Wins']
    fig1 = px.bar(wins_counts, x='Team', y='Wins', color='Team', title='All Wins')
    fig1.update_layout(xaxis_title='Team', yaxis_title='Wins', width=1300, height=800, plot_bgcolor='rgba(0, 0, 0, 0)')

    # Batting First Wins
    bat_first_wins = data[data['Bat First'] == data['Winner']]['Winner'].value_counts().reset_index()
    bat_first_wins.columns = ['Team', 'Batting First Wins']
    fig2 = px.bar(bat_first_wins, x='Batting First Wins', y='Team', color='Team', title='Batting First Wins')
    fig2.update_layout(xaxis_title='Team', yaxis_title='Wins', width=1300, height=1000, plot_bgcolor='rgba(0, 0, 0, 0)')

    # Bowling First Wins
    bowl_first_wins = data[data['Bat Second'] == data['Winner']]['Winner'].value_counts().reset_index()
    bowl_first_wins.columns = ['Team', 'Bowling First Wins']
    fig3 = px.bar(bowl_first_wins, x='Team', y='Bowling First Wins', color='Team', title='Bowling First Wins')
    fig3.update_layout(xaxis_title='Team', yaxis_title='Wins', width=1300, height=800, plot_bgcolor='rgba(0, 0, 0, 0)')

    context = {
        'fig1': fig1.to_html(full_html=True),
        'fig2': fig2.to_html(full_html=True),
        'fig3': fig3.to_html(full_html=True),
        'wins_counts': wins_counts.to_html(classes='table table-striped', index=False),
        'bat_first_wins': bat_first_wins.to_html(classes='table table-striped', index=False),
        'bowl_first_wins': bowl_first_wins.to_html(classes='table table-striped', index=False),
    }

    return render(request, 'T20.html', context)
    