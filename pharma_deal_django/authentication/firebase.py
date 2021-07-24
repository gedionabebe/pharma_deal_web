import pyrebase

config = {
    'apiKey': "AIzaSyCfi5fRVCgXm-OQfgcs_qp08qxo8yWi5oo",
    "authDomain": "pharma-deal-38f66.firebaseapp.com",
    "databaseURL": "https://pharma-deal-38f66-default-rtdb.firebaseio.com",
    "projectId": "pharma-deal-38f66",
    "storageBucket": "pharma-deal-38f66.appspot.com",
    "messagingSenderId": "273572827497",
    "appId": "1:273572827497:web:d88284a73c7df0d06eadf8",
    "measurementId": "G-4YZMM4GKHP"
  }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()