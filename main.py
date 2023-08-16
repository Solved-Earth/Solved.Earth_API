from typing import Optional, Annotated
from fastapi import FastAPI, File, UploadFile, Body
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pathlib import Path
import datetime
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from yolov5 import detect

from models import User, Photo, UserPhotoLink, Challenge

PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = os.path.join(BASE_DIR,'static/')
IMG_DIR = os.path.join(STATIC_DIR,'images/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','static/','images/')

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_folder(root) -> None:
    try:
        if not os.path.exists(root):
            os.makedirs(root)
    except OSError:
        print("ERROR: Create Folder Failed :"+root)

def challenge_check(photo_location: str, challenge_name:str) -> dict:
    objects:set = detect.run(
        weights=['../yolov5/runs/train/result_trash/weights/best.pt'], 
        source='../'+photo_location, 
        data=os.path.join(PROJECT_DIR, 'yolov5/data/coco128.yaml'), 
        imgsz=[640, 640], conf_thres=0.25, iou_thres=0.45, max_det=1000, device='', 
        view_img=False, save_txt=False, save_conf=False, save_crop=False, 
        nosave=False, classes=None, agnostic_nms=False, augment=False, visualize=False, update=False, 
        project=os.path.join(PROJECT_DIR, 'yolov5/runs/detect'), 
        name='exp', exist_ok=False, line_thickness=3, hide_labels=False, hide_conf=False, half=False, dnn=False, vid_stride=1
    )

    answer:set = ...
    founded = answer.intersection(objects)
    missing = answer.subtraction(objects)
    
    if(missing):
        result = {
            "success":False,
            "reason":"missing values",
            "missing":missing
        }
    elif(founded):
        result = {
            "success":True
        }

    return result

app = FastAPI()

@app.post("/challenge/")
def challenge(user:User, file: UploadFile):
    date = datetime.datetime.now().strftime("%Y-%m-%d")

@app.post('/upload-images')
async def upload_board(username:Annotated[str, Body(embed=True, alias="username")], challenge:Annotated[str, Body(embed=True, alias="challenge")], file:UploadFile):
    root = os.path.join(IMG_DIR, username, challenge)
    create_folder(root)
    
    """ 
    Save Image 
    """
    saved_file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".png"
    file_location = os.path.join(root, saved_file_name)

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    """
    Challenge Chack
    """

    result={
        "success": True,
        "message": {
            
        }
    }
    return result


