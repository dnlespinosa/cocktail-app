# COCKTAIL HOUR
This is an HTML/CSS/Python/Flask project for Springboard Academy. Cocktail Hour is an application that interacts with TheCocktailDB public API and contains the following pages:
* Home Page 
* User Register/Login/Logout Page
* User Profile Page
* Search page that contains - search for a cocktail by name or ingriedents
* A description page where each cocktail's recipe and instructions can be found

## The Project Structure 
* app.py contains all of the API calls and routes for the web page
* forms.py contains all of the user creation and search forms 
* models.py contains all of the information of our cocktail database
* templates contains
    * index.html - home page
    * liquorsearch.html - holds the search for cocktail by liquor form
    * liquor.html - displays the search results for the search by liquor form 
    * search.html - holds the search for cocktail by name form
    * popularDrink.html - displays the requested drink details: name, ingredients, instructions
    * randomDrink.html - displays a random drink details: name, ingredients, instructions
    * users contains
        * login.html - contains the user login page
        * register.html - contains the user register page referencing the signup function in models.py
        * userInfo.html - contains the user's profile page 

## Project Features 
* When the page loads, the user can be prompted to create an account or login to an account. There are 3 available tabs to find a cocktail by: generate random, search by name, search by type of liquor. Below the search tabs are a list of 20 of the most popular cocktails 
* When the user clicks a drink link, searches by name or generates a random drink, they will be redirected to that drink's detail page where they will get all info regarding ingredients and instructions
* On each drink page, there is a button to favorite the drink. That drink will be stored in FavoriteDrink database along with the user's ID number. That link will be available on the user's profile page for them to reference when they want to 

## Install 
To get started you can simply clone the repo and install the dependencies in the requirements.txt file
- git clone https://github.com/dnlespinosa/capstone.git
- cd capstone
- pip install -r requirements.txt
- flask run

Open http://localhost:5000 to view the page