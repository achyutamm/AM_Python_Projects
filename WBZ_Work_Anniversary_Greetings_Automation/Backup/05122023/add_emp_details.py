from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from gridfs import GridFS
from datetime import datetime

app = FastAPI()

# Serve static files like CSS and images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Connect to MongoDB
client = MongoClient("mongodb+srv://achyutammehta:7WvgmzWySS2wCLin@workannivcluster.cbvgni6.mongodb.net/?retryWrites=true&w=majority")
db = client["WorkAnnivDataHub"]
fs = GridFS(db, collection="images")

# Set up templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/add_emp_data_form", response_class=HTMLResponse)
async def show_add_data_form(request: Request):
    return templates.TemplateResponse("add_emp_details.html", {"request": request})


@app.post("/add_data")
async def add_data(
    employee_name: str = Form(...),
    work_anniversary: str = Form(...),
    image_path: str = Form(...),  # Update: Use text input for image_path
):
    try:
        # Save the image to GridFS
        # In a real-world scenario, you might want to handle file uploads for images
        # Since your HTML form uses a text input for image_path, adjust this logic accordingly
        image_id = fs.put(b"", filename=f"{employee_name}_{datetime.now()}.jpg")

        # Add employee details to MongoDB collection
        employee_details = {
            "employee_name": employee_name,
            "work_anniversary": work_anniversary,
            "image_id": image_id,
        }
        db.EmployeeAnniversaryRecords.insert_one(employee_details)

        return {"message": "Data added successfully!"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
