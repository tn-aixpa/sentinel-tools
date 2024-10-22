import sys
from util.cdsetool_handler_burst_mgs import get_query_sentinel1,download_products, get_query_sentinel2
from util.command_execution import CommandExecution
from util.geometry_modifier import get_bursts,get_bust_second,get_mgrs
from util.helper import from_geojson_to_file, from_wkt_to_geojson,get_path_geojson, get_path_geometry_burst,get_path_geometry_mgrs,create_path, remover_all_files_from_directory
from util.input_sentinel_class import InputSentinelClass
from util.preprocess_sentinel_1 import coherence_snap_cmds
from util.preprocess_sentinel_2 import start_executions
from util.skd_handler import create_json_from_env,load_all_artifacts_from_custom, set_environment_var_from_json,set_environment_variable_username_password,get_environment_variable_username_password
from util.cdsetool_handler import from_string_to_json, download_from_object_json

DOWNLOAD_PATH = '/home/mithra/Documents/donwload_sentinel_test/with_notebook' #"files" # "/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/files/demo" # 
PREPROCESS_PATH =  "preprocess" # "/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/files/preprocess" # 

if __name__ == "__main__":
    # ,"gpt assets/s1coherence.xml -Pimage1_fpath=files/S1A_IW_SLC__1SDV_20231124T171520_20231124T171547_051362_0632A5_BE31.SAFE -Pimage2_fpath=files/S1A_IW_SLC__1SDV_20231206T171520_20231206T171547_051537_0638A9_99C8.SAFE -Psubswath=IW3 -Pburst1=4 -Pburst2=4 -Pcoherence_fpath=files/preprocess/demo_work.tif"
    # "wget https://download.esa.int/step/auxdata/dem/SRTM90/tiff/srtm_39_03.zip","gpt assets/s1coherence.xml -Pimage1_fpath=files/S1A_IW_SLC__1SDV_20231124T171520_20231124T171547_051362_0632A5_BE31.SAFE -Pimage2_fpath=files/S1A_IW_SLC__1SDV_20231206T171520_20231206T171547_051537_0638A9_99C8.SAFE -Psubswath=IW3 -Pburst1=4 -Pburst2=4 -Pcoherence_fpath=files/preprocess/demo_work.tif"
    #a = CommandExecution(["echo ciao","ls /usr/local/snap/etc","gpt assets/s1coherence.xml -Pimage1_fpath=files/S1A_IW_SLC__1SDV_20231124T171520_20231124T171547_051362_0632A5_BE31.SAFE -Pimage2_fpath=files/S1A_IW_SLC__1SDV_20231206T171520_20231206T171547_051537_0638A9_99C8.SAFE -Psubswath=IW3 -Pburst1=4 -Pburst2=4 -Pcoherence_fpath=files/preprocess/demo_work.tif"])
    #a.execute()
    corret_form = sys.argv[1].replace("'","\"")
    json_input_download = from_string_to_json(corret_form)
    try:
        # sdk variables passed as argument and added to the environment for testing
        sdk_data = sys.argv[2].replace("'","\"")
        string_json = from_string_to_json(sdk_data)
        set_environment_var_from_json(string_json)
    except Exception as e:
        #if enter here it was not test
        print("You are in production")
        pass
    json_sdk_data = create_json_from_env()
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
            download_parameters.embed_parameters_preprocessing_sentienl1()
            path_geojson = get_path_geojson()
            path_burst = get_path_geometry_burst()
            df = get_bursts(path_geojson,path_burst) #df = get_bust_second() #
            # df = get_bust_second()
            # print(df.columns)
            query_df,features = get_query_sentinel1(df,download_parameters)
            # TODO add "files during production"
            # "/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/files"
            download_products(query_df,DOWNLOAD_PATH,download_parameters.user,download_parameters.password,download_parameters.tmp_path_same_folder_dwl)
            preprocess_path = create_path(DOWNLOAD_PATH,PREPROCESS_PATH) 
            snap_commands = coherence_snap_cmds(query_df,DOWNLOAD_PATH,preprocess_path)
            exectuioner = CommandExecution(snap_commands)
            # print(f"commands: {snap_commands}")
        elif download_parameters.is_sentinel2():
            # sentinel2
            download_parameters.embed_parameters_preprocessing_sentienl2()
            path_geojson = get_path_geojson()
            path_msg = get_path_geometry_mgrs()
            df = get_mgrs(path_geojson,path_msg)
            query_df = get_query_sentinel2(df,download_parameters)
            download_products(query_df,DOWNLOAD_PATH,download_parameters.user,download_parameters.password)
            preprocess_path = create_path(DOWNLOAD_PATH,PREPROCESS_PATH)
            snap_commands = start_executions(download_parameters=download_parameters,products_dir=DOWNLOAD_PATH,output_dir=preprocess_path)
            exectuionenr = CommandExecution(snap_commands)
            exectuionenr.execute()
            print("Command executed")
            # snap_path = os.path.join("assets","s1coherence.xml")
        else:
            print(f"Warning the parameter satelliteType {download_parameters.satelliteType} is not supported!")
    else:
        download_parameters.tmp_path_same_folder_dwl = DOWNLOAD_PATH
        download_from_object_json(download_parameters)
    currentpath_files = DOWNLOAD_PATH
    load_all_artifacts_from_custom(currentpath_files,json_sdk_data,artifact_name=download_parameters.artifact_name,s3_path=download_parameters.s3_path)
    # remover_all_files_from_directory(DOWNLOAD_PATH)
    print("Finished!")


