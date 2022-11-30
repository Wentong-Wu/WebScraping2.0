# Web Scraping using Selenium in Python

## Setup

- Install Visual Studio Code
- Install Python
- Creating a Scraper main class and a new Python environment
- Install Selenium into the new Python environment

## Milestone 1: Navigating the website (WaterStones)

Creating the constructor and methods to navigate around the website.
- Initialize the class which opens up the url of the website to scrape. (Constructer)
- Accepting Cookies (Most websites requires the user to click on cookie acceptance). (Method)
- Getting the navigation element using the navigation titles. (Method)
- Getting all the product link from the navigation title to store it as a list of links. (Method)
- Open up each link from the list and store the data into a dictionary which then can be changed into a json file. (Method)
- Download and store images of the product into an image folder. (Method)
