# EmergencyRoute — Mini Project Report

## 1. Title
**EmergencyRoute: Emergency Vehicle Route Optimizer Using Dijkstra's Algorithm**

## 2. Abstract
Emergency situations require an ambulance to reach a hospital efficiently. EmergencyRoute is a Python-based educational application that models a small road network as a weighted graph. It uses Dijkstra's shortest-path algorithm to calculate a route with the lowest estimated travel time. The application visualizes the selected route, displays its distance and estimated time, and compares simulated traffic scenarios. Streamlit provides the interface, while NetworkX and Matplotlib support graph handling and visualization. The road network and traffic values are sample data, so this is a prototype rather than a live emergency navigation service.

## 3. Problem Statement
A road network may contain multiple possible paths between an ambulance and a hospital. The shortest-distance route may not always have the lowest estimated travel time. This project models roads and junctions as a weighted graph and calculates a minimum-cost route using estimated travel time as the edge weight.

## 4. Objectives
- Represent road locations as vertices and roads as weighted edges.
- Implement Dijkstra's shortest-path algorithm.
- Display the recommended route and its statistics.
- Compare estimates under different simulated traffic levels.
- Explain time complexity and practical limitations.

## 5. Tools and Technologies
- Language: Python
- Interface: Streamlit
- Graph library: NetworkX
- Visualization: Matplotlib
- Algorithm: Dijkstra's shortest-path algorithm

## 6. Methodology
The sample road network is stored as a graph. Each road has a distance and base travel-time value. A traffic scenario applies an illustrative multiplier to the base time. Dijkstra's algorithm calculates the path with the lowest total estimated travel time from the selected start location to the destination hospital. The application reconstructs the route and sums distance and time across its roads. It also finds an alternative simple route and displays the road network with the recommended path highlighted.

## 7. Algorithm
1. Set the starting vertex distance to zero.
2. Set every other vertex distance to infinity.
3. Insert the source into a priority queue.
4. Remove the vertex with the smallest current cost.
5. For each neighbour, calculate the cost through the current vertex.
6. If the new cost is smaller, update the neighbour's cost and previous vertex.
7. Continue until the destination is reached or the queue is empty.
8. Reconstruct the route using the previous vertices.

## 8. Complexity Analysis
Using an adjacency list and a binary-heap priority queue, Dijkstra's algorithm has a time complexity of **O((V + E) log V)**. Here, V is the number of vertices and E is the number of edges. Graph and route-tracking structures require **O(V + E)** space.

## 9. Expected Output
- Recommended route between selected start and hospital.
- Total route distance in kilometres.
- Estimated travel time in minutes.
- A graph with the route highlighted.
- An alternative route and traffic-scenario comparison.

## 10. Limitations
The application uses fictional sample locations and simulated traffic. It does not connect to GPS, live traffic, road-closure feeds, or emergency services. Results are for algorithm demonstration only.

## 11. Future Scope
The project could be extended with a verified mapping/routing API, live traffic feeds, multiple hospitals, road-closure handling, and map-based location input. Real-world use would require reliable data, validation, and safety review.

## 12. Conclusion
EmergencyRoute demonstrates a practical application of graph modelling and Dijkstra's shortest-path algorithm. It provides an interactive way to observe how edge weights influence route selection and connects DAA concepts with a real-world-inspired problem.
