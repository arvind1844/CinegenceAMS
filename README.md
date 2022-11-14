# Cinegence AMS

Introduction:
This is the pipeline for easy execution and hiring of freelancers through the website.
Initially, the user will be directed to the home page where the user can view the company and all the static information without login. 
In the navbar, there are options to view all assets, user profile, contact, and login/signup button. Once the user is logged in they are able to view all the pages. On all assets page the postcards of an asset are given with some information once the user chooses the asset they are redirected to a single asset page where there is detailed information of the asset if the user wants to work on that asset they can easily apply to the form given at the end of the page where they need to submit work details with resume and mail will be sent to admin and task will be assigned to the user.

Backend Dependencies:
asgiref==3.5.0
certifi==2021.10.8
charset-normalizer==2.0.11
Django==3.2.11
idna==3.3
Pillow==9.0.1
pytz==2021.3
requests==2.27.1
six==1.16.0
sqlparse==0.4.2
urllib3==1.26.8


Database Dependencies: 
sqlite3


Frontend Dependencies:
HTML 5
CSS 3
Bootstrap
JavaScript


Pages:

Dynamic:-
Register, login page: For authenticating a user which has name, address, email, contact details
Home page: Containing a list of the latest 3 assets and static content about the company, founder etc.
A page showing all assets to work on which is dynamic and updated via an admin.
An individual asset page containing a detailed description of what work needs to be done and a work detail form that needs the user to fill in Aadhar number, resume, and work link.
Contact page for getting in touch with the organization.
User profile page containing personal and work details of the user
Password reset functionalities in case the user forgets his/her password
