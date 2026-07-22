import socket
import subprocess
import platform
from google.adk.agents import Agent

def get_ip_address(domain_name: str) -> dict:
    """Resolves a domain name to all its IP addresses.
    Inputs:
    A domain name (e.g., 'example.com').
    Outputs:
    An Ip address for the domain name"""
    print("IP resolver tool is running....")
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
    """A tool that uses ping with ip addresses to check if connectivity to a server is happening or not. Gives various useful infromation like round trip time, packet loss, etc.
    Inputs:
    ip_address for doing the ping
    Outputs:
    A dictionary with the status of the ping and the logs obtained from ping command."""
    print("Ping tool is running....")
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
    the ip address is getting blocked or delayed.
    Inputs:
    Ip address for doing traceroute
    Outputs:
    Logs that are obtained from traceroute along with hops and roundtrip time for each packet"""
    print("Traceroute Tool is running.....")
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

def scan_ports_between_specified_range(port_min :int,port_max:int,ip_address:str) -> str:
    """A tool that returns what ports are open and what ports are closed. Helps debug any issues with the ports or a specific service which the user is requesting like ssh maps to port 22 and so on. 
    Inputs:
    port_min: The minimum port number to scan (inclusive).
    port_max: The maximum port number to scan till (inclusive).
    ip_address: The IP address to scan for open ports.
    Outputs: 
    A string containing what ports are open and what ports are closed.
    """
    print("Port Scanner Tool is running....")
    open_ports = []
    closed_ports = []
    
    for i in range(port_min,port_max+1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)  #timeout before attempting
                result = s.connect_ex((ip_address, i))
                if result == 0:
                    print(f"Port {i} is open")
                    open_ports.append(i)
                else:
                    print(f"Port {i} is closed")
                    closed_ports.append(i)
        except Exception as e:
            return f"Traceroute error: {e}"
    return f"Open ports: {open_ports}\nClosed ports: {closed_ports}"

def check_tcp(host: str, port: int, timeout: int = 3) -> bool:
    """
    Check whether a TCP port is reachable.

    This function attempts to establish a TCP connection to the specified
    host and port. If the TCP three-way handshake completes successfully,
    the port is considered open.

    Input:
        host (str): Hostname or IP address of the target.
        port (int): TCP port number to test.
        timeout (int, optional): Connection timeout in seconds. Defaults to 3.

    Output:
        bool:
            True if the TCP connection succeeds.
            False if the port is closed, unreachable, or the connection times out.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False



root_agent = Agent(
    model='gemini-3.5-flash-lite',
    name='NetworkTroubleshooterAgent',
    description='A network troubleshooting agent who can help the users debug network issues.',
    instruction="If a user is having a network issue, he woudld reach out to you. By using your tools, you would do various tool calls and collect information and tell the user where exactly the problem is and make sure you give him proper recommendations to pinpoint where the problem is. # Rules to follow: 1.Make sure that only relevant tool calls with regard to what the user is asking is only being made. No unnecessary tool call are being made.2. Make sure that the output you give is clear and concise with point to point relevant information. and professional so that the user could easily debug the issue.Identify:- Root cause- Most likely cause- Alternative possibilities (if confidence is not high). If the user is asking anything outside networking Reply with I am an AI agent who can assist you with networking tasks only please aske me any network related queries, i would be happy to assist you with it.",
    tools=[get_ip_address,ping_an_ip_address,traceroute_to_an_ip,scan_ports_between_specified_range,check_tcp]
)