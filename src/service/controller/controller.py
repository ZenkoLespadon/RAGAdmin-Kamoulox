from fastapi import FastAPI

import torch

from handling_request import handling_request

torch.set_num_threads(24)

modelPath = "./Meta-Llama-3.1-8B-Instruct"

app = FastAPI()

@app.get("/")
def index():
    return {"data":"bonjour bienvenu sur ragadmin"}

@app.post("/{req}")
def requete(req, context):
    req_handled = handling_request(req, modelPath, context)
    return {"data":req_handled}
