from util.input_sentinel_class import InputSentinelClass 

def get_query(df,downl_params: InputSentinelClass):
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
        'relativeOrbitNumber':  int(item['Rel. orbit number'[:10]]),
        'geometry':             item['esaquerypoint'[:10]],
        'sortOrder':            'asc',
        'sortParam':            'startDate',
        'status':               'ONLINE',
        }
        if downl_params.startDate:
            search_terms['startDate'] =qdate1
        if downl_params.endDate:
            search_terms['completionDate'] =qdate2
        if downl_params.productType:
            search_terms['productType'] = downl_params.productType
        if downl_params.sensorMode:
            search_terms['sensorMode'] = downl_params.sensorMode
        if downl_params.processingLevel:
            search_terms['processingLevel'] = downl_params.processingLevel
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

def download_products(df, products_dir, username=str, password=str):
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
    options = {'credentials': credentials, 'concurrency': 4, 'monitor': StatusMonitor()}
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