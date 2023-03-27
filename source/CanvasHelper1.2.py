import tkinter as tk
from tkinter import *
from tkinter import ttk
from canvasapi import Canvas

#creating main window
root = Tk()
root.title('CanvasHelper v1.1')
root.iconbitmap('icon.ico')

#creating and filling notebook for tabs
notebook = ttk.Notebook(root,width=500,height=600)
notebook.pack()


#-----------------Page 1-----------------------------------------------
#page 1 frame
content = ttk.Frame(notebook,width=400,height=600)

#function to print to the status log
def log_message():
    global message
    output_log['state'] = 'normal'
    output_log.insert(END,message + '\n')
    output_log.see(END)
    output_log['state'] = 'disabled'

#function to set courses
def set_courses():
    global canvas

    set_courses_working_label['text'] = 'Working...'

    #clear the group fields
    source_group_text['state'] = 'normal'
    target_group_text['state'] = 'normal'
    source_group_text.delete(1.0,END)
    target_group_text.delete(1.0,END)

    #temporarily disable buttons
    import_button['state'] = 'disabled'
    sync_button['state'] = 'disabled'
    root.update_idletasks()

        
    #creating source and target courses
    try:
        global source_course
        global target_course

        #course objects
        source_course = canvas.get_course(int(source_course_num.get()))
        target_course = canvas.get_course(int(target_course_num.get()))
    
        source_course_name.set(source_course.name[0:45] + '...' + str(source_course.id))
        target_course_name.set(target_course.name[0:45] + '...' + str(target_course.id))
        sign_in_error_label['text'] = ''
        print('Source and Target Courses Set')
        global message
        message = 'Source and Target Courses Set'
        log_message()
        sign_in_error_label['text'] = ''
        root.update_idletasks()

        #display in text fields
        displayGroups()
        displayGroupAssignments()
        set_courses_working_label['text'] = ''
        #sync_status_label['text'] = ''

    #error handling
    except NameError:
        sign_in_error_label['text'] = 'No sign-in found.\nPlease log in and try again.'
        set_courses_working_label['text'] = ''
        print('no sign-in found')
    except:
        source_course_name.set('')
        target_course_name.set('')
        set_courses_working_label['text'] = ''
        sign_in_error_label['text'] = 'Course error.\n You may not have access\n to this course.'
        print('Course number error')


#fetches and displays group assignments
def displayGroupAssignments():
    global source_course
    global target_course

    global message
    message = '\nFetching Group Assignments...'
    log_message()
    root.update_idletasks()

    #clear text fields
    source_assignment_text['state'] = 'normal'
    target_assignment_text['state'] = 'normal'
    source_assignment_text.delete(1.0,END)
    target_assignment_text.delete(1.0,END)

    #fetch and count number of group assignments
    source_count = 0
    source_assignments = source_course.get_assignments()

    for source_assignment in source_assignments:
        if(source_assignment.submission_types == ['discussion_topic']):
            if(source_assignment.discussion_topic['group_category_id'] != None):
                print('group discussion detected')
                source_count += 1
                source_assignment_text.insert(END,str(source_assignment.discussion_topic['group_category_id']) + ' ' + source_assignment.name +'\n')
                

    for source_assignment in source_assignments:
        if(source_assignment.group_category_id != None):
            print('group assignment detected')
            source_count += 1
            source_assignment_text.insert(END,str(source_assignment.group_category_id) + ' ' + source_assignment.name +'\n')
        
    source_assignment_text['state'] = 'disabled'


    target_count = 0
    target_assignments = target_course.get_assignments()

    for target_assignment in target_assignments:
        if(target_assignment.submission_types == ['discussion_topic']):
            if(target_assignment.discussion_topic['group_category_id'] != None):
                print('group discussion detected')
                target_count += 1
                target_assignment_text.insert(END,str(target_assignment.discussion_topic['group_category_id']) + ' ' + target_assignment.name +'\n')

    for target_assignment in target_assignments:
        if(target_assignment.group_category_id != None):
            print('group assignment detected')
            target_count += 1
            target_assignment_text.insert(END,str(target_assignment.group_category_id) + ' ' + target_assignment.name +'\n')


    target_assignment_text['state'] = 'disabled'

    #log the number of group assignments in each course
    message = ' Group assignments fetched (Source:' + str(source_count) + ' Target:' + str(target_count) + ')'
    log_message()
    root.update_idletasks()

                
