import urllib.request
import xlsxwriter
import os


#comment out the next 4 lines if you don't want to download 3 pictures
# url = 'https://upload.wikimedia.org/wikipedia/en/thumb/4/43/Ipswich_Town.svg/255px-Ipswich_Town.svg.png'
# urllib.request.urlretrieve(url, "pica_1.png")
# urllib.request.urlretrieve(url, "picb_2.png")
# urllib.request.urlretrieve(url, "picc_3.png")


dir_wanted = os.getcwd()
#uncomment the following line if you don't want the current directory
#dir_wanted = "C:\\users\\doe_j"
path = "C:/Users/amitk/Desktop/py_lib/roll-award-sample/roll-award-sample/roll/11006"
# dir_list = os.listdir(path)
 
# counter = 1
# for x in dir_list:
#     if x.endswith(".tif"):

file_list = [file for file in os.listdir(path) if file.endswith('.tif')]
full_path_list = [dir_wanted + '\\' + file for file in file_list]

name_list = []
num_list = []

for item in file_list:
    print('item >>> ',item)
    temp_list = item.rpartition('_')
    name = str(temp_list[0])
    num = str(temp_list[2].rpartition('.')[0])
    name_list.append(name)
    num_list.append(num)

    print('name >>> ',name)
    print('num >>> ',num)
    print('temp_list >>> ',temp_list)
    print('=====================================================')
    print('=====================================================')



workbook = xlsxwriter.Workbook('pics_and_links.xlsx')
ws = workbook.add_worksheet('Links')