# sentinel-docker-image
## How to use inside the platform

 ```Python
import digitalhub_core as dh
 ```

  ```Python
  list_args =  ["main.py","{'satelliteType': 'Sentinel1', 'startDate': '2023-12-12', 'endDate': '2023-12-13', 'processingLevel': 'LEVEL1', 'sensorMode': 'IW', 'productType': 'SLC', 'geometry': 'POLYGON((10.98014831542969 45.455314263477874,11.030273437500002 45.44808893044964,10.99937438964844 45.42014226680115,10.953025817871096 45.435803739956725,10.98014831542969 45.455314263477874))', 'area_sampling': 'False', 'user': '','password':''}"]
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