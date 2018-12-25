'''
Created on 04-Jul-2018

@author: DELL
'''

import tkinter as tk
import calendar
import datetime
import sqlite3
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.constants import RAISED


'''Complex widget Calendar to display calendar'''
class Calendar:
    def __init__(self, parent, values):
        self.values = values
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        actualday = datetime.date.today().day; #print(actualday)
        self.wid = []# to delete all widgets in clear() method, it is first populated in setup()
        self.day_selected = actualday
        #self.day_selected = 1
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''
         
        self.setup(self.year, self.month)
         
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            #w.destroy()
            self.wid.remove(w)
     
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        #self.selected = (self.month, self.year)
        self.clear() # first all widgets corresponding to current month are removed    
        self.setup(self.year, self.month) # then widgets are added acc. to changed month
 
    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
         
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)
         
    def selection(self, day, name):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name
        print( name ) 
        #data
        self.values['day_selected'] = day
        self.values['month_selected'] = self.month
        self.values['year_selected'] = self.year
        self.values['day_name'] = name
        self.values['month_name'] = calendar.month_name[self.month_selected]
         
        self.clear()
        self.setup(self.year, self.month)
         
    def setup(self, y, m):
        '''Method to create widgets inside calendar'''
        
        left = tk.Button(self.parent, text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)
        #print(calendar.month_abbr[m]) 
        header = tk.Label(self.parent, height=2,
                           text='{}   {}'.format(calendar.month_abbr[m], str(y))
        )
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)
         
        right = tk.Button(self.parent, text='>', command=self.go_next)
        self.wid.append(right)
        right.grid(row=0, column=5)
         
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3])
            self.wid.append(t)
            t.grid(row=1, column=num)
        
        #print( self.cal.monthdayscalendar(y, m) ) 
        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                print( d, day )
                if day:
                    b = tk.Button(self.parent, width=1, text=day, 
                                  command = 
                                    lambda day = day : 
                    #issue   #it is giving day according to current locale not the month passed
                                        self.selection(day, calendar.day_name[(day-1) % 7])
                    )
                    
                    #Database()
                    #cursor.execute()
                    self.wid.append(b)
                    b.grid(row=w, column=d)
                     
        sel = tk.Label(self.parent, height=2, text='{} {} {} {}'.format(
                                                self.day_name,
                                                calendar.month_name[self.month_selected],
                                                self.day_selected, self.year_selected
                                              )
        )
        self.wid.append(sel)
        sel.grid(row=8, column=0, columnspan=7)
         
        ok = tk.Button(self.parent, width=5, text='OK', command=root.destroy )
        self.wid.append(ok)
        ok.grid(row=9, column=2, columnspan=3, pady=10)
 
 

