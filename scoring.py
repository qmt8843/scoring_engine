import requests
import dns.resolver
import ldap3
import mysql.connector
import socket
from smb.SMBConnection import SMBConnection
import time
import subprocess
import sqlite3

# Team Scores
SCOREBOARD_DATABASE = "score_data.db"
SCOREBOARD_TABLE = "scores"


# SERVICE CHECK FUNCTIONS

# Web Check (Srv2-Web, PLC1-OpenPLC, SCADA1-NodeRED)
def checkWeb(ip, port):
    try:
        response = requests.get(f'http://{ip}:{port}', timeout=1)
        if response.status_code in [302,200]:
            print(f'{ip} is WORKING (WEB CHECK)')
        return True
    except:
        print(f'{ip} is NOT WORKING (WEB CHECK)')
        return False

# DNS Check (AD1-DNS)
def checkDNS():
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['10.0.1.1']
        answer = resolver.resolve('google.com', 'A')
        if bool(answer) == True:
            print(f'DNS is WORKING')
            return True
    except:
        print(f'DNS is NOT WORKING')
        return False

# LDAP Check (AD1-LDAP)
def checkLDAP():
    try:
        server = ldap3.Server('10.0.1.1', connect_timeout=1)
        conn = ldap3.Connection(server)
        bind = conn.bind()
        if bind == True:
            print(f'LDAP is WORKING')
            return bind
    except:
        print(f'LDAP is NOT WORKING')
        return False

# MySQL Check
def checkSQL():
    try:
        conn = mysql.connector.connect(
            host = '10.0.2.4',
            user = 'databaseuser1',
            password = 'hamster',
            connection_timeout = 3
        )
        conn.close()
        print('MySQL is WORKING')
        return True
    except:
        print('MySQL is NOT WORKING')
        return False

# SMTP Check
def checkSMTP():
    try:
        with socket.create_connection(('10.0.1.2', 25), timeout=3) as sock:
            response = sock.recv(1024).decode()
            if response.startswith('220') == True:
                print("Mail is WORKING")
                return True
    except:
        print('Mail is NOT WORKING')
        return False

# SMB Check
def checkSMB():
    try:
        conn = SMBConnection("administrator", "Skylight2Swimmer3", "Scoring", "srv1", use_ntlm_v2=True)
        conn.connect('10.0.1.2', 139)
        shares = conn.listShares()
        if bool(shares) == True:
            print("SMB is WORKING")
            return True
    except:
        print("SMB is NOT WORKING")
        return False

serviceType = {
    "APACHE":"office",
    "SMTP":"office",
    "SMB":"office",
    "DNS":"office",
    "LDAP":"office",
    "OPENPLC":"industrial",
    "SQL":"industrial",
    "NODERED":"industrial"
}

def increase_blue_service_score(service, is_active):
    connection = sqlite3.connect(SCOREBOARD_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE {SCOREBOARD_TABLE} SET blue_points = blue_points + ? WHERE service = ?", (10, service))
    cursor.execute(f"UPDATE {SCOREBOARD_TABLE} SET is_active = ? WHERE service = ?)", (is_active, service))
    connection.commit()
    connection.close()

def increase_red_service_score(service, is_active):
    connection = sqlite3.connect(SCOREBOARD_DATABASE)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE {SCOREBOARD_TABLE} SET red_points = red_points + ? WHERE service = ?", (10, service))
    cursor.execute(f"UPDATE {SCOREBOARD_TABLE} SET is_active = ? WHERE service = ?", (is_active, service))
    connection.commit()
    connection.close()


# Scoring Function
def givePoints(service, result):
    global blueIndustrial, blueOffice, redOffice, redIndustrial, totalPossible

    if result == True:
        increase_blue_service_score(service, 1)
    elif result == False:
        increase_red_service_score(service, 0)

def main():
    while True:
        try:
            # Webserver Check
            apache = checkWeb('10.0.1.3', '80')
            # OpenPLC Check
            openplc = checkWeb('10.0.2.2', '8080')
            # NodeRed Check
            nodered = checkWeb('10.0.2.3', '1880')

            # Non-Web Checks
            dns = checkDNS()
            ldap = checkLDAP()
            sql = checkSQL()
            smtp = checkSMTP()
            smb = checkSMB()

            # List of results
            checkResults = {"APACHE":apache, 
                            "OPENPLC":openplc, 
                            "NODERED":nodered, 
                            "DNS":dns, 
                            "LDAP":ldap, 
                            "SQL":sql, 
                            "SMTP":smtp, 
                            "SMB":smb}
            

            # Calculate points
            for serviceName in checkResults:
                givePoints(serviceName, checkResults[serviceName])

            print("UPDATED POINTS")

            # Sleep and Clear
            time.sleep(30)
            subprocess.run('clear')

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()