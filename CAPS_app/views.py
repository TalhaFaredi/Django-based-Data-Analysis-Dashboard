from django.shortcuts import render
from django.http import HttpRequest
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd
from django.conf import settings

csv_path = os.path.join(settings.BASE_DIR, 'CAPS_app', 'data', 'ODI_Match_info.csv')

data = pd.read_csv(csv_path)




def index(request):
    return render(request,'index.html')

def dashboard(request):
    
    df = data[['team1', 'team2', 'winner']]
    win_counts = df['winner'].value_counts()
    team1_counts = df['team1'].value_counts()
    team2_counts = df['team2'].value_counts()
    total_matches = team1_counts.add(team2_counts, fill_value=0)
    winning_percentage = (win_counts / total_matches).fillna(0) * 100
    winning_percentage_df = pd.DataFrame({'team': winning_percentage.index, 'percentage': winning_percentage.values})
    fig4 = px.pie(winning_percentage_df, values='percentage', names='team', title='Winning Percentage for Each Team', width=700, height=600)
    fig4.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')

    # Losing Percentage
    losing_percentage = (total_matches - win_counts / total_matches).fillna(0) * 100
    losing_percentage_df = pd.DataFrame({'team': winning_percentage.index, 'percentage': losing_percentage.values})
    fig5 = px.pie(losing_percentage_df, values='percentage', names='team', title='Losing Percentage for Each Team', width=700, height=600)
    fig5.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')


    # Total Wins
    temp3 = data['winner'].value_counts().reset_index()
    temp3.columns = ['Team', 'Wins']
    fig7 = px.bar(temp3, x='Team', y='Wins', color='Team')
    fig7.update_layout(width=1200, height=800)
    fig7.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')

    context = {
       
        'fig4': fig4.to_html(full_html=False),
        'fig5': fig5.to_html(full_html=False),
        'fig7': fig7.to_html(full_html=False),
        'winning_percentage_df': winning_percentage_df.to_html(classes='table table-striped', index=False),
        'losing_percentage_df': losing_percentage_df.to_html(classes='table table-striped', index=False),
        'temp3': temp3.to_html(classes='table table-striped', index=False)
    }
    
    return render(request, 'Dashboard.html', context)


def Toss(request):
    # Load the data
    
    # Toss Winning By Every Country
    toss_winner_counts = data['toss_winner'].value_counts().reset_index()
    toss_winner_counts.columns = ['Country', 'Count']
    fig1 = px.bar(toss_winner_counts, x='Country', y='Count', color='Country', title='Total Tosses Won by Country')
    fig1.update_layout(xaxis_title='Country', yaxis_title='Count', width=800, height=800, plot_bgcolor='rgba(0, 0, 0, 0)')

    # Toss Winning Match Winning
    team_win_counts = data[data['toss_winner'] == data['winner']]['winner'].value_counts().reset_index()
    team_win_counts.columns = ['Team', 'Wins']
    fig2 = px.bar(team_win_counts, x='Wins', y='Team', color='Team')
    fig2.update_xaxes(categoryorder='total ascending')
    fig2.update_layout(width=800, height=800)

    fig2.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')

    # Toss Loser Match Winner
    team_wins_counts = data[data['toss_winner'] != data['winner']]['winner'].value_counts().reset_index()
    team_wins_counts.columns = ['Team', 'Wins']
    fig3 = px.funnel(team_wins_counts, x='Team', y='Wins', color='Team')
    fig3.update_xaxes(categoryorder='total descending')
    fig3.update_layout(width=1500, height=900)

    fig3.update_layout(title='Teams that Lost Toss but Still Won Matches', plot_bgcolor='rgba(0, 0, 0, 0)')

    # Toss Decision by Every Team
    toss_decision_count = data.groupby(['toss_winner', 'toss_decision']).size().reset_index(name='Count')
    fig6 = px.bar(toss_decision_count, x='Count', y='toss_decision', color='toss_winner', title='Toss Decisions by Teams', width=1400, height=800)
    fig6.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')


    context = {
        'fig1': fig1.to_html(full_html=False),
        'fig2': fig2.to_html(full_html=False),
        'fig3': fig3.to_html(full_html=False),
        'fig6': fig6.to_html(full_html=False),
        'toss_winner_counts': toss_winner_counts.to_html(classes='table table-striped', index=False),
        'team_win_counts': team_win_counts.to_html(classes='table table-striped', index=False),
        'team_wins_counts': team_wins_counts.to_html(classes='table table-striped', index=False),
        'toss_decision_count': toss_decision_count.to_html(classes='table table-striped', index=False),
    }
    
    return render(request, 'Toss.html', context)
