

from scrapinghelp import htmlhelper
import json
from datetime import datetime
from Scarpe_Data import ExtractData
import xlrd
import os
import requests


if __name__ == "__main__":
      filename="sdn_list_xmltojson.json"
      file = open(filename, encoding="utf8")
      jsondata= file.read()
      obj=json.loads(jsondata)
      mylist=[]
      convert_date = {
            "1": "01",
            "2": "02",
            "3": "03",
            "4": "04",
            "5": "05",
            '6': "06",
            "7": "07",
            "8": "08",
            "9": "09"
      }
      convertmonthdate = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
      }


      newfilename="mysdnjsonlist.json"

      newfile=open(newfilename,encoding="utf8")
      readdata=newfile.read()
      arr=json.loads(readdata)
      excellist=[]
      for elements  in  arr["Sheet1"]:
          excellist.append(elements)

     


      list=[]

      for  ele  in obj['sdnList']["sdnEntry"]:
          print(ele, end="\n")
          list.append(ele)


      ExtractData.Extract(list,excellist,convert_date,convertmonthdate)



































































































































































































































