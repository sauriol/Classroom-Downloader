# Classroom-Downloader
Downloads all submissions to an assignment from classroom.

## Current State:
* Downloads ~~only image files~~ anand names them using the student name 
* ~~Has no special way to handle multiple submissions or non-image files~~

## To be done:
* ~~Add options for files other than images~~
* ~~If there are multiple submissions, create a file named after the student and place them there, retaining the original file names~~
* ~~Add way to download files such as Google Docs or Slides, probably using the .export() function~~
* ~~Add options to export as something other than PDF~~

## Setup
1. Go to console.developers.google.com and make sure you are logged in with an account that has Google Apps for Education enabled. Basically, if it's your school issued account or the one you log into Google Classroom with, you're good.
2. Select the button that says "Enable API". It's blue.
3. A list of APIs will pop up. Choose the one called "Google Drive API". You might have to search for it. 
4. Click it and make sure that it's enabled. If it is, the big blue button near the top will say "DISABLE"
5. Do steps 3 and 4 for the Google Classroom API. It's called "Google Classroom API"
6. Navigate to the credentials tab. On the sidebar on the right, click "Credentials". There's a key next to it. 
7. Click "Create Credentials". This will open a little drop down tab. Select "OAuth Client ID"
8. You should now be in a screen labeled "Create Client ID" and there should be a series of radio buttons labeled "Application Type". Select "Other" and enter a name.
9. Hit "Create"
10. A dialog will pop up titled "OAuth Client" with boxes for client ID and client secret. Dismiss it by clicking "OK"
11. You should be back to the Credentials tab now but there should be something underneath a title that says "OAuth 2.0 client IDs"
13. Move the file downloaded in the previous step to the file where this Read Me is located.
