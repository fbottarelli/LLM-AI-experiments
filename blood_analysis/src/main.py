from fastapi import FastAPI, HTTPException
from blood_analysis.data_extraction import extract_blood_data, process_images
from pydantic import BaseModel

app = FastAPI()

class ProcessImagesRequest(BaseModel):
    directory: str
    test_name_list: list

@app.post("/process_images")
def api_process_images(request: ProcessImagesRequest):
    try:
        results = process_images(request.directory, request.test_name_list)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)