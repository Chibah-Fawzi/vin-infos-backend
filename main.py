from fastapi import FastAPI, HTTPException
from vininfo import Vin
from vininfo.exceptions import ValidationError

app = FastAPI(
    title="VIN Info API",
    description="Extract detailed vehicle information from VIN numbers",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "VIN Info API - Use /vin/{vin_number} to decode VIN"}

@app.get("/vin/{vin_number}")
async def get_vin_info(vin_number: str):
    try:
        vin = Vin(vin_number)
        
        # Get basic information
        basic_info = vin.annotate()
        
        # Get detailed information if available
        details_info = {}
        if vin.details:
            details_info = vin.details.annotate()
        
        return {
            "basic": basic_info,
            "details": details_info
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing VIN: {str(e)}")

@app.get("/vin/{vin_number}/check")
async def check_vin_checksum(vin_number: str):
    try:
        vin = Vin(vin_number)
        is_valid = vin.verify_checksum()
        
        return {
            "valid": is_valid,
            "message": "Checksum is valid" if is_valid else "Checksum is not valid"
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing VIN: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