#Function to open "Add Event" window
def add_event_window( button_option ) :
        global event_id, entry_date, entry_starting_time, entry_ending_time, label_interval_show,\
            entry_with_whom, entry_where 
        root.withdraw()
        
        child_window = tk.Tk()
        if button_option == 'save' :
            child_window.title( "Add Event" )
        else :
            child_window.title("Edit Event" ) 
                           
        child_window.geometry("500x600")
        
        
        #date field
        label_date = tk.Label( child_window, text = "Date", font = 30, justify = tk.LEFT )
        label_date.grid( row = 0, column = 0, columnspan = 2, padx=5, pady=15 )
        
        entry_date = tk.Entry( child_window, bd = 3, width = 50 )
        entry_date.grid( row = 0, column = 2, columnspan = 6, padx=5, pady=15 , sticky = '')
        
        
        #starting time field
        label_starting_time = tk.Label( child_window, text = "Starting Time", font = 30 )
        label_starting_time.grid( row = 1, column = 0, columnspan = 2, padx=5, pady=15 )
        
        entry_starting_time = tk.Entry( child_window, bd = 3, width = 50)
        entry_starting_time.grid( row = 1, column = 2, columnspan = 6, padx=15, pady=15  )
        
        
        #ending time field
        label_ending_time = tk.Label( child_window, text = "Ending Time", font = 30 )
        label_ending_time.grid( row = 2, column = 0, columnspan = 2, padx=5, pady=15  )
        
        entry_ending_time = tk.Entry( child_window, bd = 3, width = 50 )
        entry_ending_time.grid( row = 2, column = 2, columnspan = 6, padx=5, pady=15  )
        
        
        #interval button and field
        button_interval = tk.Button( child_window, text = "Interval", bd = 3, font = 30 ,
                                      command = calc_interval ) 
        button_interval.grid( row = 3, column = 0, columnspan = 2, padx=5, pady=15 )
        
        label_interval_show = tk.Label( child_window, text = "Interval will be shown here",
                                         font = 30, bd = 5)
        label_interval_show.grid( row = 3, column = 2, columnspan = 6, padx=5, pady=15  )
        
        
        #with whom field
        label_with_whom = tk.Label( child_window, text = "With whom", font = 30 )
        label_with_whom.grid( row = 4,column = 0, columnspan = 2, padx=5, pady=15  )
        
        entry_with_whom = tk.Entry( child_window, bd = 3, width = 50 )
        entry_with_whom.grid(  row = 4, column = 2, columnspan = 6, padx=5, pady=15 )
        
        
        #where field
        label_where = tk.Label( child_window, text = "Where", font = 30 )
        label_where.grid( row = 5, column = 0, columnspan = 2, padx=5, pady=15 )
        
        entry_where = tk.Entry( child_window, bd = 3, width = 50)
        entry_where.grid( row = 5, column = 2, columnspan = 6, padx=5, pady=15)
        
        if button_option == "save"  :
            #Save button
            button_save = tk.Button( child_window, text = "Save", font = 30, bd = 3, 
                                     command = lambda : create( child_window ) 
                                    )
            button_save.grid( row = 7, column = 5, rowspan = 2, columnspan = 2 , padx=5, pady=15)
        else :
            ''' In case of edit event'''
            curItem = tree.focus()    
            contents = tree.item( curItem )
            selectedItem = contents['values']
            event_id = selectedItem[0]  
            #print( selectedItem )
            #entry_date.delete( 0, tk.END )
            entry_date.insert( 0, selectedItem[1] )
    
            #entry_starting_time.delete( 0, tk.END )
            entry_starting_time.insert( 0, selectedItem[2] )
            
            #entry_ending_time.delete( 0, tk.END )
            entry_ending_time.insert( 0, selectedItem[3] )
            
            label_interval_show.config( text = selectedItem[4])
            
            #entry_with_whom.delete( 0, tk.END )
            entry_with_whom.insert( 0, selectedItem[5] )
            
            #entry_where.delete( 0, tk.END )
            entry_where.insert( 0, selectedItem[6] )
            
            #Edit button
            button_edit = tk.Button( child_window, text = "Save changes", font = 30, bd =3,
                                      command = lambda : edit_event( child_window ) 
                                   )
            button_edit.grid( row = 7, column = 5, rowspan = 2, columnspan = 3 , padx=5, pady=15 )    
        
        #Cancel button
        button_cancel = tk.Button( child_window, text = "Cancel", font = 30, bd = 3,
                                    command = lambda : cancel_button(child_window)
                                 )
        button_cancel.grid( row = 6, column = 1, rowspan = 2, columnspan = 4, padx = 5, pady = 15 )
        
        root.mainloop()

        
#Function to calculate interval in add_event_window
def calc_interval() :
    format_ = '%I:%M %p' # %I instead of %H to retain am/pm after parsing
    a =  str( datetime.datetime.strptime( entry_ending_time.get( ) , format_) - 
                datetime.datetime.strptime(entry_starting_time.get(), format_ ) )      
    a_time =  datetime.datetime.strptime(a, '%H:%M:%S').time()# to convert string into time object
    label_interval_show.config( text =  str(a_time.hour) + " hour and " +
                                 str(a_time.minute) + " minute" )
    
#Function to hide and bring back the root window on "Cancel" button 
def cancel_button( parent ) :
    parent.destroy()
    root.deiconify()
        
#Function to choose b/w  edit_button-> to edit event and save_button->to add event    
def button_save_chooser() :
    add_event_window( "save" )
    
def button_edit_chooser():    
    if not tree.selection() :
        messagebox.showinfo( "Error!", "Please select an event first")
    else :        
        add_event_window( "edit" )
                        
def Database() :
    global conn, cursor
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()
    cursor.execute( '''CREATE TABLE IF NOT EXISTS `event1` (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        date_of_event DATE, 
        starting_time INTEGER, 
        ending_time INTEGER,
        interval TEXT,
        with_whom TEXT,
        _where TEXT )'''
    )
    
    
