import sys

from config import INIT_RATING, PLAYER_NUM
from models import PlayerInfo, PlayerInfoList


def parse_names(csv_line):
    return csv_line.split(",")[2:2 + (PLAYER_NUM * 2):2]


# http://arcturus.su/tenhou/ids-ranks.html
def calc_rate_change(place, own_rate, average_table_rate, games_played):
    adjustment = 1 - (games_played * 0.002) if games_played < 400 else 0.2
    delta_table = [30.0, 10.0, -10.0, -30.0] if PLAYER_NUM == 4 else [30.0, 0.0, -30.0]
    base = delta_table[place - 1]
    return adjustment * (base + (average_table_rate - own_rate) / 40)


def handle_csv_lines(csv_lines):
    rating_map = {}
    games_played_map = {}
    for line in csv_lines:
        names = parse_names(line)
        ratings = [rating_map.get(name, INIT_RATING) for name in names]
        avg_ratings = sum(ratings) / PLAYER_NUM
        for place, name in enumerate(names, 1):
            rating = rating_map.get(name, INIT_RATING)
            games_played = games_played_map.get(name, 0)
            change = calc_rate_change(place, rating, avg_ratings, games_played)
            rating_map[name] = rating + change
            games_played_map[name] = games_played + 1

    player_info_map = {}
    sorted_ratings = sorted(rating_map.items(), key=lambda x: -x[1])
    for idx, kv_pair in enumerate(sorted_ratings):
        name, rating = kv_pair
        rating = round(rating)
        place = idx + 1
        if idx > 0:
            prev_pi = player_info_map[sorted_ratings[idx - 1][0]]
            if rating == prev_pi.rating:
                place = prev_pi.place
        games_played = games_played_map[name]
        player_info_map[name] = PlayerInfo(place, rating, games_played, name)
    return player_info_map


def main():
    file_name = 'records.csv'
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    with open(file_name, 'rb') as f:
        csv_lines = f.readlines()[1:]  # 去掉列名行
    csv_lines = [line.decode('utf-8') for line in csv_lines]
    csv_lines = csv_lines[::-1]  # 按时间正序

    player_info_map = handle_csv_lines(csv_lines)

    print(f"总对战数：{len(csv_lines)}")
    print("=======================")
    print(PlayerInfoList(player_info_map.values()))
    print()
    print("最近一场")
    print("=======================")
    names = parse_names(csv_lines[-1])
    print(PlayerInfoList([player_info_map[name] for name in names]))


if __name__ == '__main__':
    main()
