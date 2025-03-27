import os
import logging
from datetime import datetime
from pathlib import Path
import subprocess
import signal
import atexit
import time
from typing import List, Dict, Any, Optional

# Configure logging
log_dir = os.path.join(Path.home(), ".doro_logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"social_media_blocks_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# List of social media domains to block
SOCIAL_MEDIA_DOMAINS = [
    "facebook.com", "www.facebook.com", "fb.com", "fbcdn.net", "fbsbx.com", "www.fbsbx.com","gateway.facebook.com",
    "twitter.com", "www.twitter.com", "x.com", "www.x.com",
    "instagram.com", "www.instagram.com",
    "tiktok.com", "www.tiktok.com",
    "reddit.com", "www.reddit.com",
    "linkedin.com", "www.linkedin.com",
    "youtube.com", "www.youtube.com", "youtu.be",
    "pinterest.com", "www.pinterest.com",
    "snapchat.com", "www.snapchat.com",
    "whatsapp.com", "www.whatsapp.com",
    "discord.com", "www.discord.com",
    "twitch.tv", "www.twitch.tv"
]

# Script content for mitmproxy
MITM_SCRIPT_CONTENT = """

from mitmproxy import http
from mitmproxy import ctx

# List of social media domains to block
SOCIAL_MEDIA_DOMAINS = [
    "facebook.com", "www.facebook.com", "fb.com", "fbcdn.net", "fbsbx.com", "www.fbsbx.com","gateway.facebook.com",
    "twitter.com", "www.twitter.com", "x.com", "www.x.com",
    "instagram.com", "www.instagram.com",
    "tiktok.com", "www.tiktok.com",
    "reddit.com", "www.reddit.com",
    "linkedin.com", "www.linkedin.com",
    "youtube.com", "www.youtube.com", "youtu.be",
    "pinterest.com", "www.pinterest.com",
    "snapchat.com", "www.snapchat.com",
    "whatsapp.com", "www.whatsapp.com",
    "discord.com", "www.discord.com",
    "twitch.tv", "www.twitch.tv"
]

def request(flow):
    host = flow.request.pretty_host
    ctx.log.info(f"{host=}")
    # Check if the host is in our list of social media domains
    if any(host.endswith(domain) for domain in SOCIAL_MEDIA_DOMAINS):
        # Log the blocked request
        ctx.log.info(f"Blocked request to {host}: {flow.request.url}")

        # Return a custom response to the client
        flow.response = http.Response.make(
            403,  # Status code
            b"<html><body><h1>Focus Mode Active</h1><p>This site is blocked during your Pomodoro session.</p></body></html>",
            {"Content-Type": "text/html"}
        )

"""

def create_mitm_script():
    """Create a temporary script file for mitmproxy"""
    script_dir = os.path.join(Path.home(), ".doro_scripts")
    os.makedirs(script_dir, exist_ok=True)
    script_path = os.path.join(script_dir, "social_media_blocker.py")
    
    with open(script_path, "w") as f:
        f.write(MITM_SCRIPT_CONTENT)
    
    return script_path


def start_proxy_in_background():
    """Start the proxy in a background process"""
    try:
        # Create the mitmproxy script
        script_path = create_mitm_script()
        
        # Set environment variables for the proxy
        os.environ["HTTP_PROXY"] = "http://127.0.0.1:8080"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8080"
        
        # Start mitmproxy in a separate process
        cmd = ["mitmdump", "-s", script_path, "--listen-port", "8080", "--mode", "local"]

        try:
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Register cleanup function
            atexit.register(lambda: process.terminate() if process.poll() is None else None)
            
            # Wait a bit to ensure the proxy is started
            time.sleep(2)
            
            if process.poll() is not None:
                # Process terminated prematurely
                stdout, stderr = process.communicate()
                logging.error(f"Failed to start proxy: {stderr}")
                return False
                
            logging.info("Proxy started successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error starting proxy: {str(e)}")
            return False
    
    except Exception as e:
        logging.error(f"Error in start_proxy_in_background: {str(e)}")
        return False


def stop_proxy():
    """Stop the proxy and clean up environment variables"""
    # Clean up environment variables
    if "HTTP_PROXY" in os.environ:
        del os.environ["HTTP_PROXY"]
    if "HTTPS_PROXY" in os.environ:
        del os.environ["HTTPS_PROXY"]
    
    # Find and kill any running mitmdump processes
    try:
        subprocess.run(["pkill", "-f", "mitmdump"], check=False)
        logging.info("Proxy stopped")
    except Exception as e:
        logging.error(f"Error stopping proxy: {str(e)}")