def decision(request):
    # Load the data
    
    # Wins when batting first
    bat_first_wins = data[(data['toss_decision'] == 'bat') & (data['winner'] == data['team1']) | 
                          (data['toss_decision'] == 'field') & (data['winner'] == data['team2'])]['winner'].value_counts().reset_index()
    bat_first_wins.columns = ['Team', 'Wins']
    fig_bat_first = px.bar(bat_first_wins, x='Team', y='Wins', color='Team', title='Wins When Batting First')
    fig_bat_first.update_layout(width=800, height=600, plot_bgcolor='rgba(0, 0, 0, 0)')
    
    # Wins when bowling first
    bowl_first_wins = data[(data['toss_decision'] == 'field') & (data['winner'] == data['team1']) | 
                           (data['toss_decision'] == 'bat') & (data['winner'] == data['team2'])]['winner'].value_counts().reset_index()
    bowl_first_wins.columns = ['Team', 'Wins']
    fig_bowl_first = px.bar(bowl_first_wins, x='Team', y='Wins', color='Team', title='Wins When Bowling First')
    fig_bowl_first.update_layout(width=800, height=600, plot_bgcolor='rgba(0, 0, 0, 0)')
    
    context = {
        'fig_bat_first': fig_bat_first.to_html(full_html=False),
        'fig_bowl_first': fig_bowl_first.to_html(full_html=False),
        'bat_first_wins': bat_first_wins.to_html(classes='table table-striped', index=False),
        'bowl_first_wins': bowl_first_wins.to_html(classes='table table-striped', index=False),
    }
    
    return render(request, 'decision.html', context)


def team_stats(request):
    if request.method == 'POST':
        if 'team' in request.POST:  # Check if the first form was submitted
            team = request.POST.get('team')

            # Calculate statistics for the selected team
            total_matches_played = data[(data['team1'] == team) | (data['team2'] == team)].shape[0]
            total_wins = data[data['winner'] == team]['winner'].count()
            toss_win_match_win = data[(data['toss_winner'] == team) & (data['winner'] == team)]['winner'].count()
            bat_first_wins = data[((data['toss_winner'] == team) & (data['toss_decision'] == 'bat') & (data['winner'] == team)) | 
                                  ((data['toss_winner'] != team) & (data['toss_decision'] == 'field') & (data['team1'] == team) & (data['winner'] == team))]['winner'].count()
            bowl_first_wins = data[((data['toss_winner'] == team) & (data['toss_decision'] == 'field') & (data['winner'] == team)) | 
                                   ((data['toss_winner'] != team) & (data['toss_decision'] == 'bat') & (data['team2'] == team) & (data['winner'] == team))]['winner'].count()

            # Prepare data for Plotly graphs
            bat_first_data = [bat_first_wins, total_wins - bat_first_wins]
            bowl_first_data = [bowl_first_wins, total_wins - bowl_first_wins]

            # Create Plotly graphs
            fig_bat_first = go.Figure(data=[go.Pie(labels=['Batting First Wins', 'Other Wins'], values=bat_first_data)])
            fig_bat_first.update_traces(marker=dict(colors=['red', 'green']))
            fig_bat_first.update_layout(title='Batting First Wins')

            fig_bowl_first = go.Figure(data=[go.Pie(labels=['Bowling First Wins', 'Other Wins'], values=bowl_first_data)])
            fig_bowl_first.update_traces(marker=dict(colors=['pink', 'green']))
            fig_bowl_first.update_layout(title='Bowling First Wins')

            # Total Wins Bar Graph
            fig_total_wins = go.Figure(data=[go.Bar(x=['Total Wins'], y=[total_wins], marker=dict(color='pink'))])
            fig_total_wins.update_layout(title='Total Wins')

            # Total Matches Played Bar Graph
            fig_total_matches = go.Figure(data=[go.Bar(x=['Total Matches Played'], y=[total_matches_played], marker=dict(color='yellow'))])
            fig_total_matches.update_layout(title='Total Matches Played')
            
            # Toss Win Match Win Bar Graph
            fig_toss_win_match_win = go.Figure(data=[go.Bar(x=['Toss Win Match Win'], y=[toss_win_match_win], marker=dict(color='orange'))])
            fig_toss_win_match_win.update_layout(title='Toss Win Match Win')

            # Prepare context to pass to template
            context = {
                'team': team,
                'total_matches_played': total_matches_played,
                'total_wins': total_wins,
                'bat_first_wins': bat_first_wins,
                'bowl_first_wins': bowl_first_wins,
                'toss_win_match_win': toss_win_match_win,
                'fig_bat_first': fig_bat_first.to_html(full_html=False),
                'fig_bowl_first': fig_bowl_first.to_html(full_html=False),
                'fig_total_wins': fig_total_wins.to_html(full_html=False),
                'fig_total_matches': fig_total_matches.to_html(full_html=False),
                'fig_toss_win_match_win': fig_toss_win_match_win.to_html(full_html=False),
            }
            
            return render(request, 'team_stats.html', context)

       # Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
