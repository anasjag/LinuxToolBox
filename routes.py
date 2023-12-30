from flask import (
    Flask, 
    render_template, 
    request, 
    current_app, 
    Blueprint,
    redirect,
    session,
    flash,
    url_for
    )
from datetime import date
import xmltodict
import uuid
import functools
from forms import *
import subprocess
from models import Users , Scans
from dataclasses import asdict

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)
def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect("login.html")

        return route(*args, **kwargs)

    return route_wrapper

@pages.route("/", methods=["GET", "POST"])
def start():
    return redirect("home.html")

@pages.route("/home.html", methods=["GET", "POST"])
def home(): 
    return render_template("home.html",  title = f"Home - ")

@pages.route("/tools.html", methods=["GET", "POST"])
def tools():
    return render_template("tools.html",  title = f"Tools - ")

@pages.route("/history.html", methods=["GET", "POST"])
@login_required
def history():
    user_data = current_app.db.users.find_one({"_id": session["user_id"]})
    data = user_data['scans']
    
    scanned_data = []
    for scan in data:    
        scan_data = current_app.db.scans.find_one(
            {"_id": scan},
            {"data": 0}
        )
        if scan_data:
            scanned_data.append(scan_data)

    search_query = request.args.get("search_query", "").lower()
    scanned_data = [
        data for data in scanned_data
        if search_query in data["ip"].lower()
        or search_query in data["date"].lower()
        or (search_query in "success" and data["status"].lower() in "success")
        or (search_query in "fail" and data["status"].lower() in "fail")
    ]
    
    return render_template(
        "history.html", scanned_data=scanned_data, search_query=search_query,title = f"History - "
    )


@pages.route("/handle_action/<action_type>/<scan_id>/<scan_ip>")
def handle_action(action_type, scan_id, scan_ip):
    if action_type == "download_btn":
        print(f"download_btn clicked for item with ID {scan_id}")
    elif action_type == "showResult_btn":

        scan_data = current_app.db.scans.find_one({"_id": scan_id})
        
        if scan_data and 'data' in scan_data:
            
            scan_result = scan_data['data']
            return render_template('scan.html', scan_result=scan_result, ip=scan_ip)
        else:
            # Handle the case when data is not available or has unexpected structure
            return render_template('scan.html', scan_result=None)
        
    elif action_type == "remove_btn":
        print(f"remove_btn clicked for item with ID {scan_id}")
    return redirect(url_for("pages.history"))


@pages.route("/login.html", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect("home/html")
    form = LoginForm()
    if form.validate_on_submit():
        user_data = current_app.db.users.find_one({"email":  form.email.data})
        if not user_data:
            flash("The password or the email that you have entered is incorrect", category="danger")
            return redirect("login.html")
        user = Users(**user_data)
        if user and form.password.data == user.password: #should be || pdkf2_sha256.verify(form.password.data,user.password)
            session["user_id"]= user._id
            session["email"]= user.email
            
            return redirect("home.html")

        flash("The password or the email that you have entered is incorrect", category="danger")
       # Print flash messages for debugging
     
    return render_template("login.html", title = f"Login - ",form=form)

@pages.route("/signup.html", methods=["GET", "POST"])
def signup():
    if session.get("email"):
        return redirect("home.html")
    
    form = SignupForm()

    if form.validate_on_submit():

        user = Users(
            _id=uuid.uuid4().hex,
            fname=form.fname.data,
            lname=form.lname.data,
            email=form.email.data,
            password=form.password.data  # should be hashed using a secure method
        )
        current_app.db.users.insert_one(asdict(user))
        flash("User registered successfully", category="success")
        return redirect("login.html")
    
    return render_template("signup.html", title = f"Signup - ", form=form)
    
@pages.route("/general.html", methods=["GET", "POST"])
@login_required
def general():
    # Fetch user data from MongoDB
    user_data = current_app.db.users.find_one({"_id": session["user_id"]})
    # user = Users(**user_data) if user_data else None

    # Create a form and set default values if user data is available
    form = GeneralForm(request.form, obj=user_data) if user_data else GeneralForm()

    if form.validate_on_submit():
        # Check the btn if clicked based on the name from the form
        if "update_profile" in request.form:

            # Update user data in MongoDB
            current_app.db.users.update_one(
                {"_id": session["user_id"]},
                {"$set": {
                    "fname": form.fname.data,
                    "lname": form.lname.data,
                    "country_code": form.country_code.data,
                    "phone": form.phone.data,
                }}
            )
            flash('Profile updated successfully!',  category='success')
        return redirect("general.html")
    
    if user_data:
        form.fname.default = user_data.get('fname')
        form.lname.default = user_data.get('lname')
        form.country_code.default = user_data.get('country_code', '---')
        form.phone.default = user_data.get('phone')
    return render_template("general.html",  title = f"Profile - ", form=form)

@pages.route("/security.html", methods=["GET", "POST"])
@login_required
def security():
    user_data = current_app.db.users.find_one({"_id": session["user_id"]})
    
    form = SecurityForm(request.form, obj=user_data)
    form.email.default = user_data.get('email')
    form.password.default = user_data.get('password') if form.password.default is None else form.password.data
    if form.validate_on_submit():
       
        if "update2_profile" in request.form:
            # Update user data in MongoDB
            current_app.db.users.update_one(
                {"_id": session["user_id"]}, 
                {"$set": {
                    "email": form.email.data,
                    "password": form.password.data if form.password.data else form.password.default
                }}
            )
            if form.email.data != form.email.default:
                flash('Email changed successfully!', category='success')
            if form.password.data != "":
                flash('Password changed successfully!', category='success')
            return redirect("security.html")
    form.process
    return render_template("security.html", title=f"Profile - ", form=form)

@pages.route("/scan", methods=["GET", "POST"])
def nmap_scan():
    
    target_ip = "192.168.1.6"
    
    xml_scan = subprocess.run(['nmap', '-O', '-sV', '-oX', '-', target_ip], capture_output=True)
    nmap_output = xml_scan.stdout.decode('utf-8')

    # Parse XML string to a Python dictionary
    dict_data = xmltodict.parse(nmap_output)

    scan = Scans(
            _id=uuid.uuid4().hex,
            date= str(date.today()),
            status=dict_data['nmaprun']['runstats']['finished']['@exit'],
            ip=target_ip,
            data=dict_data
        )
    current_app.db.scans.insert_one(asdict(scan))

    if session.get("email"):
        current_app.db.users.update_one(
            {"_id": session["user_id"]}, {"$push": {"scans": scan._id}}
        )

    scan_data = current_app.db.scans.find_one({"_id": scan._id})
    
    if scan_data and 'data' in scan_data:
        
        scan_result = scan_data['data']
        return render_template('scan.html', scan_result=scan_result, ip=target_ip)
    else:
        # Handle the case when data is not available or has unexpected structure
        return render_template('scan.html', scan_result=None)

@pages.route("/logout")
def logout():
    session.clear()

    return redirect("login.html")
