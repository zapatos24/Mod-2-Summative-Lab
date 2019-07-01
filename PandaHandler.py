import pandas as pd


class PandaHandler:
    # Calculates the total number of goals scored for each home team in the
    # DataFrame, effectively giving us total goals over the period for each
    # team
    def tot_home_goals_scored(DataFrame):
        DataFrame['tot_home_goals'] = DataFrame.HomeTeam.apply(
            lambda team: DataFrame.groupby('HomeTeam')['FTHG'].sum().loc[team])
        return DataFrame

    # Counts the total number of wins, losses, or draws for each team in the
    # DataFrame passed in
    def count_games(DataFrame, game_end):
        if game_end == 'Win':
            DataFrame['HomeWin'] = DataFrame.FTR.map({'H': 1, 'A': 0, 'D': 0})
            DataFrame['AwayWin'] = DataFrame.FTR.map({'H': 0, 'A': 1, 'D': 0})
            games = DataFrame.groupby('HomeTeam').HomeWin.sum() + \
                DataFrame.groupby('AwayTeam').AwayWin.sum()

        elif game_end == 'Loss':
            DataFrame['HomeLoss'] = DataFrame.FTR.map({'H': 0, 'A': 1, 'D': 0})
            DataFrame['AwayLoss'] = DataFrame.FTR.map({'H': 1, 'A': 0, 'D': 0})
            games = DataFrame.groupby('HomeTeam').HomeLoss.sum() + \
                DataFrame.groupby('AwayTeam').AwayLoss.sum()

        elif game_end == 'Draw':
            DataFrame['HomeDraw'] = DataFrame.FTR.map({'H': 0, 'A': 0, 'D': 1})
            DataFrame['AwayDraw'] = DataFrame.FTR.map({'H': 0, 'A': 0, 'D': 1})
            games = DataFrame.groupby('HomeTeam').HomeDraw.sum() + \
                DataFrame.groupby('AwayTeam').AwayDraw.sum()

        return games

    # Takes a DataFrame and returns a new DataFrame with the wins, losses, and
    # draws for each team added to each line of the DataFrame
    def win_loss_draw(DataFrame):
        DataFrame['tot_home_win'] = DataFrame.HomeTeam.apply(
            lambda team: PandaHandler.count_games(DataFrame, 'Win')[team])

        DataFrame['tot_home_loss'] = DataFrame.HomeTeam.apply(
            lambda team: PandaHandler.count_games(DataFrame, 'Loss')[team])

        DataFrame['tot_home_draw'] = DataFrame.HomeTeam.apply(
            lambda team: PandaHandler.count_games(DataFrame, 'Draw')[team])

        return DataFrame

    # Get back a pretty version of DataFrame with only necessary information
    # before rain data added
    def match_results(DataFrame):
        df_goals_wins = DataFrame.groupby('HomeTeam')[['Season',
                                                       'tot_home_goals',
                                                       'tot_home_win',
                                                       'tot_home_loss',
                                                       'tot_home_draw']
                                                      ].first()
        df_goals_wins.index.rename('Team', inplace=True)
        df_goals_wins.columns = ['Season', 'GoalsScored',
                                 'Wins', 'Losses', 'Draws']
        return df_goals_wins

    # Returns a new DataFrame with rain information added
    def rain_results(matchesDF, rainDF):
        matchesDF = matchesDF.merge(rainDF, on='Date', how='left')
        teams = PandaHandler.match_results(matchesDF)
        num_games = teams.iloc[0].Wins + teams.iloc[0].Losses + teams.iloc[0].Draws
        print('Total Number of Games: ' + str(num_games))
        teams['RainGames'] = matchesDF.groupby(
            'HomeTeam').Rain.sum() + matchesDF.groupby('AwayTeam').Rain.sum()

        teams['RainWins'] = matchesDF[matchesDF.Rain == 1].groupby('HomeTeam').HomeWin.sum() + \
            matchesDF[matchesDF.Rain == 1].groupby('AwayTeam').AwayWin.sum()

        teams['NonRainWins'] = teams.Wins - teams.RainWins

        teams['RainWin%'] = teams.RainWins/teams.RainGames

        teams['NonRainWin%'] = teams.NonRainWins/(num_games-teams.RainGames)

        teams['%ChangeWinWithRain'] = (
            teams['RainWin%']-teams['NonRainWin%']) / teams['NonRainWin%']

        return teams
