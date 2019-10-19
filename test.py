import unittest
from app import app
from flask import request
import json


class Test_Tshirt(unittest.TestCase):

    def setUp(self):

        app.testing = True
        self.client = app.test_client()

    # function of log out

    def test_logout(self):
            return self.client.get('/logout', follow_redirects=True)

    # function of login

    def test_login_incorrect_credentials(self):
        response = self.client.post("/login", data={"username": "stn131415", "password": "111"})
        assert b'Incorrect username or password' in response.data

    def test_login_incorrect_username(self):
        response = self.client.post("/login", data={"username": "stnds41", "password": "dsdsd"})
        assert b'Incorrect username or password' in response.data

    def test_test_login_logout(self):
         response = self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
         assert b'Login Success!' in response.data
         rv=self.test_logout()
         assert b'log in' in rv.data

    # function of register

    def test_register_login(self):
            rv = self.client.post('/register', data=dict(
                username='Test',
                password='Hema7067',
                cfm_password='Hema7067'
            ), follow_redirects=True)
            assert b'You were successfully registered' in rv.data
            response = self.client.post("/login", data={"username": "Test", "password": "Hema7067"})
            assert b'Login Success!' in response.data


    def test_register_invalid_password(self):
        rv = self.client.post('/register', data=dict(
            username='test',
            password='test',
            cfm_password='test'
        ), follow_redirects=True)
        assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data

    def test_register_password_match(self):
        rv = self.client.post('/register', data=dict(
            username='test',
            password='test',
            cfm_password='test3333'
        ), follow_redirects=True)
        assert b'Passwords do not match' in rv.data

    def test_registered_users(self):
        rv = self.client.post('/register', data=dict(
            username='stn131415',
            password='test',
            cfm_password='test3333'
        ), follow_redirects=True)
        assert b'User already registered' in rv.data

    def test_registered_Invalid_password1(self):
        rv = self.client.post('/register', data=dict(
            username='Test',
            password='stnstnst',
            cfm_password='stnstnst'
        ), follow_redirects=True)
        assert b'Register new user' in rv.data

    def test_registered_Invalid_password2(self):
        rv = self.client.post('/register', data=dict(
            username='Test',
            password='12345678',
            cfm_password='12345678'
        ), follow_redirects=True)
        assert b'Register new user' in rv.data

     # function of user info
    def test_userinf(self):
        self.client.post("/login", data={"username": "Test", "password": "Hema7067"})
        rv = self.client.post('/adduserdetail', data=dict(
            email='tsun2233@uni.sydnet.edu.au',
            age = 25,
            weight = 60,
            address1 = 'burwood',
            postcode = '2134',
            city = 'sydney',
            gender='f',
            firstName='leo',
            lastName = 'sun',
            phone = '213213213'
        ), follow_redirects=True)
        assert b'add user info Success!' in rv.data
        self.test_logout()

     # update of user info
    def test_userinf_update(self):
        self.client.post("/login", data={"username": "Test", "password": "Hema7067"})
        rv = self.client.post('/updateProfile', data=dict(
            email='mche@uni.sydnet.edu.au',
            age = 22,
            weight = 37,
            address1 = 'strathfield',
            postcode = '2134',
            city = 'sydney',
            phone = '362763721'
        ), follow_redirects=True)
        assert b'update success' in rv.data

    #Fseedback
    def test_userinf_update(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv = self.client.post('/feedbacks', data=dict(
            Contact='Email',
            Subject='General Question',
            mesaage='my test'
        ), follow_redirects=True)
        assert b'send feedback success' in rv.data

    #history page
    def test_history(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv=self.client.get('/history', follow_redirects=True)
        assert b'historydata page' in rv.data


    # temp history
    def test_usertepm_history(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv=self.client.get('/get_history_temp',follow_redirects=True)
        assert b'date' in rv.data

    # bpm history
    def test_userbpm_history(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv=self.client.get('/get_history_bpm',follow_redirects=True)
        assert b'date' in rv.data

    # spo history
    def test_userspo_history(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv = self.client.get('/get_history_spo', follow_redirects=True)
        assert b'date' in rv.data

    # realtime page
    def test_realtime(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv = self.client.get('/realtime', follow_redirects=True)
        assert b'realtime page' in rv.data

     # temp realtime

    def test_usertepm_realtime(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv = self.client.get('/get_temp/', follow_redirects=True)
        assert b'date' in rv.data

        # bpm realtime

    def test_userbpm_realtime(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv = self.client.get('/get_bpm/', follow_redirects=True)
        assert b'date' in rv.data

        # spo realtime

    def test_userspo_realtime(self):
        self.client.post("/login", data={"username": "stn131415", "password": "Stn131415~"})
        rv = self.client.get('/get_spo/', follow_redirects=True)
        assert b'date' in rv.data


if __name__ == '__main__':
    unittest.main()
