import json
import os

class DataManager:
    def __init__(self, path = 'data.json'):
        self.path = path
        
    def get(self):
        if not os.path.exists(self.path):
            return dict()
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Data file is corrupted. Starting with empty data.")
            return dict()
        except Exception as e:
            print(f"Error reading data file: {e}")
            return dict()

    def set(self, data):
        try:
            dir_name = os.path.dirname(self.path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(self.path, 'w') as f:
                json.dump(data, f, indent=4)
            print('Data saved successfully!')
        except Exception as e:
            print(f"Error saving data: {e}")
       
