import requests

API_URL = "https://bbservicesutomationsystem.pythonanywhere.com/api/v1/servicetype-mapping/"
SERVICE_METADATA_URL = "https://bbservicesutomationsystem.pythonanywhere.com/api/v1/servicetype/"


def get_service_fields(service_type_name):
    URL = API_URL + str(service_type_name)
    payload = {
        "servicetype_name": service_type_name
    }
    response = requests.get(
        URL,
        params=payload
    )
    if response.status_code != 200:
        return 'Failed'
    
    return response.json()
    
    # if len(response.json().get('service_field_group')) > 0:
    #     data = {
    #         "service_fields": response.json()['service_fields'],
    #         "service_field_groups": response.json()['service_field_group'],
    #     }
    #     return data
    # else:
    #     data = {
    #         "service_fields": response.json()['service_fields'],
    #         "service_field_groups": [],
    #     } 
    #     return data
    # response_service_field_group=response.json()['service_field_group']
    # if len(response_service_field_group) == 0:
    #     return response_service_fields
    # else:
    #     get_service_group=response_service_field_group[0]
    #     pure_service_group_details=get_service_group['service_fields']
    #     return response_service_fields,pure_service_group_details
   


def get_service_metadata(service_type_name):
    URL = SERVICE_METADATA_URL + str(service_type_name)

    payload = {
        "servicetype_name": service_type_name
    }
    response = requests.get(
        URL,
        params=payload
    )

    return response.json()
