from app.models import Data_Base, engine
import hashlib
from sqlalchemy.orm import sessionmaker
from requests import HTTPError
from app.mod_auth import FirebaseAuth

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


class Auth(FirebaseAuth):
    """
    Class that handles the authentication variables with Firebase
    firebase_auth gets the configuration dictionary that will be used for authenticating the user
    firebase_db_url contains the database url to Firebase
    firebase_conn connects to the database
    firebase_database connects to the database url, enabling access to the database nodes
    """

    def __init__(self, email, password, phone_no=None):
        """
        :param email: email the user enters in the form
        :param password: password entered by the user
        """
        super(Auth, self).__init__()
        self.email = email
        self.password = password
        self.phone_no = phone_no

    def register_user(self, full_name, username):
        """
        Handles user sign up. The Try...catch block creates a new user with email and password
        Checks if the user already exists in the database and returns true if they do not.
        The user is then created in the database and their credentials are passed to the database
        :param username: auto-generated username
        :param full_name: full name of the user
        :return: :rtype boolean depending on success of the user signing up
        """

        # Hash that Password
        sha1 = hashlib.sha1()
        sha1.update(self.password)
        password = sha1.hexdigest()

        # create a user with email and password, check if the user email already exists
        try:
            auth = self.firebase_auth
            user = auth.create_user_with_email_and_password(self.email, password)
            auth.send_email_verification(user['idToken'])

            self.database_directive(username, full_name)
            return True
        except HTTPError:
            # if the email already exists, return false to display an error in the view
            return False

    @staticmethod
    def register_chama(self, chama_name, chama_members, bank_name, bank_account):
        self.firebase_app.put()

        pass

    def login_user(self):
        """
        :return: Whether the user exists in the auth configurations or whether they are new users
        :rtype Bool
        """
        try:
            self.firebase_auth.sign_in_with_email_and_password(self.email, self.password)
            return True
        except HTTPError:
            return False

    def reset_password(self, email):
        """
        Reset user password on request
        :param email: User email to reset password
        :return:
        """
        # send password reset email
        self.firebase_auth.send_password_reset_email(email=email)

    def database_directive(self, username, full_name):
        """
        Adds the user to the database with the following params
        :param username: the username generated from the user email
        :param full_name: full name of the user
        :return: no return type here
        """

        first_name, last_name = full_name.split(" ")[0], full_name.split(" ")[1]

        self.firebase_app.put(url='/users', name=username, data={
            'firstName': first_name,
            'lastName': last_name,
            'email': self.email,
            'userName': username,
            'phoneNumber': int(self.phone_no)
        }, headers={'print': 'pretty'})
