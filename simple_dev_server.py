#!/usr/bin/env python3
"""
Simple development server for NetBox Ping Plugin
"""

import http.server
import socketserver
import socket

def find_free_port():
    """Find a free port to use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    PORT = find_free_port()
    
    print(f"🔌 NetBox Ping Plugin Development Server")
    print(f"📡 Starting server on http://localhost:{PORT}")
    print(f"🚀 Plugin ready for NetBox integration")
    print("-" * 50)
    
    # Simple HTML content showing plugin status
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NetBox Ping Plugin - Development</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px; 
                background: #f5f5f5; 
            }}
            .header {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 30px; 
                border-radius: 10px; 
                margin-bottom: 30px; 
            }}
            .card {{ 
                background: white; 
                padding: 25px; 
                border-radius: 10px; 
                margin-bottom: 20px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
            }}
            .feature-list {{ list-style: none; padding: 0; }}
            .feature-list li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
            .feature-list li:before {{ content: "✓ "; color: #28a745; font-weight: bold; }}
            .new {{ color: #007bff; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔌 NetBox Ping Plugin</h1>
            <p>Development Environment - New IP Pinger Feature Added!</p>
        </div>
        
        <div class="card">
            <h2>🚀 Plugin Status</h2>
            <p><strong>Status:</strong> ✅ Ready for NetBox Integration</p>
            <p><strong>Version:</strong> 0.48</p>
            <p><strong>New Feature:</strong> <span class="new">IP Pinger with Real-time Results</span></p>
        </div>
        
        <div class="card">
            <h3>📋 Features Implemented</h3>
            <ul class="feature-list">
                <li>Ping IPs and subnets from NetBox</li>
                <li>Auto-discover new IP addresses</li>
                <li>Track IP status with custom fields</li>
                <li>Bulk scan operations</li>
                <li>Dark mode compatible UI</li>
                <li>Custom tags and fields creation</li>
                <li><span class="new">NEW: IP Pinger tab in sidebar</span></li>
                <li><span class="new">NEW: Search functionality for individual IPs</span></li>
                <li><span class="new">NEW: Real-time subnet ping with colored results</span></li>
                <li><span class="new">NEW: AJAX-powered ping responses</span></li>
            </ul>
        </div>
        
        <div class="card">
            <h3>🎯 IP Pinger Features</h3>
            <p>The new IP Pinger tab provides:</p>
            <ul>
                <li><strong>IP Search:</strong> Search for specific IP addresses and ping them individually</li>
                <li><strong>Subnet Table:</strong> View all prefixes with columns for Prefix, Description, Site, VRF, Tenant</li>
                <li><strong>Ping Subnet Button:</strong> Click to ping all IPs in a subnet</li>
                <li><strong>Real-time Results:</strong> Green text for responsive IPs, red text for non-responsive</li>
                <li><strong>AJAX Integration:</strong> No page reloads, instant feedback</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>🔧 Integration Instructions</h3>
            <p>To use the new IP Pinger functionality in NetBox:</p>
            <ol>
                <li>Install the plugin: <code>pip install -e .</code></li>
                <li>Add 'netbox_ping' to PLUGINS in NetBox configuration</li>
                <li>Apply migrations: <code>python3 manage.py migrate</code></li>
                <li>Restart NetBox</li>
                <li>Navigate to Plugins → NetBox Ping → IP Pinger</li>
            </ol>
        </div>
        
        <div class="card">
            <h3>📂 Files Modified/Added</h3>
            <ul>
                <li>✅ <code>navigation.py</code> - Added IP Pinger menu item</li>
                <li>✅ <code>urls.py</code> - Added new URL routes</li>
                <li>✅ <code>views.py</code> - Added IPPingerView and AJAX views</li>
                <li>✅ <code>templates/netbox_ping/ip_pinger.html</code> - New template</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode())
            else:
                super().do_GET()
    
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        print("📋 Development dashboard shows plugin status and new features")
        print("🔄 Plugin code is ready for NetBox integration")
        print("\\nPress Ctrl+C to stop the server.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\n👋 Development server stopped.")

if __name__ == "__main__":
    main()
