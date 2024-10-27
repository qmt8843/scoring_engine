import requests
import dns.resolver
import ldap3
import mysql.connector
import socket
from smb.SMBConnection import SMBConnection
import time
import os
import subprocess

# Team Scores
blueIndustrial = 0
blueOffice = 0
redIndustrial = 0
redOffice = 0

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

# Scoring Function
def givePoints(team):
    if team == blueIndustrial:
        blueIndustrial += 10
    elif team == blueOffice:
        blueOffice += 10
    elif team == redIndustrial:
        redIndustrial += 10
    elif team == redOffice:
        redOffice += 10


def main():
    while True:
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

        # Sleep and Clear
        time.sleep(30)
        subprocess.run('clear')
        


if __name__ == '__main__':
    main()