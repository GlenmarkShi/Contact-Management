import json
import os
import re
import time
from pymongo import MongoClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ContactHandler(FileSystemEventHandler):
    def __init__(self, db):
        self.db = db

    def process_file(self, filepath):
        temp_filepath = filepath + '.tmp'

        try:
            with open(filepath, 'r') as f:
            #try:
                contacts = json.load(f)
                for contact in contacts:
                    self.validate_contact(contact)
                    self.normalize_phone(contact)
                    self.insert_contact(contact)
                
            self.delete_file(filepath)
            print(f"Processed and deleted file: {filepath}")
        except (ValueError, KeyError) as e:
            print(f"Error processing file {filepath}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_file(self, filepath):
        # Attempt to delete the file and handle any potential errors
        try:
            os.remove(filepath)
            print(f"Processed and deleted file: {filepath}")
        except OSError as e:
            print(f"Error deleting file {filepath}: {e}")
            # Optional: Implement a retry mechanism if desired
            time.sleep(1)  # Wait a moment before trying again
            

    def validate_contact(self, contact):
        if 'name' not in contact or 'email' not in contact or 'phone' not in contact:
            raise ValueError("Contact must have name, email, and phone.")
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", contact['email']):
            raise ValueError("Invalid email format.")
        
        if self.db.contacts.find_one({"email": contact['email']}):
            raise ValueError("Email must be unique.")

    def normalize_phone(self, contact):
        digits= re.sub(r'\D', '', contact['phone'])  # Normalize to digits only

        # Check if the number has the correct length for US phone numbers
        if len(digits) == 10:
            # Format the phone number in the "+1-XXX-XXX-XXXX" format
            contact['phone'] = f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits.startswith('1'):
            # If the number has 11 digits and starts with '1', format accordingly
            contact['phone'] = f"+{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
        else:
            raise ValueError("Invalid phone number format. Expected 10 or 11 digits.")

    def insert_contact(self, contact):
        self.db.contacts.insert_one(contact)

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.contacts

    path = '/xampp/htdocs/Glenmark/contacts-api/api/storage/app/contacts/'
    observer = Observer()
    handler = ContactHandler(db)
    observer.schedule(handler, path, recursive=False)
    
    observer.start()
    print(f"Watching for changes in {path}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
