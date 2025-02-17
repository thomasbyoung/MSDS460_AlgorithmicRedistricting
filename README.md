# MSDS460_AlgorithmicRedistricting

## Group Members
Albert Lee,
Alberto Olea,
Maddie Stapulionis,
Thomas Young,
Migus Wong

## Introduction
This project focused on developing an integer programming approach to redesign Virginia's legislative districts. The goal was to craft an algorithmic solution that ensured a fair and equitable Virginia voter population distribution while maintaining geographic adjacency. By integrating demographic data with county adjacency, the model aimed to balance the "one person, one vote" principle with practical constraints. Our work demonstrates how optimizing for fairness can address complex real-world challenges with electoral representation.

Virginia was chosen as our target state due to its unique position in American politics. As a notable "Purple State," it often serves as a bellwether for future elections, with political pollsters and media closely monitoring local Virginia results as indicators of national electoral trends. The state's distinctive gubernatorial race, which prohibits consecutive term limits, creates an interesting dynamic where there's never an incumbent governor serving consecutive terms. This political landscape is further enriched by having a Republican governor alongside a Democrat-controlled legislature.

![Virginia Districts Map](https://github.com/user-attachments/assets/edc5e4f3-1234-4b18-8794-5484258227de)

## Methods
Our methodological approach began with comprehensive data collection and preprocessing. Population data for Virginia's counties and independent cities was sourced from public census records, while adjacency information between counties was obtained from the U.S. Census Bureau. The preprocessing phase ensured consistency by reconciling mismatched entries between population and adjacency datasets and preparing the data for integration into the optimization framework.

The optimization model was built in Python using the PuLP library, with the primary goal of assigning counties to one of eleven legislative districts while minimizing deviations from a target population. We introduced binary decision variables to represent district assignments, while the objective function sought to reduce absolute differences between district populations.

Visualization played a crucial role in our analysis, utilizing GeoPandas and Folium to map district assignments and population distributions. These visuals supported the interpretation of results, offering a spatial perspective on the effectiveness of the proposed model and its adherence to the constraints. The integration of computational tools and visualization techniques highlighted the potential of integer programming to inform equitable redistricting.

## Results
The optimization model successfully distributed Virginia's population of 8,715,698 across eleven districts, achieving a target population of 792,336 per district, though Fairfax County's population exceeded the target by over 40%. Despite this challenge, the model effectively balanced populations across the remaining districts. By minimizing the deviations from the target population, the model upheld the "one person, one vote" principle and ensured each of Virginia's 133 counties and independent cities was assigned to a district.

Specific district outcomes revealed varied population distributions:
- District 2, containing Fairfax County, had the highest population at 1,141,878 residents
- District 1 achieved 784,629 residents
- District 3 contained 777,058 residents
- District 4 balanced at 789,654 residents

Assignments adhered to geographic closeness by incorporating adjacent constraints. For example, Accomack County was placed in District 5, which achieved a population of 743,379 residents, maintaining natural groupings. These assignments were guided by the network flow model that ensured district proximity. Each district formed a connected component where every county could reach every other county within the same district through an adjacent neighbor.

![Optimization Results](https://github.com/user-attachments/assets/7bdcae69-eb9e-45ab-b273-924b770b9ee4)

## Model Enhancements
The team implemented several improvements to the base model by incorporating additional datasets:
- Historical Voting Trends: Added electoral data to balance partisan distribution
- Homeownership Percentage: Included property ownership patterns to reflect community stability
- Age/Gender Demographics: Incorporated population diversity metrics

## Technical Implementation
The project requires Python 3.x and several key packages including pandas, geopandas, folium, matplotlib, geopy, networkx, and pulp. The implementation includes multiple optimization models that build upon each other to create a comprehensive redistricting solution.

## Limitations and Future Work
While the current implementation provides valuable insights, several areas warrant further investigation. The model could benefit from additional variables and constraints, such as the number of available polling places and yearly road closures. There are also gaps in county-level data that are not easily addressed with current online resources. Future work might explore the impact of increasing mail-in ballot usage on district adjacency requirements and better account for transient military populations.

## Data Sources
- U.S. Census Bureau
- Virginia Department of Elections
- Federal Reserve Economic Data (FRED)
- Pew Research Center

## References
Validi, H., Buchanan, A., & Lykhovyd, E. (2022). "Imposing Contiguity Constraints in Political Districting Models." Operations Research, 70(2): 867-892.

Pew Research Center (2024). "Partisanship by Family Income, Home Ownership, Union Membership, and Veteran Status."

Federal Reserve Bank of St. Louis (2025). "Release Tables: 172256."

## GenAI Use
This README and portions of the documentation were generated and edited with assistance from Claude.ai, an AI language model by Anthropic.

## License
MIT License

Copyright (c) 2025 Albert Lee, Alberto Olea, Maddie Stapulionis, Thomas Young, Migus Wong

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.