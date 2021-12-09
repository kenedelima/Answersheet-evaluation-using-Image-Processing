from tkinter import *
from typing import Counter
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
import tksheet,ttk
import pandas as pd

import cv2
import numpy as np
from sys import exit
from db_connect import *
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
        # frame_2.place(x=650,y=15,width=120,height=170)
        # title_1 = Label(frame_1,text="choose a template image",font=('Century Gothic',15),fg="#A8A8A8",bg="white").place(x=200,y=350)
        canvas = Canvas(frame_1, width = 520, height = 670)      
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
                barcodeCou = barcodeCount.get()

                cls = self.__class__
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
                        db_obj = connect()
                        print('db_obj >>> ',db_obj)
                        if(db_obj == 'success'):
                            # on success
                            disconnected_status.config(text = ' Connected')
                            disconnected_status.config(fg = '#00FF00')
                            

                        else:
                            # on failed
                            disconnected_status.config(text = ' Connection Failed')
                            disconnected_status.config(fg = 'red')



                            database_name.config(text = 'Database Name : abc xyz database')
                            database_name.config(fg = '#00FF00')

                            table_name.config(text = 'Table Name : xxxxxxxxxx table')
                            table_name.config(fg = '#00FF00')


                            choose_excel_file = Button(frame_2,text="Choose Excel file",command=lambda : show_widgets(),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
                            choose_excel_file.pack()
                            choose_excel_file.place(x=30,y=190,width=200,height=35)


                            # entry_btn = Button(frame_2,text="Start Entry",command=lambda : show_widgets(),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
                            # entry_btn.pack()
                            # entry_btn.place(x=30,y=190,width=200,height=35)

                            # edit_btn = Button(frame_2,text="Edit Invalid Entries",command=lambda : out_of_scope(),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
                            # edit_btn.pack()
                            # edit_btn.place(x=270,y=190,width=200,height=35)

                            

                            # view_btn = Button(frame_2,text="View Entries",command=lambda : out_of_scope(),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
                            # view_btn.pack()
                            # view_btn.place(x=510,y=190,width=200,height=35)

                        
                        # =======================================================================================================================
                        # =======================================================================================================================
                    # =======================================================================================================================
                    # START DB ENTRY AND VIEW RECORDS AND OTHER WIDGETS
                    # =======================================================================================================================
                    def clear_treeview():
                        tree.delete(*tree.get_children())

                    # frame_3 = Frame(self.root,bg='white')
                    # frame_3.place(x=15,y=320,width=1165,height=350)
                    # Create a Treeview widget
                    tree = ttk.Treeview(frame_2)
                    def selectItem(a):
                        curItem = tree.focus()
                        print(tree.item(curItem))
                        cls.selectFlag = False

                    def getRecordVal():
                        if(cls.selectFlag == True):
                            messagebox.showerror('Error','Select record where to start entry from the below list.')
                        else:
                            print('Success')

                    def show_widgets():
                        # dataLabel = Label(frame_2, text='')
                        # dataLabel.place(x=30,y=230)
                        # dataLabel.pack(pady=20)

                        filename = filedialog.askopenfilename(title="Open a File", filetype=(("xlxs files", ".*xlsx"),("All Files", "*.")))
                        if filename:
                            cls.selectFlag = True
                            # try:
                            filename = r"{}".format(filename)
                            df = pd.read_excel(filename)
                            # except ValueError:
                                # dataLabel.config(text="File could not be opened")
                            # except FileNotFoundError:
                                # dataLabel.config(text="File Not Found")
                        else:
                            cls.selectFlag = True
                    # Clear all the previous data in tree
                        clear_treeview()

                    # Add new data in Treeview widget
                        tree["column"] = list(df.columns)
                        tree["show"] = "headings"

                    # For Headings iterate over the columns
                        for col in tree["column"]:
                            tree.heading(col, text=col)

                    # Put Data in Rows
                        df_rows = df.to_numpy().tolist()
                        for row in df_rows:
                            tree.insert("", "end", values=row)
                        tree.bind('<ButtonRelease-1>', selectItem)
                        tree.pack()
                        tree.place(x=15,y=320,width=1165,height=350)


                        selectionRecord = Button(frame_2,text="Start Data Entry",command= lambda : getRecordVal(),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
                        selectionRecord.pack()
                        selectionRecord.place(x=270,y=190,width=220,height=35)

                        # ----------------------------------------------------------------------------------------------------------------------
                        # header for table
                        # border = Canvas(frame_2, width=1170, height=1)
                        # border.pack()
                        # border.place(x=10,y=270)

                        # current_record_head_id_info = Label(frame_2,text="ID",font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                        # current_record_head_id_info.pack()
                        # current_record_head_id_info.place(x=25,y=280)

                        # current_record_head_name_info = Label(frame_2,text="File",font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                        # current_record_head_name_info.pack()
                        # current_record_head_name_info.place(x=150,y=280)

                        # current_record_head_booklet_info = Label(frame_2,text="Answer Booklet No.",font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                        # current_record_head_booklet_info.pack()
                        # current_record_head_booklet_info.place(x=430,y=280)

                        # current_record_head_barcode_info = Label(frame_2,text="Barcode No.",font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                        # current_record_head_barcode_info.pack()
                        # current_record_head_barcode_info.place(x=640,y=280)

                        # current_record_head_roll_info = Label(frame_2,text="Roll No.",font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                        # current_record_head_roll_info.pack()
                        # current_record_head_roll_info.place(x=840,y=280)

                        # current_record_head_roll_info = Label(frame_2,text="Invalid Flag",font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                        # current_record_head_roll_info.pack()
                        # current_record_head_roll_info.place(x=990,y=280)

                        # border_1 = Canvas(frame_2, width=1170, height=1)
                        # border_1.pack()
                        # border_1.place(x=10,y=310)
                        # ----------------------------------------------------------------------------------------------------------------------
                        # list out records
                        # frame_3 = Frame(self.root,bg='white')
                        # frame_3.place(x=15,y=320,width=1165,height=350)
                        # scroll_bar = Scrollbar(frame_3)
                        # scroll_bar.pack( side = RIGHT,fill = Y)
                        # mylist = Listbox(frame_3, yscrollcommand = scroll_bar.set,width=1165,height=350)
                        # # mylist.place(x=30,y=500)

                        # import openpyxl
  
                        # # # load excel with its path
                        # wrkbk = openpyxl.load_workbook("db_records.xlsx")
                        
                        # sh = wrkbk.active
                        # # # iterate through excel and display data
                        # # # countER = 0 
                        # cls = self.__class__
                        # try:
                        #     gotdata = dlist[cls.countER]
                        #     mylist.insert(0,f"  {line} ----------------------------- {line} ----------------- {line}")
                        #     cls.countER += 1
                        # except IndexError:
                        #     gotdata = 'null'

                            
                        # def counter_label(current_record_head_id_info):
                        #     if(cls.counter <= 500):
                        #         def count():
                        #             cls.countER += 1
                        #             # current_record_head_id_info.config(text=str(cls.countER))
                        #             mylist.insert(0,f"  {cls.countER} ----------------------------- {cls.countER} ----------------- {cls.countER}")
                            
                        #             mylist.pack( side = LEFT, fill = BOTH )
                                
                        #             scroll_bar.config( command = mylist.yview )

                        #             current_record_head_id_info.after(10, count)
                        #     else:
                        #     if(cls.counter == 500):
                        #         return 'hello'
                        #     else:
                        #         count()


                        # data = counter_label(current_record_head_id_info)
                        # print('data >>> ',data)
                        # for line in range(1, 5000):
                        #     mylist.insert(0,f"  {line} ----------------------------- {line} ----------------- {line}")
                        
                        #     mylist.pack( side = LEFT, fill = BOTH )
                            
                        #     scroll_bar.config( command = mylist.yview )

                        # inc_y = 340
                        # for i in range(15):
                            # current_record_head_id_info = Label(frame_2,text=str(i),font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                            # current_record_head_id_info.pack()
                            # current_record_head_id_info.place(x=25,y=inc_y)

                            # current_record_head_name_info = Label(frame_2,text="File"+str(i),font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                            # current_record_head_name_info.pack()
                            # current_record_head_name_info.place(x=150,y=inc_y)

                            # current_record_head_booklet_info = Label(frame_2,text="Answer Booklet No."+str(i),font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                            # current_record_head_booklet_info.pack()
                            # current_record_head_booklet_info.place(x=430,y=inc_y)

                            # current_record_head_barcode_info = Label(frame_2,text="Barcode No."+str(i),font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                            # current_record_head_barcode_info.pack()
                            # current_record_head_barcode_info.place(x=640,y=inc_y)

                            # current_record_head_roll_info = Label(frame_2,text="Roll No."+str(i),font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                            # current_record_head_roll_info.pack()
                            # current_record_head_roll_info.place(x=840,y=inc_y)

                            # current_record_head_roll_info = Label(frame_2,text="Valid",font=('Century Gothic',9,'bold'),fg="white",bg="#002e63")
                            # current_record_head_roll_info.pack()
                            # current_record_head_roll_info.place(x=990,y=inc_y)

                            # inc_y = inc_y + 20

                        # ----------------------------------------------------------------------------------------------------------------------
                        # current_record = Label(frame_2,text="Current entry",font=('Century Gothic',13,'bold'),fg="white",bg="#002e63")
                        # current_record.pack()
                        # current_record.place(x=30,y=310)

                        # current_record_id_info = Label(frame_2,text="-",font=('Century Gothic',11,'bold'),fg="white",bg="#002e63")
                        # current_record_id_info.pack()
                        # current_record_id_info.place(x=350,y=310)

                        # current_record_name_info = Label(frame_2,text="-",font=('Century Gothic',11,'bold'),fg="white",bg="#002e63")
                        # current_record_name_info.pack()
                        # current_record_name_info.place(x=760,y=310)
                        # ----------------------------------------------------------------------------------------------------------------------
                        # ---------------------------------------------------------------------------------------------------------------------

                        border_2 = Canvas(frame_2, width=1170, height=1)
                        border_2.pack()
                        border_2.place(x=10,y=680)
                        # ----------------------------------------------------------------------------------------------------------------------
                        # ----------------------------------------------------------------------------------------------------------------------
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
                    table_name.place(x=450,y=110)

                    # canvas = Canvas(frame_2, width=1170, height=1)
                    # canvas.pack()
                    # canvas.place(x=10,y=150)


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
                    x2 = x1+400
                    y1 = event.y
                    y2 = y1+200
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

            # # Verify & Proceed button
            # verify_proceed_btn = Button(self.root,text="Verify & Proceed",command=lambda : verify(),font=('Century Gothic',9,'bold'),fg="white",bg="#808080")
            # verify_proceed_btn.pack()
            # verify_proceed_btn.place(x=400,y=725,width=200,height=35)

        # choose image button
        choose_image = Button(self.root,text="Select | Change image",font=('Century Gothic',9,'bold'),fg="white",bg="#808080",command=lambda : choose_file(canvas))
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