def create( parent ) :
    if( entry_date.get() == "" or entry_starting_time.get() == "" or entry_ending_time.get() == ""
        or label_interval_show.cget("text") == "Interval will be shown here" or 
        entry_with_whom.get() == "" or entry_where.get() == "" ) :
        messagebox.showinfo( "Error !", "Please complete the required fields")
        
    else :
        Database()
        cursor.execute('''INSERT INTO `event1` ( date_of_event, starting_time, ending_time,
            interval, with_whom, _where)
            VALUES(?,?,?,?,?,?)''',
            ( 
                str(entry_date.get()), str(entry_starting_time.get()), str(entry_ending_time.get()),
                str(label_interval_show.cget("text")), str(entry_with_whom.get()),
                str(entry_where.get())
            )
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        entry_date.delete(0, tk.END )
        entry_starting_time.delete( 0, tk.END )
        entry_ending_time.delete( 0, tk.END )
        label_interval_show.config( text = "Interval will be shown here" )
        entry_with_whom.delete( 0, tk.END )
        entry_where.delete(0,tk.END)
        
        parent.destroy()
        root.deiconify()
        messagebox.showinfo("Successful!", "You have successfully created an event")

def read() :
    tree.delete( *tree.get_children() )
    Database()
    cursor.execute("SELECT * FROM 'event1' ORDER BY `date_of_event` DESC  ")  
    fetch = cursor.fetchall()
    
        
    for data in  fetch :
        tree.insert( '', "end", values = ( data[0], data[1], data[2], data[3], data[4], data[5], data[6] ) )
    cursor.close()
    conn.close()
    messagebox.showinfo("Successful", "Events are successfully read")   
    
def delete_event() :
    if not tree.selection() :
        messagebox.showinfo("Error!", "Please select an event first ")
    else :
        result = messagebox.askquestion("Warning", "Are you sure you want to delete this event ?",
                                         icon = "warning")
        if result == 'yes' :
            curItem = tree.focus()#returns the iid of the selected row
            contents = ( tree.item(curItem) ) #returns dictionary 
            selectedItem = contents['values'] #accessing dictionary element with key->'values' and value->selected row(list)
            tree.delete(curItem) 
            Database()
            
            cursor.execute( "DELETE FROM `event1` WHERE `event_id` = %d" % selectedItem[0] )
            
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Successful", "Successfully deleted the event from event scheduler")
            
            
            
def edit_event (parent ):
    Database()
    tree.delete( *tree.get_children() )
    cursor.execute( '''UPDATE `event1` 
                          SET `date_of_event` = ?,
                              `starting_time` = ?,
                              `ending_time` = ?, 
                              `interval` = ?, 
                              `with_whom` = ?, 
                              `_where` = ?
                        WHERE `event_id` = ?''',
                    ( 
                      str(entry_date.get()), str(entry_starting_time.get()), 
                      str(entry_ending_time.get()), str(label_interval_show.cget("text")),
                      str(entry_with_whom.get()), str(entry_where.get()), str(event_id)
                    )  
    )
    conn.commit()
    cursor.execute( "SELECT * FROM `event1` ORDER BY `date_of_event` DESC")  
    fetch = cursor.fetchall()
    for data in fetch :
        tree.insert( '', 'end',
                      values = ( data[0], data[1], data[2], data[3], data[4], data[5], data[6] )
        )
    cursor.close()
    conn.close()  
    
    entry_date.delete( 0, tk.END )  
    entry_starting_time.delete( 0, tk.END )
    entry_ending_time.delete( 0, tk.END )
    label_interval_show.config( text = "Interval will be shown here" )
    entry_with_whom.delete( 0, tk.END )
    entry_where.delete( 0, tk.END )
    
    parent.destroy()
    root.deiconify()
    messagebox.showinfo( "Successful", "The changes in the event detail have been successfully saved" )
    
    
if __name__  ==  '__main__' :
    root = tk.Tk()
    root.title( "Event Scheduler" )
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    width = 900
    height = 500
    
    x = (screen_width - width)/2
    y = (screen_height - height)/2
    
    #root.geometry("900x500")
    root.geometry("%dx%d+%d+%d" % (width, height, x, y ))#to place in centre of screen
    root.resizable(0, 0)


    #=========================================Frames================================================
    
    frame_left = tk.Frame( root, width = 450, height = 700, bd = 5 , relief = 'raise' )
    frame_left.pack( side = tk.LEFT, fill = tk.Y)
    
    frame_right = tk.Frame( root, width = 450, height = 700, bd = 5, relief = 'raise')
    frame_right.pack( side = tk.RIGHT)
    
    #frame for buttons
    frame_top =  tk.Frame( frame_left, width = 450, height = 250, bd = 5, relief = 'raise', padx = 40 )
    frame_top.pack( side = tk.TOP , fill = tk.Y)
    
    #frame for calendar
    frame_bottom = tk.Frame( frame_left, width = 450, height = 250, bd = 5, relief = 'raise' )
    frame_bottom.pack( side = tk.BOTTOM, fill = tk.X )
    
    
    #=========================================Buttons===============================================
    #Button to open "Add Event" window
    btn_add_event = tk.Button(  frame_top , text = "Add Event", command = button_save_chooser ,
                                 bg = '#f4b042', relief = RAISED )
    btn_add_event.flash()
    btn_add_event.grid( row = 0, column = 0, padx = 20, pady = 10 )
    
    #Button to Read event
    btn_see_event = tk.Button( frame_top, text = "See Events", command = read )
    btn_see_event.grid( row = 1, column = 0 , padx = 20, pady = 10 )
    
    #Button to Delete event
    btn_delete_event = tk.Button( frame_top, text = "Delete Event", command = delete_event )
    btn_delete_event.grid( row = 2 , column = 0, padx = 20, pady = 10 )
    
    #Button to Edit Event
    btn_edit_event = tk.Button( frame_top, text = "Edit Event", command = button_edit_chooser )
    btn_edit_event.grid( row = 3, column = 0, padx = 20, pady = 10 )
    
    data = {}
    cal = Calendar( frame_bottom, data )
    
    #==========================================ttk.Treeview widget===================================
    scrollbary = tk.Scrollbar( frame_right, orient = tk.VERTICAL )
    scrollbarx = tk.Scrollbar( frame_right, orient = tk.HORIZONTAL )
    tree = ttk.Treeview( 
                            frame_right,
                            columns = ( "Event_id","Date", "Starting_time", "Ending_time",
                                                      "Interval", "With_whom", "Where"
                            ),
                            selectmode = "extended",#The user may select multiple items at once.
                            height = 500,
                            yscrollcommand = scrollbary.set,
                            xscrollcommand = scrollbarx.set
                        )
    scrollbary.config( command = tree.yview )
    scrollbary.pack( side = tk.RIGHT, fill = tk.Y)
    scrollbarx.config( command = tree.xview )
    scrollbarx.pack( side = tk.BOTTOM, fill = tk.X)
    
    tree.heading( 'Event_id', text = "Event Id", anchor = tk.W )
    tree.heading( 'Date', text = 'Date', anchor = tk.W )
    tree.heading( 'Starting_time', text = 'Starting Time', anchor = tk.W )
    tree.heading( 'Ending_time', text = 'Ending Time', anchor = tk.W )
    tree.heading( 'Interval', text = 'Interval', anchor = tk.W )
    tree.heading( 'With_whom', text = 'With Whom', anchor = tk.W )
    tree.heading( 'Where', text = 'Where', anchor = tk.W )
    
    tree.column( '#0', stretch = False, minwidth = 0, width = 0 )
    tree.column( '#1', stretch = False, minwidth = 0, width = 0 )
    tree.column( '#2', stretch = False, minwidth = 0, width = 120 )
    tree.column( '#3', stretch = False, minwidth = 0, width = 120 )
    tree.column( '#4', stretch = False, minwidth = 0, width = 120 )
    tree.column( '#5', stretch = False, minwidth = 0, width = 120 )
    tree.column( '#6', stretch = False, minwidth = 0, width = 150 )
    tree.column( '#7', stretch = False, minwidth = 0, width = 300 )
    tree.pack()
    
    root.mainloop()
    
'''
* if..else in calc_interval
    if entry_time1.get() =='' or entry_time2 == ''
        messagebox
    else
        compute
* in Add event window,
     (i)  give expected format/e.g. before each entry.
     (ii)  Checking if the date is entered is in format      
     
*  fit frame towards left of tree frame or place Add_event window in same frame as that of tree
     by destroying one frame and loading other.
* Synchronise the calendar with tree
      (i)  those dates should be coloured which are having events
              soln: in setup()
                  check date is in database
      (ii) clicking on dates should give the events on that date
      (iii) 
* correct the day_name in setup()
        soln: by using the row in which the button is placed
*   adding images to button( add, see, delete, edit )
*   adding transluscent backgroung image to frame
'''