#function fetches and displays groups
def displayGroups(option='all'):
    global message
    
    global source_course
    global target_course

    
    root.update_idletasks()
    target_group_text['state'] = 'normal'
    target_group_text.delete(1.0,END)

    if(option == 'all'):

        message = '\nFetching Groups...'
        log_message()
        sync_status_label['text'] = ''
        root.update_idletasks()
        
        source_group_text['state'] = 'normal'
        source_group_text.delete(1.0,END)
        
        source_group_count = 0
        source_group_categories = source_course.get_group_categories()
        for category in source_group_categories:
            source_group_count += 1
            source_group_text.insert(END,str(category.id) + ' ' + category.name + "\n")

            message = ' Group category ' + category.name + ' fetched'
            log_message()
            root.update_idletasks()
            
            category_groups = category.get_groups()
            for group in category_groups:
                print(group.name)
                source_group_text.insert(END,"  " + group.name + "\n")
        if(source_group_count == 0):
            source_group_text.insert(END,'No groups')
        source_group_text['state'] = 'disabled'

    target_group_count = 0
    target_group_categories = target_course.get_group_categories()
    for category in target_group_categories:
        target_group_count += 1
        target_group_text.insert(END,str(category.id) + ' ' + category.name + "\n")
        category_groups = category.get_groups()
        for group in category_groups:
            print(group.name)
            target_group_text.insert(END,"  " + group.name + "\n")
    if(target_group_count == 0):
        target_group_text.insert(END,'No groups')
    target_group_text['state'] = 'disabled'

    import_button['state'] = 'normal'
    sync_button['state'] = 'normal'




def importGroups():
    
    import_button['state'] = 'disabled'
    sync_button['state'] = 'disabled'
    set_courses_working_label['text'] = 'Working...'
    global message
    message = '\nImporting groups...'
    log_message()
    root.update_idletasks()

    
    #deleting groups in target course
    global target_course
    target_categories = target_course.get_group_categories()

    for group_category in target_categories:
        group_category.delete()

    #importing groups
    global source_course
    source_categories = source_course.get_group_categories()

    for source_category in source_categories:
      print("Group category: " + source_category.name)
      target_category = target_course.create_group_category(source_category.name)

      source_groups = source_category.get_groups()
      for source_group in source_groups:

        print("  " + source_group.name)
        target_category.create_group(name=source_group.name)
        
      print("\n")
      target_category.update(group_limit=source_category.group_limit)    
    set_courses_working_label['text'] = ''
    
    message = 'Groups successfully imported'
    log_message()
    message = ' Group sets imported:'
    log_message()
    for source_category in source_categories:
        message = '   ' + source_category.name
        log_message()
    root.update_idletasks()
    displayGroups('target')

#begins our assignment syncing process
def start_sync():
    
    import_button['state'] = 'disabled'
    sync_button['state'] = 'disabled'
    set_courses_working_label['text'] = 'Working...'
    sync_status_label['text'] = ''
    global message
    message = '\nVerifying classes...'
    log_message()
    root.update_idletasks()
    check_classes()

