def get_bursts(geom_path: str, burst_path: str):
    """
    sentinel 1
    Returns a GeoDataFrame of the bursts footprints that intersect with the input geometry with associated SAR-MPC Burst ID maps metadata

    """
    import geopandas as gpd    
    #centroid in EPSG:4326 is not accurate, but accurate enough for point-based query
    import warnings
    warnings.simplefilter(action='ignore',category=UserWarning)
    
    #read input files
    print('Reading input geometry: {}'.format(geom_path))
    geometry_df = gpd.read_file(geom_path)
    print('Reading burst ID database...')
    burstid_df = gpd.read_file(burst_path)
    #intersect geometry with bursts
    print('Finding intersecting bursts...')
    idx = burstid_df.intersects(geometry_df.iloc[0]['geometry'])
    #get elements
    df = burstid_df.loc[idx==True].copy()
    try:
        temp = df.drop(columns=['level_0', 'level_1'])
        df = temp
    except:
        pass
    df = df.reset_index(drop=True)
    print('Converting query coordinates...')
    #get center coordinates and format for esa query: invert lat/long and build string 
    df['esaquerypoint'] = df.centroid.apply(lambda point: "POINT({} {})".format(point.x, point.y))
    # df.to_file('data/dataframe.shp') #TODO remove this later
    # input("....")  
    return df

def get_bust_second():
    import geopandas as gpd
    return gpd.read_file("data/dataframe.shp")

def get_mgrs(geom_path: str, mgrs_path: str):
    """
    sentinel 2
    Returns a GeoDataFrame of the mgrs footprints that intersect with the input geometry with associated metadata fro download @esa-scihub.

    """
    import geopandas as gpd
    #read input files
    print('Reading input geometry: {}'.format(geom_path))
    geometry_df = gpd.read_file(geom_path)
    print('Reading MGRS database...')
    mgrs_df = gpd.read_file(mgrs_path)
    #intersect geometry with bursts
    print('Finding intersecting bursts...')
    idx = mgrs_df.intersects(geometry_df.iloc[0]['geometry'])
    #get elements
    df = mgrs_df.loc[idx==True].copy()
    df.reset_index(inplace=True)
    return df