from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

SCOREBOARD_DATABASE = "score_data.db"
SCOREBOARD_TABLE = "scores"
SERVICES = {"APACHE","SMTP","SMB","DNS","LDAP","OPENPLC","SQL","NODERED"}

def get_blue_service_score(service):
    connection = sqlite3.connect(SCOREBOARD_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"SELECT blue_points FROM {SCOREBOARD_TABLE} WHERE service = '{service}'")
    output = cursor.fetchall()
    connection.close()
    return output[0][0]

def get_red_service_score(service):
    connection = sqlite3.connect(SCOREBOARD_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"SELECT red_points FROM {SCOREBOARD_TABLE} WHERE service = '{service}'")
    output = cursor.fetchall()
    connection.close()
    return output[0][0]

def get_is_service_active(service):
    connection = sqlite3.connect(SCOREBOARD_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"SELECT is_active FROM {SCOREBOARD_TABLE} WHERE service = '{service}'")
    output = cursor.fetchall()
    connection.close()
    return output[0][0]

@app.route("/")
def scoreboard():
    scoreboard_data = []
    for service in SERVICES:
        blue_og = get_blue_service_score(service)
        red_og = get_red_service_score(service)
        if blue_og==0 and red_og==0:
            blue_norm = 50
            red_norm = 50
        elif blue_og==0:
            red_norm = 100
            blue_norm = 0
        elif red_og==0 :
            blue_norm = 100
            red_norm = 0
        else:
            total = blue_og+red_og
            blue_norm = blue_og/total*100
            red_norm = red_og/total*100
        curr_service = {'service':service, 'is_active':get_is_service_active(service), 'blue_points':blue_norm , 'red_points':red_norm }
        scoreboard_data.append(curr_service)
    
    # Render the HTML template with the variables
    return render_template('index.html', scoreboard=scoreboard_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)