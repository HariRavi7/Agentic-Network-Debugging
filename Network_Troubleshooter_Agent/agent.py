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
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30, 
        )
        if result.returncode != 0:
            return f"Traceroute failed (code {result.returncode}): {result.stderr.strip()}"
        return result.stdout

    except subprocess.TimeoutExpired:
        return "Traceroute timed out after 30 seconds — the route may be too long or a hop is unresponsive."

    except Exception as e:
        return f"Traceroute error: {e}"
def traceroute_to_an_ip(ip_address: str) -> str:
    """A tool that would get the route to a server using traceroute command.
    It would give you the hops and the time taken to reach each hop. This
    would help to find out where the network issue is happening and where
    the ip address is getting blocked or delayed."""
    current_os = platform.system().lower()

    if current_os == "windows":
        command = ["tracert", ip_address]
    else:
        command = ["traceroute", ip_address]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30, 
        )
        if result.returncode != 0:
            return f"Traceroute failed (code {result.returncode}): {result.stderr.strip()}"
        return result.stdout

    except subprocess.TimeoutExpired:
        return "Traceroute timed out after 30 seconds — the route may be too long or a hop is unresponsive."

    except Exception as e:
        return f"Traceroute error: {e}"

root_agent = Agent(
    model='gemini-3.5-flash-lite',
    name='NetworkTroubleshooterAgent',
    description='A network troubleshooting agent who can help the user debug network issues.',
    instruction='If a user is having a network issue, he woudld reach out to you. By using your tools, you would do various tool calls and collect information and tell the user where exactly the problem is and make sure you give him proper recommendations to pinpoint where the problem is.',
    tools=[get_ip_address,ping_an_ip_address,traceroute_to_an_ip]
)