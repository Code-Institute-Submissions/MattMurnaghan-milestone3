# ***The Netflix analysis tool***
[Public Heroku application here](https://milestone3-mattm.herokuapp.com/)

[Google sheet with data used for analysis here](https://docs.google.com/spreadsheets/d/17R_6HWEAwSK1co3U75EFtQCfpvsylo-q3HqG1_y9ALw/edit#gid=0)

![am+i_responsive](assets/images/am_i_responsive.jpg)

[image from Am I Responsive](https://ui.dev/amiresponsive?url=https://milestone3-mattm.herokuapp.com/)

## ***Project Overview***
The Netflix analysis tool is s terminal-based application, written in python that allows for data collected on Netflix users through the pandemic to be manipulated and shown in graph form in the terminal using the [Plotext](https://pypi.org/project/plotext/) library.

## ***Table of Contents***
1. ### [User Experience(UX)](User)
    * Strategy
        * Project Goals
        * User stories
    * Scope
    * Design
    * Skeleton
        * Wireframes 
        * Logic Flowchart
2. ### Features
    * Current features
    * Future features
3. ### Technology used
4. ### Testing
    * User stories
    * Input validation
    * Known issues & Fixes
5.  ### Deployment
6. ### Credits
7. ### Acknowledgments

## ***User Experience (UX)***
### ***Strategy*** -  *Project Goals*
This project aimed to develop a terminal-based python application to demonstrate my ability to make use of the CLI. Python is a very good language for this, as it is primarily used in backend system design. It has a wide range of libraries available to pull from, which were instrumental in the completion of this project.

I chose to build the application with a focus on data analysis. I pulled the dataset from [Kaggle](https://www.kaggle.com/datasets/prasertk/netflix-daily-top-10-in-us) who in turn got it from [The Numbers](https://www.the-numbers.com/netflix-top-10). 
The dataset has over 7000 rows of data and 10 columns, arranging the different rankings, viewership-score and titles by date, showing a top ten daily rank for each day of the pandemic. There are multiple ways to analyze and present the data, but I chose to focus on the daily rankings.

### ***Strategy*** -  *User stories*
* *User goals*
    * I want to extract data from an external google sheet
    * I want to be presented with an easy-to-use CLI that clearly explains the steps required to view the data
    * I want to visualize the data in the worksheet and plot it in the terminal
    * I want to calculate the average rank of each show for the pandemic and sort them by the highest to the lowest rank.
    * I want to view the top ten rankings for specific days throughout the pandemic.

* *Site owner goals*
    * I want to provide an application that allows the user to select how and what data they view
    * I want to provide the number of unique titles to the user.
    * I want to maintain the correct order of titles and rankings when calculating the average for the course of the entire pandemic.

### ***Scope***
To achieve the goals laid out in my strategy, I want to implement the following functionality:
* A method of importing data from google sheets.
* A method of keeping the credentials needs to access the sheet in the proper scope so as not to expose them to the main.
* A method of calculating the average score of each title in the full list of titles in the dataset.
* A method of calculating the unique program titles, and the number of unique titles shown in the Netflix top ten throughout the pandemic.
* A method to get valid input from the user to interact with the program.
* A method to graph and visualize the data in the terminal where the project is being hosted. 

### ***Design*** 
The design for this project was minimal, the template given to use by the codeinstitute was pre-built and made use of the standard windows black and white terminal and CLI hosted virtually on Heroku.

### ***Design - Wireframes*** 
No wireframes were required for this project as the frontend was pre-built.

### ***Design - Logic Flowchart***