# python3.9 main.py "{'satelliteType': 'Sentinel1', 'startDate': '2023-12-24', 'endDate': '2024-01-04' , 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'SLC', 'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))', 'path': '/media/dsl/1A2226C62D41B5A2/donwload_data/try_script/files', 'area_sampling': 'True'}" "{'PROJECT_NAME':'my_project_sentinel','S3_ENDPOINT_URL':'http://172.17.0.2:9000','AWS_ACCESS_KEY_ID':'ROOTNAME','AWS_SECRET_ACCESS_KEY':'CHANGEME123','S3_BUCKET_NAME': 'prova','DIGITALHUB_CORE_ENDPOINT':''}"
# test query
# python3.9 main.py "{'satelliteType': 'Sentinel1', 'startDate': '2023-12-12', 'endDate': '2023-12-13', 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'SLC', 'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))', 'area_sampling': 'False'}" "{'PROJECT_NAME':'my_project_sentinel','S3_ENDPOINT_URL':'http://172.17.0.2:9000','AWS_ACCESS_KEY_ID':'ROOTNAME','AWS_SECRET_ACCESS_KEY':'CHANGEME123','S3_BUCKET_NAME': 'prova','DIGITALHUB_CORE_ENDPOINT':'', 'CDSETOOL_ESA_USER':'alattaruolo@fbk.eu','CDSETOOL_ESA_PASSWORD':''}"
# end test query 

# python3.9 main.py "{'satelliteType': 'Sentinel1', 'startDate': '2023-12-12', 'endDate': '2023-12-13', 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'SLC', 'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))', 'area_sampling': 'False', 'user': 'alattaruolo@fbk.eu','password':''}"
"""
#environment varible in the run command
sudo docker build -t main-python .
sudo docker run -v /home/mithra/Documents/donwload_sentinel_test/with_notebook/:/files  main-python  "{ 'tmp_path_same_folder_dwl':'True', 'startDate': '2023-12-12', 'endDate': '2023-12-13', 'satelliteParams':{'satelliteType': 'Sentinel1','processingLevel': 'LEVEL1','sensorMode': 'IW','productType': 'SLC'  } ,  'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))','area_sampling': 'True',  'artifact_name': 'directory_name_inside_s3',  's3_path': 's3://{my-bucket}/{path_to_artifact}/'  }" "{'PROJECT_NAME':'my_project_sentinel','S3_ENDPOINT_URL':'http://172.17.0.2:9000','AWS_ACCESS_KEY_ID':'ROOTNAME','AWS_SECRET_ACCESS_KEY':'CHANGEME123','S3_BUCKET_NAME': 'prova','DIGITALHUB_CORE_ENDPOINT':'', 'CDSETOOL_ESA_USER':'alattaruolo@fbk.eu','CDSETOOL_ESA_PASSWORD':''}"
"""