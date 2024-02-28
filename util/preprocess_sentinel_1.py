from collections import OrderedDict
import geopandas as gpd

from util.helper import get_path_snap_coherence

# from util.command_execution import CommandExecution

def coherence_snap_cmds(df, products_dir, output_dir):
    """
    Append to the GeoDataFrame the associated SNAP command strings. It requires reading .xml annotation in the 'products_dir' folder, thus products must be already downloaded. 
    
    :param df:               GeoDataFrame ('Name' is the only required field in df)
    :param products_dir:     Fulldirpath to the directory where Sentinel-1 products are downloaded
    :param output_dir:       Fulldirpath to the directory where coherence files should be saved (SNAP processing)
    :param snap_graph_path:  Fullfilepath to the SNAP graph file: s1coherence.xml (mazanetti@fbk.eu)
    
    """

    import xml.etree.ElementTree as et
    import zipfile
    import re
    import os
    
    #get SNAP cmd lines for each burst
    snap = {}
    snap_graph_path = get_path_snap_coherence()
    # 'Name' is the only required field in df
    #collect all products with the same 'Name' (e.g., 015_030341_IW3: orbit number, burst ID, swath number)
    names = df['Name'].unique()
    #iterate over 'Name' unique instances
    for name in names:
      #get products for this name
      df_temp = df.loc[df['Name']==name]
      #initialize arrays
      subswath = name[-1]
      idx = []
      img = []
      #read .xml annotation files to get local burst IDs
      for i,product in df_temp.iterrows():
        #fullpath to product .zip archive
        prod_fpath = os.path.join(products_dir,product['properties']['title']).replace('.SAFE','.zip')
        #open product .zip archive in read mode
        try:
          archive = zipfile.ZipFile(prod_fpath, 'r')
        except:
          print('Product: {} does not exists, cannot read annotation file'.format(prod_fpath))
        #build annotation .xml fullpath
        filename = product['properties']['title']
        annotation = 'annotation/s1[ab]-iw{}'.format(subswath) + '-slc-vh-(\d{8})t(\d{6})-(\d{8})t(\d{6})-(\d{6})-(.{6})-(\d{3}).xml'
        pattern = os.path.join(filename,annotation)
        #list files in .zip archive
        filelist = archive.namelist()
        xml = None
        for fname in filelist:
          #match the annotation .xml
          y = re.search(pattern,fname)
          if y is not None:
            #read annotation .xml from within .zip archive
            xml = archive.read(fname)
            break
        if xml != None:
          #parse .xml annotation
          element = et.fromstring(xml)
          #get burst IDs 
          ids = [int(burst.find('burstId').text) for burst in element.iter('burst')]
          #find the local burst ID position (1-9)
          try:
            idx_ = ids.index(int(name[4:10]))
          except:
            idx_ = -1
          #store info
          idx.append(idx_)
          img.append(prod_fpath)
      pairs = []
      if len(idx) >0:
        #pairs with -1 (no burst ID position found) are not made
        pairs = [ [k,k+1] if -1 not in idx[k:k+2] else None for k in range(0,len(idx)-1) ]
        #check match and write SNAP cmd lines
      snap_cmd_list = []
      for k in range(0,len(pairs)):
        if pairs[k] is not None:
          im1 = img[pairs[k][0]]
          im2 = img[pairs[k][1]]
          b1  = idx[pairs[k][0]]
          b2  = idx[pairs[k][1]]
          sw  = 'IW'+subswath
          dates = '_'.join((im1[-55:-40],im2[-55:-40]))
          out = os.path.join(output_dir, '{}_{}_B{}{}_MTC.tif'.format(dates,sw,b1,b2))
          snap_cmd = 'gpt {} -Pimage1_fpath={} -Pimage2_fpath={} -Psubswath={} -Pburst1={} -Pburst2={} -Pcoherence_fpath={}'.format(
                      snap_graph_path,
                      im1,
                      im2,
                      sw,
                      b1,
                      b2,
                      out)
      
          #update list
          snap_cmd_list.append(snap_cmd)

      #update list
      snap[name] = snap_cmd_list
  
    return snap


# def execute_commands(df):
#   list_snap_commands = df["snap"]
#   commands_i = []
#   for i in range(len(list_snap_commands)): 
#     for j in range(len(list_snap_commands[i])):
#       exe1 = CommandExecution([])
#       res = exe1.promt_command(list_snap_commands[i][j])

def connect_prod_lists(df_new, df_pre):
    """
    Insert the last product from the the list of products of df_pre as first item into the list of products of df_new

    :param df_new:      GeoDataFrame of the current call @esa-scihub
    :param df_pre:      GeoDataFrame from the previous call @esa-scihub

    """
    import numpy as np
    import copy

    # check dataframes are spatially equivalent
    assert np.all(df_new.Name == df_pre.Name)

    # deep copy (crazy)
    df = gpd.GeoDataFrame(copy.deepcopy(df_new.to_dict()))
    # return df
    # extract last products from df_pre
    the_new_dict_products = []
    for key_,item_ in df_pre['products'].items():
        # item is a dict containing product_key and item
        download_products_per_occurrency = {}
        for k,item in item_.items():
          # print(item)
          if item['last_product']:
              download_products_per_occurrency[k] = {'filename': item['filename'],'last_product':False,"index":1}
        the_new_dict_products.append(download_products_per_occurrency)
    # Copy all elements of the df in the new dict
    i = 0
    for key_,item_ in df['products'].items():
        # item is a dict containing product_key and item
        download_products_per_occurrency = the_new_dict_products[i]
        for k,item in item_.items():
          # print(item)
          download_products_per_occurrency[k] = {'filename': item['filename'],'last_product':item['last_product'],"index":item['index']+1}
        the_new_dict_products[i] = download_products_per_occurrency
        i+=1
    df = df.drop(columns=['products'])
    print(len(the_new_dict_products))
    #input("dasdsd")
    df['products'] = the_new_dict_products
    return df