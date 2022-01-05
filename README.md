# SuperPyV2

## Usage Guide

The application comes with some data (products/sales) added so you can mess around. Please take note that this data is not logical or chronological and may not make sense.

### Clean sheet

To start the application without any data you must remove/delete the Database and Uploads folders. Then restart the application. It will then take you through a set-up sequence for a clean sheet.

### Add & Sell products

You can add or sell products either manually, or by using an upload file. There is a template in the Uploads/Template folder for you to use. Fill out some products and add the file to the Uploads/Ready_For_Import folder. You can do this by following the menu which asks you what to do :)

### Get an overview

After you've added stock, generate an overview of your current stock sorted on the key and direction you prefer. you can do this by typing "review inventory" in the main menu.

### Check you financials

After you've made some sales and purchases, please type "review financials" in the main menu to get a graph in your terminal of your financial data.

## Known issues to resolve:

1. Upload csv files
When uploading a csv file (either sales or addition of products) will break on the first item it comes accross that isn't a correct input

2. Error messages
2.1 When issue 1 happens sometime a positive error message comes through while it should not
2.2 For some error messages need to be customized to user friendly messages.

3. Styling
The terminal styling is not consistent yet

## Future ideas

1. Data removal
I'd like to add more data removal options, like creating a fresh install with the use of a command and/or the ability to pinpoint items you want to remove. At this point in time you have to do this manually

2. Expand the inventory overview function filter functionalities

3. Expand the inventory overview function with export capabilities


## Report

### "Helpless"

I've used the module Rich to make the entire application as user friendly as possible. By asking questions through a prompt with rich, I've made it possible for the application to be used by a non tech savy user. One of the requirements was to add a "help" option in the application, but I've tried to make the application help all the way through.

### Set-up sequence

The application is made so that, if there are essential files missing (i.e. inventory.csv), it will prompt the user to give permission to add those files. Without this set-up the application will not start.

### PyTest

I'm proud of having used PyTest in this application, even though be I started using it way to far into the project, it did open my eyes to TDD. I will be using TDD in all of my future projects, because it saved me a couple of times ruining my own code :).

### In-terminal graph

I wanted to make the application to be fully functional in the terminal without having to open or click away from it. The graph from Matplotlib in the financial section messed this up, because it opened a new window with the graph. I've went on a search and found another package that made it able to display the graph inside the terminal. It may not be the prettiest, but I'm proud of it!



