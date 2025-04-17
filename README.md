# Black box testing AI Agent

This is planned to be an AI Agent that can crawl through a given website's frontend and find all API endpoints being called in the background.
These endpoints will be further stress tested

## Setup

In the root directory, run 
```
uv sync
```

Then go into src/blackbox with 
```
cd src/blackbox
```

Then finally, run
```
crewai install
```

## Starting the Agent

To start the agent, make sure you are in src/blackbox and then run
```
crewai run
```