import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Whats:
    def __init__(self):
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        try:
            creds_path = os.environ.get("CREDS_JSON_PATH")
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, self.scope)
        except:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", self.scope)

        self.client = gspread.authorize(self.creds)
        
        self.sheet_title = "Whats"
        self.sheet = self.client.open(self.sheet_title).sheet1  # Use the appropriate sheet index if not the first sheet
        
        self.all_rows = self.sheet.get_all_values()
        self.col_one = []
        self.col_two = []
        self.col_three = []
        self.col_four = []

        self.fill_lists()

    def fill_lists(self):
        for row in self.all_rows[1:]:
            self.col_one.append(row[0])
            self.col_two.append(row[1])
            self.col_three.append(row[2])
            self.col_four.append(row[3])
        return self.col_one, self.col_two, self.col_three, self.col_four


    def send_message(self, row_index, value):
        # Update the cell in the 5th column of the specified row with the given value
        row_index += 2
        self.sheet.update_cell(row_index, 5, value)
        print("Value '{}' added to the 5th column of row {}.".format(value, row_index))





# wh = Whats()

# print(wh.col_one)