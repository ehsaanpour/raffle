import os
import http.server
import socketserver
import webbrowser
import random
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote

# Create necessary directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
TEMPLATES_DIR = BASE_DIR / "templates"

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Global variable to store participants
participants = []

class RaffleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(TEMPLATES_DIR / 'index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/display':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(TEMPLATES_DIR / 'display.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/participants':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'participants': participants}).encode())
        else:
            # Handle static files and other paths
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        global participants

        if self.path == '/draw':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            print(f"Draw request received. Data: {post_data}")
            print(f"Parsed params: {params}")
            print(f"Current participants: {participants}")
            
            if not participants:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False, 
                    'message': 'هیچ شرکت‌کننده‌ای یافت نشد'
                }).encode())
                return
                
            count = 1
            if 'count' in params:
                try:
                    count = int(params['count'][0])
                except ValueError:
                    count = 1
                    
            if count > len(participants):
                count = len(participants)
                
            winners = random.sample(participants, count)
            
            response_data = {
                'success': True,
                'winners': winners,
                'animation_participants': random.sample(participants, min(20, len(participants)))
            }
            
            print(f"Selected winners: {winners}")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        elif self.path.startswith('/upload'):
            # Get content length
            content_length = int(self.headers['Content-Length'])
            if content_length > 0:
                # Handle actual file upload (if implemented)
                print("File upload attempted but not fully implemented in simple server")
            
            # For testing, let's load the sample CSV if it exists
            sample_path = UPLOAD_DIR / 'sample_participants.csv'
            if os.path.exists(sample_path):
                try:
                    with open(sample_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Skip header row
                    if len(lines) > 1:
                        header = lines[0].strip().split(',')
                        phone_column = -1
                        for i, col in enumerate(header):
                            if any(keyword in col.lower() for keyword in ['phone', 'mobile', 'شماره', 'موبایل', 'تلفن']):
                                phone_column = i
                                break
                        
                        if phone_column >= 0:
                            participants = []
                            for i in range(1, len(lines)):
                                row = lines[i].strip().split(',')
                                if len(row) > phone_column:
                                    phone = row[phone_column].replace(' ', '').replace('-', '')
                                    participants.append(phone)
                            
                            print(f"Loaded {len(participants)} participants from sample CSV")
                            
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({
                                'success': True,
                                'message': f"{len(participants)} شماره تلفن یافت شد",
                                'participants': participants
                            }).encode())
                            return
                except Exception as e:
                    print(f"Error reading sample CSV: {str(e)}")
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'success': False,
                        'message': f"خطا در خواندن فایل: {str(e)}"
                    }).encode())
                    return
            
            # If we get here, either the sample file doesn't exist or we couldn't read it
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'message': 'لطفا ابتدا با اجرای make_sample_csv.py یک فایل نمونه بسازید.'
            }).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

if __name__ == "__main__":
    PORT = 8000
    
    print(f"Starting simple Raffle server on port {PORT}...")
    print("This is a basic implementation with limited functionality.")
    print("For full features, use the FastAPI version with 'python app.py'")
    
    # Generate some sample participants if none exist
    if not participants:
        for i in range(10):
            participants.append(f"0912{random.randint(1000000, 9999999)}")
        print(f"Generated {len(participants)} sample participants")
    
    # Create a simple server with our handler
    with socketserver.TCPServer(("", PORT), RaffleHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print("Opening browser...")
        webbrowser.open(f"http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.") 