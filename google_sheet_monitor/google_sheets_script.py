import httplib2
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from config_script import *
from bs4 import BeautifulSoup
from time import sleep

import psycopg2

class DB():
    def __init__(self):

        self.connection = psycopg2.connect(user=USER_DB,
                                          password=PASSWORD_DB,
                                          host=HOST_DB,
                                          port=PORT_DB,
                                          database=NAME_DB)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT version();")
        record = self.cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

    def select_db(self, sheet_values):
        self.cursor.execute("SELECT * FROM page_static_table")
        table = self.cursor.fetchall()
        list_x = []
        for sv in sheet_values[1:]:
            list_x.append(int(sv[0]))

        list_y = []
        for t in table:
            list_y.append(t[0])

        for y in list_y:
            if y not in list_x:
                delete_one = f"""DELETE FROM page_static_table  WHERE number={y}"""
                self.cursor.execute(delete_one)
        self.connection.commit()

    def inser_or_update_db(self, sheet_values):
        self.select_db(sheet_values)
        for sv in sheet_values[1:]:
            insert_one = '''
                INSERT INTO page_static_table (number, order_number, price_usd, price_rub, delivery_time)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (number) DO UPDATE SET
                (order_number, price_usd, price_rub, delivery_time) = (EXCLUDED.order_number, EXCLUDED.price_usd, EXCLUDED.price_rub, EXCLUDED.delivery_time);
            '''
            value_insert_one = (sv[0], sv[1], sv[2], sv[4], sv[3])
            self.cursor.execute(insert_one, value_insert_one)
        self.connection.commit()


class GoogleSheets():
    def __init__(self):
        self.CREDENTIALS_FILE = CREDENTIALS_FILE
        self.spreadsheet_id = SPREADSHEET_ID
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('sheets', 'v4', http=self.httpAuth)
        self.range = ['Лист']

        sheet_values = self.read_table()
        sheet_values_rub = self.price_rub(sheet_values)

        db = DB()
        db.inser_or_update_db(sheet_values_rub)
        db.connection.close()

    def read_table(self):
        results = self.service.spreadsheets().values().batchGet(spreadsheetId=self.spreadsheet_id,
                                                                ranges=self.range,
                                                                valueRenderOption='FORMATTED_VALUE',
                                                                dateTimeRenderOption='FORMATTED_STRING').execute()
        sheet_values = results['valueRanges'][0]['values']
        return sheet_values

    def price_rub(self, sheet_values):
        date_url = datetime.now().date().strftime("%d/%m/%Y")
        r = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_url}')
        b = BeautifulSoup(r.text, features='xml')
        kurs_rub = float(b.find('Valute', ID="R01235").find('Value').text.replace(',', '.'))
        for sv in sheet_values[1:]:
            price_rub = int(float(sv[2]) * kurs_rub)
            sv.append(price_rub)
        return sheet_values


def main():
    while True:
        g = GoogleSheets()
        g.read_table()
        sleep(10)

if __name__ == '__main__':
    main()