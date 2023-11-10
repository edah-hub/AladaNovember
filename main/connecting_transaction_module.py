import requests
import json
TXN_BASE_URL='http://bharathbrandsdotin.pythonanywhere.com/'
TXN_NAMING_CONVENTION='api/'
TXN_ENDPOINT='services/'
TXN_LOGIN_ENDPOINT='token/'
import time
def transaction_login(data):
    '''
    This function is specially calling the login apis.
    '''
    print('this is transaction login')
    login_credential={
        'username':data['username'],
        'password':data['Password'],
    }
    LOGIN_CREDENTIAL=json.dumps(login_credential) 
    response = requests.post(TXN_BASE_URL+TXN_NAMING_CONVENTION+TXN_LOGIN_ENDPOINT,data=LOGIN_CREDENTIAL, headers={"Content-type": "application/json;charset=utf-8"})
    responses=response.json()
    print('Trying..')
    if response.status_code == 200:
        print('success login')
        access_token=responses['access']
        return access_token
    else:
        print('not succuess')
        return 'AuthenticationFailed'

def all_transaction_process(data):
    '''
    from here we are calling transaction mudole of the all services.S
    '''
    dict_key = []
    dict_value = []
    for key, values in dict(data).items():
        if key != 'csrfmiddlewaretoken':
            dict_key.append(key)
            if len(values) == 1:
                value = ''.join(values)
                dict_value.append(value)
            else:
                value = ','.join(values)
                dict_value.append(value)

        else:
            continue
    field_name_value = dict(zip(dict_key, dict_value))  # converting two list into the dict.

    print('field_name_value ', field_name_value)
    my_data = {
                "service_id": data['service_ID'],
                "process_workflow":data['process_workflow'],
                "channel_id": data['channel_id'],
                "total_fees": data['total_fees'],
                "service_description": data['service_description'],
                "user_id": "SU001",
                "national_id": "234567886",
                "service_type": "DirectServicePayment",
                "phone_number": 254711849456,
                "input_params_values": field_name_value,
        }
    DATA=json.dumps(my_data)   
    request_time = time.time() 
    print('request time ',request_time)    
    response=requests.post(TXN_BASE_URL+TXN_NAMING_CONVENTION+TXN_ENDPOINT,data=DATA, headers={"Content-type": "application/json;charset=utf-8"})
    print(response)
    response_code = response.status_code
   
    if response_code == 200:
        responses=response.json()
        return 'success'
    else:
        print('response_code ',response_code)
        return 'failed'



def send(): 
    file = open("Application.pdf", "rb")

    response = requests.post(
        "http://127.0.0.1:8000/upload", 
        files={"birth certificate": file}, 
        data={"name": "edwin the dev"},
        )

    print("HELLO0000") 
    print(response.json())