# قرعه‌کشی (Raffle System)

A web-based lottery/raffle system with a Persian UI, designed for Windows environments with dual-monitor support.

## Features

- Import participants from Excel files (.xlsx, .xls) or CSV files
- Beautiful animated interface for audience viewing
- Dual-monitor support (admin interface + audience display)
- Customizable winner selection
- Confetti animations and visual effects
- Full-screen mode for display monitor

## Requirements

- Python 3.8 or higher
- The following Python packages:
  - fastapi
  - uvicorn
  - openpyxl (for Excel files)
  - pandas
  - python-dotenv
  - python-multipart
  - jinja2
  - websockets

## Installation

1. Make sure you have Python 3.8+ installed on your system.

2. Clone this repository:
```
git clone https://github.com/yourusername/raffle.git
cd raffle
```

3. Install the required dependencies:
```
pip install fastapi==0.103.1 uvicorn==0.23.2 openpyxl==3.1.2 pandas==2.1.0 python-dotenv==1.0.0 python-multipart==0.0.6 jinja2==3.1.2 websockets==11.0.3
```

## Project Structure

```
raffle/
│
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── README.md              # This documentation
├── make_sample_csv.py     # Script to generate sample data
│
├── static/                # Static files
│   ├── uploads/           # Uploaded files (Excel/CSV)
│   └── screenshots/       # Screenshots for documentation
│
└── templates/             # HTML templates
    ├── index.html         # Admin interface
    └── display.html       # Display interface for audience
```

## Usage

1. Start the application:
```
python app.py
```

2. Open a web browser and navigate to:
```
http://localhost:8000
```

3. Use the admin interface to:
   - Upload an Excel file or CSV file containing mobile numbers
   - Select the number of winners
   - Draw winners
   - Open the display screen

4. For the audience's view:
   - Click the "نمایش صفحه نمایشگر" button to open the display screen
   - Move this window to your second monitor
   - Click the fullscreen button (bottom right) for the best experience

## Creating a Sample CSV File

To create a sample CSV file with random mobile numbers, run:
```
python make_sample_csv.py
```

This will generate a file in `static/uploads/sample_participants.csv` that you can use for testing.

## File Format

The application automatically detects columns containing phone numbers. The column should have one of these names (case insensitive):
- phone
- mobile
- شماره
- موبایل
- تلفن

Both Excel files (.xlsx, .xls) and CSV files are supported.

## License

This project is licensed under the MIT License.

## Author

Created by Ehsan Ehsanpour

## Screenshots

![Admin Interface](screenshots/admin.png)
![Audience Display](screenshots/display.png) 
