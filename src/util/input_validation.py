
def validate_download_json(download_json):
    if download_json != None and download_json != {}:
        if 'satelliteType' in download_json:
            if download_json['satelliteType'] == 'Sentinel1':
                print(1, download_json['startDate'], download_json['endDate'], download_json['geometry'], download_json['user'], download_json['password'], download_json['path'])
                #TODO decide which ones are required and which one are optional
                if 'startDate' in download_json and 'endDate' in download_json and 'geometry' in download_json and 'user' in download_json and 'password' in download_json and 'path' in download_json:
                    if 'processingLevel' in download_json and 'sensorMode' in download_json and 'sensorMode' in download_json and 'productType' in download_json:
                        return True
            if download_json['satelliteType'] == 'Sentinel2':
                if 'startDate' in download_json:
                    if 'endDate' in download_json:
                        if 'processingLevel' in download_json:
                            if 'sensorMode' in download_json:
                                if 'productType' in download_json:
                                    if 'geometry' in download_json:
                                        if 'path' in download_json:
                                            if 'user' in download_json:
                                                if 'password' in download_json:
                                                    return True
    return False

def validate_json(json_object):
    downl_obj, processing_obj = {},{}
    if json_object != None and json_object != {}:
        if 'download' in json_object:
            tmp_down = json_object['download']
            if validate_download_json(tmp_down):
                downl_obj = tmp_down
            else:
                print(f"Waring: {tmp_down} is not a valid format for download!")
        else:
            print(f"Waring: {json_object} is not a valid json file, not data for download provided!")
        if 'processing' in json_object:
            # TODO
            pass
        else:
            print(f"Waring: {json_object} is not a valid json file, not processing data provided!")
    return downl_obj, processing_obj