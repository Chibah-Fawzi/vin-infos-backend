## Description

_Extracts useful information from Vehicle Identification Number (VIN)_

- FastAPI web server that provides VIN decoding via REST API endpoints.
- One can also import it as any other package in your Python code.
- Gives basic and detailed info (when available) about VIN.
- Allows VIN checksum verification.

Additional info available for many vehicles from:

- AvtoVAZ
- Nissan
- Opel
- Renault

## Requirements

- Python 3.10+
- `fastapi` package for web server
- `uvicorn` package for ASGI server

## Usage

### Web API

Install the required packages:

```bash
pip install fastapi uvicorn
pip install vininfo
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`

#### API Endpoints

**Get VIN information:**

```bash
GET /vin/{vin_number}
```

Example:

```bash
curl http://localhost:8000/vin/XTAGFK330JY144213
```

Response:

```json
{
  "basic": {
    "Country": "USSR/CIS",
    "Manufacturer": "AvtoVAZ",
    "Region": "Europe",
    "Years": "2018, 1988"
  },
  "details": {
    "Body": "Station Wagon, 5-Door",
    "Engine": "21179",
    "Model": "Vesta",
    "Plant": "Izhevsk",
    "Serial": "144213",
    "Transmission": "Manual Renault"
  }
}
```

**Verify VIN checksum:**

```bash
GET /vin/{vin_number}/check
```

Example:

```bash
curl http://localhost:8000/vin/1M8GDM9AXKP042788/check
```

Response:

```json
{
  "valid": true,
  "message": "Checksum is valid"
}
```

### Python Library

You can also use the library directly in your Python code:

```python
from vininfo import Vin

vin = Vin('VF1LM1B0H36666155')

vin.country  # France
vin.manufacturer  # Renault
vin.region  # Europe
vin.wmi  # VF1
vin.vds  # LM1B0H
vin.vis  # 36666155

annotated = vin.annotate()
details = vin.details

vin.verify_checksum()  # False
Vin('1M8GDM9AXKP042788').verify_checksum()  # True
```

## Development

One can add missing WMI(s) using instructions from `dicts/wmi.py`:
`WMI` dictionary, that maps WMI strings to manufacturers.

Those manufacturers may be represented by simple strings, or instances of `Brand`
subclasses (see `brands.py`).

If you know how to decode additional information (model, body, engine, etc.)
encoded in VIN, you may also want to create a so-called `details extractor`
for a brand.

Details extractors are `VinDetails` subclasses in most cases making use of
`Detail` descriptors to represent additional information
(see `details/nissan.py` for example).
