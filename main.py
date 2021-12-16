from tkinter import *
from typing import Counter
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
import tksheet,ttk
import pandas as pd
import mysql.connector
import pymysql
# ==========================
import cv2
import pytesseract
import os
from pyzbar.pyzbar import decode
# ==========================
import cv2
import numpy as np
from sys import exit
from db_connect import *

pytesseract.pytesseract.tesseract_cmd = 'A:/New folder/tesseract.exe'
# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
'''Utility function for redirection and destroying the login screen'''
# ##################################################################################################################################################################################
def goto_template():
    root = Tk()
    obj = template_selection(root)
    root.mainloop()

def change():
    root.destroy()
    goto_template()

# ##################################################################################################################################################################################
'''screen for choosing templates and selecting area parameters for the "Answer booklet no., Barcode no. and OMR data from an answer sheer'''
# ##################################################################################################################################################################################
class template_selection():
    counter = 0
    file = ''
    countER = 0 
    selectFlag = True
    rowLength = 0
    dataFrameCounter = 0
    invalidEntry = 0
    # =====================================
    # important params
    # -------------------------------------
    answerBookletX1 = 0
    answerBookletX2 = 0
    answerBookletY1 = 0
    answerBookletY2 = 0

    barcodeX1 = 0
    barcodeX2 = 0
    barcodeY1 = 0
    barcodeY2 = 0

    omrX1 = 0
    omrX2 = 0
    omrY1 = 0
    omrY2 = 0

    barcode_count_var = 0
    # =====================================
    def __init__(self,root):
        self.root = root
        self.root.title('Answer Sheet Evaluation Management')
        self.root.geometry('1190x700+100+50')
        self.root.resizable(False,False)

        # Setting icon of master window
        p1 = ImageTk.PhotoImage(file = 'logo.png')
        self.root.iconphoto(False, p1)

        # self.root.attributes('-fullscreen', True)
        # Background image
        self.bg = ImageTk.PhotoImage(file='login_background.jpg')
        self.bg_image = Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1, relheight=1)

        # Title & subtitle
        title = Label(self.root,text="Template & Parameter Selection",font=('Century Gothic',17,'bold'),fg="white",bg="#002e63").place(x=20,y=10)
        subtitle = Label(self.root,text="Choose template image : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63").place(x=30,y=60)
        select_params = Label(self.root,text="Select Area from Image to add following parameters",font=('Century Gothic',13,'bold'),fg="white",bg="#002e63").place(x=30,y=150)

        # View selected Image frame
        frame_1 = Frame(self.root,bg='white')
        frame_1.place(x=650,y=15,width=520,height=670)

        frame_2 = Frame(self.root,bg='#002e63')
        frame_3 = Frame(frame_2,bg='#002e63',highlightbackground="blue", highlightthickness=2)
        

        # frame_2.place(x=650,y=15,width=120,height=170)
        # title_1 = Label(frame_1,text="choose a template image",font=('Century Gothic',15),fg="#A8A8A8",bg="white").place(x=200,y=350)
        canvas = Canvas(frame_1, width = 520, height = 670,highlightbackground="blue", highlightthickness=2)      
        canvas.pack() 
        canvas.create_text(270,390,fill="#A8A8A8",font=('Century Gothic',15),text="choose a template image")
        # ##################################################################################
        # choose and display selected image
        barcodeCount = StringVar()
        def choose_file(canvas):
            f_type = [('Jpg files','*.jpg'),('PNG files','*.png'),("tiff","*.tiff"),("tif","*.tif")]
            file_name = filedialog.askopenfilename(filetypes=f_type)
            image = cv2.imread(file_name)
            cls = self.__class__
            cls.file = file_name
            
            #Rearrang the color channel
            b,g,r = cv2.split(image)
            img = cv2.merge((r,g,b)) 
            # Convert the Image object into a TkPhoto object
            imgg = Image.fromarray(img)
            im = imgg.resize((520,670), Image.ANTIALIAS)
            pic = ImageTk.PhotoImage(image=im) 

            canvas.create_image(0,0, image=pic, anchor="nw")
            canvas.place(x=0, y=0)
            canvas.image=pic
            canvas.borderwidth=0
            cls = self.__class__
            cls.counter = 0
            # ##################################################################################
            # Area selection for answer booklet number
            select_Booklet_params = Label(self.root,text="1. Select Area Parameters for Answer Booklet No.",font=('Century Gothic',12,'bold'),fg="white",bg="#002e63")
            select_Booklet_params.pack()
            select_Booklet_params.place(x=30,y=200)

            select_Booklet_params_x1 = Label(self.root,text="X1 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Booklet_params_x1.pack()
            select_Booklet_params_x1.place(x=40,y=230)
            self.booklet_x1 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.booklet_x1.place(x=70,y=230,width=70,height=20)

            select_Booklet_params_x2 = Label(self.root,text="X2 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Booklet_params_x2.pack()
            select_Booklet_params_x2.place(x=200,y=230)
            self.booklet_x2 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.booklet_x2.place(x=230,y=230,width=70,height=20)

            select_Booklet_params_y1 = Label(self.root,text="Y1 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Booklet_params_y1.pack()
            select_Booklet_params_y1.place(x=40,y=260)
            self.booklet_y1 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.booklet_y1.place(x=70,y=260,width=70,height=20)

            select_Booklet_params_y2 = Label(self.root,text="Y2 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Booklet_params_y2.pack()
            select_Booklet_params_y2.place(x=200,y=260)
            self.booklet_y2 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.booklet_y2.place(x=230,y=260,width=70,height=20)

            # ##################################################################################
            # Area selection for Barcode number
            select_Barcode_params = Label(self.root,text="2. Select Area Parameters for Barcode No.",font=('Century Gothic',12,'bold'),fg="white",bg="#002e63")
            select_Barcode_params.pack()
            select_Barcode_params.place(x=30,y=320)

            select_Barcode_params_x1 = Label(self.root,text="X1 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Barcode_params_x1.pack()
            select_Barcode_params_x1.place(x=40,y=350)
            self.barcode_x1 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.barcode_x1.place(x=70,y=350,width=70,height=20)

            select_Barcode_params_x2 = Label(self.root,text="X2 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Barcode_params_x2.pack()
            select_Barcode_params_x2.place(x=200,y=350)
            self.barcode_x2 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.barcode_x2.place(x=230,y=350,width=70,height=20)

            select_Barcode_params_y1 = Label(self.root,text="Y1 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Barcode_params_y1.pack()
            select_Barcode_params_y1.place(x=40,y=380)
            self.barcode_y1 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.barcode_y1.place(x=70,y=380,width=70,height=20)

            select_Barcode_params_y2 = Label(self.root,text="Y2 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Barcode_params_y1.pack()
            select_Barcode_params_y1.place(x=200,y=380)
            self.barcode_y2 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.barcode_y2.place(x=230,y=380,width=70,height=20)


            # ##################################################################################
            # Area selection for OMR - registration number
            select_Omr_params = Label(self.root,text="3. Select Area Parameters for OMR - Registration No.",font=('Century Gothic',12,'bold'),fg="white",bg="#002e63")
            select_Omr_params.pack()
            select_Omr_params.place(x=30,y=440)

            select_Omr_params_x1 = Label(self.root,text="X1 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Omr_params_x1.pack()
            select_Omr_params_x1.place(x=40,y=470)
            self.omr_x1 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.omr_x1.place(x=70,y=470,width=70,height=20)

            select_Omr_params_x2 = Label(self.root,text="X2 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Omr_params_x2.pack()
            select_Omr_params_x2.place(x=200,y=470)
            self.omr_x2 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.omr_x2.place(x=230,y=470,width=70,height=20)

            select_Omr_params_y1 = Label(self.root,text="Y1 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Omr_params_y1.pack()
            select_Omr_params_y1.place(x=40,y=500)
            self.omr_y1 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.omr_y1.place(x=70,y=500,width=70,height=20)

            select_Omr_params_y2 = Label(self.root,text="Y2 : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_Omr_params_y2.pack()
            select_Omr_params_y2.place(x=200,y=500)
            self.omr_y2 = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.omr_y2.place(x=230,y=500,width=70,height=20)
            


            select_barcode_count = Label(self.root,text="Number of Barcodes in sheet : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
            select_barcode_count.pack()
            select_barcode_count.place(x=40,y=570)
            self.bacode_count = Entry(self.root,textvariable = barcodeCount,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
            self.bacode_count.place(x=260,y=570,width=100,height=20)

            # ##################################################################################
            # messagebox.showinfo('Info','Choose area for Answer booklet No.',parent=self.root)
            # Verify & Proceed button
            verify_proceed_btn = Button(self.root,text="Verify & Proceed",command=lambda : verify(),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
            verify_proceed_btn.pack()
            verify_proceed_btn.place(x=490,y=640,width=150,height=35)
            canvas.config(scrollregion=canvas.bbox(ALL))

            # verify all parameters
            def verify():
                cls = self.__class__
                barcodeCou = barcodeCount.get()

                cls.answerBookletX1 = self.booklet_x1.get()
                cls.answerBookletX2 = self.booklet_x2.get()
                cls.answerBookletY1 = self.booklet_y1.get()
                cls.answerBookletY2 = self.booklet_y2.get()

                cls.barcodeX1 = self.barcode_x1.get()
                cls.barcodeX2 = self.barcode_x2.get()
                cls.barcodeY1 = self.barcode_y1.get()
                cls.barcodeY2 = self.barcode_y2.get()

                cls.omrX1 = self.omr_x1.get()
                cls.omrX2 = self.omr_x2.get()
                cls.omrY1 = self.omr_y1.get()
                cls.omrY2 = self.omr_y2.get()

                cls.barcode_count_var = barcodeCou
                print('cls.answerBookletX1 >>>> ',cls.answerBookletX1)
                print('cls.answerBookletX2 >>>> ',cls.answerBookletX2)
                print('cls.answerBookletY1 >>>> ',cls.answerBookletY1)
                print('cls.answerBookletY2 >>>> ',cls.answerBookletY2)

                print('cls.barcodeX1 >>>> ',cls.barcodeX1)
                print('cls.barcodeX2 >>>> ',cls.barcodeX2)
                print('cls.barcodeY1 >>>> ',cls.barcodeY1)
                print('cls.barcodeY2 >>>> ',cls.barcodeY2)

                print('cls.omrX1 >>>> ',cls.omrX1)
                print('cls.omrX2 >>>> ',cls.omrX2)
                print('cls.omrY1 >>>> ',cls.omrY1)
                print('cls.omrY2 >>>> ',cls.omrY2)

                print('cls.barcode_count_var >>>> ',cls.barcode_count_var)



                if(cls.counter < 2):
                    messagebox.showerror('Error','Choose all parameter area to proceed.',parent=self.root)
                elif(barcodeCou == ''):
                    messagebox.showerror('Error','Enter number of barcodes in the sheet.',parent=self.root)
                else:
                    # remove everything from the screen
                    frame_2.pack(fill='both', expand=1)
                    frame_1.pack_forget()
                    self.booklet_x1.destroy()
                    self.booklet_x2.destroy()
                    self.booklet_y1.destroy()
                    self.booklet_y2.destroy()
                    select_Booklet_params.destroy()
                    select_Booklet_params_x1.destroy()
                    select_Booklet_params_x2.destroy()
                    select_Booklet_params_y1.destroy()
                    select_Booklet_params_y2.destroy()

                    self.barcode_x1.destroy()
                    self.barcode_x2.destroy()
                    self.barcode_y1.destroy()
                    self.barcode_y2.destroy()
                    select_Barcode_params.destroy()
                    select_Barcode_params_x1.destroy()
                    select_Barcode_params_x2.destroy()
                    select_Barcode_params_y1.destroy()
                    select_Barcode_params_y2.destroy()

                    self.omr_x1.destroy()
                    self.omr_x2.destroy()
                    self.omr_y1.destroy()
                    self.omr_y2.destroy()
                    select_Omr_params.destroy()
                    select_Omr_params_x1.destroy()
                    select_Omr_params_x2.destroy()
                    select_Omr_params_y1.destroy()
                    select_Omr_params_y2.destroy()

                    select_barcode_count.destroy()
                    self.bacode_count.destroy()
                    
                    choose_image.destroy() 
                    verify_proceed_btn.destroy()



                    # =======================================================================================================================
                    #                                   PAGE 03 : DATABASE CONNECTION AND DATA ENTRY
                    # =======================================================================================================================
                    def out_of_scope():
                        messagebox.showinfo('Info','Out of scope.Under development.')
                    # =======================================================================================================================
                    '''database connectivity'''
                    def connectDB():
                        disconnected_status.config(text = ' Connecting ...')
                        disconnected_status.config(fg = 'grey')
                        try:
                            # ----------------------------------------------------------------------------------------------------------------------
                            # DATABASE HANDLER and connections
                            # ----------------------------------------------------------------------------------------------------------------------
                            my_db = mysql.connector.connect(host='localhost',user='root',password="",db="university_db")
                            my_cursor = my_db.cursor()
                            # my_cursor.execute('show databases')

                            # for i in my_cursor:
                            #     print(i)
                            # cur = db.cursor()

                            # fetch records
                            my_cursor.execute("SELECT * FROM answer_sheet_table_01")
                            # for row in my_cursor.fetchall():
                            #     print(row)

                            # my_cursor.close()
                            # ----------------------------------------------------------------------------------------------------------------------
                            # ----------------------------------------------------------------------------------------------------------------------

                            disconnected_status.config(text = ' Connected')
                            disconnected_status.config(fg = '#00FF00')

                            database_name.config(text = 'Database Name : university_db')
                            database_name.config(fg = 'white')


                            table_name.config(text = 'Table Name : answer_sheet_table_01')
                            table_name.config(fg = 'white')

                            entryStatus = Label(frame_2,text="",font=('Century Gothic',11,'bold'),fg="white",bg="#002e63")
                            entryStatus.pack()
                            entryStatus.place(x=20,y=280)

                            viewDbRecords = Button(frame_2,text="View Records",command=lambda : show_widgets(entryStatus),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
                            viewDbRecords.pack()
                            viewDbRecords.place(x=30,y=190,width=200,height=35)

                            

                        except:
                            message = 'fail'
                            disconnected_status.config(text = ' Connection Failed')
                            disconnected_status.config(fg = 'red')



                            database_name.config(text = 'Database Name : ')
                            database_name.config(fg = 'white')


                            table_name.config(text = 'Table Name : ')
                            table_name.config(fg = 'white')

                    # =======================================================================================================================
                    # START DB ENTRY AND VIEW RECORDS AND OTHER WIDGETS
                    # =======================================================================================================================
                    def clear_treeview():
                        tree.delete(*tree.get_children())

                    tree = ttk.Treeview(frame_2)

                    # ----------------------------------------------------------------------------------------------------------------------
                    # ----------------------------------------------------------------------------------------------------------------------
                    def selectItem(a):
                        curItem = tree.focus()
                        print(tree.item(curItem))
                        cls.selectFlag = False
                        fileName = tree.item(curItem)['values'][1]
                        answeBookletNo = tree.item(curItem)['values'][2]
                        barcodeNo = tree.item(curItem)['values'][3]
                        rollNo = tree.item(curItem)['values'][4]

                        self.updateFileName.config(text = f'File Name : {fileName}')

                        if(answeBookletNo != '-'):
                            self.bookletData.delete(0,"end")
                            self.bookletData.insert(0, str(answeBookletNo))
                        else:
                            self.bookletData.delete(0,"end")

                        if(barcodeNo != '-'):
                            self.barcodeData.delete(0,"end")
                            self.barcodeData.insert(0, str(barcodeNo))
                        else:
                            self.barcodeData.delete(0,"end")

                        if(rollNo != '-'):
                            self.rollData.delete(0,"end")
                            self.rollData.insert(0, str(rollNo))
                        else:
                            self.rollData.delete(0,"end")

                    # ----------------------------------------------------------------------------------------------------------------------
                    # ----------------------------------------------------------------------------------------------------------------------
                    def stopFunc():
                        print('process stopped!')

                    # ----------------------------------------------------------------------------------------------------------------------
                    # Make one method to decode the barcode
                    def BarcodeReader(image):
                        data = ''
                        img = cv2.imread(image)
                        detectedBarcodes = decode(img)
                        
                        if not detectedBarcodes:
                            print("Barcode Not Detected or your barcode is blank/corrupted!")
                        else:
                            for barcode in detectedBarcodes:
                                (x, y, w, h) = barcode.rect
                                cv2.rectangle(img, (x-10, y-10),
                                            (x + w+10, y + h+10),
                                            (255, 0, 0), 2)
                                
                                if barcode.data!="":
                                    # print(barcode.data)
                                    # print(barcode.type)
                                    data = data + str(barcode.data.decode("utf-8")) + "|"
                                    
                        #Display the image
                        # cv2.imshow("Image", img)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()
                        return data


                    def updateFunc(dataFrameCounter,index,df,entryStatus,processedRecordsLabel,InvalidRecordsLabel):
                        entryStatus.config(text = 'Status : Inserting records in table ...')
                        for i in range(10):
                            pass
                        try:
                            dbcon = mysql.connector.connect(host='localhost',user='root',password="",db="university_db")
                            my_cursor = dbcon.cursor()
                            if(dataFrameCounter <= 0 ):
                                print('Task Finished!')
                                entryStatus.config(text = '')
                                entryStatus.config(text = 'Status : Finished')
                            else:
                                print('Doing Task!')
                                # entryStatus.config(text = '')
                                # ------------------------------------------------------------------------------
                                # fetch answer booklet number from images
                                # ------------------------------------------------------------------------------
                                img_path = f'C:/Users/amitk/Desktop/University-answer-booklet-eval-dash/New folder/Test data/{df[index]}'
                                img = cv2.imread(img_path)
                                height, width = img.shape[0:2]

                                startRow = int(height * 0.10)
                                startCol = int(width * 0.10)
                                endRow = int(height * 0.90)
                                endCol = int(width * 0.40)

                                # cropped_image = img[41:123, 191:203]
                                cropped_image = img[int(cls.answerBookletX1)+20:int(cls.answerBookletY1)+20, int(cls.answerBookletX2)+20:int(cls.answerBookletY2)+20]

                                text = pytesseract.image_to_string(cropped_image)
                                print('text >>> ',text)

                                data = [int(s) for s in text.split() if s.isdigit() and len(s)>=6]

                                y = BarcodeReader(img_path)
                                str_list = list(filter(None, y.split('|')))

                                print('str_list >>> ',str_list)
                                answerBookletNumber = ''
                                barcodeNumber = ''

                                if(len(str_list) > 1):
                                    answerBookletNumber = str(str_list[1])
                                    barcodeNumber = str(str_list[0])
                                    # ------------------------------------------------------------------------------
                                    print('answerBookletNumber >>> ',answerBookletNumber)
                                    # ------------------------------------------------------------------------------
                                    sql = f"UPDATE answer_sheet_table_01 SET Answer_Booklet_No = {str(answerBookletNumber)},Barcode_No = {str(barcodeNumber)} WHERE File = '{str(df[index])}'"
                                    my_cursor.execute(sql)
                                    # print("affected rows = {}".format(my_cursor.rowcount))
                                    # ========================================================================================
                                    # ========================================================================================
                                    processedRecordsLabel.config(text = '')
                                    processedRecordsLabel.config(text = f'Processed Records : {index+1}')
                                    InvalidRecordsLabel.config(text = '')
                                    InvalidRecordsLabel.config(text = f'Invalid Records : {cls.invalidEntry}')
                                elif(len(str_list) == 1):
                                    barcodeNumber = str(str_list[0])
                                    # ------------------------------------------------------------------------------
                                    print('answerBookletNumber >>> ',answerBookletNumber)
                                    # ------------------------------------------------------------------------------
                                    sql = f"UPDATE answer_sheet_table_01 SET Answer_Booklet_No = '-',Barcode_No = {str(barcodeNumber)} WHERE File = '{str(df[index])}'"
                                    my_cursor.execute(sql)
                                    # print("affected rows = {}".format(my_cursor.rowcount))
                                    # ========================================================================================
                                    cls.invalidEntry = cls.invalidEntry + 1
                                    # ========================================================================================
                                    processedRecordsLabel.config(text = '')
                                    processedRecordsLabel.config(text = f'Processed Records : {index+1}')
                                    InvalidRecordsLabel.config(text = '')
                                    InvalidRecordsLabel.config(text = f'Invalid Records : {cls.invalidEntry}')
                                else:
                                    # ------------------------------------------------------------------------------
                                    print('answerBookletNumber >>> ',answerBookletNumber)
                                    # ------------------------------------------------------------------------------
                                    sql = f"UPDATE answer_sheet_table_01 SET Answer_Booklet_No = '-',Barcode_No = '-' WHERE File = '{str(df[index])}'"
                                    my_cursor.execute(sql)
                                    # print("affected rows = {}".format(my_cursor.rowcount))
                                    # ========================================================================================
                                    cls.invalidEntry = cls.invalidEntry + 1
                                    # ========================================================================================
                                    processedRecordsLabel.config(text = '')
                                    processedRecordsLabel.config(text = f'Processed Records : {index+1}')
                                    InvalidRecordsLabel.config(text = '')
                                    InvalidRecordsLabel.config(text = f'Invalid Records : {cls.invalidEntry}')
                                    # try:
                                    #     if(len(data) == 1):
                                    #         answerBookletNumber = str(data[0])
                                    #     elif(len(data) == 0):
                                    #         answerBookletNumber = '-'
                                    #     else:
                                    #         answerBookletNumber = '-'
                                    # except:
                                        # answerBookletNumber = str('-')



                                # ========================================================================================
                                # ========================================================================================
                                dbcon.commit()
                                updateFunc(dataFrameCounter -1,index+1,df,entryStatus,processedRecordsLabel,InvalidRecordsLabel)
                        except:
                            disconnected_status.config(text = ' Connection Failed')
                            disconnected_status.config(fg = 'red')

                            database_name.config(text = 'Database Name : ')
                            database_name.config(fg = 'white')

                            table_name.config(text = 'Table Name : ')
                            table_name.config(fg = 'white')
                            messagebox.showerror('Error','Database connection lost')
                    # ----------------------------------------------------------------------------------------------------------------------
                    def getRecordVal(df,entryStatus):
                        print('Success')
                        # cls.dataFrameCounter = 0
                        cls.index = 0
                        cls.invalidEntry = 0
                        # entryStatus = Label(frame_2,text="Status : Inserting records in table ...",font=('Century Gothic',11,'bold'),fg="white",bg="#002e63")
                        # entryStatus.pack()
                        # entryStatus.place(x=20,y=280)

                        
                        totalRecordsLabel = Label(frame_2,text="Total Records : "+str(cls.rowLength),font=('Century Gothic',8,'bold'),fg="yellow",bg="#002e63")
                        totalRecordsLabel.pack()
                        totalRecordsLabel.place(x=30,y=250)

                        processedRecordsLabel = Label(frame_2,text="Processed Records : 0",font=('Century Gothic',8,'bold'),fg="#00FF00",bg="#002e63")
                        processedRecordsLabel.pack()
                        processedRecordsLabel.place(x=200,y=250)

                        InvalidRecordsLabel = Label(frame_2,text="Invalid Records : 0",font=('Century Gothic',8,'bold'),fg="red",bg="#002e63")
                        InvalidRecordsLabel.pack()
                        InvalidRecordsLabel.place(x=390,y=250)

                        entryStatus.config(text = 'Status : Records fetched from table')
                        updateFunc(cls.dataFrameCounter,cls.index,df,entryStatus,processedRecordsLabel,InvalidRecordsLabel)
                    # ----------------------------------------------------------------------------------------------------------------------
                    def update_selected_record():
                        dbcon = mysql.connector.connect(host='localhost',user='root',password="",db="university_db")
                        my_cursor = dbcon.cursor()
                        # ========================================================
                        # PARAMS
                        # ========================================================
                        file_name = self.updateFileName.cget("text").split(':')
                        answerBook_no = self.bookletData.get()
                        bar_no = self.barcodeData.get()
                        roll_no = self.rollData.get()
                        # ========================================================
                        if(answerBook_no == ''):
                            answerBook_no = '-'
                        if(bar_no == ''):
                            bar_no = '-'
                        if(roll_no == ''):
                            roll_no = '-'
                        # ========================================================
                        print('file_name >>>> ',file_name)
                        print('answerBook_no >>>> ',answerBook_no)
                        print('bar_no >>>> ',bar_no)
                        print('roll_no >>>> ',roll_no)
                        if(len(file_name) > 1):
                            sql = f"UPDATE answer_sheet_table_01 SET Answer_Booklet_No = '{answerBook_no}',Barcode_No = '{str(bar_no)}',Roll_No='{str(roll_no)}' WHERE File = '{str(file_name[1].strip())}'"
                            my_cursor.execute(sql)
                            dbcon.commit()
                            messagebox.showinfo('Success','Record updated successfullyy.')
                            # ----------------------------------------------------------------------------------
                            clear_treeview()
                            # Add new data in Treeview widget
                            tree["column"]=['File Path', 'File Name','Answer Booklet No','Barcode No','Roll No']
                            tree["show"] = "headings"

                            # For Headings iterate over the columns
                            for col in tree["column"]:
                                tree.heading(col, text=col)

                            dbcon = mysql.connector.connect(host='localhost',user='root',password="",db="university_db")
                            SQL_Query = pd.read_sql_query("select * from answer_sheet_table_01 where Answer_Booklet_No='-' or Barcode_No='-' or Roll_No='-'", dbcon)
                            df = pd.DataFrame(SQL_Query, columns=['File_Path', 'File','Answer_Booklet_No','Barcode_No','Roll_No'])

                            df_data = df['File']

                            # Put Data in Rows
                            df_rows = df.to_numpy().tolist()
                            cls.rowLength = 0
                            cls.rowLength = cls.rowLength + len(df_rows)
                            cls.dataFrameCounter = cls.rowLength
                            for row in df_rows:
                                tree.insert("", "end", values=row)
                            tree.bind('<ButtonRelease-1>', selectItem)
                            tree.pack()
                            tree.place(x=15,y=320,width=1165,height=350)
                            # ----------------------------------------------------------------------------------
                        else:
                            messagebox.showinfo('Info','Select a record to update.')
                    # ----------------------------------------------------------------------------------------------------------------------
                    def show_widgets(entryStatus):
                        clear_treeview()

                        # Add new data in Treeview widget
                        tree["column"]=['File Path', 'File Name','Answer Booklet No','Barcode No','Roll No']
                        tree["show"] = "headings"

                        # For Headings iterate over the columns
                        for col in tree["column"]:
                            tree.heading(col, text=col)

                        dbcon = mysql.connector.connect(host='localhost',user='root',password="",db="university_db")
                        SQL_Query = pd.read_sql_query("select * from answer_sheet_table_01 where Answer_Booklet_No='-' or Barcode_No='-' or Roll_No='-'", dbcon)
                        df = pd.DataFrame(SQL_Query, columns=['File_Path', 'File','Answer_Booklet_No','Barcode_No','Roll_No'])

                        df_data = df['File']

                        # Put Data in Rows
                        df_rows = df.to_numpy().tolist()
                        cls.rowLength = 0
                        cls.rowLength = cls.rowLength + len(df_rows)
                        cls.dataFrameCounter = cls.rowLength
                        for row in df_rows:
                            tree.insert("", "end", values=row)
                        tree.bind('<ButtonRelease-1>', selectItem)
                        tree.pack()
                        tree.place(x=15,y=320,width=1165,height=350)
                        # ----------------------------------------------------------------------------------------------------------------------
                        # entryStatus = Label(frame_2,text="Status : Records Fetched from Table",font=('Century Gothic',11,'bold'),fg="white",bg="#002e63")
                        # entryStatus.pack()
                        # entryStatus.place(x=20,y=280)
                        entryStatus.config(text = 'Status : Record fetched from table')
                        # ----------------------------------------------------------------------------------------------------------------------
                        selectionRecord = Button(frame_2,text="Start Data Entry",command= lambda : getRecordVal(df_data,entryStatus),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
                        selectionRecord.pack()
                        selectionRecord.place(x=270,y=190,width=220,height=35)
                        # ----------------------------------------------------------------------------------------------------------------------
                        # ----------------------------------------------------------------------------------------------------------------------
                        border_2 = Canvas(frame_2, width=1170, height=1)
                        border_2.pack()
                        border_2.place(x=10,y=680)
                        
                        
                        # ----------------------------------------------------------------------------------------------------------------------
                        frame_3.place(x=700,y=45,width=478,height=265)
                        

                        self.updateLabel = Label(self.root,text="Update Record",font=('Century Gothic',14,'bold'),fg="white",bg="#002e63")
                        self.updateLabel.pack()
                        self.updateLabel.place(x=725,y=32)

                        self.updateFileName = Label(self.root,text="File Name : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
                        self.updateFileName.pack()
                        self.updateFileName.place(x=750,y=90)

                        self.update_answer_Booklet = Label(self.root,text="Answer Booklet No : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
                        self.update_answer_Booklet.pack()
                        self.update_answer_Booklet.place(x=750,y=130)
                        self.bookletData = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
                        self.bookletData.place(x=890,y=130,width=200,height=20)

                        self.update_barcode = Label(self.root,text="Barcode No : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
                        self.update_barcode.pack()
                        self.update_barcode.place(x=750,y=170)
                        self.barcodeData = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
                        self.barcodeData.place(x=890,y=170,width=200,height=20)

                        self.update_rooll = Label(self.root,text="Roll No : ",font=('Century Gothic',10,'bold'),fg="white",bg="#002e63")
                        self.update_rooll.pack()
                        self.update_rooll.place(x=750,y=210)
                        self.rollData = Entry(self.root,font=('Century Gothic',10),fg="white",bg="#1d1d1d")
                        self.rollData.place(x=890,y=210,width=200,height=20)

                        self.updateBtn = Button(self.root,text="Update",command= lambda : update_selected_record(),font=('Century Gothic',8,'bold'),fg="white",bg="#808080")
                        self.updateBtn.pack()
                        self.updateBtn.place(x=1040,y=255,width=100,height=25)
                        # ----------------------------------------------------------------------------------------------------------------------

                    # =======================================================================================================================
                    # =======================================================================================================================
                    # =======================================================================================================================
                    '''Append db connect data to the frame'''
                    title2 = Label(frame_2,text="Database Connection",font=('Century Gothic',17,'bold'),fg="white",bg="#002e63")
                    title2.pack()
                    title2.place(x=20,y=10)

                    back_btn = Button(frame_2,text="Back",command=lambda : out_of_scope(),font=('Century Gothic',7,'bold'),fg="white",bg="#808080")
                    back_btn.pack()
                    back_btn.place(x=1120,y=10,width=60,height=25)

                    database_connect = Button(frame_2,text="Connect to Database table",command=lambda : connectDB(),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
                    database_connect.pack()
                    database_connect.place(x=30,y=60,width=180,height=30)

                    connection_status = Label(frame_2,text="Status : ",font=('Century Gothic',15,'bold'),fg="white",bg="#002e63")
                    connection_status.pack()
                    connection_status.place(x=280,y=60)

                    disconnected_status = Label(frame_2,text="Disconnected",font=('Century Gothic',12,'bold'),fg="red",bg="#002e63")
                    disconnected_status.pack()
                    disconnected_status.place(x=350,y=64)

                    database_name = Label(frame_2,text="Database Name : -",font=('Century Gothic',10,'bold'),fg="grey",bg="#002e63")
                    database_name.pack()
                    database_name.place(x=30,y=110)

                    table_name = Label(frame_2,text="Table Name : -",font=('Century Gothic',10,'bold'),fg="grey",bg="#002e63")
                    table_name.pack()
                    table_name.place(x=380,y=110)
                    # =======================================================================================================================
                    # =======================================================================================================================

            #function to be called when mouse is clicked
            def printcoords(event):
                print ('x : ',event.x,'<==>','y : ',event.y)
                x1 = 0
                x2 = 0
                y1 = 0
                y2 = 0
                cls = self.__class__
                if(cls.counter == 2):
                    x1 = event.x
                    x2 = x1+370
                    y1 = event.y
                    y2 = y1+190
                    self.omr_x1.delete(0,"end")
                    self.omr_x1.insert(0, str(x1))
                    self.omr_x2.delete(0,"end")
                    self.omr_x2.insert(0, str(x2))
                    self.omr_y1.delete(0,"end")
                    self.omr_y1.insert(0, str(y1))
                    self.omr_y2.delete(0,"end")
                    self.omr_y2.insert(0, str(y2))
                    canvas.create_rectangle(x1,y1,x2,y2,width=5, outline='#ff0000')

                elif(cls.counter == 0):
                    x1 = event.x
                    x2 = x1+150
                    y1 = event.y
                    y2 = y1+80
                    self.booklet_x1.delete(0,"end")
                    self.booklet_x1.insert(0, str(x1))
                    self.booklet_x2.delete(0,"end")
                    self.booklet_x2.insert(0, str(x2))
                    self.booklet_y1.delete(0,"end")
                    self.booklet_y1.insert(0, str(y1))
                    self.booklet_y2.delete(0,"end")
                    self.booklet_y2.insert(0, str(y2))
                    canvas.create_rectangle(x1,y1,x2,y2,width=5, outline='#00ff00')
                    # messagebox.showinfo('Info','Choose area for Barcode No.',parent=self.root)

                elif(cls.counter == 1):
                    x1 = event.x
                    x2 = x1+300
                    y1 = event.y
                    y2 = y1+80
                    self.barcode_x1.delete(0,"end")
                    self.barcode_x1.insert(0, str(x1))
                    self.barcode_x2.delete(0,"end")
                    self.barcode_x2.insert(0, str(x2))
                    self.barcode_y1.delete(0,"end")
                    self.barcode_y1.insert(0, str(y1))
                    self.barcode_y2.delete(0,"end")
                    self.barcode_y2.insert(0, str(y2))
                    canvas.create_rectangle(x1,y1,x2,y2,width=5, outline='#ffff00')
                    # messagebox.showinfo('Info','Choose area for OMR',parent=self.root)

                else:
                    messagebox.showwarning('Info','All parameters selected. You can proceed.',parent=self.root)
                cls.counter = cls.counter + 1

            # mouseclick event
            canvas.bind("<Button 1>",printcoords)

        # choose image button
        choose_image = Button(self.root,text="Select image",font=('Century Gothic',9,'bold'),fg="white",bg="#808080",command=lambda : choose_file(canvas))
        choose_image.pack()
        choose_image.place(x=220,y=58,width=180,height=30)

# ##################################################################################################################################################################################
'''Login GUI for entering and validating valid administrator user'''
# ##################################################################################################################################################################################
class Login():
    def __init__(self,root):
        self.root = root
        self.root.title('Answer Sheet Evaluation Management | LOGIN')
        self.root.geometry('1199x800+100+50')
        self.root.resizable(False,False)
        # self.root.attributes('-fullscreen', True)
        # Setting icon of master window
        p1 = ImageTk.PhotoImage(file = 'logo.png')
        self.root.iconphoto(False, p1)

        # Background image
        self.bg = ImageTk.PhotoImage(file='login_background.jpg')
        self.bg_image = Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1, relheight=1)
        # Banner
        banner = Label(self.root,text="Answer Sheet Evaluation & Record Entry",underline=True,font=('Impact',32,'bold'),fg="white",bg="#002e63").place(x=325,y=50)

        # login frame
        Frame_login = Frame(self.root,bg='#002e63')
        Frame_login.place(x=250,y=150,width=500,height=400)

        # Title & subtitle
        title = Label(Frame_login,text="ADMIN LOGIN",underline=True,font=('Impact',27,'bold'),fg="white",bg="#002e63").place(x=80,y=80)
        # subtitle = Label(Frame_login,text="",font=('Century Gothic',15,'bold'),fg="white",bg="#002e63").place(x=80,y=100)

        # username
        username_label = Label(Frame_login,text="Username",font=('Century Gothic',13,'bold'),fg="white",bg="#002e63").place(x=80,y=150)
        self.username = Entry(Frame_login,font=('Century Gothic',13),fg="white",bg="#1d1d1d")
        self.username.place(x=80,y=177,width=320,height=35)

        # password
        password_label = Label(Frame_login,text="Password",font=('Century Gothic',13,'bold'),fg="white",bg="#002e63").place(x=80,y=230)
        self.password = Entry(Frame_login,show="\u2022",font=('Century Gothic',13),fg="white",bg="#1d1d1d")
        self.password.place(x=80,y=255,width=320,height=35)

        # login btn
        # change()
        submit = Button(Frame_login,text="Login",command=self.check_function,font=('Century Gothic',13,'bold'),fg="white",bg="#808080").place(x=280,y=320,width=120,height=35)

    # Login credentials verification after login
    def check_function(self):
        if(self.username.get() == '' and self.password.get() == ''):
            messagebox.showerror('Error','Enter valid Username & Password!',parent=self.root)

        elif(self.username.get() == '' and self.password.get() != ''):
            messagebox.showerror('Error','Enter valid Username!',parent=self.root)

        elif(self.username.get() != '' and self.password.get() == ''):
            messagebox.showerror('Error','Enter valid Password!',parent=self.root)

        elif(self.username.get() == 'Admin' and self.password.get() == 'admin'):
            change()

        else:
            messagebox.showerror('Error','Invalid credentials!',parent=self.root)

# ##################################################################################################################################################################################
# ##################################################################################################################################################################################
root = Tk()
obj = Login(root)
root.mainloop()

