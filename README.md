# ddos-attack-tool (Educational Tool)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Educational](https://img.shields.io/badge/Purpose-Educational-orange)

> **⚠️ IMPORTANT: This tool is for EDUCATIONAL PURPOSES only. Use only on systems you own or have written permission to test.**

## 🎓 What You Can Learn

- How DDoS attacks work internally
- Different attack types (HTTP, SYN, UDP, ICMP)
- Network traffic generation techniques
- Load testing concepts
- How to protect servers against these attacks

## 🎯 Features

- 🌊 **HTTP Flood** - Layer 7 attack simulation
- 📡 **SYN Flood** - Layer 4 half-open connection attack
- 📦 **UDP Flood** - Layer 4 bandwidth consumption
- 🔌 **ICMP Flood** - Ping flood simulation
- 🧵 **Multi-threaded** - Configurable thread count
- 📊 **Real-time Stats** - Live attack statistics
- ⏱️ **Duration Control** - Set attack time limit
- 🎛️ **Target Configuration** - Customizable target and port

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| HTTP Attacks | requests, urllib3 |
| SYN Attacks | scapy |
| UDP/ICMP Attacks | socket, scapy |
| Multi-threading | threading, concurrent.futures |
| Statistics | time, datetime |
