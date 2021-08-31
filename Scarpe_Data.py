from scrapinghelp import htmlhelper
import json
from datetime import datetime
import hashlib

import xlrd
import requests
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def transform_name(name):
  name=name.replace("  ","")
  name=name.replace("\r","")
  name=name.replace("\t","")
  name=name.replace('\n','')
  name = name.replace("_", "")
  name = name.replace("Shri ", "")
  name = name.replace("SRI ", "")
  name = name.replace("Smt. ", "")
  name = name.replace("Dr. ", "")
  name = name.replace("Dr ", "")
  name = name.replace("Capt. ", "")
  name = name.replace("Sh. ", "")
  name = name.split(',')
  name = name[0]
  name = name.strip()

  return name

def alias_name(name):
  alias_list=[]
  subname = name.split(' ')
  l = len(subname)
  if l>=3:
    name1 = subname[l-1] + " " + subname[0]
    name2 = subname[l-2] + " " + subname[0]
    alias_list.append(transform_name(name1))
    alias_list.append(transform_name(name2))
  if l==2:
    name1 = subname[1] + " " + subname[0]
    alias_list.append(transform_name(name1))

  return alias_list


class ExtractData:
    def Extract(list,excellist,convert_date,convertmonthdate):
        my_list=[]
        for ele in list:
            d = {
                "name": "",
                "uid": "",
                "alias_name": [],
                "country": [],

                "address": [
                    {
                        "complete_address": "",
                        "state": "",
                        "city": "",
                        "country": ""
                    }
                ],
                "list_type": "individual",
                "nns_status": "False",
                "last_updated": last_updated_string,
                "individual_details": {
                    "gender": "",
                    "date_of_birth": [],
                    "organisation": ""
                },
                "documents": {
                    "passport": "",
                    "ssn": ""
                }
            }
            sanction_list = {
                "sl_authority": "U.S. DEPARTMENT OF THE TREASURY",
                "sl_url": "https://home.treasury.gov/",
                "sl_host_country": "United States",
                "sl_type": "SDN",
                "sl_source": "OFAC",
                "sl_description": "The U.S. Department of the Treasury's mission is to maintain a strong economy and create economic and job opportunities by promoting the conditions that enable economic growth and stability at home and abroad, strengthen national security by combating threats and protecting the integrity of the financial system, and manage the U.S. Government’s finances and resources effectively."
            }
            d["sanction_list"] = sanction_list


            try:
                get_firstname=ele['firstName']
            except:
                get_firstname=""
                pass
            try:
                get_lastname=ele['lastName']
            except:
                pass

            try:
                if get_firstname!="":
                    getname=get_firstname+" "+get_lastname
                    d['name']=transform_name(getname)
                else:
                    d['name']=transform_name(get_lastname)
            except:
                pass

            try:
                get_city=ele['addressList']['address']['city']
                if get_city!="":
                    d["address"][0]['city']=get_city
            except:
                pass


            try:
                get_country=ele['addressList']['address']['country']
                if get_country != "":
                    d["address"][0]['country'] = get_country
                    d['country'].append(get_country)
            except:
                pass


            try:
                get_complete_add=get_city+', '+get_country
                if get_complete_add!="":
                    d['address'][0]["complete_address"]=get_complete_add
            except:
                pass

            try:
                get_sdntype = ele['sdnType']
                if get_sdntype!="":
                    d["list_type"]=get_sdntype
            except:
                pass

            try:
                get_aliases=ele['akaList']['aka']['firstName']


            except:
                get_aliases=""
                pass
            try:
                get_secondalias=ele['akaList']['aka']['lastName']
            except:
                get_secondalias=""
                pass
            try:
                get_allaliases=get_aliases+" "+get_secondalias
                get_allaliases=get_allaliases.strip()
                if get_allaliases!="":
                    d["alias_name"].append(get_allaliases)
            except:
                pass





            try:


                get_name_alias_leangth = ele["akaList"]["aka"][1]
                getalias_first=get_name_alias_leangth["firstName"]
                getalias_last=get_name_alias_leangth["lastName"]
                d["alias_name"].append(getalias_first+" "+getalias_last)

            except:
                pass

            try:

                get_name_alias_leangth = ele["akaList"]["aka"][2]
                get1alias_first = get_name_alias_leangth["firstName"]
                get1alias_last = get_name_alias_leangth["lastName"]
                d["alias_name"].append(get1alias_first + " " + get1alias_last)

            except:
                pass

            try:

                get_name_alias_leangth = ele["akaList"]["aka"][3]
                get2alias_first = get_name_alias_leangth["firstName"]
                get2alias_last = get_name_alias_leangth["lastName"]
                d["alias_name"].append(get2alias_first + " " + get2alias_last)

            except:
                pass


            try:
                get_dob=ele['dateOfBirthList']['dateOfBirthItem']['dateOfBirth']
                if len(get_dob) == 4:
                    get_dob = get_dob + "-" + "00" + "-" + "00"
                    d["individual_details"]["date_of_birth"].append(get_dob)
                    if get_dob!="":
                        d["individual_details"]["date_of_birth"].append(get_dob)
                elif len(get_dob)==11:
                    get_dob=get_dob.split(" ")
                    getdate=get_dob[0]
                    getmonth=get_dob[1]
                    getyear=get_dob[2]
                    if getdate in convert_date:
                        getdate=convert_date[getdate]
                    if getmonth in convertmonthdate:
                        getmonth=convertmonthdate[getmonth]

                    completedob=getyear+"-"+getmonth+"-"+getdate
                    d["individual_details"]["date_of_birth"].append(completedob)



            except:
                pass





            try:
                get_programlist=ele['programList']['program']
                if get_programlist!="":
                    for go in excellist:
                        if get_programlist in go['Program Tag']:
                            try:
                                get_my_program=go['Program']
                                if get_my_program!="":

                                    d['sanction_list']['sl_type']=d['sanction_list']['sl_type']+", "+go['Program']
                                    d['sanction_list']["sl_source"]=d['sanction_list']["sl_source"]+"- "+"("+go['\u200bDefinition']+")"
                                    break
                            except:
                                d['sanction_list']["sl_source"] = d['sanction_list']["sl_source"] + "- " + "(" + go[
                                    '\u200bDefinition'] + ")"
                                continue
            except:
                pass

            try:
                d["uid"] = hashlib.sha256(((d["name"] + d["sanction_list"]["sl_type"]).lower()).encode()).hexdigest()
            except:
                pass


            try:
                if d["list_type"]=="Entity":

                    del d["individual_details"]
                    del d["documents"]["passport"]
                    del d["documents"]["ssn"]
                    documents={
                        "CIN":""
                    }
                    d['documents']=documents



            except:
                pass


            try:
                splitsource=d['sanction_list']["sl_source"]
                if ";" in splitsource:

                    splitsource=htmlhelper.returnvalue(splitsource,"OFAC",";")
                    d['sanction_list']["sl_source"] = "OFAC" + splitsource + ")"
                elif "," in splitsource:
                    splitsource = htmlhelper.returnvalue(splitsource, "OFAC", ",")
                    d['sanction_list']["sl_source"] = "OFAC" + splitsource + ")"






            except:
                pass




            try:
                my_list.append(d)
            except:
                pass

        with open('sdn_list.json', 'w', encoding="utf-8") as file:
            json.dump(my_list, file, ensure_ascii=False, indent=4)













