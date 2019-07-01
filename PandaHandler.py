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

        DataFrame = DataFrame.drop(['HomeWin', 'AwayWin', 'HomeLoss',
                                    'AwayLoss', 'HomeDraw', 'AwayDraw'],
                                   axis=1)

        return DataFrame
