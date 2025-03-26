# How to use Sentinel Tools to download images

Sentinel Tools may be used to download and preprocess the Sentinel data from ESA portal.


1. Initialize the project

 ```Python
import digitalhub as dh
# conda install -c conda-forge gdal
PROJECT_NAME = "project_name" # here goes the project name that you are creating on the platform
proj = dh.get_or_create_project(PROJECT_NAME) # source="git://github.com/scc-digitalhu
```

2. Set credentials to access ESA data

```Python
# set esa credentials as secrets
secret0 = proj.new_secret(name="CDSETOOL_ESA_USER", secret_value="put_your_username_esa_credential_here") #credentials esa
secret1 = proj.new_secret(name="CDSETOOL_ESA_PASSWORD", secret_value="put_your_password_esa_credential_here") #credentials esa 

```

3. Define the function to download data with all the specification parameters.

```Python
# for sentinel1:
  "satelliteParams":{
      "satelliteType": "Sentinel1",
      "processingLevel": "LEVEL1", # Select the processing level
      "sensorMode": "IW", # Select the sensor mode
      "productType": "SLC" # Select the product type
  } ,
```

 ```Python
string_dict_data = """{
  "satelliteParams":{
      "satelliteType": "Sentinel1",
      "processingLevel": "LEVEL1",
      "sensorMode": "IW",
      "productType": "SLC"
  } ,
  "startDate": "2023-12-12",
  "endDate": "2023-12-13",
  "geometry": "POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))",
  "area_sampling": "False",
  "artifact_name": "name_for_artifact",
  "s3_path": "s3://{bucket_name}/{project_name}/{path_continuations}",
  "preprocess_data_only": "true"
  }"""
list_args =  ["main.py",string_dict_data]
function = proj.new_function("downoad_images",kind="container",image="ghcr.io/tn-aixpa/sentinel-tools:0.10.0",command="python")
 ```
 the explanation of the list_args second argument  is explained as follow:

 - startDate: the starting date from where to start downloading the images format: yyyy/mm/dd
 - endDate: the ending date from where to start downloading the images format: yyyy/mm/dd
 - geometry: this is a geometry in the format WKT. It is possible to create a WKT POLYGON using the following website https://wktmap.com/ or any of your choise
 - area_sampling: this should be setted to true when we want the preprocessing of the data downloaded as for the coherence or normal difference, when setted this will automatically add some parameters at the query depending from the satelliteType, this means that if you want the coherence this parameters should be true (and the parameters used for sentinel1 are: productType = "SLC", sensorMode = "IW")
 - artifact_name: is the name of the artifact in which it will be uploaded all the data downloaded and preprocessed by the application
 - s3_path: is the path in which you can find inside the s3 the downloaded data this is optional and the deafult path is : {bucket_name}/{project_name}/{artifact_name}/
 - preprocess_data_only: this should be setted to true when only preprocessing of data must be logged as artifact. This is optional flag which by default is
 set to false to log all data (downloaded + preprocess).

4. Execute the operation

The process requires a volume to be createn on Kubernetes. Create a volume (with KRM) as follows:

-  persistent volume claim as disk  readWriteOnce, and 
-  the volume name should be the same as the name passed in claim_name inside the volume in the code below

  ```Python
 run = function.run(action="job",
        secrets=["CDSETOOL_ESA_USER","CDSETOOL_ESA_PASSWORD"],
        fs_group='8877',
        args=list_args,           
        volumes=[{
            "volume_type": "persistent_volume_claim",            
            "name": "volume-sentinel", # this name has to be equal to the name of the volume created in krm
            "mount_path": "/app/files,
            "spec": {
                "claim_name": "volume-sentinel"
  }}])
 ```

 One complete, the run creates the data at the specified path. 
