# Fog Project

## Overview
The Fog Project is a distributed image processing system that divides an image into parts, processes them in parallel across multiple machines, and combines the results for visualization. Each machine (or node) computes the grayscale matrix for its assigned part of the image, and the combined result is displayed.

## Features
- **Distributed Image Processing:** Distributes image processing tasks to multiple nodes.
- **WebSocket-based Communication:** Uses WebSockets to manage task distribution between nodes.
- **Grayscale Image Processing:** Each node processes its part of the image to compute a grayscale matrix.
- **Combines Results:** Collects processed image parts from all nodes to form the final image.

## Tech Stack
- **Programming Language:** Python
- **Libraries:** OpenCV, NumPy, WebSockets, and other necessary Python libraries
- **Architecture:** Distributed computing using WebSockets

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/medkarim19/Fog_project.git
   cd Fog_project

2. **Set Up Virtual Environment Make sure Python 3.8 (or your chosen version) is installed.**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `.\env\Scripts\activate`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

## Usage

- **Configure Nodes:** Ensure that each node has a running instance of the Fog Project.
- **Start the Main Server:** Run the following command to start the main server responsible for distributing tasks:
  ```bash
   python main_server.py

- **Run the Node Clients:** On each machine (node) that will process a part of the image, run the client script:
   ```bash
  python node_client.py
- **Process an Image:** Upload or specify an image in the main server interface to begin processing. The main server will split the image into smaller parts and distribute them to available nodes for processing.
- - **Combine and Display Results:** Once all nodes complete their assigned tasks, the results are combined to form the final processed image.


## Project Structure
```bash
Fog_project/
│
├── main_server.py          # Main server script for task distribution
├── node_client.py          # Client script for individual nodes
├── image_processing.py     # Image processing functions (grayscale conversion)
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
└── utils/                  # Utility functions and additional scripts



