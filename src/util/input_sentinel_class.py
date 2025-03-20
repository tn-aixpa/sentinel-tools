SENTINEL1 = "Sentinel1"
SENTINEL2 = "Sentinel2"

class Sentinel1Parameters():
    productType:str = None
    sensorMode:str = None
    processingLevel:str = None
    orbitDirection:str = None
    relativeOrbitNumber:str = None

    def __init__(self,productType=None,processingLevel=None,sensorMode=None):
        self.productType = productType
        self.processingLevel = processingLevel
        self.sensorMode = sensorMode

    def embed_parameters_preprocessing_sentienl1(self):
        """ These parameters if we need the preprocessing for sentinel1 need to be with these values"""
        self.productType = 'SLC'
        self.sensorMode = 'IW'
        self.processingLevel = None
    
    def fromJson(self,params):
        if 'processingLevel' in params:
            self.processingLevel = params['processingLevel']
        if 'sensorMode' in params:
            self.sensorMode = params['sensorMode']
        if 'productType' in params:
            self.productType = params['productType']
        if 'orbitDirection' in params:
            self.orbitDirection = params['orbitDirection']
        if 'relativeOrbitNumber' in params:
            self.relativeOrbitNumber = params['relativeOrbitNumber']

class Sentinel2Parameters():
    processingLevel:str = None
    rgb_commands: list = None
    bandmath: list = None
    norm_diff: list = None
    orbitDirection:str = None
    relativeOrbitNumber:str = None
    

    def __init__(self,processingLevel=None):
        self.processingLevel = processingLevel
    
    def embed_parameters_preprocessing_sentienl2(self):
        self.processingLevel =  'S2MSI2A'
    

    def fromJson(self,params):
        if 'processingLevel' in params:
            self.processingLevel = params['processingLevel']
        if 'rgb_commands' in params:
            self.rgb_commands = params['rgb_commands']
            for rgb in self.rgb_commands:
                self.validate_dict(rgb,'rgb')
        else:
            self.rgb_commands = []
        if 'bandmath' in params:
            self.bandmath = params['bandmath']
        else:
            self.bandmath =[]
        if 'norm_diff' in params:
            self.norm_diff = params['norm_diff']
            for norm in self.norm_diff:
                self.validate_dict(norm,'norm_diff')
        else:
            self.norm_diff =[]
        if 'orbitDirection' in params:
            self.orbitDirection = params['orbitDirection']
        if 'relativeOrbitNumber' in params:
            self.relativeOrbitNumber = params['relativeOrbitNumber']
    
    def validate_dict(self,dictio: list,type: str):
        if 'name' not in dictio:
            raise(f'There is a dictionary {dictio} that does not contain the key "name"')
        if 'value' not in dictio:
            raise(f'There is a dictionary {dictio} that does not contain the key "value"')
        if type=='rgb':
            if len(dictio['value']) !=3:
                raise(f'The value provided for {dictio} is invalid! {dictio["value"]} it should have length equal to 3!!')
        elif type=='norm_diff':
            if len(dictio['value']) !=2:
                raise(f'The value provided for {dictio} is invalid! {dictio["value"]} it should have length equal to 2!!')
            
        
class InputSentinelClass():
    satelliteType:str = None 
    startDate:str = None
    endDate:str = None
    geometry:str = None
    artifact_name:str = None
    s3_path:str = None
    user:str = None
    password:str = None
    area_sampling:bool = None
    tmp_path_same_folder_dwl: bool = False
    orbitDirection:str = None
    relativeOrbitNumber:str=None
    sortOrder:str = 'asc'
    sortParam:str = 'startDate'
    sentinel1Param : Sentinel1Parameters = None
    sentinel2Param : Sentinel2Parameters = None
    cloudCover:str = "[0,10]",
    preprocess_data_only:bool = None


    def __init__(self,json_input,user=None,password=None) -> None:
        if 'satelliteParams' in json_input:
            params = json_input['satelliteParams']
            if 'satelliteType' in params:
                self.satelliteType = params['satelliteType'].capitalize()
            else:
                raise Exception("There is no satelliteType in the params please specify for Sentinel1 or Sentinel2")
            if self.satelliteType == SENTINEL1:
                self.sentinel1Param = Sentinel1Parameters()
                self.sentinel1Param.fromJson(params)
            elif self.satelliteType == SENTINEL2:
                self.sentinel2Param = Sentinel2Parameters()
                self.sentinel2Param.fromJson(params)
            else:
                raise Exception("SatelliteType provided not recognized. Please insert one between 'sentinel1' or 'sentinel2'")
        if 'startDate' in json_input:
            self.startDate = json_input['startDate']
        if 'endDate' in json_input:
            self.endDate = json_input['endDate']
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
        else:
            self.area_sampling = False
        if 'tmp_path_same_folder_dwl' in json_input:
            self.tmp_path_same_folder_dwl = json_input['tmp_path_same_folder_dwl'].lower() in ['true','vero','t','yes','v']
        else:
            self.tmp_path_same_folder_dwl = False
        if 'tileId' in json_input:
            self.tileId = json_input['tileId']
        if 'cloudCover' in json_input:
            self.cloudCover = json_input['cloudCover']
        if 'preprocess_data_only' in json_input:
            self.preprocess_data_only = json_input['preprocess_data_only'].lower() in ['true','vero','t','yes','v']
        else:
            self.preprocess_data_only = False
    
    def embed_parameters_preprocessing_sentienl1(self):
        """ These parameters if we need the preprocessing for sentinel1 need to be with these values"""
        self.sentinel1Param.embed_parameters_preprocessing_sentienl1()

    def embed_parameters_preprocessing_sentienl2(self):
        self.sentinel2Param.embed_parameters_preprocessing_sentienl2()
    
    def is_sentinel1(self):
        if self.satelliteType == SENTINEL1:
            return True
        return False

    def is_sentinel2(self):
        if self.satelliteType == SENTINEL2:
            return True
        return False

    def log_preprocess_only(self):
        return self.preprocess_data_only