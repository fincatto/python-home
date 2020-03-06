import subprocess
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

if __name__ == '__main__':
    try:
        # mede a velocidade da conexao
        speed = subprocess.check_output(["speedtest", "--csv"]).strip().decode('utf-8').split(",")
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        download = float(speed[6]) / 1000 / 1000
        upload = float(speed[7]) / 1000 / 1000
        srv_id = int(speed[0])
        srv_sponsor = speed[1]
        srv_name = speed[2]
        distance = float(speed[4])
        ping = float(speed[5])
        ip = speed[9]
        # print(speed)

        scope = ['https://spreadsheets.google.com/feeds']
        cred = ServiceAccountCredentials.from_json_keyfile_name('/Users/diego/Downloads/fincatto-home-key.json', scope)
        gc = gspread.authorize(cred)
        wks = gc.open_by_key('1q4qvTF3gCS5B1sPnh-HsBhfgTQmWg0t2Mo2xIq2E_Fo')
        worksheet = wks.get_worksheet(0)
        row = worksheet.append_row([date, time, srv_id, srv_sponsor, srv_name, ip, distance, ping, download, upload])
    except Exception as e:
        print("Error measuring internet speed", e)
