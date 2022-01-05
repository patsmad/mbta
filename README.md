# Broad DSP Engineering Interview Take-Home
## Patrick Smadbeck

The project consisted of three parts:
(1) a main file which consumes input from the user from the command line or python shell
(2) src which contains the classes which fetch process and return the data
(3) tests which test the api converting code and mbta map functions

Before starting you might want to consider adding your API key to a config file in the same directory as main.py.
Call this file config.json (which can be copied from config.copy.json).
The API key can also be passed in from the command line using the argument:
```buildoutcfg
python -m main --api_key=<<YOUR API KEY>>
```

### Requirements
This program was developed in Python 3.6.6

The requests package will need to be installed in order to run the program.
This program was developed with requests version 2.26.0

### Running the Main Program
The program can be run using command line arguments.

#### Part 1
Command:
```buildoutcfg
python -m main --print_routes
```
This will print off a list of routes of type 0 or 1 from the API.

There are two ways to filter results for subway-only routes.
1. Download all results from https://api-v3.mbta.com/routes then filter locally
2. Rely on the server API (i.e., https://api-v3.mbta.com/routes?filter[type]=0,1) to filter before results are received

I've employed the second option, as this will be very likely to be faster. The main reason being that the data likely goes through a bunch of steps to be serviced on my end:
1. It is taken out of some database.
2. It is transformed into a json blob.
3. It is transferred to my computer.
4. I filter it in the API service.

It will save time fetching / transferring / transforming by asking the service to do the filtering up front (likely in step 1)

#### Part 2
Command:
```buildoutcfg
python -m main --print_stop_analysis
```

This will print off the route with the maximum number of stops, the route with the minimum number of stops, 
and all of the stops which service multiple routes. These three statements can also be done individually:
```buildoutcfg
python -m main --print_min_stops
```
```buildoutcfg
python -m main --print_max_stops
```
```buildoutcfg
python -m main --print_connecting_stops
```

#### Part 3
A path between two stations can be requested using:
```buildoutcfg
python -m main --get_path=<<STOP 1>>,<<STOP 2>>
```
Make sure the stop names are exactly as defined in the MBTA API. An example:
```buildoutcfg
python -m main --get_path=Davis,Kendall/MIT
```
This will return a set of routes that will take you from STOP 1 to STOP 2. The example above gives:
Davis to Kendall/MIT: Red Line

#### All parts
```buildoutcfg
python -m main --print_routes --print_stop_analysis --get_path=Davis,Kendall/MIT
```

### Running tests
There are two ways to run tests.

You can run them directly from the command line from the main directory:
```buildoutcfg
python -m unittest tests.map_test tests.mbta_api_test -v
```

or you can run it using a command line argument:
```buildoutcfg
python -m main --run_tests
```

NOTE: When running tests with the command line argument other command line arguments will be ignored.
