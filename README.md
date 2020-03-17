# Description

How do we personalize our customer’s trip? From their recent flight searches, how do we plan to get them to reactivate their cart again? Can we suggest some of the exiting attractions from their searched destination and reigniting their interests? This mini-project plan to provide answers for some of these questions. We will be suggesting a planned itinerary for their searched destination based on the length of stays using K-means. 

# Implementation

## Getting lat and long

We need to get the latitude and longitude for the attractions at the destination. Google’s My Maps can be used to get these coordinates as the community has helped to pin some attractions for a particular destination on My Maps. By exporting the file in KML format, we can use Beautiful Soup to help transform it.

## Using the length of stays to create clusters

The number of clusters are determined by the length of stays.

## Using finding the shortest path to determine plans for particular day

We select the starting point based on the clusters generated then using shortest path to determine the nearest clusters. This would create a plan whereby the furthest clusters would be explored at the last day. It can also be tweaked to allow us to select to start from the furthest first.

## Exporting to CSV and Exported to Google My Map

After the result has been generated we will export it to My Map to be visualized. Sample trip itinerary for Penang:  

Kuala Lumpur 7 Days:  

The Web App

With the help from  , we were able to deploy a simple flasks web app for itinerary planner onto app engine. 

Web app: https://malaysia-trip-planner.appspot.com/

# Improvements

We would like to be able to automate the entire process so results can be generated instantly without any interference. 

We would like to find new ways to display the result instead of using google maps as it has to been imported and exported everytime. Ideally we can present them in email templates instead of links. 

# Future/Envisioned Outcome

1. Cart Abandonment Email 

“We are sad to see you go   Here’s a personalized itinerary that’s planned for you! Why not check it out and rethink again?  “

2. Post purchase Engagement Email

“We thank you for purchasing a flight ticket with us! Here’s a personalized itinerary that would fit your need! ”

# References

https://towardsdatascience.com/how-to-improve-holiday-itinerary-with-machine-learning-6b3cd3c79d1

