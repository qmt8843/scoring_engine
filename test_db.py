import sqlite3

SCOREBOARD_DATABASE = "score_data.db"
SCOREBOARD_TABLE = "scores"


def get_blue_score(service):
    connection = sqlite3.connect(SCOREBOARD_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {SCOREBOARD_TABLE} WHERE service = '{service.upper()}'")
    output = cursor.fetchall()
    connection.close()
    return output

print(get_blue_score("LDAP"))

