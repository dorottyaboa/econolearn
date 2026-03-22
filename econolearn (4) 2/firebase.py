try:
    import streamlit as st
except ImportError:
    # Mock streamlit for testing environments
    class MockSt:
        def error(self, msg): print(f"ST ERROR: {msg}")
        @property
        def session_state(self): return {}
    st = MockSt()

import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from enum import Enum
from datetime import datetime

import os

# Load config
config_path = os.path.join(os.path.dirname(__file__), 'firebase-applet-config.json')
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    # Fallback to current working directory
    try:
        with open('firebase-applet-config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

PROJECT_ID = config.get('projectId', '')
DATABASE_ID = config.get('firestoreDatabaseId', '(default)')
API_KEY = config.get('apiKey', '')

class OperationType(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    LIST = 'list'
    GET = 'get'
    WRITE = 'write'

class FirestoreDB:
    def __init__(self, project_id, database_id, api_key):
        self.project_id = project_id
        self.database_id = database_id
        self.api_key = api_key
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/{database_id}/documents"

    def _request(self, method, path, data=None):
        url = f"{self.base_url}/{path}?key={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(data).encode('utf-8') if data else None
        
        req = Request(url, data=body, headers=headers, method=method)
        try:
            with urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except HTTPError as e:
            error_msg = e.read().decode('utf-8')
            if e.code == 404:
                return None
            raise Exception(f"Firestore Error: {error_msg}")

    def get_doc(self, path):
        return self._request('GET', path)

    def set_doc(self, path, data, merge=True):
        firestore_data = self._to_firestore_format(data)
        return self._request('PATCH', path, firestore_data)

    def _to_firestore_format(self, data):
        fields = {}
        for k, v in data.items():
            if isinstance(v, str):
                fields[k] = {"stringValue": v}
            elif isinstance(v, (int, float)):
                fields[k] = {"doubleValue": v}
            elif isinstance(v, bool):
                fields[k] = {"booleanValue": v}
            elif isinstance(v, list):
                fields[k] = {"arrayValue": {"values": [self._to_firestore_format({"_": x})["fields"]["_"] for x in v]}}
            elif isinstance(v, dict):
                fields[k] = {"mapValue": {"fields": self._to_firestore_format(v)["fields"]}}
            elif v is None:
                fields[k] = {"nullValue": None}
        return {"fields": fields}

    def _from_firestore_format(self, fields):
        data = {}
        for k, v in fields.items():
            if "stringValue" in v:
                data[k] = v["stringValue"]
            elif "doubleValue" in v:
                data[k] = v["doubleValue"]
            elif "integerValue" in v:
                data[k] = int(v["integerValue"])
            elif "booleanValue" in v:
                data[k] = v["booleanValue"]
            elif "arrayValue" in v:
                data[k] = [self._from_firestore_format({"_": x})["_"] for x in v["arrayValue"].get("values", [])]
            elif "mapValue" in v:
                data[k] = self._from_firestore_format(v["mapValue"].get("fields", {}))
            elif "nullValue" in v:
                data[k] = None
        return data

db = FirestoreDB(PROJECT_ID, DATABASE_ID, API_KEY)
auth = None # Mock auth

def googleProvider():
    return "google"

def signInWithPopup(provider):
    user = {
        "uid": "mock_user_123",
        "displayName": "Demo User",
        "photoURL": "https://picsum.photos/seed/user/200",
        "email": "demo@example.com"
    }
    if hasattr(st, 'session_state'):
        st.session_state.user = user
    return user

def onAuthStateChanged(callback):
    if hasattr(st, 'session_state') and "user" in st.session_state:
        callback(st.session_state.user)
    else:
        callback(None)

def doc(db_instance, collection_name, doc_id):
    return f"{collection_name}/{doc_id}"

def collection(db_instance, collection_name):
    return collection_name

def setDoc(doc_path, data, merge=True):
    return db.set_doc(doc_path, data, merge)

def getDoc(doc_path):
    try:
        res = db.get_doc(doc_path)
        return MockDocSnapshot(res)
    except Exception as e:
        raise e

class MockDocSnapshot:
    def __init__(self, data):
        self._raw = data
        self.exists = data is not None

    def data(self):
        if not self._raw or "fields" not in self._raw:
            return None
        return db._from_firestore_format(self._raw["fields"])

def onSnapshot(ref, callback, error_callback=None):
    try:
        if "/" in ref:
            res = getDoc(ref)
            callback(res)
        else:
            callback(MockQuerySnapshot([]))
    except Exception as e:
        if error_callback:
            error_callback(e)

class MockQuerySnapshot:
    def __init__(self, docs):
        self.docs = docs

def query(ref, *args):
    return ref

def orderBy(field, direction="asc"):
    return ("orderBy", field, direction)

def limit(n):
    return ("limit", n)

def serverTimestamp():
    return datetime.utcnow().isoformat() + "Z"

def handleFirestoreError(error, operation_type, path):
    st.error(f"Firestore Error during {operation_type.value} at {path}: {str(error)}")
