# FileSearchTCP

**FileSearchTCP** is a high-performance, multi-threaded TCP server designed for fast and efficient string search operations within large text files. The server supports concurrent connections, real-time file updates, and secure communication via SSL. It is optimized for speed and built to function as a Linux service.

## Features

- [x] Multi-threaded TCP Server Handles unlimited concurrent connections.
- [x] Configurable File Path Reads the search file path from a configuration file.
- [x] Efficient String Search Finds exact string matches within large files (up to 250,000 rows).
- [x] Real-time File Updates Optional `REREAD_ON_QUERY` mode for dynamic file changes.
- [x] Optimized Performance Designed for low-latency execution.
- [x] Debug Logging Tracks search queries, IP addresses, execution time, and timestamps.
- [ ] Security Focused Includes buffer overflow protection and SSL authentication.
- [ ] Linux Service Support Runs as a system daemon.

---

## Installation

### Prerequisites

- **Linux-based system**
- **Python 3.8+**
- **OpenSSL** (for SSL support)
- **pip** (Python package manager)

### Clone the Repository

```sh
git clone https://github.com/SymonMuchemi/FileSearchTCP.git
cd FileSearchTCP
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

## Author

👤 **[Symon Muchemi](https://github.com/SymonMuchemi)**
