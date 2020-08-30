import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SheetsBot:

    def __init__(self, listOfIds):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'client_secret.json', scope)
        client = gspread.authorize(creds)

        # Replace with name of google sheets file
        sheet = client.open('Sunset Series Point Collection Sheet')
        self.gameWorksheet = sheet.worksheet("VAL")
        self.ids = listOfIds
        self.inputWorksheet = sheet.worksheet("Input")

    # Replace with the date you want to update
    def updateGameTabCells(self, date):
        date_cell = self.gameWorksheet.find(date)
        row_number = date_cell.row
        column_number = date_cell.col
        for i in range(len(self.ids)):
            temp = self.gameWorksheet.cell(row_number + 1, column_number).value
            if len(temp):
                listOfCurrentUsers = self.gameWorksheet.col_values(
                    column_number)
                isUserAlreadyInList = False
                for user in listOfCurrentUsers:
                    if user == self.ids[i]:
                        isUserAlreadyInList = True
                if not isUserAlreadyInList:
                    lastRowWithValues = len(listOfCurrentUsers)
                    self.gameWorksheet.update_cell(
                        lastRowWithValues + 1, column_number, self.ids[i])
            else:
                self.gameWorksheet.update_cell(
                    i + 1 + row_number, column_number, self.ids[i])

    def updatePointSystem(self, date, points):
        date_cell = self.inputWorksheet.find(date)
        column_number = date_cell.col
        for i in range(len(self.ids)):
            try:
                user_cell = self.inputWorksheet.find(self.ids[i])
                self.inputWorksheet.update_cell(
                    user_cell.row, column_number, points)
            except:
                lastRowWithValues = len(self.inputWorksheet.col_values(1))
                self.inputWorksheet.update_cell(
                    lastRowWithValues + 1, 1, self.ids[i])
                self.inputWorksheet.update_cell(
                    lastRowWithValues + 1, column_number, points)
