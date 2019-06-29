class PlayerInfo:
    def __init__(self, place, rating, games_played, name):
        self.place = place
        self.rating = rating
        self.games_played = games_played
        self.name = name

    def __str__(self):
        return f' {self.place:2d}   {self.rating}     {self.games_played:2d} {self.name}'


class PlayerInfoList:
    def __init__(self, player_info_list):
        self.player_info_list = sorted(player_info_list, key=lambda p: p.place)

    def __str__(self):
        out = "排名 Rating 对战数 名字\n"
        out += "\n".join([str(player_info) for player_info in self.player_info_list])
        return out
