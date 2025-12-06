import os
import requests
from fastapi import FastAPI, HTTPException, status
from typing import List, Dict, Any

# --- Configuration ---

MAIN_SERVICE_VERSION = os.environ.get("MAIN_SERVICE_VERSION", "v0.0.0")

AUXILIARY_SERVICE_URL = os.environ.get("AUX_SERVICE_URL", "http://localhost:8001") 

# --- Initialization ---
app = FastAPI(
    title="Main API",
    description="Public-facing API that orchestrates data retrieval from AWS via Auxiliary Service.",
    version=MAIN_SERVICE_VERSION
)

# --- Internal Utility Function for Response Formatting ---
def aggregate_response(aux_response: Dict[str, Any]) -> Dict[str, Any]:
    """Combines Main API version and data from Auxiliary Service."""

    response = {
        "main_api_version": MAIN_SERVICE_VERSION,
        "aux_service_version": aux_response.get("aux_service_version", "unknown"),
        "data": aux_response.get("data", {})
    }
    return response

# --- Endpoints ---

@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Basic health check."""
    return aggregate_response({"aux_service_version": "N/A", "data": {"status": "ok", "message": "Main API is running."}})

@app.get("/s3/buckets", response_model=Dict[str, Any])
async def list_all_s3_buckets():
    """Lists all S3 buckets via Auxiliary Service."""
    endpoint = f"{AUXILIARY_SERVICE_URL}/aws/s3/buckets"
    try:
        response = requests.get(endpoint)
        response.raise_for_status() 
        aux_data = response.json()
        return aggregate_response(aux_data)
    except requests.exceptions.RequestException as e:
        
        print(f"Error connecting to Auxiliary Service at {endpoint}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"main_api_version": MAIN_SERVICE_VERSION, "error": f"Auxiliary Service connection failed: {e}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"main_api_version": MAIN_SERVICE_VERSION, "error": f"An unexpected error occurred: {e}"}
        )

@app.get("/aws/parameters", response_model=Dict[str, Any])
async def list_all_ssm_parameters():
    """Lists all parameters in AWS Parameter Store via Auxiliary Service."""
    endpoint = f"{AUXILIARY_SERVICE_URL}/aws/ssm/parameters"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        aux_data = response.json()
        return aggregate_response(aux_data)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Auxiliary Service at {endpoint}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"main_api_version": MAIN_SERVICE_VERSION, "error": "Auxiliary Service connection failed."}
        )

@app.get("/aws/parameter/{name:path}", response_model=Dict[str, Any])
async def retrieve_specific_ssm_parameter(name: str):
    """Retrieves the value of a specific parameter via Auxiliary Service."""
    endpoint = f"{AUXILIARY_SERVICE_URL}/aws/ssm/parameter/{name}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        aux_data = response.json()
        return aggregate_response(aux_data)
    except requests.exceptions.HTTPError as e:
       
        if e.response.status_code == 404:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.response.json()
            )
        
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"main_api_version": MAIN_SERVICE_VERSION, "error": "Auxiliary Service returned an error."}
        )
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Auxiliary Service at {endpoint}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"main_api_version": MAIN_SERVICE_VERSION, "error": "Auxiliary Service connection failed."}
        )