from flask import Flask, jsonify
import urllib.request, json, datetime

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

class Schedule:

    def __init__(self, gameID, date, UTCtime, visitor, home):
        self.gameID = gameID
        self.date = date
        self.UTCtime = UTCtime
        self.visitor = visitor
        self.home = home

@app.route('/nba')
def get_games():
    with urllib.request.urlopen("http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json") as url:
        data = json.load(url)

        datenow = str(datetime.date.today())
        gamesList = []
        lscd = data['lscd']
        # print(lscd)

        for i in lscd:
            # print(i['mscd']['g'])
            for j in i['mscd']['g']:
                gameID = j['gid']
                date = j['gdte']
                UTCtime = j['utctm']
                visitor = j['v']['tn']
                home = j['h']['tn']

                if date == datenow:
                    game = Schedule(gameID, date, UTCtime, visitor, home)

                    gamesList.append(game.__dict__)

    return jsonify(gamesList)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
