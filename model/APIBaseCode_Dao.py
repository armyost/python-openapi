import requests
from sqlalchemy import text

class APIBaseCodeDao:
    def __init__(self, database, commonBackendUrl):
        self.db = database
        self.COMMON_BACKEND_URL = commonBackendUrl

    def selectPnuCode(self, state, city, town1, town2):
        row = self.db.execute(text("""
            SELECT PNUCODE
            FROM TBPNUCODE
            WHERE STATE = :state
            AND CITY = :city
            AND TOWN1 = :town1
            AND TOWN2 = :town2
            """), {'state' : state,
            'city' : city,
            'town1' : town1,
            'town2' : town2}
        ).fetchone()
        return {
            'PNUCODE' : row['PNUCODE']
        } if row else None
        
    def selectCropName(self, search_word):
        rows = self.db.execute(text("""
            SELECT * FROM TBCROPCODE 
            WHERE DESCRIPTION LIKE "%":search_word"%"
            """), {'search_word' : search_word}
        ).fetchall()
        return [{
            'CODE' : row['CODE'],
            'DESCRIPTION'   : row['DESCRIPTION']
        } for row in rows]

    def selectCropCode(self, crop_name):
        row = self.db.execute(text("""
            SELECT * FROM TBCROPCODE 
            WHERE DESCRIPTION = :crop_name
            """), {'crop_name' : crop_name}
        ).fetchone()
        return row['CODE']

    def selectDeviceLocation(self, group_id):
        url = self.COMMON_BACKEND_URL+"/detailEndpointGroup/"+group_id
        print("URL IS",url)
        headers = {
            'Content-Type': 'application/json',
            'charset': 'UTF-8',
            'Accept': '*/*',
            } 
        try: 
            responseJson = requests.get(url, headers=headers)
            print(responseJson.json()['device_info']) # api에서 가져와서 dao찍는거 하자
        except Exception as ex: 
            print(ex)
        return responseJson.json()['device_info']