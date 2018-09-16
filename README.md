# DisasterGuide

Disaster Guide is your guide when disaster strikes!

This is our 2018 HackMIT project to build an iOS application and server application for natural disaster alerting.

## Inspiration
During a natural disaster, it's difficult to remain calm and figure out the best course of action the face of danger. This is where Disaster Guide comes in. By giving disaster victims clear instructions through a hands-free speech based interface, it provides the guidance necessary to help save lives. In addition, Disaster Guide is able to provide GPS data to allow first-responders to more efficiently find people who need help.

## What it does
When a disaster occurs, the Disaster Guide app will notify users, and then give immediate to-do guidance to optimize the user’s chances of survival. The app will also send constant updates to our central server, which can then relay this information to first-responders. Users can also use voice commands to request various forms of assistance. These commands include activating a distress beacon, which will inform first responders which people are in the most need of first AID or other assistance.

## How we built it
Disaster Guide consists of a centralized server which communicates with iOS clients as well as an online dashboard for first-responders. The server was built from scratch using python, post press, and WebSockets, with the help of IBM-Watson for processing user dialogue. We used the Google Maps API's to display the real-time GPS locations for all disaster victims and first-responders. The user interface was built in Swift, with Speech-to-text capabilities, and Watson NLP processing.

## Challenges we ran into
Finding a real-time source of natural disasters and who they would affect was challenging because many of the available sources are APIs which have limited hit capacities. To overcome this challenge, we created Mother Nature which pushes disaster information to the connected servers.

## Accomplishments that we're proud of
We are very proud of our use of IBM-Watson Assistant to create hands-free interface for providing guidance while minimizing unnecessary distractions, and our robust hand-made server to organize emergency information for a large number of people, all while providing clean visualizations of this data in Google Maps.

## What we learned
This was our first time doing natural speech processing, and we are very satisfied with the result. We also learned that we can build a fast server and database completely from scratch for a hackathon.

## What's next for Disaster Guide
We would like to extend the capabilities to allow even more coordination between people. For example, Disaster Guide could potentially reduce traffic during evacuations by coordinating users to travel together. We would also like to integrate an extensive library of medical information to allow the app to further rank which people are in the most danger, as well as to provide medical instructions for users to perform first aid on themselves and on others.


## Requirements

To run the test suite, you will need at least the following:
* Python 3.x (preferably at least 3.5 or higher)
* jq - used to pretty print JSON responses
* watson-developer-cloud - IBM Watson's Python SDK
* websockets - used to create a web socket for receiving disaster information
* PostgreSQL - the relational database which stores all of the data

## Deployment

To run the server, navigate to the `DisasterGuide-server` directory and run
```
python3 server.py
```

## Testing

To test the server APIs, run the server and then in a new terminal run
```
./DisasterGuide-server/tests/test_all.sh
```
IMPORTANT: this will clear the data in the database, so use this with caution.

## Database Setup
After installing PostgreSQL, use Pgadmin or command-line tools to create a database called `disasterguide`. Then run
the test suite above to set up the schema of the database, or run the commands in database_schema.sql to configure the
database.