#groups and assignments need to be in the same order for sync to work
def check_classes():
    global message
    
    global source_course
    global target_course

    source_group_categories = source_course.get_group_categories()
    target_group_categories = target_course.get_group_categories()


    passed = True

    #making sure group category names are the same
    source_category_count = 0
    target_category_count = 0
    #making sure number of group categories is the same
    for target_category in target_group_categories:
      target_category_count += 1
    for source_category in source_group_categories:
      source_category_count += 1
    if(source_category_count != target_category_count):
      passed = False
    #making sure names of group categories are the same
    if(passed):
      for i in range(source_category_count):
        if(source_group_categories[i].name != target_group_categories[i].name):
          passed = False

    if(passed):
      for i in range(source_category_count):
        source_group_count = 0
        target_group_count = 0
        source_groups = source_group_categories[i].get_groups()
        target_groups = target_group_categories[i].get_groups()
        for group in source_groups:
          print(group.name)
          source_group_count += 1
        for group in target_groups:
          print(group.name)
          target_group_count += 1
        if(source_group_count == target_group_count):
          for i in range(source_group_count):
            print(source_groups[i].name, target_groups[i].name)
            if(source_groups[i].name != target_groups[i].name):
              passed = False
        else:
          passed = False
    
    #create our group dictionary while we are here
    if(passed):
        global group_category_dictionary
        message = '\nCreating group matching dictionary'
        log_message()
        root.update_idletasks()
        group_category_dictionary = {}

        count = 0
        for source_category in source_group_categories:
            if (source_category.name == target_group_categories[count].name):
                print("Group categories match")
                group_category_dictionary[source_category.id] = target_group_categories[count].id
            count += 1

        print(group_category_dictionary)
        message = str(group_category_dictionary)
        log_message()
        root.update_idletasks()
    
    #assignments
    source_course_assignments = source_course.get_assignments()
    target_course_assignments = target_course.get_assignments()

    source_assignment_count = 0
    target_assignment_count = 0
    for assignment in source_course_assignments:
      source_assignment_count += 1
    for assignment in target_course_assignments:
      target_assignment_count += 1
    if(source_assignment_count != target_assignment_count):
      passed = False

    if(passed):
      for i in range(source_assignment_count):
        if(source_course_assignments[i].name != target_course_assignments[i].name):
          passed = False

    if(passed):
        print('course groups and assignments are identical... preparing to sync')
        set_courses_working_label['text'] = 'Working...'
        sync_status_label['text'] = 'Course groups and assignments match. Syncing now...'
        sync_status_label['foreground'] = 'green'

        
        message = '\nVerification complete, syncing courses...'
        log_message()
        root.after(200,sync_classes)
    else:
        sync_status_label['text'] = 'Courses were not identical. Please revise and re-set courses.'
        sync_status_label['foreground'] = 'red'
        set_courses_working_label['text'] = ''
        message = '\nVerification failed'
        log_message()
        import_button['state'] = 'disabled'
        sync_button['state']= 'disabled'

#syncing course assignments
def sync_classes():
    print('Syncing classes...')
    global message
    
    source_assignments = source_course.get_assignments()
    target_assignments = target_course.get_assignments()
    global group_category_dictionary

    count1 = 0
    count2 = 0
    for assignment in source_assignments:
      count1 += 1
    for assignment in target_assignments:
      count2 += 1

    if(count1 != count2):
      raise Exception("Course assignment lists are not the same size")


    #iterate through assignments
    for i in range(0,count1):


      
      #if our submission type is discussion topic
      if(target_assignments[i].submission_types == ['discussion_topic']):

        #for that discussion assignment, iterate through our dictionary of group category id's (indexed by source id)
        for group_id in group_category_dictionary:


          #if this assignment discussion topic group category id matches with one in the dictionary (it should match only once or not at all)
          if(source_assignments[i].discussion_topic['group_category_id'] == group_id):

            #snag the discussion_topic id from the current assignment (in the target course)
            discussion_id = target_assignments[i].discussion_topic['id']

            #fetch the discussion_topic from target course using its id
            target_discussion = target_course.get_discussion_topic(discussion_id)


            #update that discussion's group category using the corresponding source group_category_id as the index in the dictionary
            target_discussion.update(group_category_id=group_category_dictionary[group_id])

            #print statement
            print("Group Category " + str(group_id) + " matched to discussion " + source_assignments[i].name)



      #for general assignments
      else:
        
        for group_id in group_category_dictionary:

          if(source_assignments[i].group_category_id == group_id):

            target_assignments[i].edit(assignment={'group_category_id': group_category_dictionary[group_id]})
            
            root.update_idletasks()
            print("Group Category " + str(group_id) + " matched to assignment " + source_assignments[i].name)


    set_courses_working_label['text'] = ''
    sync_status_label['text'] = 'Courses have been successfully synced. Re-set courses to sync again.'
    message = '\nSync successful. Group assignments have been set  in the target course'
    log_message()
    root.update_idletasks()

