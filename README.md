# CS450-Network-Interference-Mapper

## Official Project Title: Network Interference Mapper 

## Application Category: Environmental Control 

## Project Purpose Statement: 
Interference can be caused by many different problems, which can make it difficult to pinpoint where the issue lies. The Network Interference Mapper aims to assist Network Engineers with this problem by collecting related data via multiple edge devices. These devices pull data from their connected magnetometers for measuring magnetic interference and from iw scans for measuring interference from other devices. Use of this system will allow for quicker network-related troubleshooting. 

## Operational Boundaries:

HMI Pi Role: data aggregation, display, and logging 

Sense HAT Pi Role: magnetometer and iw polled 

Remote Storage / Infrastructure Role (NAS Database, MQTT Broker, or SFTP/SCP Server): NAS Database 

Optional Additional Nodes (Other Sandbox Table Pis or PLCs—note table consultation if applicable): two other Sandbox Table Pis (probably from Table 3 and Table 8) 

Out-of-Scope Boundaries (List 1–2 features your team is intentionally excluding to ensure completion by Week 15): Features we intend to exclude are creating a web-based application and implementing scalability.
