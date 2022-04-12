# FlightDeals
Here's how the program works. First, I have a Google sheet which keeps track of the locations that I want to visit and a price cutoff.

![FlightDeals](https://user-images.githubusercontent.com/63019595/140406444-aae200d0-261e-4fe7-9ce5-0e1743672556.png)

It takes data from my Google sheet with lots of different locations and their lowest prices and feeds that into a flight search API, which runs
searching through all of the locations. Looking for the cheapest flight in JKIA in the next six months.

When it comes up with a hit and it finds a flight that's actually cheaper than my predefined price,
then it sends that date and price via Twilio SMS module to my mobile phone. I can then book the flight if i wish to.

<img src="https://user-images.githubusercontent.com/63019595/140407729-627245fc-9359-4d6a-8f98-b572eba8c3bf.png" alt="Message Screenshot" width=350 height=800>
 
