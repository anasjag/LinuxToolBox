#README

## Project Overview

LinuxToolBox is a user-friendly web platform designed to provide seamless access to essential Linux tools. Developed as a graduation project for the Bachelor of Computer Science degree at Al-Balqa Applied University, this platform aims to bridge the gap between complex command-line interfaces and user-friendly web interfaces, making Linux tools more accessible to both beginners and experienced users.


## Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- Bootstrap 

## Installation

1. Clone the repository: `git clone https://github.com/anasjag/LinuxToolBox.git`
2. Navigate to the project directory: `cd LinuxToolBox`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: 
     ```
     venv\Scripts\activate
     set FLASK_ENV=development
     set FLASK_APP=app.py
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     export FLASK_ENV=development
     export FLASK_APP=app.py
     ```
5. Install dependencies: `pip install -r requirements.txt`
6. Install Nmap:
   - For Linux: `sudo apt-get install nmap`
   - For macOS (using Homebrew): `brew install nmap`
   - For Windows: Download the installer from [Nmap.org](https://nmap.org/download.html) and follow the installation instructions.
7. Create a `.env` file in the root directory of the project and add the following variables:
   - MONGODB_URI="your_mongodb_uri"
   - MONGODB_DB="your_database_name"
Replace `"your_mongodb_uri"` with your actual MongoDB URI and `"your_database_name"` with your desired database name.
8. Start the Flask development server: `sudo flask run` *Note: For certain functionalities like OS detection using Nmap, you may need to run the command prompt as an administrator using `sudo`.*


## Usage

1. Open your web browser.
2. Enter the following URL in the address bar: `http://127.0.0.1:5000`
3. Explore the different pages and features of the website.