#instantiating widgets in content frame
source_course_num_label = ttk.Label(content,text='Source Course #:')
target_course_num_label = ttk.Label(content, text='Target Course #:')
source_course_num = StringVar()
target_course_num = StringVar()
source_course_num_entry = ttk.Entry(content,textvariable=source_course_num)
target_course_num_entry = ttk.Entry(content,textvariable=target_course_num)
set_courses_button = ttk.Button(content,text='Set Courses',command=set_courses)
set_courses_working_label = ttk.Label(content,font = 'TKDefault 10 bold',foreground='green')
sign_in_error_label = ttk.Label(content,text='',foreground='red',font='TKDefault 8 italic')
current_courses_label = ttk.Label(content,text='Current Set Courses:',font='TkDefaultFont 8 bold')
source_course_label = ttk.Label(content,text='Source Course:')
target_course_label = ttk.Label(content,text='Target Course:')
source_course_name = StringVar()
source_course_name_label = ttk.Label(content, textvariable=source_course_name,font='TkDefaultFont 8 bold')
target_course_name = StringVar()
target_course_name_label = ttk.Label(content, textvariable=target_course_name,font='TkDefaultFont 8 bold')
source_group_label = ttk.Label(content, text='Source Course Groups', font='TkDefaultFont 8 bold')
source_group_text = Text(content,height=5,width=20,wrap=NONE)
source_group_text['state'] = 'disabled'
source_group_scrollbar = ttk.Scrollbar(content, orient='vertical',command=source_group_text.yview)
source_group_text['yscrollcommand'] = source_group_scrollbar.set
target_group_label = ttk.Label(content, text='Target Course Groups', font='TkDefaultFont 8 bold')
target_group_text = Text(content,height=5,width=20,wrap=NONE)
target_group_text['state'] = 'disabled'
target_group_scrollbar = ttk.Scrollbar(content, orient='vertical',command=target_group_text.yview)
target_group_text['yscrollcommand'] = target_group_scrollbar.set
import_button = ttk.Button(content,text='Import\nGroups',command=importGroups)
import_button['state'] = 'disabled'
import_label = ttk.Label(content,text='→',font='Helvetica 20 bold')
import_warning = ttk.Label(content,text='Warning: Importing groups will delete the existing groups in the target course.\nIn a future update more features will be added.',foreground='red',font='TKDefault 8 italic')
source_assignment_label = ttk.Label(content, text='Source Group Assignments', font='TkDefaultFont 8 bold')
source_assignment_text = Text(content,height=5,width=20,wrap=NONE)
source_assignment_text['state'] = 'disabled'
source_assignment_scrollbar = ttk.Scrollbar(content, orient='vertical',command=source_assignment_text.yview)
source_assignment_text['yscrollcommand'] = source_assignment_scrollbar.set
target_assignment_label = ttk.Label(content, text='Target Group Assignments', font='TkDefaultFont 8 bold')
target_assignment_text = Text(content,height=5,width=20,wrap=NONE)
target_assignment_text['state'] = 'disabled'
target_assignment_scrollbar = ttk.Scrollbar(content, orient='vertical',command=target_assignment_text.yview)
target_assignment_text['yscrollcommand'] = target_assignment_scrollbar.set
sync_button = ttk.Button(content,text='       Sync\nAssignments',command=start_sync)
sync_button['state'] = 'disabled'
sync_label = ttk.Label(content,text='∞',font='Helvetica 20 bold')
sync_warning_label = ttk.Label(content,font='TKDefault 8 italic',text='Before syncing, Canvashelper will check that groups and assignments are identical and\nin the same order in both courses. Assignment groupings do not cause issues,\nbut it is recommended to delete the empty \'Assignments\' group, if present, before syncing.')
sync_status_label = ttk.Label(content,font='TKDefault 8 bold',foreground='red')
output_log_label = ttk.Label(content,text='Status Log',font='TKDefault 8 bold')
output_log = Text(content,height=8,width=50)
output_log['state'] = 'disabled'
output_log['foreground'] = 'blue'

