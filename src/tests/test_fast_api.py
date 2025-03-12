import json
from cdsetool.query import query_features
from cdsetool.credentials import Credentials
from cdsetool.download import download_features
from cdsetool.monitor import StatusMonitor
import threading
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager

def execution():
    collection = 'Sentinel1'
    search_terms = {'orbitDirection': 'ASCENDING', 'relativeOrbitNumber': 15, 'geometry': 'POINT(10.637208711454361 45.401959349421986)', 'sortOrder': 'asc', 'sortParam': 'startDate', 'status': 'ONLINE', 'startDate': '2023-12-01T00:00:00.000Z', 'completionDate': '2023-12-13T23:59:59.999Z', 'productType': 'SLC', 'sensorMode': 'IW', 'processingLevel': 'LEVEL1'}
    #query products features
    features = query_features(collection, search_terms)
    credentials = Credentials("","")
    options = {'credentials': credentials, 'concurrency': 4}
    #options = {"tmpdir": products_dir,'credentials': credentials, 'concurrency': 4, 'monitor': StatusMonitor()}
    list(download_features(features, "/home/mithra/Documents/donwload_sentinel_test/", options))


class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        execution()



# class BackgroundTasks(threading.Thread):
#     def run(self,*args,**kwargs):
#         execution()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     execution()

# app = FastAPI(lifespan=lifespan)
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def try_2_start():
    t = BackgroundTasks()
    t.start()

if __name__ == "__main__":   
    uvicorn.run(app, host="0.0.0.0", port=8000)

# sudo docker build -t test-python .
# sudo docker run -v /home/mithra/Documents/donwload_sentinel_test/:/files test-python