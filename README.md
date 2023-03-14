# Python3-Route-Manager
The route_manager.py program takes user input that specifies a specific quesiton to be answered and what type of graph the user wants the information displayed in.

**The 5 questions include**  
1. What are the top 20 airlines that offer the greatest number of routes with destination country as Canada?  
2. What are the top 30 countries with least appearances as destination country on the routes data?  
3. What are the top 10 destination airports?  
4. What are the top 15 destination cities?  
5. What are the unique top 10 Canadian routes (i.e., if CYYJ-CYVR is included, CYVR-CYYJ should not) with most difference between the destination altitude and the origin altitude?  

The user can also pick whether they want the information displayed in a bar or pie graph.

The input should be formatted as follows...  
./route_manager.py --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q<x>" --TYPE="type of graph"  
The questions can be input as q1, q2, etc.  
The type of graph can be input as "pie" or "bar"  
  
  
**OUTPUT:**  
The output data will be stored in a .csv file called q<x>.csv, where x is the question input by the user.  
And the graph will be output in a file called q<x>.pdf, where x is the question input by the user.


