from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.parser import parse_brand_kit
import shutil, os
# uncomment this import if enough resources
# from app.llm_evaluator import LLaVAChecker
from app.llm_mock import MockLLaVAChecker  # Use mock instead

# Initialize mock checker
llava_checker = MockLLaVAChecker()

app = FastAPI(title="Brand Compliance API")

# Initialize LLaVA checker if running with enough resources
#llava_checker = LLaVAChecker()

os.makedirs("temp", exist_ok=True)

@app.post("/upload/brand-kit")
async def upload_brand_kit(file: UploadFile = File(...)):
    try:
            brandkit_path = f"temp/{file.filename}"
            with open(brandkit_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            brand_data = parse_brand_kit(brandkit_path)
            os.remove(brandkit_path)  # Cleanup
            
            return JSONResponse(content={
                "status": "success",
                "brand compliance data": brand_data
            })
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Brand kit parsing failed: {str(e)}"
        )


@app.post("/check-compliance")
async def check_compliance(image: UploadFile = File(..., description="Marketing asset image"),
    brand_kit: UploadFile = File(..., description="Brand guidelines PDF")):
    try:
        image_path = f"temp/{image.filename}"
        brandkit_path = f"temp/{brand_kit.filename}"
        
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        with open(brandkit_path, "wb") as buffer:
            shutil.copyfileobj(brand_kit.file, buffer)
        
        
        brand_data = parse_brand_kit(brandkit_path)
        compliance_report = llava_checker.check_compliance(image_path, brand_data)
        
        # Cleanup
        os.remove(image_path)
        os.remove(brandkit_path)
        
        return JSONResponse(content={
            "status": "success",
            "report": compliance_report
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Compliance check failed: {str(e)}"
        )


