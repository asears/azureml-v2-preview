## Running a DASK job

Before running the sample, the data needs to be copied to the datastore using this [script](src/copy_nyc_taxi.py). This will upload the data to the workspace default blobstorage in the subfolder `nyctaxi`. 

This example shows how a distribted DASK job can be run on multiple nodes of a cluster. In this example we are using 4 nodes using this job yaml. The startup of the cluster is done by the [startDask.py](src/startDask.py) script which launches a scheduler and a worker on the first node of the cluster and a worker on all the other nodes.

For debugging and interactive work, the script also launches a Jupyter server on the first node which can be accessed most easily from a Compute Instance deployed to the same VNet as the Compute Cluster. 

If a --script parameter is provided, then the script will run that script after the cluster has been brought up and the job will be terminated after the script has completed. To start a DASK cluster for interactive work, don't provide a --script parameter, which will have the job run indefinitely (i.e. until you terminate it).

The job below is currently launched as a pytorch job since that gives the full flexibility of assigning the work to the different nodes of the cluster by just checking the $RANK environment variable. In the future we will provide a more generic name for that mode of launching a distributed job.


```yaml
# yaml-language-server: $schema=https://azuremlsdk2.blob.core.windows.net/latest/commandJob.schema.json
code: 
  directory: src
  
command: >-
  python startDask.py
  --datastore {inputs.nyc_taxi_dataset}
  --script batch.py 

environment: 
  conda_file: file:dask-conda.yaml

inputs:
  nyc_taxi_dataset:
    data: 
      datastore: azureml:workspaceblobstore
      directory: /
    mode: mount

compute:
  target: azureml:goazurego
  instance_count: 4

distribution:
  type: pytorch
```