from django.shortcuts import render

def team_stats(request):
    teams = sorted(set(data['team1']).union(set(data['team2'])))
    venues = data['venue'].unique()

    if request.method == 'POST':
        if 'team' in request.POST:  # Check if the first form was submitted
            team = request.POST.get('team')

            # Calculate statistics for the selected team
            total_matches_played = data[(data['team1'] == team) | (data['team2'] == team)].shape[0]
            total_wins = data[data['winner'] == team]['winner'].count()
            toss_win_match_win = data[(data['toss_winner'] == team) & (data['winner'] == team)]['winner'].count()
            bat_first_wins = data[((data['toss_winner'] == team) & (data['toss_decision'] == 'bat') & (data['winner'] == team)) | 
                                  ((data['toss_winner'] != team) & (data['toss_decision'] == 'field') & (data['team1'] == team) & (data['winner'] == team))]['winner'].count()
            bowl_first_wins = data[((data['toss_winner'] == team) & (data['toss_decision'] == 'field') & (data['winner'] == team)) | 
                                   ((data['toss_winner'] != team) & (data['toss_decision'] == 'bat') & (data['team2'] == team) & (data['winner'] == team))]['winner'].count()

            # Prepare data for Plotly graphs
            bat_first_data = [bat_first_wins, total_wins - bat_first_wins]
            bowl_first_data = [bowl_first_wins, total_wins - bowl_first_wins]

            # Create Plotly graphs
            fig_bat_first = go.Figure(data=[go.Pie(labels=['Batting First Wins', 'Other Wins'], values=bat_first_data)])
            fig_bat_first.update_traces(marker=dict(colors=['red', 'green']))
            fig_bat_first.update_layout(title='Batting First Wins')

            fig_bowl_first = go.Figure(data=[go.Pie(labels=['Bowling First Wins', 'Other Wins'], values=bowl_first_data)])
            fig_bowl_first.update_traces(marker=dict(colors=['pink', 'green']))
            fig_bowl_first.update_layout(title='Bowling First Wins')

            # Total Wins Bar Graph
            fig_total_wins = go.Figure(data=[go.Bar(x=['Total Wins'], y=[total_wins], marker=dict(color='pink'))])
            fig_total_wins.update_layout(title='Total Wins')

            # Total Matches Played Bar Graph
            fig_total_matches = go.Figure(data=[go.Bar(x=['Total Matches Played'], y=[total_matches_played], marker=dict(color='yellow'))])
            fig_total_matches.update_layout(title='Total Matches Played')
            
            # Toss Win Match Win Bar Graph
            fig_toss_win_match_win = go.Figure(data=[go.Bar(x=['Toss Win Match Win'], y=[toss_win_match_win], marker=dict(color='orange'))])
            fig_toss_win_match_win.update_layout(title='Toss Win Match Win')

            # Prepare context to pass to template
            context = {
                'team': team,
                'total_matches_played': total_matches_played,
                'total_wins': total_wins,
                'bat_first_wins': bat_first_wins,
                'bowl_first_wins': bowl_first_wins,
                'toss_win_match_win': toss_win_match_win,
                'fig_bat_first': fig_bat_first.to_html(full_html=False),
                'fig_bowl_first': fig_bowl_first.to_html(full_html=False),
                'fig_total_wins': fig_total_wins.to_html(full_html=False),
                'fig_total_matches': fig_total_matches.to_html(full_html=False),
                'fig_toss_win_match_win': fig_toss_win_match_win.to_html(full_html=False),
            }
            
            return render(request, 'team_stats.html', context)

        elif 'team1' in request.POST and 'team2' in request.POST and 'venue' not in request.POST:  # Check if the second form was submitted
            team1 = request.POST.get('team1')
            team2 = request.POST.get('team2')

            # Calculate statistics for the selected teams
            matches_team1_vs_team2 = data[((data['team1'] == team1) & (data['team2'] == team2)) | ((data['team1'] == team2) & (data['team2'] == team1))]
            total_matches_played_team1_vs_team2 = matches_team1_vs_team2.shape[0]
            wins_team1_vs_team2 = matches_team1_vs_team2[matches_team1_vs_team2['winner'] == team1].shape[0]
            wins_team2_vs_team1 = matches_team1_vs_team2[matches_team1_vs_team2['winner'] == team2].shape[0]

            # Batting First Wins
            bat_first_wins_team1 = matches_team1_vs_team2[((matches_team1_vs_team2['toss_winner'] == team1) & (matches_team1_vs_team2['toss_decision'] == 'bat') & (matches_team1_vs_team2['winner'] == team1)) | 
                                                           ((matches_team1_vs_team2['toss_winner'] == team2) & (matches_team1_vs_team2['toss_decision'] == 'field') & (matches_team1_vs_team2['winner'] == team1))].shape[0]
            bat_first_wins_team2 = matches_team1_vs_team2[((matches_team1_vs_team2['toss_winner'] == team2) & (matches_team1_vs_team2['toss_decision'] == 'bat') & (matches_team1_vs_team2['winner'] == team2)) | 
                                                           ((matches_team1_vs_team2['toss_winner'] == team1) & (matches_team1_vs_team2['toss_decision'] == 'field') & (matches_team1_vs_team2['winner'] == team2))].shape[0]

            # Bowling First Wins
            bowl_first_wins_team1 = matches_team1_vs_team2[((matches_team1_vs_team2['toss_winner'] == team1) & (matches_team1_vs_team2['toss_decision'] == 'field') & (matches_team1_vs_team2['winner'] == team1)) | 
                                                            ((matches_team1_vs_team2['toss_winner'] == team2) & (matches_team1_vs_team2['toss_decision'] == 'bat') & (matches_team1_vs_team2['winner'] == team1))].shape[0]
            bowl_first_wins_team2 = matches_team1_vs_team2[((matches_team1_vs_team2['toss_winner'] == team2) & (matches_team1_vs_team2['toss_decision'] == 'field') & (matches_team1_vs_team2['winner'] == team2)) | 
                                                            ((matches_team1_vs_team2['toss_winner'] == team1) & (matches_team1_vs_team2['toss_decision'] == 'bat') & (matches_team1_vs_team2['winner'] == team2))].shape[0]

            # Create Plotly graphs for wins against each other
            fig_wins_vs_each_other = go.Figure(data=[go.Bar(x=[team1, team2], y=[wins_team1_vs_team2, wins_team2_vs_team1], marker=dict(color=['pink', 'yellow']))])
            fig_wins_vs_each_other.update_layout(title='Wins Against Each Other')

            # Create Plotly graphs for batting first wins
            fig_bat_first_wins = go.Figure(data=[go.Bar(x=[team1, team2], y=[bat_first_wins_team1, bat_first_wins_team2], marker=dict(color=['blue', 'orange']))])
            fig_bat_first_wins.update_layout(title='Batting First Wins')

            # Create Plotly graphs for bowling first wins
            fig_bowl_first_wins = go.Figure(data=[go.Bar(x=[team1, team2], y=[bowl_first_wins_team1, bowl_first_wins_team2], marker=dict(color=['green', 'red']))])
            fig_bowl_first_wins.update_layout(title='Bowling First Wins')
            
            
            # Create Plotly graphs for batting first wins and bowling first wins
            fig_wins_and_losses = go.Figure(data=[
                go.Bar(name='Batting First Wins', x=[team1, team2], y=[bat_first_wins_team1, bat_first_wins_team2], marker=dict(color='pink')),
            ])
            fig_wins_and_losses.update_layout(barmode='group', title='Batting First Wins ')
            
            Bowling = go.Figure(data=[
                go.Bar(name='Bowling First Wins', x=[team1, team2], y=[bowl_first_wins_team1, bowl_first_wins_team2], marker=dict(color='green'))
            ])
            Bowling.update_layout(barmode='group', title='Bowling First Wins ')

            # Prepare context to pass to template
            context = {
                'team1': team1,
                'team2': team2,
                'total_matches_played_team1_vs_team2': total_matches_played_team1_vs_team2,
                'wins_team1_vs_team2': wins_team1_vs_team2,
                'wins_team2_vs_team1': wins_team2_vs_team1,
                'bat_first_wins_team1': bat_first_wins_team1,
                'bat_first_wins_team2': bat_first_wins_team2,
                'bowl_first_wins_team1': bowl_first_wins_team1,
                'bowl_first_wins_team2': bowl_first_wins_team2,
                'fig_wins_vs_each_other': fig_wins_vs_each_other.to_html(full_html=False),
                'fig_bat_first_wins': fig_bat_first_wins.to_html(full_html=False),
                'fig_bowl_first_wins': fig_bowl_first_wins.to_html(full_html=False),
                'fig_wins_and_losses': fig_wins_and_losses.to_html(full_html=False),
                'Bowling_first_win': Bowling.to_html(full_html=False),
            }
            
            return render(request, 'team_against_team.html', context)

        elif 'team1' in request.POST and 'team2' in request.POST and 'venue' in request.POST:  # Check if the third form was submitted
            team1 = request.POST.get('team1')
            team2 = request.POST.get('team2')
            venue = request.POST.get('venue')

            # Calculate statistics for the selected teams at the selected venue
            matches_at_venue = data[(data['venue'] == venue) & (((data['team1'] == team1) & (data['team2'] == team2)) | ((data['team1'] == team2) & (data['team2'] == team1)))]
            total_matches_played_at_venue = matches_at_venue.shape[0]
            wins_team1_at_venue = matches_at_venue[matches_at_venue['winner'] == team1].shape[0]
            wins_team2_at_venue = matches_at_venue[matches_at_venue['winner'] == team2].shape[0]

            # Batting First Wins at Venue
            bat_first_wins_team1_at_venue = matches_at_venue[((matches_at_venue['toss_winner'] == team1) & (matches_at_venue['toss_decision'] == 'bat') & (matches_at_venue['winner'] == team1)) | 
                                                             ((matches_at_venue['toss_winner'] == team2) & (matches_at_venue['toss_decision'] == 'field') & (matches_at_venue['winner'] == team1))].shape[0]
            bat_first_wins_team2_at_venue = matches_at_venue[((matches_at_venue['toss_winner'] == team2) & (matches_at_venue['toss_decision'] == 'bat') & (matches_at_venue['winner'] == team2)) | 
                                                             ((matches_at_venue['toss_winner'] == team1) & (matches_at_venue['toss_decision'] == 'field') & (matches_at_venue['winner'] == team2))].shape[0]

            # Bowling First Wins at Venue
            bowl_first_wins_team1_at_venue = matches_at_venue[((matches_at_venue['toss_winner'] == team1) & (matches_at_venue['toss_decision'] == 'field') & (matches_at_venue['winner'] == team1)) | 
                                                              ((matches_at_venue['toss_winner'] == team2) & (matches_at_venue['toss_decision'] == 'bat') & (matches_at_venue['winner'] == team1))].shape[0]
            bowl_first_wins_team2_at_venue = matches_at_venue[((matches_at_venue['toss_winner'] == team2) & (matches_at_venue['toss_decision'] == 'field') & (matches_at_venue['winner'] == team2)) | 
                                                              ((matches_at_venue['toss_winner'] == team1) & (matches_at_venue['toss_decision'] == 'bat') & (matches_at_venue['winner'] == team2))].shape[0]

            # Create Plotly graphs for wins at the venue
            fig_wins_at_venue = go.Figure(data=[go.Bar(x=[team1, team2], y=[wins_team1_at_venue, wins_team2_at_venue], marker=dict(color=['pink', 'yellow']))])
            fig_wins_at_venue.update_layout(title=f'Wins at {venue}')

            # Create Plotly graphs for batting first wins at venue
            fig_bat_first_wins_at_venue = go.Figure(data=[go.Bar(x=[team1, team2], y=[bat_first_wins_team1_at_venue, bat_first_wins_team2_at_venue], marker=dict(color=['blue', 'orange']))])
            fig_bat_first_wins_at_venue.update_layout(title=f'Batting First Wins at {venue}')

            # Create Plotly graphs for bowling first wins at venue
            fig_bowl_first_wins_at_venue = go.Figure(data=[go.Bar(x=[team1, team2], y=[bowl_first_wins_team1_at_venue, bowl_first_wins_team2_at_venue], marker=dict(color=['green', 'red']))])
            fig_bowl_first_wins_at_venue.update_layout(title=f'Bowling First Wins at {venue}')
            
            # Create Plotly graphs for batting first wins and bowling first wins at venue
            fig_wins_and_losses_at_venue = go.Figure(data=[
                go.Bar(name='Batting First Wins', x=[team1, team2], y=[bat_first_wins_team1_at_venue, bat_first_wins_team2_at_venue], marker=dict(color='pink')),
            ])
            fig_wins_and_losses_at_venue.update_layout(barmode='group', title=f'Batting First Wins at {venue}')
            
            fig_bowling_wins_at_venue = go.Figure(data=[
                go.Bar(name='Bowling First Wins', x=[team1, team2], y=[bowl_first_wins_team1_at_venue, bowl_first_wins_team2_at_venue], marker=dict(color='green'))
            ])
            fig_bowling_wins_at_venue.update_layout(barmode='group', title=f'Bowling First Wins at {venue}')

            # Prepare context to pass to template
            context = {
                'team1': team1,
                'team2': team2,
                'venue': venue,
                'total_matches_played_at_venue': total_matches_played_at_venue,
                'wins_team1_at_venue': wins_team1_at_venue,
                'wins_team2_at_venue': wins_team2_at_venue,
                'bat_first_wins_team1_at_venue': bat_first_wins_team1_at_venue,
                'bat_first_wins_team2_at_venue': bat_first_wins_team2_at_venue,
                'bowl_first_wins_team1_at_venue': bowl_first_wins_team1_at_venue,
                'bowl_first_wins_team2_at_venue': bowl_first_wins_team2_at_venue,
                'fig_wins_at_venue': fig_wins_at_venue.to_html(full_html=False),
                'fig_bat_first_wins_at_venue': fig_bat_first_wins_at_venue.to_html(full_html=False),
                'fig_bowl_first_wins_at_venue': fig_bowl_first_wins_at_venue.to_html(full_html=False),
                'fig_wins_and_losses_at_venue': fig_wins_and_losses_at_venue.to_html(full_html=False),
                'fig_bowling_wins_at_venue': fig_bowling_wins_at_venue.to_html(full_html=False),
            }

            return render(request, 'team_against_venue.html', context)

 
    teams = sorted(set(data['team1']).union(set(data['team2'])))
    venues = sorted(data['venue'].unique())
    matches = data.to_dict(orient='records')  # Convert matches data to a list of dicts for JavaScript

    return render(request, 'select_team.html', {
        'teams': teams,
        'venues': venues,
        'matches': matches  # Pass matches data to template
    })
    
    
    
    
# CAPS/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, LoginForm

# Example view for login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Example view for registration
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
