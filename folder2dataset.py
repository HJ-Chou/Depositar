# ----------------------------------------------------------------------------------------------------
# HJC
# IESDMC
# 2024-12-11
# ver1.0
# This code is used to upload a folder that the user wants to save as a dataset to the depositar.
# ----------------------------------------------------------------------------------------------------
import os
import requests
import pprint


# Set local folder path
local_folder_path = ''  # local folder that user wants to upload.
folder_name = ''  # Dataset name on depositar

# Dataset details
dataset_dict = {
    'name': folder_name,  # Use the folder name as the dataset name
    #'notes': '',  # Description of dataset
    'owner_org': '',  # Project ID, if your project link is 'https://data.depositar.io/organization/abc' the abd would be Project ID.
    'author': '',  # Author name
    'data_type': 'other',  # Dataset type
    'license_id': 'cc-by-4.0'  # License type
}

# CKAN API URLs and API Key
ckan_package_create_url = 'https://data.depositar.io/api/3/action/package_create'
ckan_resource_create_url = 'https://data.depositar.io/api/3/action/resource_create'
api_key = ''  # user need to create an api token, it can be found on the depositar user page

# Headers
headers = {
    'Authorization': api_key,
    'Content-Type': 'application/json'
}

try:
    # Step 1: Create dataset
    response = requests.post(ckan_package_create_url, headers=headers, json=dataset_dict)
    if response.status_code == 200:
        response_dict = response.json()
        if response_dict.get('success'):
            created_package = response_dict['result']
            dataset_id = created_package['id']  # Retrieve the created dataset ID
            print(f"Successfully created dataset: {created_package['name']}")
            pprint.pprint(created_package)
        else:
            print("Failed to create dataset")
            pprint.pprint(response_dict)
            exit()
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        exit()

    # Step 2: Iterate through local folder and upload each file as a resource
    for file_name in os.listdir(local_folder_path):
        file_path = os.path.join(local_folder_path, file_name)

        # Ensure it is a file and not a subdirectory
        if os.path.isfile(file_path):
            print(f"Uploading file: {file_name}")

            # Open file and prepare for upload
            with open(file_path, 'rb') as file_data:
                resource_dict = {
                    'package_id': dataset_id,  # Dataset ID
                    'name': file_name,  # Resource name
                    #'description': f'Resource uploaded from {file_path}'  # Resource description
                }
                files = {
                    'upload': file_data  # File upload
                }
                response = requests.post(ckan_resource_create_url, headers={'Authorization': api_key}, data=resource_dict, files=files)

                # Check response
                if response.status_code == 200:
                    response_dict = response.json()
                    if response_dict.get('success'):
                        print(f"Successfully uploaded resource: {file_name}")
                        pprint.pprint(response_dict['result'])
                    else:
                        print(f"Failed to upload resource: {file_name}")
                        pprint.pprint(response_dict)
                else:
                    print(f"HTTP Error: {response.status_code}")
                    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

