# Delete previous client files and database
# Parse and fill the database with the data from the input files
# Run the FastAPI server
# Open the scripts in controlled browser instance and print the client
import os
import subprocess
import time

import requests
from selenium import webdriver
import pdfkit

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.base import Base
from models.document import Document
from new_extractor import DocumentGraphExtractor


def delete_previous_data():
    try:
        os.remove("data.db")
        os.removedirs("output")
        os.mkdir("output")
    except:
        pass


def parse_and_fill_database():
    engine = create_engine('sqlite:///data.db', echo=True)
    Base.metadata.create_all(engine)
    files = os.listdir('data')
    with Session(engine) as session:
        for f in files:
            with open(os.path.join('data', f), 'r') as file:
                text = file.read()
                doc = Document(text=text, name=f)
                session.add(doc)
                extractor = DocumentGraphExtractor(doc)
                nodes, edges = extractor.extract_from_text()
                for node in nodes:
                    session.add(node)
                for edge in edges:
                    session.add(edge)

        session.commit()
        session.close()


def run_server():
    try:
        print("Running server")
        subprocess.Popen(["uvicorn server:app --reload"], shell=True)
        time.sleep(2)
    except:
        pass


def run_client_server():
    try:
        print("Running client server")
        subprocess.Popen(["cd client && python -m http.server 8080"], shell=True)
    except:
        pass


def fetch_ids():
    ids = requests.get("http://localhost:8000/documents").json()
    ids = [doc['id'] for doc in ids['documents']]
    return ids


def process_ids(ids):
    for doc_id in ids:
        run_and_print_page(doc_id)


def run_and_print_page(doc_id):
    print("Starting Selenium")
    driver = webdriver.Firefox()
    print("Getting page")
    driver.get(f'http://localhost:8080/?document_id={doc_id}')
    time.sleep(2)
    print("Printing page")
    html = driver.page_source
    try:
        pdfkit.from_string(html, f'output/{doc_id}.pdf')
    except:
        pass
    driver.quit()


def main():
    delete_previous_data()
    parse_and_fill_database()
    # run_server()
    # run_client_server()
    ids = fetch_ids()
    process_ids(ids)


main()
