from azureml.core import Workspace, Experiment
from azureml.train.estimator import Estimator
from azureml.widgets import RunDetails
from azureml.core.runconfig import MpiConfiguration
from azureml.core import VERSION
import uuid
import time
VERSION

ws = Workspace.from_config()

import io
import os
import sys
import urllib.request
from tqdm import tqdm
from time import sleep

cwd = os.getcwd()

data_dir = os.path.abspath(os.path.join(cwd, 'data'))
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

taxidir = os.path.join(data_dir, 'nyctaxi')
if not os.path.exists(taxidir):
    os.makedirs(taxidir)

filenames = []
local_paths = []
for i in range(1, 13):
    filename = "yellow_tripdata_2015-{month:02d}.csv".format(month=i)
    filenames.append(filename)
    
    local_path = os.path.join(taxidir, filename)
    local_paths.append(local_path)

for idx, filename in enumerate(filenames):
    url = "http://dask-data.s3.amazonaws.com/nyc-taxi/2015/" + filename
    print("- Downloading " + url)
    if not os.path.exists(local_paths[idx]):
        with open(local_paths[idx], 'wb') as file:
            with urllib.request.urlopen(url) as resp:
                length = int(resp.getheader('content-length'))
                blocksize = max(4096, length // 100)
                with tqdm(total=length, file=sys.stdout) as pbar:
                    while True:
                        buff = resp.read(blocksize)
                        if not buff:
                            break
                        file.write(buff)
                        pbar.update(len(buff))
    else:
        print("- File already exists locally")

print("- Uploading taxi data... ")
ws = Workspace.from_config()
ds = ws.get_default_datastore()

ds.upload(
    src_dir=taxidir,
    target_path='nyctaxi',
    show_progress=True)

print("- Data transfer complete")