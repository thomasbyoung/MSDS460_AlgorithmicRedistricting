# MSDS460_AlgorithmicRedistricting

**Group Members**
Albert Lee
Alberto Olea
Maddie Stapulionis
Thomas Young
Migus Wong

**Introduction**

This project focused on developing an integer programming approach to redesign Virginia’s legislative districts. The goal was to craft an algorithmic solution that ensured a fair and equitable Virginia voter population distribution while maintaining geographic adjacency. By integrating demographic data with county adjacency, the model aimed to balance the “one person, one vote” principle with practical constraints. Our work demonstrates how optimizing for fairness can address complex real-world challenges with electoral representation. Below is a visual representation of how the countries/ independent cities of Virginia are split into districts. The reason our group decided to pick Virginia is because it’s a good example of a “Purple State” and is oftentimes a bellwether state for future elections. Political pollsters and the media tend to hyperfocus on local Virginia results because it may indicate how national election results may play out. Virginia is also unique in that its gubernatorial race does not allow for consecutive term limits so there’s never an incumbent governor serving two consecutive terms. In addition to the uniqueness of Virginia’s election, it’s also a Purple State. Virginia’s governor is a Republican but the state legislature is controlled by Democrats.

![image](https://github.com/user-attachments/assets/edc5e4f3-1234-4b18-8794-5484258227de)

**Methods**

Methodologically we began with data collection and preprocessing. Population data for Virginia’s counties and independent cities was sourced from public census records, while adjacency information between counties was obtained from the U.S. Census Bureau. Preprocessing ensured consistency by reconciling mismatched entries between population and adjacency datasets and preparing the data for integration into the optimization framework.

The optimization model was built in Python using the PuLP library, With the primary goal of assigning counties to one of eleven legislative districts while minimizing deviations from a target population. We introduced binary decision variables to represent district assignments, whereas the object function sought to reduce absolute differences between district populations. 

Visualization played an important role- utilizing GeoPandas and Folium to map district assignments and population distributions. The visuals supported the interpretation of results, thus offering a spatial perspective on the effectiveness of the proposed model and its adherence to the constraints. Integrating computational tools and visualization techniques highlighted the potential of integer programming to inform equitable redistricting. 

**Results**

The optimization model successfully distributed Virginia's population of 8,715,698 across eleven districts, achieving a target population of 792,336 per district, though Fairfax County's population exceeded the target by over 40%. The model effectively balanced populations across the remaining districts despite this challenge. By minimizing the deviations from the target population the model upheld the 1P1V principle and ensured each of Virginia’s 133 counties and independent cities was assigned to a district. 

Reviewing specific district outcomes, District 2, containing Fairfax County, had the highest population at 1,141,878 residents. Other districts demonstrated more balanced populations: District 1 with 784,629 residents, district 3 with 777.058 residents, and District 4 with 789,654 residents. District 8 ..

Assignments adhered to geographic closeness by incorporating adjacent constraints. Accomack County was placed in District 5, which achieved a population of 743,379 residents, maintaining natural groupings. These assignments were guided by the network flow model that ensured district proximity. Each district formed a connected component where every county could reach every other county within the same district through an adjacent neighbor.

Optimization achieved an optimal status, minimizing population imbalances while respecting contiguity constraints. Visualizations created via GeoPandas and Folium provided clarity into the district boundaries and population distributions. An example would be Fairfax County’s large population required careful balancing; other districts combined urban and rural counties to achieve equity. Such visuals offered a spatial perspective, thus supporting the validation of the model’s results and confirming the geographic coherence of district assignments.

The redistricting plan model could benefit from adding additional variables and constraints. Constraints like number of available polling places, yearly road closures, and  There are gaps in county level data that are not easy to address with current online resources.

![image](https://github.com/user-attachments/assets/7bdcae69-eb9e-45ab-b273-924b770b9ee4)

**Other Methods**

The team tried to improve the base model by adding additional datasets such as Historical Voting Trends, Homeownership Percentage, and Age / Gender Demographics.