#inserting widgets into content frame
content.grid(column=0, row=0)
source_course_num_label.grid(column=0,row=0,padx=5,pady=5)
target_course_num_label.grid(column=0,row=1,padx=5,pady=5)
source_course_num_entry.grid(column=1,row=0)
target_course_num_entry.grid(column=1,row=1)
set_courses_button.grid(column=2,row=0,rowspan=2,padx=15)
set_courses_working_label.grid(column=1,row=5,rowspan=2)
sign_in_error_label.grid(column=2,row=2,rowspan=2,padx=(15,0))
current_courses_label.grid(column=0,row=2,padx=5)
source_course_label.grid(column=0,row=3)
target_course_label.grid(column=0,row=4)
source_course_name_label.grid(column=1,row=3,columnspan=2)
target_course_name_label.grid(column=1,row=4,columnspan=2)
source_group_label.grid(row=6,column=0,pady=(10,0))
source_group_text.grid(row=7,column=0)
source_group_scrollbar.grid(row=7,column=1,sticky=(N,S,W))
target_group_label.grid(row=6,column=2,pady=(10,0))
target_group_text.grid(row=7,column=2)
target_group_scrollbar.grid(row=7,column=3,sticky=(N,S,W))
import_button.grid(row=7,column=1,pady=(0,35),padx=(15,0))
import_label.grid(row=7,column=1,pady=(45,0),padx=(15,0))
import_warning.grid(row=8,column=0,columnspan=3)
source_assignment_label.grid(row=9,column=0,pady=(10,0))
source_assignment_text.grid(row=10,column=0)
source_assignment_scrollbar.grid(row=10,column=1,sticky=(N,S,W))
target_assignment_label.grid(row=9,column=2,pady=(10,0))
target_assignment_text.grid(row=10,column=2)
target_assignment_scrollbar.grid(row=10,column=3,sticky=(N,S,W))
sync_button.grid(row=10,column=1,pady=(0,35),padx=(15,0))
sync_label.grid(row=10,column=1,pady=(45,0),padx=(15,0))
sync_warning_label.grid(row=11,column=0,columnspan=3,padx=(10,0))
sync_status_label.grid(row=12,column=0,columnspan=3)
output_log_label.grid(row=13,column=0,padx=(0,50))
output_log.grid(row=14,column=0,columnspan=3)

#------------------------------------------------------------------------
#-----------------Page 2-------------------------------------------------

#signing in and creating the canvas object
def sign_in(*args):
    global canvas

    try:
        canvas = Canvas(API_ADDRESS.get(),USER_KEY.get())

        current_username.set(canvas.get_current_user().name + ' ID#' + str(canvas.get_current_user().id) + '✔')
        current_username_label['foreground'] = 'green'
        current_username_label['font'] = 'TKDefault 10 bold'
        current_username_label.grid(column=0,row=3,columnspan=2)
        print('Sign-in confirmed')
    except:
        print('Sign-in error')
        current_username.set('Sign-in unsuccessful, check that URL\n and user key are correct')
        current_username_label['foreground'] = 'red'
        current_username_label['font'] = 'TKDefault 10 italic'
        current_username_label.grid(column=0,row=3,columnspan=3)


content2 = ttk.Frame(notebook,width=400,height=600)

#widgets in content2
api_address_label = ttk.Label(content2,text='API Address:')
API_ADDRESS = StringVar()
api_address_entry = ttk.Entry(content2,textvariable=API_ADDRESS)
api_example_label = ttk.Label(content2,text='(ex: https://asu.instructure.com)')
user_key_label = ttk.Label(content2, text='User Key:')

USER_KEY = StringVar()
user_key_entry = ttk.Entry(content2,textvariable=USER_KEY)
signin_button = ttk.Button(content2,text='Sign In',command=sign_in)
current_signedin_label = ttk.Label(content2,text='Current Signed-in User:',font='TKDefaultFont 8 bold')
current_username = StringVar()
current_username_label = ttk.Label(content2,textvariable=current_username,font='TKDefaultFont 8 bold')

#positioning in content2
content2.grid(column=0,row=0)
api_address_label.grid(column=0,row=0,padx=10,pady=(10,5))
api_address_entry.grid(column=1,row=0,pady=(10,5))
api_example_label.grid(column=2,row=0,padx=5)
user_key_label.grid(column=0,row=1,padx=10)
user_key_entry.grid(column=1,row=1)
signin_button.grid(column=2,row=1)
current_signedin_label.grid(column=0,row=2,pady=5,columnspan=2)
current_username_label.grid(column=0,row=3,columnspan=2)

#version label
version_label = ttk.Label(content2,text='CanvasHelper v1.2 CGF ID Team')
version_label.grid(row=10,column=2,padx=(20,0),pady=(470,0))

#tab names
notebook.add(content, text='Home')
notebook.add(content2, text='Configure')

root.mainloop()
