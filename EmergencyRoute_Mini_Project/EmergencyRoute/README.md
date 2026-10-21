# EmergencyRoute — Emergency Vehicle Route Optimizer

**DAA Mini Project | Python | Streamlit | NetworkX | Matplotlib**

EmergencyRoute is an educational prototype that represents a sample road network as a weighted graph and uses **Dijkstra's shortest-path algorithm** to find a route from an ambulance starting location to a selected hospital. It visualizes the recommended route, estimates distance and travel time, displays an alternative route, and compares simulated traffic scenarios.

> **Safety note:** Locations, distances, and traffic levels are sample data. This is not connected to live GPS or traffic and must not be used for real emergency dispatch.

## Features
- Select an ambulance starting point and destination hospital.
- Choose Low, Moderate, or Heavy simulated traffic.
- Calculate a minimum estimated travel-time route with Dijkstra's algorithm.
- Visualize the road network and highlighted route.
- Display route distance, estimated time, route steps, and an alternative.
- Compare route estimates under different simulated traffic levels.
- Includes algorithm explanation, complexity, limitations, and future scope.

## Technology
- Python
- Streamlit — interactive web interface
- NetworkX — graph representation
- Matplotlib — route visualization

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install packages: `pip install -r requirements.txt`
4. Start the app: `streamlit run app.py`
5. Open the local address Streamlit displays (usually `http://localhost:8501`).

## Dijkstra's algorithm
Each location is a **vertex**, each road is an **edge**, and estimated travel time is the **edge weight**. Dijkstra repeatedly explores the lowest-cost known vertex and updates the costs of its neighbours.

**Time complexity:** `O((V + E) log V)` using an adjacency list and binary heap, where `V` is the number of vertices and `E` is the number of edges.

## Demo plan
1. Choose **Ambulance Base** and **District Hospital**.
2. Compare Low, Moderate, and Heavy traffic.
3. Show the highlighted route and alternative route.
4. Explain vertices, edges, weights, and Dijkstra's complexity in the algorithm tab.

## Repository structure
```text
EmergencyRoute/
├── app.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
└── .gitignore
```

## Limitations and future work
The current road network and traffic values are illustrative. A future version could connect to a verified routing API and live traffic feed, handle road closures, and support map-based location selection. Any real-world use would require validation and safety review.
