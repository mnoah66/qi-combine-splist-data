import os
import json
import requests
import logging


def cleaned_consumer_columns():

    client_id = os.getenv('clientId')
    client_secret = os.getenv('clientSecret')
    tenant = os.getenv('tenant')
    tenant_id = os.getenv('tenantId')
    client_id = client_id + '@' + tenant_id


    data = {
        'grant_type':'client_credentials',
        'resource': "00000003-0000-0ff1-ce00-000000000000/" + tenant + ".sharepoint.com@" + tenant_id, 
        'client_id': client_id,
        'client_secret': client_secret,
    }

    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    # Make a POST request to LOGIN and get the token
    r = requests.post("https://accounts.accesscontrol.windows.net/0e461760-99dd-4c07-8103-77f2c7465ea4/tokens/OAuth/2", data=data, headers=headers)
    
    json_data = json.loads(r.text)
    # Add the bearer token to the header
    headers = {
        'Authorization': "Bearer " + str(json_data['access_token']),
        'Accept':'application/json;odata=verbose',
        'Content-Type': 'application/json;odata=verbose'
    }

    intro = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlyIntro')/Fields", headers=headers).json()
    consumer = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlyConsumer')/Fields", headers=headers).json()
    eea = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlyEEA')/Fields", headers=headers).json()
    facility = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlyFacility')/Fields", headers=headers).json()
    safety = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlySafety')/Fields", headers=headers).json()
    fleet = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlyVehicleFleet')/Fields", headers=headers).json()
    support = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlySupportDepartment')/Fields", headers=headers).json()
    documentation = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlyDocumentation')/Fields", headers=headers).json()
    medical = requests.get("https://arcessex.sharepoint.com/sites/QualityImprovement/_api/web/lists/getbytitle('ResQuarterlyMedDocStorage')/Fields", headers=headers).json()

    lookup = {}

    
    intro_dict = {}
    for item in intro['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            intro_dict[item['InternalName']] = item['Title']
    lookup['intro_dict'] = intro_dict

    consumer_dict = {}
    for item in consumer['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            consumer_dict[item['InternalName']] = item['Title']
    lookup['consumer_dict'] = consumer_dict
    
    eea_dict={}
    for item in eea['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            eea_dict[item['InternalName']] = item['Title']
    lookup['eea_dict'] = eea_dict
    
    facility_dict={}
    for item in facility['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            facility_dict[item['InternalName']] = item['Title']
    lookup['facility_dict'] = facility_dict


    safety_dict={}
    for item in safety['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            safety_dict[item['InternalName']] = item['Title']
    lookup['safety_dict'] = safety_dict
    
    fleet_dict={}
    for item in fleet['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            fleet_dict[item['InternalName']] = item['Title'] 
    lookup['fleet_dict'] = fleet_dict
    
    support_dict = {}
    for item in support['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            support_dict[item['InternalName']] = item['Title']  
    lookup['support_dict'] = support_dict

    docu_dict = {}
    for item in documentation['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            docu_dict[item['InternalName']] = item['Title']   
    lookup['docu_dict'] = docu_dict

    medical_dict = {}
    for item in medical['d']['results']:
        if not item['FromBaseType']: # Ignore the auto generated columns
            medical_dict[item['InternalName']] = item['Title']
    lookup['medical_dict'] = medical_dict
    
    
    return lookup