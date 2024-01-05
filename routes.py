from flask import (
    Flask,
    render_template,
    request,
    current_app,
    Blueprint,
    redirect,
    session,
    flash,
    url_for,
    make_response,
)
from datetime import date
import xmltodict
import ast
import socket
import pdfkit
import uuid
import functools
from forms import *
import subprocess
from models import Users , Scans, Pings
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
    return render_template("home.html", title=f"Home - ")

def scan_page(scan_id, scan_ip):
    scan_data = current_app.db.scans.find_one({"_id": scan_id})

    if scan_data and "data" in scan_data:
        scan_result = scan_data["data"]
        return render_template("scan.html", scan_result=scan_result, ip=scan_ip)
    else:
        # Handle the case when data is not available or has unexpected structure
        return render_template("scan.html", scan_result=None)

@pages.route("/login.html", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect("home.html")
    form = LoginForm()
    if form.validate_on_submit():
        user_data = current_app.db.users.find_one({"email": form.email.data})
        if not user_data:
            flash(
                "The password or the email that you have entered is incorrect",
                category="danger",
            )
            return redirect("login.html")
        user = Users(**user_data)
        if (
            user and form.password.data == user.password
        ):  # should be || pdkf2_sha256.verify(form.password.data,user.password)
            session["user_id"] = user._id
            session["email"] = user.email

            return redirect("home.html")

        flash(
            "The password or the email that you have entered is incorrect",
            category="danger",
        )

    return render_template("login.html", title=f"Login - ", form=form)


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
            password=form.password.data,  # should be hashed using a secure method
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
                {
                    "$set": {
                        "fname": form.fname.data,
                        "lname": form.lname.data,
                        "country_code": form.country_code.data,
                        "phone": form.phone.data,
                    }
                },
            )
            flash("Profile updated successfully!", category="success")
        return redirect("general.html")

    if user_data:
        form.fname.default = user_data.get("fname")
        form.lname.default = user_data.get("lname")
        form.country_code.default = user_data.get("country_code", "---")
        form.phone.default = user_data.get("phone")
    return render_template("general.html", title=f"Profile - ", form=form)


@pages.route("/security.html", methods=["GET", "POST"])
@login_required
def security():
    user_data = current_app.db.users.find_one({"_id": session["user_id"]})

    form = SecurityForm(request.form, obj=user_data)
    form.email.default = user_data.get("email")
    form.password.default = (
        user_data.get("password")
        if form.password.default is None
        else form.password.data
    )
    if form.validate_on_submit():
        if "update2_profile" in request.form:
            # Update user data in MongoDB
            current_app.db.users.update_one(
                {"_id": session["user_id"]},
                {
                    "$set": {
                        "email": form.email.data,
                        "password": form.password.data
                        if form.password.data
                        else form.password.default,
                    }
                },
            )
            if form.email.data != form.email.default:
                flash("Email changed successfully!", category="success")
            if form.password.data != "":
                flash("Password changed successfully!", category="success")
            return redirect("security.html")
    form.process
    return render_template("security.html", title=f"Profile - ", form=form)
@pages.route("/ping.html", methods=["GET", "POST"])
def ping_page(): 
    form = PingForm()
    if form.validate_on_submit():
        show_modal = True
        target_ip = form.targetForm.data
        return render_template("ping.html",  title = f"Ping - ", form=form, show_modal=show_modal, target_ip=target_ip)
    return render_template("ping.html", form=form, show_modal=False)

@pages.route("/ping/<target_ip>", methods=["GET", "POST"])
def ping(target_ip):
    
    ping_command = ['ping', '-c', '5', target_ip]
    ping_output = subprocess.run(ping_command, capture_output=True).stdout.decode('utf-8')
    scan = Pings(
            _id=uuid.uuid4().hex,
            data=ping_output,
            date= str(date.today()),
            status='success' if ping_output is not None else 'faild',
            ip=target_ip,
            tool_name="Ping"
        )
    current_app.db.scans.insert_one(asdict(scan))

    if session.get("email"):
        current_app.db.users.update_one(
            {"_id": session["user_id"]}, {"$push": {"scans": scan._id}}
        )
    
    return render_template('ping_result.html', scan_result=ping_output, ip=target_ip)

