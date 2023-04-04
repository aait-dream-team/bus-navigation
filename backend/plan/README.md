### Inorder for the /plan endpoint to work
    - it needs the otp conainter running
    - the network of the backend and the otp container to be configured [link](https://levelup.gitconnected.com/how-to-access-a-docker-container-from-another-container-656398c93576)

### The end point takes parameters as a url query 
 #### the parameters are:
    - fromPlace - coordinates of the start point
    - toPlace - coordinates of the end point
    - time - the initial/arrival time of the trip
    - date - the initial/arrival date of the trip
    - mode - modes of transport to be used, WALK, BICYCLE, CAR, BUS, TRAM, RAIL, SUBWAY, FERRY, CABLE_CAR, GONDOLA, FUNICULAR
    - arriveBy - if true, the trip will be planned to arrive at the time specified, otherwise it will be planned to depart at the time specified
    - wheelchair - boolean, if true, the trip will be planned to be wheelchair accessible
    - showIntermediateStops - boolean, if true, the trip will be planned to include intermediate stops
    - debugItineraryFilter - boolean, if true, the trip will be planned to include debug information
    - locale - the locale of the trip

### Example request
    - GET http://localhost:8000/plan/?fromPlace=45.45049747764105%2C-122.79762268066405&toPlace=45.46109386344247%2C-122.61497497558594&time=9%3A19am&date=05-05-2023&mode=TRANSIT%2CWALK&maxWalkDistance=4828.032&arriveBy=true&wheelchair=false&debugItineraryFilter=false&locale=en