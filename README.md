# Micheasz Maciąg - Project solution

The solution I'm forwarding consists of two main scripts:
- main.py
- constants.py

Inside the main.py file, there is a class called **BallDontLieAPI**.
The above mentioned class contains three different methods that allow the user to extract some statistical data from the API at the url: https://www.balldontlie.io

constants.py only contains a dictionary with the most common error codes that a request can return as a response.
It can be further improved to contain different constants used throughout the code.

---------------------------------------------------

## **BallDontLieAPI - Class**
- ### **grouped_teams**
        params: None
        return: None

        This method requires no additional parameters, 
        and returns no data. All the data processed by 
        this method will be instead displayed to the stdout.

        Functionality:
        This method's main objective is to group all the 
        teams based on their division and display them 
        to the standard output.
        The output will be sorted based on the division
        alphabetical order.

- ### **players_stats**
        params: name (str)
        return: None

        This method requires the name parameter, 
        and returns no data. All the data processed by 
        this method will be instead displayed to the stdout.

        Functionality:
        This method's main objective is to find the 
        tallest and heaviest player with the given name.
        In case no data is provided by the API,
        it will display Not found instead.
        All the measurements are based on the metric system.

- ### **teams_stats**
        params: season (int), [output (str) - default stdout]
        return: None

        This method requires the season parameter, 
        while the output parameter is not required.
        The output will be set by default to "stdout".
        This method will not return any data, but will 
        save the data to a specific file instead 
        (or print to the standard output).

        Functionality:
        This method's main objective is to find the 
        victories/losses statistics for every team
        and if a specific output format is given, then 
        those statistical data will be saved to that 
        specific file in that file format.
        
        Supported file formats:
            - csv
            - json
            - sqlite

### **Usage examples:**

1. `python main.py grouped-teams`
---
2. `python main.py players-stats --name michael`
3. `python main.py players-stats --name ike`
4. `python main.py players-stats --name Kosta`
---
5. `python main.py teams-stats --season 2019`
6. `python main.py teams-stats --season 2019 --output csv`
7. `python main.py teams-stats --season 2015 --output json`
8. `python main.py teams-stats --season 2018 --output sqlite`
9. `python main.py teams-stats --season 2017 --output stdout`