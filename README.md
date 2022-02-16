# SuperPyV2

## Dependencies

Rich 11.2.0
Plotext 4.1.5

## Usage Guide

The application comes with some data (products/sales) added so you can mess around. Please take note that this data is not logical or chronological and may not make sense.I.e. there is some sales data to review as a graph and you can set the amount of days you want to look back for data to include in the graph. At the time of writing (2022-02-16) the standard days to look back is 100 and this will show you a nice graph. If you use this in the future the graph might not show data.

### Clean sheet

To start the application without any data you must remove/delete the Database and Uploads folders. Then restart the application. It will then take you through a set-up sequence for a clean sheet.

### Add & Sell products

You can add or sell products either manually, or by using an upload file. There is a template in the Uploads/Template folder for you to use. Fill out some products and add the file to the Uploads/Ready_For_folder. You can do this by following the menu which asks you what to do. You could also use some ready to import files that have some data filled in.

### Get an overview

After you've added stock, generate an overview of your current stock sorted on the key and direction you prefer. you can do this by typing "review inventory" in the main menu.

### Export inventory data

You can export selections of inventory data to a csv file. This file will be in the "Downloads" folder

### Check you financials

After you've made some sales and purchases, please type "review financials" in the main menu to get a graph in your terminal of your financial data. Standard days to look back and fetch data from is 100 and with the template this amount will actually show you a graph. 

## Known issues to resolve:

1. Upload csv files
When uploading a csv file (either sales or addition of products) will break on the first item it comes accross that isn't a correct input

2. Error messages
2.1 When issue 1 happens sometime a positive error message comes through while it should not
2.2 For some error messages need to be customized to user friendly messages.

3. Styling
The terminal styling is not consistent yet

4. Export csv file
The export file will be appended to if it is extracted on the same day

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



