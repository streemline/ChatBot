import gspread, time
from oauth2client.service_account import ServiceAccountCredentials

def update_sheet():
    """Получить кортеж из списков триггеров и реакций из гугл таблицы"""
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    #Название документа для редактирования
    sheet = client.open("Название таблицы").sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    #получить число строк
    rows = len(list_of_hashes) + 2
    #циклом с первой до последней строки получить значения для двух списков
    #(каждому индексу триггера соответствует индекс реакции)
    triggers = []
    reactions = []
    for i in range (2, rows):
        try:
        #Получает значение триггеров из строки, форматирует его, обрезая лишние символы и разбивая по символу ;
            trigger = sheet.cell(i,1)
            a = str(trigger).index("'") + 1
            b = str(trigger).index("/")
            trigger = str(trigger)[a:b].split(';')
            #Делает то же самое для реакции
            reaction = sheet.cell(i, 2)
            a = str(reaction).index("'") + 1
            b = str(reaction).index("/")
            reaction = str(reaction)[a:b].split(';')
            triggers.append(trigger)
            reactions.append(reaction)
        except:
            pass
        time.sleep(3)
    return triggers, reactions

if __name__ == '__main__':
    triggers, reactions = update_sheet()
    print(f"Список триггеров: \n {triggers}")
    print(f"Список реакций: \n {reactions}")
