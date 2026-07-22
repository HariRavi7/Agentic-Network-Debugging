# Agentic Network Debugging

## What is this?

This is an AI powered network troubleshooter that you can talk to just like you would a human network engineer. Instead of having to remember complex command line flags or dig through man pages, you simply describe what network issue you are facing and the agent takes care of the rest.

The agent is built using Google's Agent Development Kit (ADK) and has a set of networking tools at its disposal. It will figure out which tools to use, in what order, and then give you a clear summary of what it found and what you should do next.

## How it works

The core of this project is an intelligent agent called the **NetworkTroubleshooterAgent**. When you tell it something like "I cannot access example.com" or "check if port 22 is open on this server", here is what happens behind the scenes:

1. The agent thinks about what tools it needs to solve your problem
2. It calls one or more tools to gather information
3. It analyses the results
4. It comes back to you with a clear diagnosis and recommended next steps

The agent is smart about this. It will only call the tools that are relevant to your specific issue and will not waste time or resources on unnecessary checks.

## What tools does it have?

The agent comes with five networking tools built right in:

### 1. IP Address Resolver
Takes a domain name like `google.com` and resolves it to all of its IP addresses. This is usually the first step in diagnosing connectivity issues.

### 2. Ping Tool
Pings an IP address to check if the remote server is reachable. It gives you useful information like round trip time and packet loss percentage. If packets are being dropped, you know there is a connectivity problem.

### 3. Traceroute Tool
Maps the entire route from your computer to the target server hop by hop. This is extremely useful when you want to find out exactly where the network is slowing down or where a packet is being blocked.

### 4. Port Scanner
Scans a range of ports on a given IP address and tells you which ones are open and which are closed. If you are wondering whether a specific service like SSH (port 22) or HTTP (port 80) is accessible, this is the tool to use.

### 5. TCP Connectivity Check
A lightweight check to see if a specific TCP port is reachable on a host. It attempts the three way handshake and returns a simple yes or no answer.

## What kind of problems can it solve?

You can use this agent to diagnose all sorts of network issues like:

- A website or server is not accessible
- You are experiencing slow network performance
- You want to check if a specific service is running
- You need to find where a network connection is being blocked
- You want to verify DNS resolution is working correctly
- You need to scan for open ports on a server

The agent will identify the root cause, the most likely cause, and if it is not fully confident, it will mention alternative possibilities too.

## Getting started

### Prerequisites

You will need Python installed on your machine along with the Google ADK package.

### Installation

Clone the repository and install the dependencies:

```
git clone <your-repo-url>
cd Agentic-Network-Debugging
pip install google-adk
```

### Running the agent

The main agent code lives in `Network_Troubleshooter_Agent/agent.py`. You can import and run the agent from your own script or interact with it through the ADK interface.

There is also a standalone tool in `tools/domain_resolver.py` that you can run directly if you just want a quick domain to IP lookup:

```
python tools/domain_resolver.py
```

## Project structure

```
Agentic-Network-Debugging/
├── Network_Troubleshooter_Agent/
│   ├── __init__.py              # Makes the folder a Python package
│   ├── agent.py                 # The main agent with all the tools
│   └── .gitignore
├── tools/
│   └── domain_resolver.py       # A standalone domain resolver utility
├── TODO.md                      # Track what needs to be done next
└── README.md                    # You are here
```

## A note about the tools

The tools in the `tools/` folder are standalone utilities that you can use independently. The domain resolver for example is a clean, reusable function that returns data in a simple format. The agent itself has its own set of tools integrated directly into it, so you do not need to worry about wiring anything up manually.

## Why this approach?

Traditional network debugging involves knowing the right commands, the right flags, and the right sequence of steps. This agent abstracts all of that away. You just tell it what is wrong in plain English and it handles the technical details. It is like having a network engineer sitting right next to you.

