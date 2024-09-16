from fastapi import APIRouter, HTTPException
from ..services import move_files_between_sftp

sftp_router = APIRouter()

@sftp_router.post('/transfer-file')
def transfer_file(source_file_path: str, destination_file_path: str):
    try:
        move_files_between_sftp(source_file_path, destination_file_path)
        
        return {"message": "File transfer successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))