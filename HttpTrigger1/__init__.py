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
   
    data = {}

    for key, value in intro.items():
        data[key] = value
    
    if consumer:
        for key, value in consumer.items():
            try:
                data[cleaned_cols['consumer_dict'][key]] = value
            except:
                data[key] = value
    if eea:
        for key, value in eea.items():
            try:
                data[cleaned_cols['eea_dict'][key]] = value
            except:
                data[key] = value
    if facility:
        for key, value in facility.items():
            try:
                data[cleaned_cols['facility_dict'][key]] = value
            except:
                data[key] = value
    if safety:
        for key, value in safety.items():
            try:
                data[cleaned_cols['safety_dict'][key]] = value
            except:
                data[key] = value
    if fleet:
        for key, value in fleet.items():
            try:
                data[cleaned_cols['fleet_dict'][key]] = value
            except:
                data[key] = value
    if support:
        for key, value in support.items():
            try:
                data[cleaned_cols['support_dict'][key]] = value
            except:
                data[key] = value
    if documentation:
        for key, value in documentation.items():
            try:
                data[cleaned_cols['docu_dict'][key]] = value
            except:
                data[key] = value
    if medical:
        for key, value in medical.items():
            try:
                data[cleaned_cols['medical_dict'][key]] = value
            except:
                data[key] = value

    for key in list(data.keys()):
        if "x0020" in key or "x003a" in key or "#Id" in key:
            del data[key]
            continue 
        try:
            data[key] = data[key]['Value']
        except:
            pass       

    data = [data] # put into a list as Power Automate expects a list of objects
    return func.HttpResponse(
             json.dumps(data),
             status_code=200
        )
