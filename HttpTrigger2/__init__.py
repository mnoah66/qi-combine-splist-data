import logging

import azure.functions as func
import json
import os

import requests

from helper import column_names

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    intro = req_body['intro']
    consumer = req_body['consumer']
    eea = req_body['eea']    
    facility = req_body['facility']
    safety = req_body['safety']
    fleet = req_body['fleet']
    support = req_body['support']
    documentation = req_body['documentation']
    medical = req_body['medical']
    
    cleaned_cols = column_names.cleaned_consumer_columns()
   
    data = []

    if intro:
        for key, value in intro.items():
            my_l = []
            try:
                my_l.append(cleaned_cols['intro_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass
    
    if consumer:
        for key, value in consumer.items():
            my_l=[]
            try:
                my_l.append(cleaned_cols['consumer_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass
    if eea:
        for key, value in eea.items():
            my_l=[]
            try:
                my_l.append(cleaned_cols['eea_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass
    if facility:
        for key, value in facility.items():
            my_l=[]
            try:
                #data[cleaned_cols['facility_dict'][key]] = value
                my_l.append(cleaned_cols['facility_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass
    if safety:
        for key, value in safety.items():
            my_l=[]
            try:
                #data[cleaned_cols['safety_dict'][key]] = value
                my_l.append(cleaned_cols['safety_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass
    if fleet:
        for key, value in fleet.items():
            my_l=[]
            try:
                #data[cleaned_cols['fleet_dict'][key]] = value
                my_l.append(cleaned_cols['fleet_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass
    if support:
        for key, value in support.items():
            my_l=[]
            try:
                #data[cleaned_cols['support_dict'][key]] = value
                my_l.append(cleaned_cols['support_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass
    if documentation:
        for key, value in documentation.items():
            my_l=[]
            try:
                #data[cleaned_cols['docu_dict'][key]] = value
                my_l.append(cleaned_cols['docu_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass
    if medical:
        for key, value in medical.items():
            my_l=[]
            try:
                #data[cleaned_cols['medical_dict'][key]] = value
                my_l.append(cleaned_cols['medical_dict'][key])
                my_l.append(value)
                data.append(my_l)
            except:
                pass

   
    data = [x for x in data if not any(word in x[0] for word in ["x0020","x003a","#Id"])]

    def util_func(l):
       try:
         l[1] = l[1]['Value']
         return l
       except:
         return l
  
    # clean any of the mult-choice data
    data = [util_func(x) for x in data]
    

    ### EXCEPTIONS SPOT ###
    exceptions = []
    l = ['program', 'date','status','modified','created']
    for key, value in intro.items():
        my_l = []
        if key.lower() in l:
            my_l.append(key)
            my_l.append(value)
            exceptions.append(my_l) 

    falsey = ['FALSE', "FALSE", False, 0, "No"]
    for item in data:
        my_l = []
        if item[1] in falsey:
            if item[0] not in [r"{IsFolder}",r"{HasAttachments}"]: 
                my_l.append(item[0]) 
                my_l.append(item[1])
                exceptions.append(my_l) 
    for item in data:
        my_l = []
        if "comments" in item[0].lower():
            my_l.append(item[0]) 
            my_l.append(item[1])
            exceptions.append(my_l) 

    resp = []
    resp.append({"meta":{"ProgramName":"Ashwood","Date":"7/13/22"}})
    #resp[1]["exceptions"] = exceptions
    resp.append({"exceptions": exceptions})
    #resp[2]["all_data"] = data
    resp.append({"all_data": data})
    #logging.info(exceptions)
    #data = exceptions
    return func.HttpResponse(
             json.dumps(resp),
             status_code=200
        )
