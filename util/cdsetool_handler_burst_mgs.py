from util.input_sentinel_class import InputSentinelClass 

def get_query_sentinel1(df,downl_params: InputSentinelClass):
    """
    Append to the GeoDataFrame the query of the products to download @esa-scihub.

    :param df:       GeoDataFrame coming out from get_bursts()
    :param date1:    String isoformat, date from which to start searching for the closest product
    :param date2:    String isoformat, date up to which searching for the closest product

    """
    from cdsetool.query import query_features
    import pandas as pd

    #set dates
    qdate1 = downl_params.startDate+'T00:00:00.000Z'
    qdate2 = downl_params.endDate+'T23:59:59.999Z'

    #iterate over bursts items
    features_list = []
    iter_ = 0
    for index,item in df.iterrows():
        collection = downl_params.satelliteType
        search_terms = {
        'orbitDirection':       item['Orbit pass'],
        'relativeOrbitNumber':  int(item['Rel. orbit number']),
        'geometry':             item['esaquerypoint'],
        'sortOrder':            'asc',
        'sortParam':            'startDate',
        'status':               'ONLINE',
        }
        if downl_params.startDate:
            search_terms['startDate'] =qdate1
        if downl_params.endDate:
            search_terms['completionDate'] =qdate2
        if downl_params.sentinel1Param.productType:
            search_terms['productType'] = downl_params.sentinel1Param.productType
        if downl_params.sentinel1Param.sensorMode:
            search_terms['sensorMode'] = downl_params.sentinel1Param.sensorMode
        if downl_params.sentinel1Param.processingLevel:
            search_terms['processingLevel'] = downl_params.sentinel1Param.processingLevel
        #query products features
        features = query_features(collection, search_terms)
        for f in features:
            f['Name'] = item['Name']
            iter_+=1
            # print(f['properties']['title'])
            # f['Orbit pass'] = item['Orbit pass']
            # f['relativeOrbitNumber'] = int(item['Rel. orbit number'[:10]])
            # f['esaquerypoint'] = item['esaquerypoint'[:10]]
            # if 'Burst ID' in list(df.columns.values):
            #     f['Burst ID'] = item['Burst ID']
            # if 'Subswath name'[:10] in list(df.columns.values):
            #     f['Subswath name'] = item['Subswath name'[:10]]
            features_list.append(f)
    # input(f" {iter_ }...")
    #make dataframe
    df = pd.DataFrame.from_dict(features_list)

    return df,features

def get_query_sentinel2(df, downl_params: InputSentinelClass):
    """
    Append to the GeoDataFrame the query of the products to download @cdse.
    
    :param df:       GeoDataFrame coming out from get_mgrs()
    :param date1:    String isoformat, date from which to start searching for the closest product
    :param date2:    String isoformat, date up to which searching for the closest product
    
    """
    
    from cdsetool.query import query_features
    import pandas as pd
    
    #set dates
    qdate1 = downl_params.startDate+'T00:00:00.000Z'
    qdate2 = downl_params.endDate+'T23:59:59.999Z'
    
    #iterate over mgrs tile items
    features_list = []
    for index,item in df.iterrows():
      collection = 'Sentinel2'
      search_terms = {
        'startDate':        qdate1,
        'completionDate':   qdate2,
        'processingLevel':  'S2MSI2A',
        'tileId':           item['Name'],
        'sortOrder':        'asc',
        'sortParam':        'startDate',
      }
      #query products features
      features = query_features(collection, search_terms)
      for f in features:
        f['tileId'] = item['Name']
        f['relativeOrbitNumber'] = f['properties']['relativeOrbitNumber']
        f['Name'] = 'T{}_R{:03d}'.format(f['tileId'],f['relativeOrbitNumber'])
        features_list.append(f)

    #make dataframe
    df = pd.DataFrame.from_dict(features_list)

    return df

def download_products(df, products_dir, username:str, password:str,tmp_path_same_folder_dwl:bool):
    """
    Consistent download of all products from the DataFrame.

    :param df:           GeoDataFrame coming out from get_query()
    :param products_dir: Fulldirpath to the directory where Sentinel-1 products are downloaded
    :param username:     String username
    :param password:     String password

    """  

    from cdsetool.credentials import Credentials
    from cdsetool.download import download_features
    from cdsetool.monitor import StatusMonitor

    #remove duplicate products
    df = df.drop_duplicates(subset='id',inplace=False)
    #get features as list of dicts
    features_list = df.to_dict(orient='records')
    #istantiate credentials
    credentials = Credentials(username, password)
    #download products
    # iter_ = 0
    # for feature in features_list:
    #     print(feature['properties']['title'])
    #     iter_+=1
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #print(f"features: {features_list}")
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    options = {'credentials': credentials, 'concurrency': 4, 'monitor': StatusMonitor()}
    if tmp_path_same_folder_dwl:
        options['tmpdir'] = products_dir
    #options = {"tmpdir": products_dir,'credentials': credentials, 'concurrency': 4, 'monitor': StatusMonitor()}
    list(download_features(features_list, products_dir, options))
    #downloads are yelded
    # return list(downloads)

def download_products_new(features, products_dir, username=str, password=str):
    """
    Consistent download of all products from the DataFrame.

    :param df:           GeoDataFrame coming out from get_query()
    :param products_dir: Fulldirpath to the directory where Sentinel-1 products are downloaded
    :param username:     String username
    :param password:     String password

    """  

    from cdsetool.credentials import Credentials
    from cdsetool.download import download_features
    from cdsetool.monitor import StatusMonitor

    credentials = Credentials(username, password)
    options = {'credentials': credentials, 'concurrency': 4, 'monitor': StatusMonitor()}
    print(features,products_dir,options,username,password)
    list(download_features(features, products_dir, options))