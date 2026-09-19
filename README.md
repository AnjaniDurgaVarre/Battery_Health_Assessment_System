# Battery Health Assessment and Dynamic Allocation for Light Electric Vehicles

## Overview

The Battery Health Assessment and Dynamic Allocation System is a web-based application designed to recommend and allocate suitable batteries to Light Electric Vehicles (LEVs).

Unlike conventional battery-swapping systems that mainly consider State of Charge (SoC), this system evaluates multiple battery parameters such as State of Charge (SoC), State of Health (SoH), temperature, and battery availability before recommending a battery.

The system provides battery and vehicle dataset management, vehicle search, battery health assessment, battery recommendation, battery allocation, dashboard monitoring, and graphical visualization.

## Problem Statement

Battery-swapping systems often select batteries mainly based on their charge level. However, a battery with sufficient charge may have poor health, high temperature, or may not be available for allocation.

This project addresses this issue by evaluating multiple battery health and operating parameters before recommending a battery for a vehicle.

## Objectives

- Assess battery suitability using multiple health parameters.
- Recommend a suitable battery based on vehicle requirements.
- Allocate batteries safely and efficiently.
- Prevent duplicate battery assignments.
- Provide dashboard-based monitoring.
- Visualize battery status and performance using graphs.
- Adapt the system to updated battery and vehicle datasets.

## Key Features

- Battery dataset upload and processing
- Vehicle dataset upload and processing
- Vehicle search using Request ID
- Battery health assessment
- Battery eligibility checking
- Battery recommendation
- Dynamic battery allocation
- Prevention of duplicate battery assignment
- Battery status updates
- Dashboard monitoring
- Graphical visualization
- Updated dataset handling using Battery IDs and Request IDs
- Battery suitability ranking

## System Workflow

Upload Battery Dataset → Upload Vehicle Dataset → Search Vehicle → Battery Health Assessment → Battery Recommendation → Battery Allocation → Dashboard → Graphs

## Battery Selection Criteria

A battery is considered eligible for allocation when it satisfies the following conditions:

- Battery Status = AVAILABLE
- Battery SoC ≥ Vehicle Required SoC
- Battery SoH ≥ 80%
- Battery Temperature < 40°C

Among the eligible batteries, the system recommends a suitable battery based on the defined allocation logic.

## Allocation Process

The allocation process follows these steps:

1. Load the battery and vehicle datasets.
2. Read the vehicle request.
3. Check battery availability.
4. Check the required State of Charge (SoC).
5. Check State of Health (SoH).
6. Check battery temperature.
7. Recommend the best eligible battery.
8. Allocate the battery to the vehicle.
9. Update the dashboard.

## 30% Twist Adaptation

During the onsite stage, the project was adapted to handle updated battery and vehicle datasets without rebuilding the complete system.

The updated datasets are compared with the existing datasets using unique Battery IDs and Vehicle Request IDs.

### Battery Dataset Update

- Same Battery ID → Updated battery record is considered.
- Old-only Battery ID → Existing battery record is retained.
- New-only Battery ID → New battery record is added.

### Vehicle Dataset Update

- Same Request ID → Updated vehicle requirements are considered.
- Old-only Request ID → Existing vehicle request is retained.
- New-only Request ID → New vehicle request is added.

After updating the datasets, the system reassesses battery eligibility and ranks the eligible batteries using suitability parameters.

## Battery Ranking

The updated system evaluates eligible batteries using parameters such as:

- State of Charge (SoC)
- State of Health (SoH)
- Temperature
- Internal Resistance
- Cycle Count
- Cell-Voltage Imbalance

The eligible batteries are ranked according to their suitability score, and the highest-ranked eligible battery is recommended for the selected vehicle.

## Dashboard and Visualization

The application provides a dashboard for monitoring battery information and allocation status.

The dashboard includes graphical visualization of:

- State of Charge
- State of Health
- Temperature
- Battery Status
- Battery Allocation Information

## Technologies Used

- Python
- Flask
- Pandas
- HTML
- CSS
- Bootstrap
- JavaScript
- Chart.js
- CSV

## Project Structure

Battery_Health_Assessment_System/

├── static/

├── templates/

├── uploads/

├── app.py

├── battery.csv

├── vehicle.csv

├── runtime.txt

└── README.md

## Testing and Validation

The system was tested using battery fleet and vehicle request datasets.

The testing included:

- Battery dataset upload
- Vehicle dataset upload
- Vehicle search
- Battery recommendation
- Battery allocation
- Dashboard monitoring
- Graph generation

The system validated that only eligible batteries satisfying the predefined conditions were recommended and allocated.

## Results

The developed system successfully performs battery and vehicle dataset processing, vehicle request searching, battery health assessment, battery recommendation, and battery allocation.

The dashboard provides battery statistics and graphical visualization for monitoring battery status and allocation information.

## Project Team

### Team Name

DREAM CHASERS

### Team Members

- Bindu Sri Matha Medapati — Team Lead
- Anjani Durga Varre
- Bharath Sai Gubbala
- Karthik Tagaram

### Institution

Swarnandhra College of Engineering and Technology

Narsapur, West Godavari, Andhra Pradesh.

## Future Scope

- Integration with real-time battery sensors
- Integration with physical battery-swapping stations
- Real-time IoT-based battery monitoring
- Advanced battery health prediction
- Improved battery suitability scoring
