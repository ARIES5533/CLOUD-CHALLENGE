import os
import json
import boto3
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any

# --- Configuration ---

SERVICE_VERSION = os.environ.get("AUX_SERVICE_VERSION", "v0.0.0")

# --- Initialization ---
app = FastAPI(
    title="Auxiliary Service",
    description="Handles secure interactions with AWS services (S3, Parameter Store).",
    version=SERVICE_VERSION
)


SERVICE_VERSION = os.environ.get("AUX_SERVICE_VERSION", "v0.0.0")

REGION = os.environ.get("AWS_REGION", "us-east-1") 

# --- Initialization ---
app = FastAPI(

)
# Initialize AWS Clients: PASS REGION EXPLICITLY
s3_client = boto3.client('s3', region_name=REGION)  
ssm_client = boto3.client('ssm', region_name=REGION) 

# --- Internal Utility Function for Response Formatting ---
def format_response(data: Any) -> Dict[str, Any]:
    """Helper to ensure service versions are included in every response."""
    response = {
        "aux_service_version": SERVICE_VERSION,
        "data": data
    }
    return response

# --- Endpoints ---

@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Basic health check."""
    return format_response({"status": "ok"})

@app.get("/aws/s3/buckets", response_model=Dict[str, Any])
async def list_s3_buckets():
    """Lists all S3 buckets in the AWS account."""
    try:
        response = s3_client.list_buckets()
        bucket_names = [bucket['Name'] for bucket in response.get('Buckets', [])]
        return format_response({"buckets": bucket_names})
    except Exception as e:

        print(f"Error listing S3 buckets: {e}")
        
        raise HTTPException(status_code=500, detail=format_response({"error": "Failed to list S3 buckets due to internal AWS error."}))

@app.get("/aws/ssm/parameters", response_model=Dict[str, Any])
async def list_ssm_parameters():
    """Lists all parameters in AWS Parameter Store."""
    try:
        
        response = ssm_client.describe_parameters()
        parameters = [
            {"Name": param['Name'], "Type": param['Type'], "ARN": param['ARN']}
            for param in response.get('Parameters', [])
        ]
        return format_response({"parameters": parameters})
    except Exception as e:
        print(f"Error listing SSM parameters: {e}")
        raise HTTPException(status_code=500, detail=format_response({"error": "Failed to list SSM parameters."}))

@app.get("/aws/ssm/parameter/{name:path}", response_model=Dict[str, Any])
async def get_ssm_parameter(name: str):
    """Retrieves the value of a specific parameter."""
    try:
        response = ssm_client.get_parameter(
            Name=name,
            WithDecryption=True 
        )
        parameter = response.get('Parameter', {})
        
        return format_response({"name": parameter.get('Name'), "value": parameter.get('Value')})
    except ssm_client.exceptions.ParameterNotFound:
        raise HTTPException(status_code=404, detail=format_response({"error": f"Parameter '{name}' not found."}))
    except Exception as e:
        print(f"Error retrieving parameter '{name}': {e}")
        raise HTTPException(status_code=500, detail=format_response({"error": f"Failed to retrieve parameter '{name}'."}))

