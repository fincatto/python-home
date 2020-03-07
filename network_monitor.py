#!/usr/bin/env python3
import argparse
import subprocess
import sys
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def __measure_internet_speed():
    try:
        speed = subprocess.check_output(["speedtest", "--csv"]).strip().decode('utf-8').split(",")
        return True, {
            'date': datetime.now().strftime("%d/%m/%Y"),
            'time': datetime.now().strftime("%H:%M:%S"),
            'download': float(speed[6]) / 1000 / 1000,
            'upload': float(speed[7]) / 1000 / 1000,
            'srv_id': int(speed[0]),
            'srv_sponsor': speed[1],
            'srv_name': speed[2],
            'distance': float(speed[4]),
            'ping': float(speed[5]),
            'ip': speed[9]
        }
    except Exception as e:
        return False, e


def __upload_measurements(_credential, _sheet, _measurement):
    try:
        cred = ServiceAccountCredentials.from_json_keyfile_name(_credential, ['https://spreadsheets.google.com/feeds'])
        gc = gspread.authorize(cred)
        wks = gc.open_by_key(_sheet)
        worksheet = wks.get_worksheet(0)
        return True, worksheet.append_row([
            _measurement['date'],
            _measurement['time'],
            _measurement['srv_id'],
            _measurement['srv_sponsor'],
            _measurement['srv_name'],
            _measurement['ip'],
            _measurement['distance'],
            _measurement['ping'],
            _measurement['download'],
            _measurement['upload']
        ])
    except Exception as e:
        return False, e


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='Internet speed measurement system.')
    parser.add_argument('-c', type=str, required=False, action='store', dest='credential',
                        help='credential of google sheet to upload measurement data')
    parser.add_argument('-s', type=str, required=False, action='store', dest='sheet',
                        default='1q4qvTF3gCS5B1sPnh-HsBhfgTQmWg0t2Mo2xIq2E_Fo',
                        help='id of sheet to write measurement data')
    args = parser.parse_args()

    # test intenet speed
    print("Measuring internet connection speed...")
    measurement_ok, measurement_data = __measure_internet_speed()
    if not measurement_ok:
        sys.exit("Error measuring internet speed: {}".format(measurement_data))

    # if user set a credential, upload the results do google sheets
    if args.credential:
        print("Writing data do sheet '{}'...".format(args.sheet))
        upload_ok, upload_data = __upload_measurements(args.credential, args.sheet, measurement_data)
        if not upload_ok:
            sys.exit("Error uploading measurement do Google Sheets: {}".format(upload_data))
    else:
        print(measurement_data)
