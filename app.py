import os, sys
import pandas as pd
import certifi
import pymongo

ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url=os.getenv("MONGO_URL_KEY")
print(mongo_db_url)

from mlops.exception import NetworkSecurityException
from mlops.logger import logging
from mlops.pipeline.training_pipeline import TrainingPipeline
from mlops.constants.training_pipeline import *

# FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from mlops.utils.main_utils.utils import load_object
from mlops.utils.ml_utils.model.estimator import NetworkModel

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = client[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# from fastapi.templating import Jinja2Templates
# templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
if __name__=="__main__":
    app_run(app, host="0.0.0.0", port=8000)