@pages.route("/tools.html", methods=["GET", "POST"])
def tools():
    form= ToolsForm()
    if form.validate_on_submit():
        target_ip = form.targetForm.data
        command = ['nmap']
        if form.svCheck.data:
            command.append('-sV')
        if form.osCheck.data:
            command.append('-O')
        if form.radio_field.data == 'Common ports':
            if form.topPorts.data == 'option1':
                command.append('--top-ports')
                command.append('10')
            elif form.topPorts.data == 'option2':
                command.append('--top-ports')
                command.append('100')
            else:
                command.append('--top-ports')
                command.append('1000')
        else:
            command.append('-p')
            command.append(f'{form.listPorts.data}')
        command.append('-oX')
        command.append('-')
        command.append(socket.gethostbyname(target_ip))
        form.process()
        return render_template("tools.html", form=form, show_modal=True, command=command, target_ip=target_ip)
    return render_template("tools.html", form=form, show_modal=False)

@pages.route("/scan/<command>/<target_ip>", methods=["GET", "POST"])
def scan(command,target_ip):
    
    command = ast.literal_eval(command) 
    xml_scan = subprocess.run(command, capture_output=True)
    nmap_output = xml_scan.stdout.decode('utf-8')

    # Parse XML string to a Python dictionary
    dict_data = xmltodict.parse(nmap_output)
    scan = Scans(
            _id=uuid.uuid4().hex,
            date= str(date.today()),
            status=dict_data['nmaprun']['runstats']['finished']['@exit'],
            ip=target_ip,
            data=dict_data,
            tool_name="Nmap"
        )
    current_app.db.scans.insert_one(asdict(scan))

    if session.get("email"):
        current_app.db.users.update_one(
            {"_id": session["user_id"]}, {"$push": {"scans": scan._id}}
        )

    scan_data = current_app.db.scans.find_one({"_id": scan._id})

    if scan_data and 'data' in scan_data:
        scan_result = scan_data['data']
        if 'nmaprun' not in scan_result or 'host' not in scan_result['nmaprun'] or 'ports' not in scan_result['nmaprun']['host'] or 'port'not in scan_result['nmaprun']['host']['ports']:
            current_app.db.scans.update_one(
                {"_id": scan._id}, {"$set": {"status": "faild"}}
            )
        return render_template('scan.html', scan_result=scan_result, ip=target_ip)


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

def scan_page(scan_id, scan_ip):
    scan_data = current_app.db.scans.find_one({"_id": scan_id})
        
    if scan_data and 'data' in scan_data:
        if scan_data['tool_name']== 'Nmap':
            scan_result = scan_data['data']
            return render_template('scan.html', scan_result=scan_result, ip=scan_ip)
        else:
            scan_result = scan_data['data']
            return render_template('ping_result.html', scan_result=scan_result, ip=scan_ip)
    
@pages.route("/handle_action/<action_type>/<scan_id>/<scan_ip>")
def handle_action(action_type, scan_id, scan_ip):
    if action_type == "download_btn":
        rendered_html = scan_page(scan_id, scan_ip)
         # Use pdfkit.from_string to generate the PDF content
        pdf = pdfkit.from_string(rendered_html)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] =f'attachment; filename={scan_ip}.pdf'

        return response
    elif action_type == "showResult_btn":
        scan_data = current_app.db.scans.find_one({"_id": scan_id})
        
        if scan_data and 'data' in scan_data:
            if scan_data['tool_name']== 'Nmap':
                scan_result = scan_data['data']
                return render_template('scan.html', scan_result=scan_result, ip=scan_ip)
            else:
                scan_result = scan_data['data']
                return render_template('ping_result.html', scan_result=scan_result, ip=scan_ip)
    elif action_type == "remove_btn":
        current_app.db.scans.delete_one({"_id": scan_id})
        current_app.db.users.update_one(
            {"scans": scan_id},
            {"$pull": {"scans": scan_id}}
        )
    return redirect(url_for("pages.history"))
@pages.route("/logout")
def logout():
    session.clear()

    return redirect("login.html")

