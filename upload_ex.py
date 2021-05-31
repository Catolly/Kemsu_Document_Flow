import openpyxl
import time
book = openpyxl.open("C:\\Users\\pc\\Desktop\\data.xlsx",read_only=True) #change path or replace file in root dict
sheet = book.active
list_with_info = []
dictionary = {}

time1 = time.time()
for row in range (2,sheet.max_row+1):
    dictionary.update({"Fullname":sheet[row][0].value, "Gender": sheet[row][1].value, "Group": sheet[row][2].value,
                       "Institute": sheet[row][3].value, "Cours":sheet[row][4].value,
                       "Year of admission": sheet[row][5].value, "Specialty code": sheet[row][6].value,
                       "Specialty":sheet[row][7].value,"Lvl":sheet[row][8].value,
                       "Form of education":sheet[row][9].value,"Training period":sheet [row][10].value,
                       "Competition":sheet [row][11].value,"Academic year":sheet [row][12].value,
                       "Status":sheet [row][13].value})

    list_with_info.append(dictionary)
    dictionary={}
    print(row)
time2= time.time()
print(time2-time1)


