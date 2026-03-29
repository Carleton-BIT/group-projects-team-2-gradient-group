### Group 2: Gradient Group
# Raven's Bargain
A marketplace for Carleton University students to save money on textbooks.

## Features
- Students can create users accounts using their cmail addresses.
- Users can view and edit thier profiles.
- Users can message other users.
- Users can create product listings.
- Users can purchase listed products.

<img width="1855" height="952" alt="Screenshot 2026-02-28 123115" src="https://github.com/user-attachments/assets/ed264322-f580-48a7-bec8-10636efa7ad3" />

## Installation
1. **Make sure you have Python and Git installed.**
2. Clone this repository either by using the command line or using PyCharm's built in repository cloner:
`$ git clone https://github.com/Carleton-BIT/group-projects-team-2-gradient-group.git`
3. Once you have properly installed the project, open it up in PyCharm and a pop-up should appear telling you to create a virtual environment, just click OK.
   
![create-virtual-environment](https://github.com/user-attachments/assets/3c2e0cdc-727b-455b-8097-291a44c62864)

4. Next, type `pip install -r requirements.txt` into the terminal to install the requirements of the project.
5. Create a file called `.env` in the top level directory (should be in the same folder as manage.py)
6. In the terminal, run `python manage.py migrate`
7. Run the server by clicking the play button or running `python manage.py runserver` in the terminal
8. Navigate to 127.0.0.1:8000! The project should be running in your web browser.

## Usage
### Creating an account
- On the homepage you will see a hero section with the website's name, a description of it, and two buttons saying "Create account" and "Log in."
- Click the "Create account" button to be redirected to the sign up page.
- Create an account which follows the guidelines provided on the page.
- Once you are done creating an account it will redirect you to the main page where you now how full access to the website.
### Creating a product listing
- On the navigation bar there will now be two new options, 'create listing' and 'Hello, [ your profile name ]'.
- Clicking on your profile name will redirect you to your profile page, right now there shouldn't be any products yet because you haven't created a listing.
- Clicking on 'create listing' will redirect you to a product creation page, fill out the form with the required information and click the Create Product button. 
- Once you have successfully created a product listing you should be able to see the listing under which ever category you set it to.
### User profile and listings
- Now that you have created a product listing, it will appear in your user profile.
- Navigate to your profile page, then click on 'My listings'.
- You can view your created listings. When you are viewing your own product listing there will be a delete button where you can delete the listing.
### Browse listings
- On the homepage you are able to see the latest listings that have been uploaded to the website.
- Above the latest listings section there is a search bar and category filter. You can either filter by keyword or product category... or both.
- There is also a view all button to see all the products sorted from newest to oldest.
### Saving listings
- On product listings there will be a star icon which you can click to save it for later.
- To view your starred listings navigate to your profile and click 'Saved items' to view all the listings you have saved.
