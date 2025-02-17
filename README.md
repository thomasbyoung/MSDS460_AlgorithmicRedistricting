# MSDS460_AlgorithmicRedistricting -- Algorithmic Redistricting for Virginia

## Overview

This project implements an integer programming approach to redesign Virginia's legislative districts. The model optimizes for fair voter population distribution while maintaining geographic adjacency across 11 districts. It serves as a practical demonstration of how mathematical optimization can address real-world electoral representation challenges.

## Why Virginia?

Virginia was chosen as the target state due to its unique position in American politics. As a notable "Purple State," it often serves as a bellwether for national elections, with political analysts closely monitoring local results for broader electoral trends. The state's distinctive gubernatorial term limits, which prohibit consecutive terms, create an additional layer of political dynamism. This, combined with its current political landscape of a Republican governor alongside a Democrat-controlled legislature, makes Virginia an ideal case study for redistricting analysis.

## Features and Implementation

The project implements multiple optimization models that build upon each other to create a comprehensive redistricting solution. The base model focuses on optimizing population variance to ensure fair vote distribution using PuLP for integer programming. This foundation is enhanced by a contiguity model that incorporates geographic adjacency constraints and implements network flow for district connectivity while minimizing moment of inertia.

Further enhancements to the model consider additional factors such as historical voting patterns, home ownership rates, and demographic data including gender and age distributions. The implementation also accounts for unique aspects of Virginia's population, such as the significant presence of military personnel and their impact on district formation.

## Technical Requirements and Installation

The project requires Python 3.x and several key packages including pandas, geopandas, folium, matplotlib, geopy, networkx, and pulp. To get started, clone the repository and install the required packages using `pip install -r requirements.txt`. You'll also need to download the Virginia county shapefile to `./data/VirginiaCounty.shp`.

## Usage and Visualization

Running the main script (`python redistricting.py`) initiates a comprehensive process that downloads and processes county/city data, loads adjacency information, executes the redistricting models, and generates visualizations. The results are saved to `final_district_assignments.csv`.

The visualization components include county-level population heat maps, district boundary maps, population distribution charts, and interactive web-based maps using Folium. These visual aids help in understanding the distribution patterns and effectiveness of the redistricting model.

## Data Sources and Methods

Our analysis draws from multiple authoritative sources including the U.S. Census Bureau, Virginia Department of Elections, Wikipedia's county/city information, Federal Reserve Economic Data (FRED), and Pew Research Center. This diverse data collection enables a thorough understanding of Virginia's demographic and political landscape.

## Limitations and Future Work

While the current implementation provides valuable insights into redistricting optimization, several areas warrant further investigation. The model could benefit from additional variables and constraints, and there are still gaps in county-level data that need to be addressed. Future work might explore the impact of increasing mail-in ballot usage on district adjacency requirements and better account for transient military populations, which are particularly relevant in Virginia given its numerous military installations.

## Contributors

This project was developed through the collaborative efforts of Albert Lee, Alberto Olea, Maddie Stapulionis, Thomas Young, and Migus Wong.

## References

Validi, H., Buchanan, A., & Lykhovyd, E. (2022). "Imposing Contiguity Constraints in Political Districting Models." Operations Research, 70(2): 867-892.

Pew Research Center (2024). "Partisanship by Family Income, Home Ownership, Union Membership, and Veteran Status."

Federal Reserve Bank of St. Louis (2025). "Release Tables: 172256."

## License

MIT License
