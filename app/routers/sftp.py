from fastapi import APIRouter, HTTPException
from app.services.file_transfer import move_file_between_sftp

router = APIRouter()

@router.post('/transfer-file')
def transfer_file(source_file_path: str, destination_file_path: str):
    try:
        move_file_between_sftp(source_file_path, destination_file_path)
        
        return {"message": "File transfer successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))