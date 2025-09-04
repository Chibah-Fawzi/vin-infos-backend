from fastapi import FastAPI

import click

from vininfo import Vin
app = FastAPI()

import re

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:3000/*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/show/{vin}")
def read_item(vin: str):
    
    vin_pattern = r'^[A-HJ-NPR-Z0-9]{17}$'
    if re.fullmatch(vin_pattern, vin, re.IGNORECASE):
        """Show information for VIN"""
        num = Vin(vin)
        basic = {}
        details= {}
        def out(annotatable):
            for k, v in annotatable.annotate().items():
                basic[k] = v
            return basic
        
        out(num)

        details = num.details
        if details:
            return {"vin": vin, "details": out(details), "success":True}
        else:
            return {"vin": vin, "details": basic, "success":False}
    else:
        return {"vin": vin, "basic": "VIN is not valid", "success":False}
    