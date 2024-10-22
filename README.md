# sentinel-docker-image

## How to use inside the platform

 ```Python
import digitalhub as dh
# conda install -c conda-forge gdal
PROJECT_NAME = "project_name" # here goes the project name that you are creating on the platform
proj = dh.get_or_create_project(PROJECT_NAME) # source="git://github.com/scc-digitalhu
```

```Python
# set esa credentials as secrets
secret0 = proj.new_secret(name="CDSETOOL_ESA_USER", secret_value="put_your_username_esa_credential_here") #credentials esa
secret1 = proj.new_secret(name="CDSETOOL_ESA_PASSWORD", secret_value="put_your_password_esa_credential_here") #credentials esa 

```

  ```Python
string_dict_data = """{
  'satelliteParams':{
      'satelliteType': 'Sentinel1',
      'processingLevel': 'LEVEL1',
      'sensorMode': 'IW',
      'productType': 'SLC'
  } ,
  'startDate': '2023-12-12',
  'endDate': '2023-12-13',
  'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))',
  'area_sampling': 'False',
  'artifact_name': 'name_for_artifact',
  's3_path': 's3://{bucket_name}/{project_name}/{path_continuations}', 
  }"""
list_args =  ["main.py",string_dict_data]
function = proj.new_function("donwload_images",kind="container",image="alattaruolo/sentinel-basic:v0.0.21",command="python",args=list_args)
 ```
 the explanation of the list_args second argument  is explained as follow:
 - satelliteParams: is a json that takes two different values :
  
```Python
# for sentinel1:
  'satelliteParams':{
      'satelliteType': 'Sentinel1',
      'processingLevel': 'LEVEL1', # Select the processing level
      'sensorMode': 'IW', # Select the sensor mode
      'productType': 'SLC' # Select the product type
  } ,
```
 
  ```Python
  # for sentinel2:
    'satelliteParams':{
      'satelliteType': 'Sentinel2',
      'processingLevel': '', # Select the processing level
      'rgb_commands': [{'name':'elaborations_name','value':['B1','B2','B2']}], # this elaborations are optionals
      'bandmath': ['NDVI','EVI','NDWI','NDSI','NBR'], # this elaborations are optionals
      'norm_diff': [{'name':'elaborations_name','value':['B1','B2'],'name':'elaborations_name','value':['B1','B2']}] # this elaborations are optionals
  } ,
  ```
 - startDate: the starting date from where to start downloading the images format: yyyy/mm/dd
 - endDate: the ending date from where to start downloading the images format: yyyy/mm/dd
 - geometry: this is a geometry in the format WKT. It is possible to create a WKT POLYGON using the following website https://wktmap.com/ or any of your choise
 - area_sampling: this should be setted to true when we want the preprocessing of the data downloaded as for the coherence or normal difference, when setted this will automatically add some parameters at the query depending from the satelliteType, this means that if you want the coherence this parameters should be true (and the parameters used for sentinel1 are: productType = 'SLC', sensorMode = 'IW')
 - artifact_name: is the name of the artifact in which it will be uploaded all the data downloaded and preprocessed by the application
 - s3_path: is the path in which you can find inside the s3 the downloaded data this is optional and the deafult path is : {bucket_name}/{project_name}/


First create a volume inside krm persistent volume claim as disk  readWriteOnce, and the volume name should be the same as the name passed in claim_name inside the volume in the code below


  ```Python
 run = function.run(action="job",
 #envs=[{"name":"CDSETOOL_ESA_USER","value":"alattaruolo@fbk.eu"},{"name":"CDSETOOL_ESA_PASSWORD","value":""}],
volumes=[{
    "volume_type": "persistent_volume_claim",
    "name": "volume-sentinel",
    "mount_path": "/files",
    "spec": {
        "claim_name": "test-sentinel"
    }}],)
 ```

 ### HOW to build the image for testing and deploy in production (N.B. Not needed for jupiter notebook user)
 ```
 sudo docker build -t IMAGE-NAME .
 sudo docker build -t main-python .
 ```

With the previous command in the it's possible to create the image, to run the command in the folder where the Dockerfile is present.



```
docker run -v PATH_TO_LOCAL_STORAGE:/files IMAGE-NAME string_dict_data [ENVIRONMENT_VAR]
sudo docker run -v /media/mithra/DISK/donwload_data:/files alattaruolo/sentinel-basic:v0.0.13 "{'satelliteType': 'Sentinel1','startDate': '2023-12-12','endDate':'2023-12-13',  'processingLevel': 'LEVEL1',  'sensorMode': 'IW',  'productType': 'SLC',  'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))',  'area_sampling': 'False', 'artifact_name': 'directory_name_inside_s3',}" "{    'PROJECT_NAME':'',    'S3_ENDPOINT_URL':'',    'AWS_ACCESS_KEY_ID':'',    'AWS_SECRET_ACCESS_KEY':'',    'S3_BUCKET_NAME': 'prova',    'DIGITALHUB_CORE_ENDPOINT':'',     'CDSETOOL_ESA_USER':'',    'CDSETOOL_ESA_PASSWORD':''    }"
```
this command is used to test locally the image specifing the local volume which is going to be mounted to /files inside the image, IMAGE_NAME it's the name used during the build, string_dict_data it's the same string showed before in the code. Whith environment var it is possible to insernt in the environment some parameters instead of specifing them on the ENV. This parameter can be passed as:
```
"""{
    'PROJECT_NAME':'',
    'S3_ENDPOINT_URL':'',
    'AWS_ACCESS_KEY_ID':'',
    'AWS_SECRET_ACCESS_KEY':'',
    'S3_BUCKET_NAME': 'prova',
    'DIGITALHUB_CORE_ENDPOINT':'', 
    'CDSETOOL_ESA_USER':'',
    'CDSETOOL_ESA_PASSWORD':''
    }"""
```
Those are parameters used in the digitalhub_core, CDSETOOL_ESA_USER and CDSETOOL_ESA_PASSWORD are also passed on the string_dict_data as user and password, later it will only be possible to pass through ENV.

```
sudo docker login
docker tag IMAGE-NAME alattaruolo/sentinel-basic:v?.?.?
docker push alattaruolo/sentinel-basic:v?.?.?
sudo docker tag main-python alattaruolo/sentinel-basic:v0.0.21
sudo docker push alattaruolo/sentinel-basic:v0.0.21
```

Tagging the image and making it public.

```
sudo docker image ls // images
sudo docker image rm __ID__ // delete image
sudo docker ps -a //list all containers
sudo docker rmi alattaruolo/sentinel-basic-new:v0.0.1 //delete image by tags
```
