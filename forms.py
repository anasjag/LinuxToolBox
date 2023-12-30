from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField ,validators, TelField, SelectField
from wtforms.validators import InputRequired, DataRequired, ValidationError
import re

class GeneralForm(FlaskForm):
    fname = StringField("First Name:",validators=[InputRequired(),
            validators.Regexp(
            regex=re.compile(r"^[a-zA-Z'-]+$"),
            message='The name should not contain any numbers or special characters.'
        )])
    lname = StringField("Last Name:", validators=[InputRequired(),
            validators.Regexp(
            regex=re.compile(r"^[a-zA-Z'-]+$"),
            message='The name should not contain any numbers or special characters.'
        )])
    #something2
    country_code = SelectField('Country Code',default='962', choices=[ 
    "---","004", "008", "012", "016", "020", "024", "028", "031", "032", "036",
    "040", "044", "048", "050", "051", "052", "056", "060", "064", "068",
    "070", "072", "074", "076", "084", "086", "090", "092", "096", "100",
    "104", "108", "112", "116", "120", "124", "132", "136", "140", "144",
    "148", "152", "156", "158", "162", "166", "170", "174", "175", "178",
    "180", "184", "188", "191", "192", "196", "203", "204", "208", "212",
    "214", "218", "222", "226", "231", "232", "233", "234", "238", "242",
    "246", "248", "250", "254", "258", "262", "266", "268", "270", "275",
    "276", "288", "292", "296", "300", "304", "308", "312", "316", "320",
    "324", "328", "332", "334", "336", "340", "344", "348", "352", "356",
    "360", "364", "368", "372", "376", "380", "384", "388", "392", "398",
    "400", "404", "408", "410", "414", "417", "418", "422", "426", "428",
    "430", "434", "438", "440", "442", "446", "450", "454", "458", "462",
    "466", "470", "474", "478", "480", "484", "492", "496", "498", "499",
    "500", "504", "508", "512", "516", "520", "524", "528", "531", "533",
    "534", "535", "540", "548", "554", "558", "562", "566", "570", "574",
    "578", "580", "581", "583", "584", "585", "586", "591", "598", "600",
    "604", "608", "612", "616", "620", "624", "626", "630", "634", "638",
    "642", "643", "646", "652", "654", "659", "660", "662", "663", "666",
    "670", "674", "678", "682", "686", "688", "690", "694", "702", "703",
    "704", "705", "706", "710", "716", "724", "728", "732", "736", "740",
    "744", "748", "752", "756", "760", "762", "764", "768", "772", "776",
    "780", "784", "788", "792", "795", "796", "798", "800", "804", "807",
    "818", "826", "831", "832", "833", "834", "840", "850", "854", "858",
    "860", "862", "876", "882", "887", "891", "894", "896", "899", "900",
    "901", "902", "903", "904", "905", "906", "907", "908", "909", "910",
    "911", "912", "913", "914", "915", "916", "917", "918", "919", "920",
    "921", "922", "923", "924", "925", "926", "927", "928", "929", "930",
    "931", "932", "933", "934", "935", "936", "937", "938", "939", "940",
    "941", "942", "943", "944", "945", "946", "947", "948", "949", "950",
    "951", "952", "953", "954", "955", "956", "957", "958", "959", "960",
    "961", "962", "963", "964", "965", "966", "967", "968", "969", "970",
    "971", "972", "973", "974", "975", "976", "977", "978", "979", "980",
    "981", "982", "983", "984", "985", "986", "987", "988", "989", "990",
    "991", "992", "993", "994", "995", "996", "997", "998", "999"],
    validators=[ validators.NoneOf(['---'], message='Please select a  country code.')])

    phone = TelField('Phone Number:', validators=[DataRequired(),
            validators.Regexp(
            regex=re.compile(r"^[0-9]{7,}$"),
            message='Please enter a valid phone number with only numerical digits.'
        )])
    
    submit = SubmitField("Save Changes", name="update_profile")
    


class SecurityForm(FlaskForm):
    email = StringField("Email:", validators=[validators.Email(), validators.Optional()])
    password = PasswordField('Password:', validators=[
        validators.Regexp(
            regex=re.compile(r"^(?=.*\d)(?=.*[a-z]).{8,}$"),
            message='Password must be at least 8 characters long and include at least one letter, one number, and one special character'
        ),
        validators.Optional()
    ])
    confirm = PasswordField('Confirm Password:', validators=[
        validators.EqualTo('password', message='Passwords must match')
    ])

    def validate_confirm(form, field):
        if form.password.data and not field.data:
            raise ValidationError('Confirm Password is required when entering a password.')
    submit = SubmitField("Save Changes", name="update2_profile")

class SignupForm(FlaskForm):
    fname = StringField("First Name:",validators=[InputRequired(),
            validators.Regexp(
            regex=re.compile(r"^[a-zA-Z'-]+$"),
            message='The name should not contain any numbers or special characters.'
        )])
    lname = StringField("Last Name:", validators=[InputRequired(),
            validators.Regexp(
            regex=re.compile(r"^[a-zA-Z'-]+$"),
            message='The name should not contain any numbers or special characters.'
        )])
    email = StringField("Email:",validators=[validators.Email(),InputRequired() ])
    password = PasswordField('Password:', validators=[
        validators.DataRequired(),
        validators.Regexp(
            regex=re.compile(r"^(?=.*\d)(?=.*[a-z]).{8,}$"),
            message='Password must be at least 8 characters long and include at least one letter, one number, and one special character'
        )  
    ])
    confirm = PasswordField('Confirm Password:', validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match'),
    ])
    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):
    email = StringField("Email:",validators=[validators.Email(),InputRequired() ])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Regexp(
            regex=re.compile(r"^(?=.*\d)(?=.*[a-z]).{8,}$"),
            message='The password or the email that you have entered is incorrect'
        )  
    ])
    submit = SubmitField("Login")