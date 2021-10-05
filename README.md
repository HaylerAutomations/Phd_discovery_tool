# PhD Discovery Tool
Python script to automate the scraping of FindAPhD.com

## Copy the FindAPhD.com url

Using the filters on FindAPhD.com when you search on FindAPhD.com will generate a specific URL for those parameters (make sure the order of the list is set to newest first). Copy this URL and insert it into the code where appropriate. N.B: I wrote this code for two specific searches however this code can easily be modified to do more or less searches.

## Set up an email account to email the results to you

In order for the script to be able to email you the results, it is best to set up a new email, one that supports app passwords (I would recommend Gmail as there is plenty of guidance online as to how to do this. Generating an app password will allow the script to interact with gmail and pass the html formatted email for sending. It should be obvious in the script where the email addresses and app password are required.

## Automatocally running the script

I ran this script on a MacOS based server so instructions for this step will be MacOS specific, although the linked article will have windows instructions also. In short, this script will need to be converted into a unix executable to be run automatically. Once this has been done, a simple Automator programm will be able to call the executable. Finally this can be called in a time dependent manner using the MacOS calendar: create a new calendar (I called mine: PhD automation) and within that calendar create a repeating event (this can be as frequent as you like (I used thrice daily) with the alert launching the automation program.

## Automation instructions:
https://medium.com/analytics-vidhya/effortlessly-automate-your-python-scripts-cd295697dff6
