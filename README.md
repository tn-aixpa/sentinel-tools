# sentinel-docker-image

## How to use inside the platform

 ```Python
import digitalhub_core as dh
 ```

  ```Python
  string_dict_data = "{
    'satelliteType': 'Sentinel1',
    'startDate': '2023-12-12',
    'endDate': '2023-12-13',
    'processingLevel': 'LEVEL1',
    'sensorMode': 'IW',
    'productType': 'SLC',
    'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))',
    'area_sampling': 'False',
    'user': '',
    'password':''
    }"
  list_args =  ["main.py",string_dict_data]
 function = dh.new_function("container-project",name="function_name",kind="container",image="alattaruolo/sentinel-basic:v0.0.8",command="python",args=list_args)
 ```
 the explanation of the list_args second argument  is explained as follow:
 - satelliteType: the type of images the two values accepted are Sentinel1/Senitnel2 
 - startDate: the starting date from where to start downloading the images
 - endDate: the ending date from where to start downloading the images
 - processingLevel: this is the processing level. The values accepted are: [TODO]
 - sensorMode: the mode of sensor: The values accepted are: [TODO]
 - productType: the product type of the image. The values accepted are: [TODO]
 - geometry: this is a geometry in the format WKT. It is possible to create a WKT POLYGON using the following website https://wktmap.com/
 - area_sampling: this should be setted to true when we want the preprocessing of the data downloaded
 - user: user for esa credentials
 - password: password for esa credentials

  ```Python
 run = function.run(action="job",
volumes=[{
    "volume_type": "persistent_volume_claim",
    "name": "volume",
    "mount_path": "/files",
    "spec": {
        "claim_name": "test-sentinel"
    }}],)
 ```

 ### HOW to build the image
 ```
 docker build -t IMAGE-NAME .
 ```

With the previous command in the it's possible to create the image, to run the command in the folder where the Dockerfile is present.

```
docker run -v PATH_TO_LOCAL_STORAGE:/files IMAGE-NAME string_dict_data [ENVIRONMENT_VAR]
```
this command is used to test locally the image specifing the local volume which is going to be mounted to /files inside the image, IMAGE_NAME it's the name used during the build, string_dict_data it's the same string showed before in the code. Whith environment var it is possible to insernt in the environment some parameters instead of specifing them on the ENV. This parameter can be passed as:
```
"{
    'PROJECT_NAME':'',
    'S3_ENDPOINT_URL':'',
    'AWS_ACCESS_KEY_ID':'',
    'AWS_SECRET_ACCESS_KEY':'',
    'S3_BUCKET_NAME': 'prova',
    'DIGITALHUB_CORE_ENDPOINT':'', 
    'CDSETOOL_ESA_USER':'',
    'CDSETOOL_ESA_PASSWORD':''
    }
```
Those are parameters used in the digitalhub_core, CDSETOOL_ESA_USER and CDSETOOL_ESA_PASSWORD are also passed on the string_dict_data as user and password, later it will only be possible to pass through ENV.

```
docker tag IMAGE-NAME alattaruolo/sentinel-basic:v?.?.?
docker push alattaruolo/sentinel-basic:v?.?.?
```

Tagging the image and making it public.