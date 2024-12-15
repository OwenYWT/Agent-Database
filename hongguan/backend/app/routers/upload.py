from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.data_processing import DataProcessor
from app.utils.security import authenticate_user

router = APIRouter()
data_processor = DataProcessor()

# @router.post('/api/upload')
# async def upload_file(
#     file: UploadFile = File(...),
#     user=Depends(authenticate_user)  # 身份验证依赖
# ):
#     try:
#         contents = await file.read()
#         saved_path = data_processor.save_file(file.filename, contents)
#         return {"filename": file.filename, "message": "文件上传并处理成功"}
#     except Exception as e:
#         logger.error(f"文件上传失败: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.post('/api/upload')
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        saved_path = data_processor.save_file(file.filename, contents)
        return {"filename": file.filename, "message": "文件上传并处理成功"}
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")
