# Sentinel Tool Usage

 - First create a Volume on krm with the volume-name as the name used in the name inside the json of the list of volumes

  ```Python
 run = function.run(action="job",
  volumes=[{
    "volume_type": "persistent_volume_claim",
    "name": "volume-sentinel",
    "mount_path": "/files",
    "spec": {
        "claim_name": "test-sentinel"
    }}],)
 ```

 in this case volume-sentinel, then select the amount of Gb desired. N.B. The capacity of the volum should be large enough to storage the images and the preprocessed images. Consider that for sentinel-1 images one image is around 8 GB and for 2 weeks there could be around 10 images (easily reaching 80GB just for downloads not considering the preprocessed images). So the range of dates should be considered based on the amount of space available when starting downloading images.

- Storage class name: #disk as a parameter
- Access mode: ReadWriteOnce as a parameter


 Once the Volume is created it is possible to use the [Download Sentinel data](./docs/howto/download.md) doocumentation or [Download Sentinel data and prerocessing](./docs/howto/download-preprocess.md)