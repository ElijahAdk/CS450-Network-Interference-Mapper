# CS450-Network-Interference-Mapper

## Official Project Title: Network Interference Mapper 

## Application Category: Environmental Control 

## Project Purpose Statement: 
Interference can be caused by many different problems, which can make it difficult to pinpoint where the issue lies. The Network Interference Mapper aims to assist Network Engineers with this problem by collecting related data via multiple edge devices. These devices pull data from their connected magnetometers for measuring magnetic interference and from iw scans for measuring interference from other devices. Use of this system will allow for quicker network-related troubleshooting. 

## Operational Boundaries:

HMI Pi Role: data aggregation, display, and logging 

Sense HAT Pi Role: magnetometer and iw polled 

Remote Storage / Infrastructure Role: NAS Database 

Optional Additional Nodes: two other Sandbox Table Pis (probably from Table 3 and Table 8) 

Out-of-Scope Boundaries: Features we intend to exclude are creating a web-based application and implementing scalability.

## Functional Requirements:

1. The HMI Pi must have one UDP client socket for each Sense HAT Pi that the HMI Pi will use to send data requests to and receive data reports from each Sense HAT Pi. 

2. The HMI Pi must have one TCP client socket that the HMI Pi will use to communicate with and send data logs to the classroom NAS. 

3. Each Sense HAT Pi must have one UDP server socket that each Sense HAT Pi will use to receive data requests from and send data reports to the HMI Pi.

4. Docker Swarm (running on the HMI Pi) must assign the correct container image to each Pi. 

5. The polling service on the HMI Pi must request data from each Sense HAT Pi's data reporting service. 

6. Each Sense HAT Pi's data reporting service must transmit sensor data to the HMI Pi's data processing service. 

7. The HMI Pi's data processing service must pass processed data to the HMI Pi's data logging service.

8. Each Sense HAT Pi must record Wi-Fi signal strength data from the output of the "iw" Linux command. 

9. Each Sense HAT Pi must record data from its own onboard magnetometer. 

10. Data collection must occur once every minute. 

11. After receiving data from all Sense HAT Pis, the HMI Pi must update its touchscreen UI with the new data before sending the next data request.

12. The HMI Pi must update the touchscreen UI with the most recent data received from each Sense HAT Pi. 

13. The HMI Pi must update the touchscreen UI once every minute.

14. Each record in the database on the NAS must contain a timestamp marking when a set of data was recorded. 

15. Each record in the database on the NAS must contain an ID uniquely identifying each Sense HAT Pi. 

16. Each record in the database on the NAS must contain each Sense HAT Pi's reported Wi-Fi signal strength data. 

17. Each record in the database on the NAS must contain each Sense HAT Pi's reported magnetometer data. 

18. The HMI Pi must push a data record to the database on the NAS upon receipt of data from all Sense HAT Pis.

19. The data polling service on the HMI Pi must be containerized. 

20. The data processing/aggregation service on the HMI Pi must be containerized. 

21. The data logging service on the HMI Pi must be containerized. 

22. The UI controller service on the HMI Pi must be containerized. 

23. The data reporting service on each Sense HAT Pi must be containerized. 

## Non-Functional Requirements:

1. Each GitHub commit must be made with a singular purpose and a comment that describes the details and purpose of the commit. 

2. Data records must be sent to the NAS and project code must be backed up on the GitHub repository.

3. Docker Swarm requires port number 2337 for cluster management. 

4. Docker Swarm requires port number 7946 for node discovery. 

5. Docker Swarm requires port number 4789 for VXLAN traffic. 

6. The classroom NAS requires port number 2049 for data logging.

7. A vacant subnet must be explicitly declared for Docker Swarm to use to prevent subnet 	collision.

8. Traffic, broadcasts, and discovery probes must be restricted to the 192.168.5.0/24 	subnet.

9. We will execute ss -tulnp | grep -E ':(2337|7946|4789|2049)\b' during the expo to prove the sockets are operating as designed. 

10. We will execute sudo lsof -i :2337 -i :7946 -i :4789 -i :2049 during the expo to prove the processes are operating as designed. 

11. We will execute ip -br addr, ping -c 4 192.168.42 on the SenseHat Pis, and sudo ethtool eth0 during the expo to prove the links are operating as designed.

12. We will execute sudo systemctl enable --now docker for automatic startup on system boot and immediate startup in the current session. 

13. The system must be able to launch cleanly within 180 seconds of a cold reboot. 
