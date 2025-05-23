import sys
from util.cdsetool_handler_burst_mgs import get_query_sentinel1,download_products, get_query_sentinel2
from util.command_execution import CommandExecution
from util.geometry_modifier import get_bursts,get_mgrs
from util.helper import from_geojson_to_file, from_wkt_to_geojson,get_path_geojson, get_path_geometry_burst,get_path_geometry_mgrs,create_path
from util.input_sentinel_class import InputSentinelClass
from util.preprocess_sentinel_1 import coherence_snap_cmds
from util.preprocess_sentinel_2 import start_executions
from util.skd_handler import load_all_artifacts_from_custom, get_environment_variable_username_password
from util.cdsetool_handler import from_string_to_json, download_from_object_json

DOWNLOAD_PATH = "files" # "/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/files/demo" # 
PREPROCESS_PATH =  "preprocess" # "/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/files/preprocess" # 

if __name__ == "__main__":
    corret_form = sys.argv[1].replace("'","\"")
    json_input_download = from_string_to_json(corret_form)
    try:
        # sdk variables passed as argument and added to the environment for testing
        sdk_data = sys.argv[2].replace("'","\"")
        string_json = from_string_to_json(sdk_data)
        # set_environment_var_from_json(string_json)
    except Exception as e:
        #if enter here it was not test
        print("You are in production")
        pass
    # set_environment_variable_username_password("","") # TODO remove this and take just the user,password from env
    user,password = get_environment_variable_username_password()
    download_parameters = InputSentinelClass(json_input_download,user=user,password=password)
    if download_parameters.area_sampling:
        """
        Here are executed also the preprocessing of the images
        """
        geoj = from_wkt_to_geojson(download_parameters.geometry)
        from_geojson_to_file(geoj)
        if download_parameters.is_sentinel1():
            # sentinel1
            path_geojson = get_path_geojson()
            path_burst = get_path_geometry_burst()
            df = get_bursts(path_geojson,path_burst)
            query_df,features = get_query_sentinel1(df,download_parameters)
            download_products(query_df, DOWNLOAD_PATH, download_parameters.user, download_parameters.password, download_parameters.tmp_path_same_folder_dwl)
            if (download_parameters.sentinel1Param.productType == 'SLC'):
                download_parameters.embed_parameters_preprocessing_sentienl1()
                preprocess_path = create_path(DOWNLOAD_PATH,PREPROCESS_PATH) 
                snap_commands = coherence_snap_cmds(query_df,DOWNLOAD_PATH,preprocess_path)
                exectuioner = CommandExecution(snap_commands)
                exectuioner.execute()
                print("Command executed")
            else:
                print('preprocess not supported for product type ' + download_parameters.sentinel1Param.productType)
        elif download_parameters.is_sentinel2():
            # sentinel2
            download_parameters.embed_parameters_preprocessing_sentienl2()
            path_geojson = get_path_geojson()
            path_msg = get_path_geometry_mgrs()
            df = get_mgrs(path_geojson,path_msg)
            query_df = get_query_sentinel2(df,download_parameters)
            download_products(query_df, DOWNLOAD_PATH, download_parameters.user, download_parameters.password, download_parameters.tmp_path_same_folder_dwl)
            preprocess_path = create_path(DOWNLOAD_PATH,PREPROCESS_PATH)
            snap_commands = start_executions(download_parameters=download_parameters,products_dir=DOWNLOAD_PATH,output_dir=preprocess_path)
            exectuionenr = CommandExecution(snap_commands)
            exectuionenr.execute()
            print("Command executed")
        else:
            print(f"Warning the parameter satelliteType {download_parameters.satelliteType} is not supported!")
    else:
        download_parameters.tmp_path_same_folder_dwl = DOWNLOAD_PATH
        download_from_object_json(download_parameters)
    
    if (download_parameters.log_preprocess_only()):
        currentpath_files = preprocess_path
        print(f"Logging only preprocess data from {currentpath_files}")
    else:
        currentpath_files = DOWNLOAD_PATH
        print(f"Logging all data (downloaded + preporcess) from {currentpath_files}")
    
    load_all_artifacts_from_custom(currentpath_files,artifact_name=download_parameters.artifact_name)
   
    print("Finished!")
