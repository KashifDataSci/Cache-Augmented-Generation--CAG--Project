from fastapi import APIRouter, UploadFile, File, HTTPException, Query 
import uuid as uuid_pkg
import os
import logging 

router = APIRouter()

# Configure basic logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# import the Shared Data Store

from src.data_store import data_store

# PDF processing utility

from src.utils.pdf_processor import extract_text_from_pdf

# LLM client Utility

from src.utils.llm_client import get_llm_responce



# Define temporary directory for uploads

UPLOAD_DIR = "/tmp/cag_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/{uuid}", status_code=201) 
def upload_pdf(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid File type.Only PDF Files are allowed"
        )
    uuid_str = str(uuid)
    if uuid_str in data_store:
        raise HTTPException(
            status_code=400,
            detail=f"UUID {uuid_str} already Exist ,Use PUT api/V1/update/{uuid_str} to modify"
        )

    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_{file.filename}")

    try:
        # Save the uploaded file temporarily

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Extract Text using the utility function
        
        extracted_text = extract_text_from_pdf(file_path)
        if extracted_text is None:
            raise HTTPException(
                status_code=500, detail="Failed to extract text from PDF."
            )
        # Store the Extracted Text
        data_store[uuid_str] = extracted_text
        return {
            "message": "File uploaded and text extracted successfully",
            "uuid": uuid_str
        }
    except Exception as e:
        logging.error(f"Error during PDF upload and processing for UUID {uuid_str}: {e}", exc_info=True) # Log the exception
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file Processing {str(e)}",
        )
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

@router.put("/update/{uuid}")
def update_pdf_data(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type,Only pdfs files are Allowed"
        )
    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404,
            detail=f"UUID {uuid_str} not found,Use POST /api/V1/upload/... "
        )
    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_update_{file.filename}")
    try:
        # Save the uploaded file temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        # Extract Text from the new PDF
        new_text = extract_text_from_pdf(file_path)
        if new_text is None:
            raise HTTPException(
                status_code=500, detail="Failed to extract text from PDF."
            )
        
        data_store[uuid_str] += "\n\n" + new_text
        return {
            "message": f"Data for UUID {uuid_str} updated successfully",
            "uuid": uuid_str
        }
    except Exception as e:
        logging.error(f"Error during PDF update and processing for UUID {uuid_str}: {e}", exc_info=True) # Log the exception
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file Processing {str(e)}",
        )
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

@router.get("/query/{uuid}")
def query_data(uuid: uuid_pkg.UUID, query: str = Query(..., min_length=1)):
    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail=f"UUID {uuid_str} not found ."
        )
    stored_text = data_store[uuid_str]
    llm_responce = get_llm_responce(context=stored_text, query=query)
    return {"uuid": uuid_str, "query": query, "llm_responce": llm_responce}

@router.delete("/data/{uuid}", status_code=200) 
def delete_data(uuid: uuid_pkg.UUID):
    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail=f"UUID {uuid_str} not found ."
        )
    del data_store[uuid_str]
    return {"message": f"Data for UUID {uuid_str} deleted successfully"}

@router.get("/list_uuids")
def list_all_uuids():
    return {"uuids": list(data_store.keys())}