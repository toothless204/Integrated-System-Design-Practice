# PPST III — Integrated Production Planning, Quality Control, and Decision Support System

This repository contains the documentation and project files of **Integrated System Design Practicum III (TI3093)**. The project focuses on improving the manufacturing system of a tripod production case through demand forecasting, assembly line balancing, statistical quality control, acceptance sampling, data modeling, and decision support system development.

The project integrates industrial engineering, statistics, production planning, quality control, database management, and business intelligence to support better operational decision-making in a manufacturing environment.

## Project Overview

PT PPST Manufacturing is a manufacturing company that produces several types of tripod products. As market demand increases, the company needs to improve its production planning, assembly efficiency, quality control, supplier inspection system, and shop floor decision-making capability.

This project applies a structured industrial engineering approach to convert historical demand, production data, quality measurements, supplier inspection data, and shop floor information into actionable decisions.

## Objectives

The main objectives of this project are:

1. To forecast market demand using appropriate quantitative forecasting methods.
2. To design and evaluate an efficient assembly line based on demand, precedence relationships, and standard time.
3. To implement statistical quality control using appropriate control charts and process capability analysis.
4. To design acceptance sampling plans for incoming supplier components.
5. To model and organize manufacturing data using database design principles.
6. To build a simple shop floor-level Decision Support System using Microsoft Power BI.
7. To support manufacturing decisions through data-driven dashboards and performance indicators.

## Project Scope

| Module     | Focus Area                  | Main Output                                                                                      |
| ---------- | --------------------------- | ------------------------------------------------------------------------------------------------ |
| Module 1   | Market Demand Forecasting   | Forecasting model, forecast performance evaluation, and demand estimation                        |
| Module 2   | Assembly Line Balancing     | Assembly line design, cycle time, minimum workstation calculation, and line performance analysis |
| Module 3   | Statistical Quality Control | Control charts, process capability, OC Curve, and ARL analysis                                   |
| Module 4   | Acceptance Sampling         | Single sampling plan, double sampling plan, Dodge-Romig sampling, and Military Standard sampling |
| Module 5   | Decision Support System     | Shop floor-level Power BI dashboard and decision support prototype                               |
| Supplement | Data Modeling               | ERD, LDM, PDM, normalization, and database structure                                             |
| Supplement | Microsoft Power BI          | Data preparation, data exploration, visualization, slicer, filter, and dashboard development     |

## Methodology

The project follows an integrated production system improvement methodology:

### 1. Demand Forecasting

Historical demand data is analyzed to identify demand patterns and select an appropriate forecasting method. The forecasting process includes data preprocessing, model selection, parameter estimation, forecast generation, performance measurement, and forecast verification.

### 2. Assembly Line Balancing

The forecasted demand is used as input for designing the assembly line. The analysis includes cycle time calculation, minimum workstation estimation, precedence diagram interpretation, bottleneck identification, and line balancing using heuristic algorithms.

### 3. Statistical Quality Control

Quality data from tripod components and assembly processes is analyzed using statistical process control methods. The project selects appropriate control charts based on data characteristics, evaluates process stability, calculates process capability, and analyzes OC Curve and Average Run Length.

### 4. Acceptance Sampling

The project identifies critical parts and designs incoming inspection plans for supplier components. The sampling plan considers producer risk, consumer risk, AQL, LTPD, AOQL, administrative feasibility, supplier relationship, material flow, and inspection cost.

### 5. Data Querying and Database Processing

SQL queries are used to extract relevant quality measurement data from the production dataset. The queried data supports control chart construction, defect analysis, nonconformity analysis, and statistical quality evaluation.

### 6. Data Modeling

Manufacturing data is structured using data modeling principles. The process includes conceptual data modeling, entity relationship modeling, logical data modeling, physical data modeling, and normalization.

### 7. Decision Support System Development

A shop floor-level Decision Support System is developed using Microsoft Power BI. The DSS prototype transforms production and quality data into interactive dashboards that support operational monitoring, analysis, and decision-making.

## Key Findings

The main findings from this project are:

* Demand forecasting is essential for determining production targets and supporting capacity planning.
* Forecasting errors can affect production planning, capacity allocation, and inventory decisions.
* Assembly line balancing helps reduce bottlenecks, operator waiting time, and workstation imbalance.
* Statistical quality control supports early detection of process instability and product quality deviation.
* Control chart selection must be adjusted to the type of quality data, including variable data, attribute data, individual measurements, and multivariate measurements.
* Process capability analysis helps evaluate whether the production process can consistently meet specification limits.
* Acceptance sampling is useful when full inspection is costly, time-consuming, or operationally inefficient.
* Supplier inspection plans need to balance quality risk, inspection cost, and operational practicality.
* SQL-based data extraction improves the efficiency of quality data processing.
* Data modeling improves the structure, consistency, and usability of manufacturing data.
* Power BI dashboards help transform raw data into visual insights for shop floor decision-making.

## Tools and Methods

This project uses a combination of forecasting, production planning, statistical quality control, database, and business intelligence methods.

### Forecasting and Demand Planning

* Time Series Forecasting
* Naïve Forecasting
* Simple Moving Average
* Weighted Moving Average
* Single Exponential Smoothing
* Double Exponential Smoothing
* Holt’s Method
* Holt-Winters Method
* Linear Regression with Time
* Forecast Error Measurement
* Forecast Verification

### Assembly Line Balancing

* Precedence Diagram
* Cycle Time Calculation
* Minimum Workstation Calculation
* Bottleneck Analysis
* Largest Candidate Rule
* Region Approach
* Helgeson-Birnie Method
* Ranked Positional Weight
* Mixed Model Assembly
* Line Efficiency Analysis
* Balance Delay Analysis

### Statistical Quality Control

* Control Chart
* X-bar and R Chart
* X-bar and S Chart
* Moving Range Chart
* p Chart
* np Chart
* c Chart
* u Chart
* CUSUM Chart
* EWMA Chart
* Hotelling T² Chart
* Process Capability Analysis
* Operating Characteristic Curve
* Average Run Length

### Acceptance Sampling

* Critical Part Identification
* Lot Formation
* Random Sampling
* Single Sampling Plan
* Double Sampling Plan
* Dodge-Romig Sampling
* Military Standard Sampling
* AQL
* LTPD
* AOQL
* Producer Risk
* Consumer Risk
* Rectifying Inspection

### Database and Data Modeling

* SQL Query
* Database Management System
* Entity Relationship Diagram
* Logical Data Model
* Physical Data Model
* Normalization
* Data Table Relationship
* Data Preparation

### Decision Support System and Business Intelligence

* Decision Support System Design
* Problem Scoping
* Modelling
* System Design
* Prototyping
* Microsoft Power BI
* Data Visualization
* Dashboard Design
* Data Slicer
* Data Filter
* Drill Mode
* New Column
* New Measure

## Notes

This repository is an academic documentation of the Integrated System Design Practicum III project. The main focus is to demonstrate how forecasting, assembly line balancing, quality control, acceptance sampling, database modeling, and decision support systems can be integrated to improve manufacturing performance.

