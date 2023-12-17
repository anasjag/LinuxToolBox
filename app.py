from flask import Flask, render_template, request
from pymongo import MongoClient 
import os, subprocess

def create_app():
    
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.LinuxToolBox
    
    

    @app.route("/", methods=["GET", "POST"])
    def start():
        return render_template("home.html")
    @app.route("/home.html", methods=["GET", "POST"])
    def home(): 
        title = f"Home - "
        return render_template("home.html", title=title)
    @app.route("/tools.html", methods=["GET", "POST"])
    def tools():
        return render_template("tools.html")
    @app.route("/general.html", methods=["GET", "POST"])
    def general():
        return render_template("general.html")
    @app.route("/history.html", methods=["GET", "POST"])
    def history():
        return render_template("history.html")
    @app.route("/login.html", methods=["GET", "POST"])
    def login():
        return render_template("login.html")
    @app.route("/signup.html", methods=["GET", "POST"])
    def signup():
        return render_template("signup.html")
    @app.route("/security.html", methods=["GET", "POST"])
    def security():
        return render_template("security.html")
    @app.route("/scan.html", methods=["GET", "POST"])
    def scan():
        return render_template("scan.html")
    @app.route("/sss", methods=["GET", "POST"])
    def nmap_scan():
       
        target_ip = "192.168.1.9"
        
        
        subprocess.run(['nmap', '-oX', 'templates/nmaptest.xml', target_ip])

        subprocess.run(['xsltproc', 'templates/nmaptest.xml', '-o', 'templates/nmaptest.html'])
        return render_template('nmaptest.html')
    @app.route("/nmap", methods=["GET", "POST"])
    def pop_result():
        return render_template("nmaptest.html") 


    return app 