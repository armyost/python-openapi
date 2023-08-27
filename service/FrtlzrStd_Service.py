import requests
import xmltodict, json
from datetime import date
import re

class FrtlzrStdService:
    def __init__(self, APIBaseCodeDao):
        self.APIBaseCodeDao = APIBaseCodeDao
        self.NCP_API_KEYID = "xqd4yaaj35"
        self.NCP_API_KEY = "3X746SZhS6G0JpwszFm8utFDbz3ASwP2Tgyayoh8"
        self.SERVICEKEY ="a4hWawJoXOQSd1ao8PZkv6hkhi9jnCIHeIAhO0XgNm1f0%2F3O%2F7QLbVu4r5semkmEkbTJKs8R5068AYyX9niv8A%3D%3D"
       
    def addressFind(self, group_id):
        API_HOST = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
        LATITUDE = str(self.APIBaseCodeDao.selectDeviceLocation(group_id)['LATITUDE'])
        LONGITUDE = str(self.APIBaseCodeDao.selectDeviceLocation(group_id)['LONGITUDE'])
        url = API_HOST+"?coords="+LATITUDE+","+LONGITUDE+"&output=json"
        headers = {
            'Content-Type': 'application/json',
            'charset': 'UTF-8',
            'Accept': '*/*',
            'X-NCP-APIGW-API-KEY-ID': self.NCP_API_KEYID,
            'X-NCP-APIGW-API-KEY': self.NCP_API_KEY
            } 
        try: 
            responseJson = requests.get(url, headers=headers)
            # print("response status %r" % responseJson.status_code) 
            # print("response text %r" % responseJson.text)
        except Exception as ex: 
            print(ex)
        return responseJson.json()
        
    # def pnuCodeFind(self, STATE, CITY, TOWN1, TOWN2):
    #     return self.APIBaseCodeDao.selectPnuCode(STATE, CITY, TOWN1, TOWN2)['PNUCODE']
    
    def pnuCodeFind(self, dicAddress):
        STATE = dicAddress['results'][0]['region']['area1']['name']
        CITY = dicAddress['results'][0]['region']['area2']['name']
        TOWN1 = dicAddress['results'][0]['region']['area3']['name']
        TOWN2 = dicAddress['results'][0]['region']['area4']['name']
        return self.APIBaseCodeDao.selectPnuCode(STATE, CITY, TOWN1, TOWN2)['PNUCODE']
        
    def frtlzrStdPnuFind(self, endpoint_pnu):
        API_HOST = "http://apis.data.go.kr/1390802/SoilEnviron/SoilExam/getSoilExamList"
        url = API_HOST+"?serviceKey="+self.SERVICEKEY+"&Page_Size=10&Page_No=1&BJD_Code="+str(endpoint_pnu)
        headers = {
            'Content-Type': 'application/json',
            'charset': 'UTF-8',
            'Accept': '*/*'
            } 
        try: 
            responseXml = requests.get(url, headers=headers)
            # print("response status %r" % responseXml.status_code) 
            # print("response text %r" % responseXml.text)
        except Exception as ex: 
            print(ex)
        return json.dumps(xmltodict.parse(responseXml.text))
    
    def frtlzrStdPnuTopFind(self, endpoint_pnu):
        API_HOST = "http://apis.data.go.kr/1390802/SoilEnviron/SoilExam/getSoilExamList"
        url = API_HOST+"?serviceKey="+self.SERVICEKEY+"&Page_Size=100&Page_No=1&BJD_Code="+str(endpoint_pnu)
        current_yyyymmdd = re.sub(r"[^0-9]", "", str(date.today()))
        candidateIndex = 0
        index = 0
        tempValue = 20000
        headers = {
            'Content-Type': 'application/json',
            'charset': 'UTF-8',
            'Accept': '*/*'
            } 
        try: 
            responseXml = requests.get(url, headers=headers)
            # print("response status %r" % responseXml.status_code) 
            # print("response text %r" % responseXml.text)
        except Exception as ex: 
            print(ex)
        resJson = json.loads(json.dumps(xmltodict.parse(responseXml.text)))
        items = resJson['response']['body']['items']
        for i in items['item']:
            if(int(i['Exam_Day'])-int(current_yyyymmdd) < tempValue):
                tempValue = int(current_yyyymmdd)-int(i['Exam_Day'])
                candidateIndex = index
            index = index + 1
        return items['item'][candidateIndex]
    
    def frtlzrStdCropFind(self, crop_code):
        API_HOST = "http://apis.data.go.kr/1390802/SoilEnviron/FrtlzrStdUse/getSoilFrtlzrQyList"
        url = API_HOST+"?serviceKey="+self.SERVICEKEY+"&fstd_Crop_Code="+str(crop_code)
        headers = {
            'Content-Type': 'application/json',
            'charset': 'UTF-8',
            'Accept': '*/*'
            } 
        try: 
            responseXml = requests.get(url, headers=headers)
        except Exception as ex: 
            print(ex)
        return json.loads(json.dumps(xmltodict.parse(responseXml.text)))

