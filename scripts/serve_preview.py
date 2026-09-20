import http.server
import socketserver
import os
import sys

PORT = 8123
WEB_DIR = "/home/user/monorepo/projects/btp-conduite-travaux"
PROJECTS_DIR = "/home/user/monorepo/projects"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Normalize path
        clean_path = path.split('?')[0].split('#')[0]
        
        # If root or direct index
        if clean_path in ['/', '/index.html']:
            return os.path.join(WEB_DIR, 'index.html')
        
        # If /btp-conduite-travaux/...
        if clean_path.startswith('/btp-conduite-travaux/'):
            rel = clean_path[len('/btp-conduite-travaux/'):]
            return os.path.join(WEB_DIR, rel if rel else 'index.html')
            
        # If /preview/btp-conduite-travaux/...
        if clean_path.startswith('/preview/btp-conduite-travaux/'):
            rel = clean_path[len('/preview/btp-conduite-travaux/'):]
            return os.path.join(WEB_DIR, rel if rel else 'index.html')
            
        # If /projects/...
        if clean_path.startswith('/projects/'):
            rel = clean_path[len('/projects/'):]
            return os.path.join(PROJECTS_DIR, rel)
            
        # Default fallback to projects dir or web dir
        cand1 = os.path.join(WEB_DIR, clean_path.lstrip('/'))
        if os.path.exists(cand1):
            return cand1
        cand2 = os.path.join(PROJECTS_DIR, clean_path.lstrip('/'))
        if os.path.exists(cand2):
            return cand2
            
        return os.path.join(WEB_DIR, 'index.html')

    def end_headers(self):
        # Enable CORS and iframe embedding
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('0.0.0.0', PORT), CustomHandler) as httpd:
        print(f"Serving BTP Autonomous Command on 0.0.0.0:{PORT} from {WEB_DIR}")
        sys.stdout.flush()
        httpd.serve_forever()
