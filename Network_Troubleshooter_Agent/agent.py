import socket
import subprocess
import platform
from google.adk.agents import Agent

def get_ip_address(domain_name: str) -> dict:
    """Resolves a domain name to all its IP addresses."""
    results = socket.getaddrinfo(domain_name, None)
    ip_addresses = []
    for result in results:
        ip = result[4][0]
        if ip not in ip_addresses:
            ip_addresses.append(ip)
    return {
        "status": "success",
        "ip_addresses": ip_addresses
    }
def ping_an_ip_address(ip_address: str) -> dict:
    """A tool that uses ping with ip addresses to check if connectivity to a server is happening or not. Gives various useful infromation like round trip time, packet loss, etc."""
    current_os = platform.system().lower()
    
    # Windows uses '-n' for packet count; Linux/macOS uses '-c'
    if current_os == "windows":
        command = ["ping", "-n", "3", ip_address]
    else:
        command = ["ping", "-c", "3", ip_address]
        
    try:
        # Run command silently without throwing raw terminal text to screen
        result = str(subprocess.run(command, stdout=subprocess.PIPE, text=True))
        
        # A return code of 0 means the host responded
        return result
    except Exception:
        return False

root_agent = Agent(
    model='gemini-3.5-flash-lite',
    name='root_agent',
    description='A network troubleshooting agent who can help the user debug network issues.',
    instruction='If a user is having a network issue, he woudld reach out to you. By using your tools, you would do various tool calls and collect information and tell the user where exactly the problem is and make sure you give him proper recommendations to pinpoint where the problem is.',
    tools=[get_ip_address,ping_an_ip_address]
)