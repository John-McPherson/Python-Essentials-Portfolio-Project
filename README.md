# **Comic Sales tracker**

This project is the third milestone project for the Code Institute Diploma in Full Stack Software Development. You can see the final deployed site [here.](link)

<!-- ![Site mock-up](link) -->

## **Contents**
* [UX](#ux)
    * [User Stories](#user-stories)
    * [Flow Chart](#flowchart)
* [Features](#features) 
    * [Welcome Screen](#welcome-screen)
    * [Update Stock](#update-stock)
    * [Update Sales](#update-sales)
    * [Con Sales](#con-sales)
    * [Online Sales](#online-sales)
    * [Update Spreadsheets](#update-spreadsheets)
    * [Confirm Data](#confirm-data)
    * [Rerun Application](#rerun-application)

## **UX** 

### **User stories**

The application is designed to be a stock management system for comic creators. 

#### As a user, I expect:
* To be able to easily understand what information the application is asking for. 
* To be prompted to reorder stock when an item is running low. 
* To get reports after each input showing both gross and net profit in an easy to understand manner. 
* To be able to easily update sales.
* To be able to easily update stock. 
 
#### As a user, I want:
* To be able to see the data I am to input to confirm it is correct. 
* To be able to easily navigate through the data. 
* To be able to add additional books directly to the command line without having to manually modify the code or the spreadsheet. 

### **Flow Chart**
Before starting on the project, I created a mock up using lucid chart to break down the logic I would need to follow to ensure that the application worked correctly.  

![Flowchart](./assets/imgs/flowchart.jpeg)

## **Features**

### **Welcome Screen**
 * The application displays a welcome message on first launch. This would clearly layout the purpose of the application. This should be followed with the choice to update stock or to update sales. 

### **Update Stock**
 * The application should give the user the option to update stock of individual books. This should be easy to update while getting all the information needed to maintain the sales data base including: 
    * Number of items ordered.
    * Cost of the order
    * Date of the order

### **Update Sales**
 * The application should prompt to see if the user is update sales from a convention or from the online store. 

### **Con Sales**
 * When updating con sales the program prompts the user following information: 
	* The name of the convention. 
	* The date of the convention. 
	* The sales of each book. 
	* The expenses incurred during the convention (broken down into table costs, travel costs, parking, and miscellaneous costs.

### ** Online Sales **
* When updating online sales the program prompts the user following information: 
	* The date of the sales. 
	* The sales of each book. 

### **Update Spreadsheets**
 * The application pushes all information to a linked google sheets doc for easy viewing. 

 ### ** Confirm Data **
* After each input the application repeats the information back to the user and ask them to confirm before it pushes the data to the spreadsheet. 

 ### ** Rerun Application **
 * Once the application has finished running it gives the user the option to rerun to add any additional sales/ stock that’s required.   







