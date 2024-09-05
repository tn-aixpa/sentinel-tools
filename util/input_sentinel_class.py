class InputSentinelClass():
    satelliteType:str = None 
    startDate:str = None
    endDate:str = None
    processingLevel:str = None
    sensorMode:str = None
    productType:str = None
    geometry:str = None
    artifact_name:str = None
    s3_path:str = None
    user:str = None
    password:str = None
    area_sampling:bool = None
    tmp_path_same_folder_dwl: bool = False
    sortOrder:str = 'asc'
    sortParam:str = 'startDate'
    tileId:str = None #Sentinel2 specific


    def __init__(self,json_input,user=None,password=None) -> None:
        if 'satelliteType' in json_input:
            self.satelliteType = json_input['satelliteType']
        if 'startDate' in json_input:
            self.startDate = json_input['startDate']
        if 'endDate' in json_input:
            self.endDate = json_input['endDate']
        if 'processingLevel' in json_input:
            self.processingLevel = json_input['processingLevel']
        if 'sensorMode' in json_input:
            self.sensorMode = json_input['sensorMode']
        if 'productType' in json_input:
            self.productType = json_input['productType']
        if 'geometry' in json_input:
            self.geometry = json_input['geometry']
        if 'artifact_name' in json_input:
            self.artifact_name = json_input['artifact_name']
        if 's3_path' in json_input:
            self.s3_path = json_input['s3_path']
        if user:
            self.user = user
        if password:
            self.password = password
        if 'area_sampling' in json_input:
            self.area_sampling = json_input['area_sampling'].lower() in ['true','vero','t','yes','v']
        if 'tmp_path_same_folder_dwl' in json_input:
            self.tmp_path_same_folder_dwl = json_input['tmp_path_same_folder_dwl'].lower() in ['true','vero','t','yes','v']
        else:
            self.area_sampling = False
        if 'tileId' in json_input:
            self.tileId = json_input['tileId']
    
    def embed_parameters_preprocessing_sentienl1(self):
        """ These parameters if we need the preprocessing for sentinel1 need to be with these values"""
        self.productType = 'SLC'
        self.sensorMode = 'IW'
        self.processingLevel = None

    def embed_parameters_preprocessing_sentienl2(self):
        pass