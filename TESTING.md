# **Testing** 

### **Note When Testing**
To test all functions you may need to delete the data in the google sheet. To do this when the program prompts you to choose between stock or sales type "delete" all in lower case. 

![Delete step 1](./assets/imgs/delete-1.png)

It will then ask you to confirm your choice three times. Then it will clear the sheet. If it has been preformed correctly it will look like this;

![Delete step 2](./assets/imgs/delete-2.png)

* [Validation](#Validation)
* [Functionality Testing](#functionality-testing)
    * [User Story Evaluation](#user-story-valuation)
* [Bug Fixes](#bug-fixes)

## **Validation**
I ran my code through the [pep8online linter](http://pep8online.com/) to check for errors. The original code came back with the following errors;

![peponline fail](./assets/imgs/peponline-fail.png)

These were fixed in commit [1ef6d64](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/1ef6d6481bbeb06daed090ac80b0ed134fbbc72d#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0). After that the code passed through the linter with no further issues;

![peponline pass](./assets/imgs/peponline-pass.png)

## **Functionality Testing**
* [User Story Evaluation](#user-story-valuation)
* [Additional User Stories](#additional-user-stories)
* [Manual Testing](#manual-testing)

### **User Story Evaluation**

Once development was complete I reevaluated my user stories to ensure that I had met the project goals; 

#### As a user, I expect:
* To be able to easily understand what information the application is asking for. 

**The application uses simple language when asking for user input. And when a speficic format is required (for example when inputting dates) that is indicated through a print statment**

**The application also uses data validation to ensure that the inputs are correct and uses error handling to help the user to know how to resolve any input errors**
* To be prompted to reorder stock when an item is running low.

**After updating sales the application checks to see if the stock levels for each book are less than 50 books. If they are it will prompt the user to place a reorder for the book**

* To get reports after each input showing both gross and net profit in an easy to understand manner. 

**After updating sales the infomation is presented to the user in an easy to understand format. This is then saved in the google sheet so that users can refer back to it.**

* To be able to easily update sales.

**On running the application the user is asked if they are asked if they are updating stock or sales. If they choose sales the program prompts them for the infomation required.**

* To be able to easily update stock. 

**On running the application the user is asked if they are asked if they are updating stock or sales. If they choose stock the program prompts them for the infomation required.**
 
#### As a user, I want:
* To be able to see the data I am to input to confirm it is correct.
**When updating a sale the program shows the user their input and asks them to comfirm it is correct before procedding.**

* To be able to easily navigate through the data.

**The application updates a google sheet that presents the data in an easy to understand way. Summaries for sales and stock are easily accesable. And there is a further break down for convention sales**

**Each book has it's own section which will display a more detailed breakdown of infomation.** 

* To be able to add additional books through the command line interface without having to manually modify the code or the spreadsheet.

**The stock update program has the option to add books to the spreadsheet. This function gets all the infomation required to run the program without requiring the user to have to update any spreadsheets manually** 

### **Additional User Stories**

During development it became clear that from a UX pov that I needed to add the following user stories; 

#### As a user, I expect:

* To be able to clear the google sheet from within the application. 

**While testing the application it quickly became irritating to have to manually delete the data everytime a new feature was added. To avoid this I implemented a function to clear the sheet and start again.**

**To avoid this being accidently being called I made it a hidden function and made it so that the user would have to confirm that they wanted to delete the data three times before deleting the data**

**To access the function when the program asks the user to choose between stock or sales you type "delete" in lowercase.**

* If the program is run without any data it will run a set up function to ensure that all the functions run correctly. 

**After excuting the delete function the next time the program runs it will run a set up function. This prevents the user from updating sales when there is nothing to update.**

### **Manual Testing**

After running the program through the linter I manually checked to ensure that all functions and validation was working as intended. 

My intial run through revealed that the delete function was not adding the correct headings in the con sheet which was making the data difficult to parse. This was fixed in commit [0d61bf](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/0d61bf9df038751700188dcce306495a8d868886#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0).

I then tested the confirm choice function and it was not working as intended. Instead of just rerunning the confirm choice function it would rerun the whole function that called it. That was fixed in commit [c0fa215](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/c0fa215326292c33258c38d1db739cb7fb5240a3). 

I first checked the set up function. It worked as intended. I then checked the intial data validation and that worked as intended;

![Data validation](./assets/imgs/data-validation-1.png)

![Data validation 2](./assets/imgs/data-validation-2.png)

I then tested the date validation process. And that worked as expected. 

![Date validation](./assets/imgs/date-validation-1.png)

![Date validation 2](./assets/imgs/date-validation-2.png)

![Date validation 3](./assets/imgs/date-validation-3.png)

![Date validation 4](./assets/imgs/date-validation-4.png)

I then checked the spreadsheet to check to see if the infomation pulled through and everything was working as intended. 

![New book worksheet](./assets/imgs/new-book-worksheet-1.png)

![New book worksheet](./assets/imgs/new-book-worksheet-2.png)

![New book worksheet](./assets/imgs/new-book-worksheet-3.png)

![New book worksheet](./assets/imgs/new-book-worksheet-4.png)

I then reran the program to see if everything worked as expected. I also tried to input a book with the same title to see if the data validation was working as intended. 

![Same Title](./assets/imgs/same-title.png)

I then checked to see if the stock and sales function was working as intended. The data validation was working as expected. 

![Stock Sales](./assets/imgs/stock-sales.png)

I then checked the online sales function and that worked as expected. 

![Online Sales 1](./assets/imgs/online-sales-1.png)

![Online Sales 2](./assets/imgs/online-sales-2.png)

I entered a input high enough to trigger the auto reorder function and that worked as expected. 

![Auto Reorder](./assets/imgs/auto-reorder-1.png)

Then I checked the con-sales function and that was working as expected. 

![Con Sales 1](./assets/imgs/con-sales-1.png)

![Con Sales 2](./assets/imgs/con-sales-2.png)

![Con Sales 3](./assets/imgs/con-sales-3.png)

I then checked the sheet to see if it had pulled through the infomation as intended and everything had worked okay. 

![Update sheet sales 1](./assets/imgs/update-sheet-sales-1.png)

![Update sheet sales 2](./assets/imgs/update-sheet-sales-2.png)

![Update sheet sales 3](./assets/imgs/update-sheet-sales-3.png)

![Update sheet sales 4](./assets/imgs/update-sheet-sales-4.png)

![Update sheet sales 5](./assets/imgs/update-sheet-sales-5.png)

![Update sheet sales 6](./assets/imgs/update-sheet-sales-6.png)

I then checked to see if stock limit I put in place was working. It was functioning as expected. 

![Stock limit](./assets/imgs/stock-limit-1.png)

Finally I checked the delete function to see if that was working as intended. During testing I discovered that it would let you access the sales function but without any books it would throw up an error. 

![Delete 1](./assets/imgs/delete-func-1.png)

![Delete 2](./assets/imgs/delete-func-2.png)

This was fixed in commit [633bf1](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/633bf145635bf83962da59f74fd3cf87e74219f2)

![Delete 3](./assets/imgs/delete-func-3.png)

While fixing the delete function issues I discovered a new validation issue with some inputs that required integers rather than floats. This was fixed in commit [ee1c67](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/ee1c6769879fb97fa0e2f3e933e36ca600d0e0ef).

![Data validation](./assets/imgs/data-validation-3.png)

## **Bug Fixes**

1. The wrong function was called to update the cost per unit whenever stock levels were updated. This was causing issues with the calculations and caused incorrect data to pushed to the google sheet. This was fixed in commit [e5b10f9](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/e5b10f9722dc373dd86bb3937275b0badd991a95#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0).

2. The recalculate_cpu function was returning it's value as an unweildy integer. I added a round function so that the data that it returned was more readable. Fixed in commit [d3e251](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/d3e25141fd14017182a28fb1b292dd572850d3fc#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0).

3. The gross profit was being miscalculated. This was fixed in commit [877dd5](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/877dd5ab14d9329f251e99daa778dead32e1952a#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0).

4. The program would crash whenever there was no data being provided to the update_header function. This was fixed in commit [d48f68](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/d48f68d2ca953a7a1b6d7500d15e52eb84b60953#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0).

5. The gross and net profit was being updated in the wrong section. This was fixed in commit [a45241](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/a452412f3ea9cdcc13c0f462a13e0032b7e2e5ed#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0).

6. When reordering stock due to low stock levels the new data was being overwritten with the old code meaning the stock tracker was not working. This was fixed in commit [dda9e2](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/dda9e260ea8d7564a28b1a7330e6475ca6c4b13b#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0), [d42bf4](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/d42bf429a0e0bef0ca132a47ae3252a01fb905fd#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0), and [ 6be11a](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/6be11a23482554e768d6f98d5e33b596d8f4ad46#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0)

7. The populate comic list was updating the price with the value of the original book. This was fixed in commit [a8decb](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/a8decb26d14efc6fd7baacc71cc96229aa0d2828).

8. The populate comics list function was pulling the data from the wrong sheet. This was fixed in commit  [5f71f3](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/5f71f3393348019ea18c6daf34327832221fc7ea#diff-d6af0459a37d985953d7040c14f53feb3b9cc9e58b543aa3c2b80256d276c5e0).

9. The validata_date function was transposing the day and the month causing correct inputs to not pass through the validation. This was fixed in commit [8a8eaa](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/8a8eaa8a73e061017a6cc787d975102c9d1acfcb).

10. The select book function was not displaying the list of books to choose from. This was fixed in commit [560e88](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/560e88290ae7864b0d3b6b3951e2ee109384cae8).

11. The confirm choice function was not working as intended. Instead of just rerunning the confirm choice function it would rerun the whole function that called it. That was fixed in commit [c0fa215](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/c0fa215326292c33258c38d1db739cb7fb5240a3). 

12. If 0 is entered for price or stock it causes a divde by 0 error. This was fixed in commit [c0fa21](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/c0fa215326292c33258c38d1db739cb7fb5240a3).

13. The delete content function was causing errors when it the run application again choice was made after deleteion. This was fixed in commit [633bf1](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/633bf145635bf83962da59f74fd3cf87e74219f2).

14. Some functions would cause the system to crash when the user inputed a float. This was fixed in commit [ee1c67](https://github.com/John-McPherson/Python-Essentials-Portfolio-Project/commit/ee1c6769879fb97fa0e2f3e933e36ca600d0e0ef).