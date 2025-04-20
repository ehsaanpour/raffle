from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import random
import os
import csv
from pathlib import Path

# Optional imports - handle gracefully if not installed
try:
    import uvicorn
except ImportError:
    print("Warning: uvicorn not found. You'll need to run the server using alternative methods.")
    uvicorn = None

# Create necessary directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
TEMPLATES_DIR = BASE_DIR / "templates"

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app = FastAPI(title="قرعه کشی")

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialize templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Global variable to store participants
participants = []

# Generate some sample participants for testing
for i in range(10):
    participants.append(f"0912{random.randint(1000000, 9999999)}")
print(f"Generated {len(participants)} sample participants")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/display", response_class=HTMLResponse)
async def display(request: Request):
    return templates.TemplateResponse("display.html", {"request": request})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global participants
    
    # Save the file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Process file based on extension
    try:
        file_ext = file.filename.lower().split('.')[-1]
        
        if file_ext in ['xlsx', 'xls']:
            # Process Excel file
            try:
                df = pd.read_excel(file_path)
            except Exception as e:
                return JSONResponse(content={"success": False, "message": f"خطا در خواندن فایل اکسل: {str(e)}. لطفا از فایل CSV استفاده کنید."}, status_code=400)
        elif file_ext == 'csv':
            # Process CSV file
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                # Try different encodings if UTF-8 fails
                try:
                    df = pd.read_csv(file_path, encoding='windows-1256')
                except:
                    df = pd.read_csv(file_path, encoding='latin-1')
        else:
            return JSONResponse(content={"success": False, "message": "فرمت فایل پشتیبانی نمی‌شود. فقط Excel و CSV"}, status_code=400)
        
        # Extract phone numbers - assuming the column name is 'phone' or 'mobile'
        phone_columns = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['phone', 'mobile', 'شماره', 'موبایل', 'تلفن'])]
        
        if phone_columns:
            phone_col = phone_columns[0]
            participants = df[phone_col].dropna().astype(str).tolist()
            # Format phone numbers (remove spaces, dashes, etc.)
            participants = [p.replace(' ', '').replace('-', '') for p in participants]
            print(f"Loaded {len(participants)} participants from file")
            return JSONResponse(content={"success": True, "message": f"{len(participants)} شماره تلفن یافت شد", "participants": participants})
        else:
            return JSONResponse(content={"success": False, "message": "ستون شماره تلفن در فایل پیدا نشد"}, status_code=400)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return JSONResponse(content={"success": False, "message": f"خطا در پردازش فایل: {str(e)}"}, status_code=400)

@app.get("/participants")
async def get_participants():
    return {"participants": participants}

@app.post("/draw")
async def draw_winner(count: int = Form(1)):
    print(f"Draw request received. Count: {count}")
    print(f"Current participants: {participants}")
    
    if not participants:
        print("No participants found")
        return JSONResponse(content={"success": False, "message": "هیچ شرکت‌کننده‌ای یافت نشد"}, status_code=400)
    
    if count > len(participants):
        count = len(participants)
    
    winners = random.sample(participants, count)
    print(f"Selected winners: {winners}")
    
    animation_participants = random.sample(participants, min(20, len(participants)))
    response = {
        "success": True,
        "winners": winners,
        "animation_participants": animation_participants
    }
    
    print(f"Sending response: {response}")
    return response

if __name__ == "__main__":
    if uvicorn:
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    else:
        print("Please run this application with: python -m uvicorn app:app --host 0.0.0.0 --port 8000")
        # Alternative option for Windows users
        print("Or simply open another command prompt and run: python -m http.server 8000")
        print("Then open your browser to http://localhost:8000") 