
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from mypackages import tkint_gui_const as gc  # constants for the GUI application
import os
import json
import pandas as pd


class p101_class:

    def __init__(self):
        self.gui = Tk()  # instantiate the gui handler
        self.winWidth = self.gui.winfo_screenwidth()  # GUI window width
        self.winHeight = self.gui.winfo_screenheight()  # GUI window height
        self.gui.minsize(width=int(self.winWidth), height=int(self.winHeight))  # create full screen GUI

        print(f"width={self.winWidth} height={self.winHeight}")

        self. gui.title(gc.TITLE_STRING)  # display app bar title
        self.gui.iconbitmap(gc.TITLE_ICON_FILE)  # display app bar icon

        self.mainCanvas = Canvas(self.gui, bg="blue", width=self.winWidth, height=self.winHeight)  # create canvas for widget placement
        self.mainCanvas.pack()  # display the canvas

        self.mainCanvas.create_rectangle(gc.OUTPUT_FOLDER_BUTTON_POS['x'] - 100, gc.OUTPUT_FOLDER_BUTTON_POS['y'] - 100,\
                                         gc.OUTPUT_FOLDER_BUTTON_POS['x'] + 250, gc.OUTPUT_FOLDER_BUTTON_POS['y'] + 100,\
                                         fill='red')

        self.messageBox_pos = {'x': -1, 'y': -1}  # to be updated
        self.messagebox = self.create_message_box()

        self.output_folder_button = Button(self.gui, text="~Select Output Folder~", command=self.output_folder_button_callback)
        self.mainCanvas.create_window(gc.OUTPUT_FOLDER_BUTTON_POS['x'], gc.OUTPUT_FOLDER_BUTTON_POS['y'], window=self.output_folder_button)  # specify x,y location in canvas
        self.output_folder_dir = None

        self.config_file_button = Button(self.gui, text="~Select Configuration File~", bg='purple', fg='white', command=self.config_file_button_callback)
        self.mainCanvas.create_window(gc.MENTORS_DIR_BUTTON_POS['x'] + 160, gc.OUTPUT_FOLDER_BUTTON_POS['y'], window=self.config_file_button)  # specify x,y location in canvas
        self.config_filepath = None
        self.config_json_dict = None

        self.teams_member_addition_instructions_button = Button(self.gui, text="~Show instructions for Teams member ADDITION~", fg='blue', command=self.teams_member_addition_instructions_button_callback)
        self.mainCanvas.create_window(self.winWidth - 150, gc.OUTPUT_FOLDER_BUTTON_POS['y'], window=self.teams_member_addition_instructions_button)  # specify x,y location in canvas

        self.teams_member_removal_instructions_button = Button(self.gui, text="~Show instructions for Teams member REMOVAL~", fg='blue', command=self.teams_member_removal_instructions_button_callback)
        self.mainCanvas.create_window(self.winWidth - 150, gc.OUTPUT_FOLDER_BUTTON_POS['y'] + 50, window=self.teams_member_removal_instructions_button)  # specify x,y location in canvas

        self.teams_member_retrieval_instructions_button = Button(self.gui, text="~Show instructions for Teams member RETRIEVAL~", fg='blue', command=self.teams_member_retrieval_instructions_button_callback)
        self.mainCanvas.create_window(self.winWidth - 150, gc.OUTPUT_FOLDER_BUTTON_POS['y'] + 100, window=self.teams_member_retrieval_instructions_button)  # specify x,y location in canvas

        self.mentors_dir_button = Button(self.gui, text="~Select Mentors Directory~", command=self.mentors_dir_button_callback)
        self.mainCanvas.create_window(gc.MENTORS_DIR_BUTTON_POS['x'], gc.MENTORS_DIR_BUTTON_POS['y'], window=self.mentors_dir_button)  # specify x,y location in canvas
        self.mentors_dir = None

        self.mentors_count_button = Button(self.gui, text="~Get Mentor Count~", bg='purple', fg='white', command=self.mentors_count_button_callback)
        self.mainCanvas.create_window(gc.MENTORS_DIR_BUTTON_POS['x'] + 150, gc.MENTORS_DIR_BUTTON_POS['y'], window=self.mentors_count_button)  # specify x,y location in canvas

        self.registration_dir_button = Button(self.gui, text="~Select Registration Directory~", bg='yellow', command=self.registration_dir_button_callback)
        self.mainCanvas.create_window(gc.MENTORS_DIR_BUTTON_POS['x'] + 10, gc.MENTORS_DIR_BUTTON_POS['y'] + 150, window=self.registration_dir_button)  # specify x,y location in canvas
        self.registration_dir = None

        self.prep_onboarding_button = Button(self.gui, text="~Generate Onboarding Files~", bg='yellow', command=self.prep_onboarding_button_callback)
        self.mainCanvas.create_window(gc.MENTORS_DIR_BUTTON_POS['x'] + 10, gc.MENTORS_DIR_BUTTON_POS['y'] + 200, window=self.prep_onboarding_button)  # specify x,y location in canvas

        self.teams_member_file_button = Button(self.gui, text="~Select Teams ALL Members Csv File~", bg='black', fg='white', command=self.teams_member_file_button_callback)
        self.mainCanvas.create_window(gc.MENTORS_DIR_BUTTON_POS['x'] + 300, gc.MENTORS_DIR_BUTTON_POS['y'] + 150, window=self.teams_member_file_button)  # specify x,y location in canvas
        self.teams_member_csv_file = None

        self.teams_member_list_gen_button = Button(self.gui, text="~Extract PARTICIPANT Members Only~", bg='black', fg='white', command=self.teams_member_list_gen_button_callback)
        self.mainCanvas.create_window(gc.MENTORS_DIR_BUTTON_POS['x'] + 300, gc.MENTORS_DIR_BUTTON_POS['y'] + 200, window=self.teams_member_list_gen_button)  # specify x,y location in canvas
        # populates self.participant_emails list

        self.about_message_button = Button(self.gui, text="~About~", bg='purple', fg='white', command=self.about_message_button_callback)
        self.mainCanvas.create_window(self.winWidth - 50, self.messageBox_pos['y'] - 30, window=self.about_message_button)  # specify x,y location in canvas

        self.messagebox_clear_button = Button(self.gui, text="~Press to Clear Box Below~", bg='purple', fg='white', command=self.messageBox_clear_callback)
        self.messageBox_clear_pos = {'x': self.messageBox_pos['x'] + 80, 'y': self.messageBox_pos['y'] - 30}  # to be updated
        self.mainCanvas.create_window(self.messageBox_clear_pos['x'], self.messageBox_clear_pos['y'], window=self.messagebox_clear_button)  # specify x,y location in canvas

        ##### Patent 101 script variables follow
        self.organizers_lists = []  # will have the file paths to mentor lists selected
        self.organizer_emails = []  # will have the emails of each mentor
        self.registration_files_list = []  # will have the paths to Meet Up registration csv files
        self.registration_day_dict = None  # { <day index> : {'alias' : <day's alias>, 'reg_file_list_idx': <index in self.registration_files_list>}}
        self.participant_emails = None  # will store the participant emails as list
        self.attendance_list_dataframe = None  # will store the participant attendance list details as data frame
        self.registration_profile_dataframe = None  # will store the registration profile across all days as data frame
        self.teams_members_dataframe = None  # will store the Teams members list as a data frame to simplify access

    def create_message_box(self):
        # Box used for outputting text messages to the user for guidance
        box_width = self.winWidth - 2 * gc.MESSAGE_BOX_ATTRIBS['x_offset']
        handler = Text(self.gui, state='disabled')  # any edits to the text box are disabled by default.
        self.messageBox_pos['x'] = gc.MESSAGE_BOX_ATTRIBS['x_offset']
        self.messageBox_pos['y'] = self.winHeight - (gc.MESSAGE_BOX_ATTRIBS['box_height'] + gc.MESSAGE_BOX_ATTRIBS['y_offset'])
        handler.place(x=self.messageBox_pos['x'], y=self.messageBox_pos['y'], width=box_width, height=gc.MESSAGE_BOX_ATTRIBS['box_height'])

        return handler  # for giving access to the message box created

    def messagebox_write(self, position, text_string):
        # displays  in messagebox widget at given position
        self.messagebox['state'] = 'normal'  # enable text edit in box
        self.messagebox.insert(position, text_string)
        self.messagebox.see(END) # autoscroll to see the newest text output in message box
        self.messagebox['state'] = 'disabled' # disable edits by user after text update

    def messageBox_clear_callback(self):
        self.messagebox['state'] = 'normal'  # enable text edit in box
        self.messagebox.delete("1.0", END)
        self.messagebox['state'] = 'disabled'  # disable edits by user after text update

    def about_message_button_callback(self):
        messagebox.showinfo(gc.TOOL_NAME_STRING, f'\t\tversion - {gc.APPLICATION_VERSION_STRING} \n\n== Please forward queries to cagri.tanriover@intel.com ==')

    def mentors_dir_button_callback(self):
        self.mentors_dir = filedialog.askdirectory()
        self.messagebox_write(END, "Selected mentors directory: " + self.mentors_dir + "\n")
        self.organizers_lists = self.get_mentors_files()  # attempts to get the file paths to all mentor files
        if len(self.organizers_lists):
            self.get_mentors_emails()  # populates the self.organizer_emails list
            self.generate_supporting_mentors_file()  # creates gc.SUPPORTING_MENTORS_FILENAME file with mentor emails for communication.

    def generate_supporting_mentors_file(self):
        filePath = os.path.join(self.output_folder_dir, gc.DEFAULT_CONFIG_DICT["SUPPORTING_MENTORS_FILENAME"])
        fCC = open(filePath, 'w')

        for eachEmail in self.organizer_emails:
            fCC.write(eachEmail + ';')  # semicolon separated emails in text file for Outlook To field
        fCC.close()

    def get_mentors_files(self):

        file_list = os.listdir(self.mentors_dir)
        fullpaths_list = []

        if len(file_list) == 0:
            # No files found!
            self.messagebox_write(END, f"FAILED : No files found under {self.mentors_dir}. Please retry...\n")
        else:
            # Files found. Create return list with full path info next

            for eachFile in file_list:
                if eachFile.split('.')[-1] == 'txt':
                    # found file with txt extension as expected
                    temp_path = os.path.join(self.mentors_dir, eachFile)
                    fullpaths_list.append(temp_path)
                    self.messagebox_write(END, f"SUCCESS : Located {fullpaths_list[-1]}\n")

            if len(fullpaths_list) == 0:
                # Could not find any file with txt extension.
                self.messagebox_write(END, f"FAILED : No file with extension *.txt under {self.mentors_dir} Please retry...\n")

        return fullpaths_list

    def get_mentors_emails(self):

        for eachFile in self.organizers_lists:
            with open(eachFile) as f:
                lines = f.readlines()

                # lines will be a single element list as a long string of ; delimited emails
                email_list = lines[0].split(';')  # all emails are in this list

                for eachEmail in email_list:
                    if eachEmail not in self.organizer_emails:
                        self.organizer_emails.append(eachEmail)  # a new mentor email found
                    #else: #not a unique email. Skipping

    def mentors_count_button_callback(self):
        # Counts the number of unique mentors available
        self.messagebox_write(END, f"INFO : There are {len(self.organizer_emails)} mentors\n")

    def registration_dir_button_callback(self):
        self.registration_dir = filedialog.askdirectory()
        self.messagebox_write(END, "Selected registration directory: " + self.registration_dir + "\n")
        self.registration_files_list = self.get_registration_files()  # attempts to get the file paths to all Meet Up registration csv files
        # Next extract the day alias for each registration file detected. (expected format for each file is xx_N_xx.csv where N is the workshop day number)
        if len(self.registration_files_list):
            self.registration_day_dict = self.extract_registration_day_aliases()
            self.messagebox_write(END, "Following registration day naming convention will be used:" + "\n")
            for eachDay in self.registration_day_dict:
                self.messagebox_write(END, f"{self.registration_day_dict[eachDay]['alias']} ---> {self.registration_files_list[self.registration_day_dict[eachDay]['reg_file_list_idx']]}" + "\n")

    def get_registration_files(self):

        file_list = os.listdir(self.registration_dir)
        fullpaths_list = []

        if len(file_list) == 0:
            # No files found!
            self.messagebox_write(END, f"FAILED : No files found under {self.registration_dir}. Please retry...\n")
        else:
            # Files found. Create return list with full path info next

            for eachFile in file_list:
                if eachFile.split('.')[-1] == 'csv':
                    # found file with csv extension as expected
                    temp_path = os.path.join(self.registration_dir, eachFile)
                    fullpaths_list.append(temp_path)
                    self.messagebox_write(END, f"SUCCESS : Located {fullpaths_list[-1]}\n")

            if len(fullpaths_list) == 0:
                # Could not find any file with csv extension.
                self.messagebox_write(END, f"FAILED : No file with extension *.csv under {self.registration_dir} Please retry...\n")

        return fullpaths_list

    def extract_registration_day_aliases(self):
        # ret_dict = { <day index> : {'alias' : <day's alias>, 'reg_file_list_idx': <index in self.registration_files_list>}}

        num_days = len(self.registration_files_list)  # number of registration files gives the number of workshop days
        keys = [i+1 for i in range(num_days)]  # starts from 1 as the expected first day string
        ret_dict = {key: {} for key in keys}  # creates a keys only dictionary
        # Check filename compliance first
        naming_compliant = self.check_day_naming_compliance(keys)

        # Depending on the naming_compliant state, proceed with the right processing
        if naming_compliant:
            # number of days and the numbering of days are as expected
            for fileIdx, eachFile in enumerate(self.registration_files_list):
                filename = eachFile.split('\\')[-1].split('.')[0]  # gives the filename WITHOUT the extension
                delimited_fields = filename.split('_')  # at least two underscores expected in filename (i.e. day_1_xxxx etc)
                cur_key = int(delimited_fields[1])  # second field is the day number
                cur_day_alias = delimited_fields[0] + '_' + delimited_fields[1]  # created the day alias
                ret_dict[cur_key]['alias'] = cur_day_alias
                ret_dict[cur_key]['reg_file_list_idx'] = fileIdx  # index to use while accessing self.registration_files_list through ret_dict
        else:
            # registration file names are not following the expected convention. Assign alias randomly.
            for fileIdx, eachFile in enumerate(self.registration_files_list):
                cur_day_alias = 'day_' + str(fileIdx + 1)  # created the day alias
                ret_dict[fileIdx + 1]['alias'] = cur_day_alias
                ret_dict[fileIdx + 1]['reg_file_list_idx'] = fileIdx  # index to use while accessing self.registration_files_list through ret_dict

        return ret_dict

    def check_day_naming_compliance(self, keys):
        naming_compliant = True
        for eachFile in self.registration_files_list:
            filename = eachFile.split('\\')[-1].split('.')[0]  # gives the filename WITHOUT the extension
            delimited_fields = filename.split('_')  # at least two underscores expected in filename (i.e. day_1_xxxx etc)
            if len(delimited_fields) < 2:
                # Not in compliance with the expected file naming convention.
                naming_compliant = False
                break  # exit for loop
            else:
                # Might be compliant.
                # Check the delimited_fields[1] value to make sure it is a number between [1,num_days]
                isInt = True
                try:
                    # converting to integer
                    int(delimited_fields[1])
                except ValueError:
                    isInt = False

                if isInt:
                    # second field is an integer
                    cur_day_num = int(delimited_fields[1])
                    if cur_day_num in keys:
                        keys.remove(cur_day_num)  # expect the day numbers in registration files to be unique !
                    else:
                        naming_compliant = False
                        break  # exit for loop
                else:
                    naming_compliant = False
                    break  # exit for loop

        return naming_compliant

    def output_folder_button_callback(self):
        self.output_folder_dir = filedialog.askdirectory()
        self.messagebox_write(END, "Selected output directory: " + self.output_folder_dir + "\n")

    def config_file_button_callback(self):
        self.config_filepath = filedialog.askopenfilename()  # selects a file

        # Next check to make sure the specified file matches the expected fiename
        specified_file_name = self.config_filepath.split('/')[-1]
        if specified_file_name.lower() == gc.CONFIGURATION_FILENAME:
            self.messagebox_write(END, "Selected configuration file: " + self.config_filepath + "\n")

            with open(self.config_filepath) as fIn:
                self.config_json_dict = json.load(fIn)

            # Next compare built in defaults in gc.DEFAULT_CONFIG_DICT and self.config_json_dict
            # and update gc.DEFAULT_CONFIG_DICT if needed for use as reference in the application
            self.update_default_config()

        else:
            self.messagebox_write(END, "User selection: " + self.config_filepath + "\n")
            self.messagebox_write(END, f"ERROR: Filename {specified_file_name} invalid. Please provide {gc.CONFIGURATION_FILENAME} file " + "\n")
            self.config_filepath = ''  # invalidate file variable

    def update_default_config(self):

        for eachKey in gc.DEFAULT_CONFIG_DICT:
            if eachKey in self.config_json_dict:
                # key exists
                if self.config_json_dict != gc.DEFAULT_CONFIG_DICT:
                    gc.DEFAULT_CONFIG_DICT[eachKey] = self.config_json_dict[eachKey]  # update using user filename
                #else do not change default as it is the same as user's
            #else key does not exist in user file. Leave defaults alone.
            self.messagebox_write(END, f"Using {eachKey} = {gc.DEFAULT_CONFIG_DICT[eachKey]}" + "\n")

    def prep_onboarding_button_callback(self):
        # 1 - Prepare attendees list for tracking purposes
        # 2 - Prepare the status of the participants across all days of the workshop
        # 3 - Prepare Teams compliant csv list of all participants that need to be added to relevant Teams space
        # 4 - Prepare semicolon delimited text file with all participants' emails (for email correspondence as needed)

        # Following generates the attendance data frame including all participants
        # Following also populates the emails list for all the participants on all registration days.
        # Following also populated the registration profile for each workshop day
        self.participant_emails, self.attendance_list_dataframe, self.registration_profile_dataframe = self.get_participants_registration_details()

        # Write generated reports to relevant output files

        filepath = os.path.join(self.output_folder_dir, gc.DEFAULT_CONFIG_DICT["TEAMS_INPUT_PARTICIPANTS_FILENAME"])
        fTeamsCsv = open(filepath, 'w')
        fTeamsCsv.write('email\n')  # this is the column name assigned to the csv file (this is needed in PowerShell command!)

        filepath = os.path.join(self.output_folder_dir, gc.DEFAULT_CONFIG_DICT["SEMICOLON_DELIMITED_PARTICIPANTS_FILENAME"])
        fCcTxt = open(filepath, 'w')

        for eachEntry in self.participant_emails:
            fTeamsCsv.write(eachEntry + '\n')
            fCcTxt.write(eachEntry + ';')  # semicolon separated emails in text file for Outlook To field
        fTeamsCsv.close()
        fCcTxt.close()

        # The final step is to write the attendance data frame to a csv file
        filepath = os.path.join(self.output_folder_dir, gc.DEFAULT_CONFIG_DICT["ATTENDANCE_TRACKING_LIST_FILENAME"])
        self.attendance_list_dataframe.to_csv(filepath, index=False, header=True)

        # Also write the attendee profile over all workshop days to file for tracking
        filepath = os.path.join(self.output_folder_dir, gc.DEFAULT_CONFIG_DICT["REGISTRATION_PROFILE_FILENAME"])
        self.registration_profile_dataframe.to_csv(filepath, index=True, header=True)

    def get_participants_registration_details(self):

        # Fixed part of the attendees list columns
        attendees_list_columns = ['Last & First Name', 'WWID', 'Email', 'IDFs to date', 'Filed patents to date']

        # The days part of the attendees_list_columns[] can vary from workshop to workshop hence appended below
        for eachDay in self.registration_day_dict:
            # append the string alias for each day
            attendees_list_columns.append(self.registration_day_dict[eachDay]['alias'])

        returningGuests = 0
        days_guest_count = 0
        days_unique_guest_count = 0
        days_waitlisted_guest_count = 0
        participants_email_list = []
        attdf = pd.DataFrame(columns=attendees_list_columns)  # create an empty attendees data frame for adding attendees for Teams tracking
        profileDf = pd.DataFrame(columns=gc.REGISTRATION_PROFILE_COLUMNS)  # create an empty attendees data frame for getting a snaphot of attendee breakdown
        for eachDayNum in self.registration_day_dict:
            # eachDayNum starts from 1
            self.messagebox_write(END, f"{'-'*20} Processing {self.registration_day_dict[eachDayNum]['alias']} registration" + "\n")
            cur_file_path = self.registration_files_list[self.registration_day_dict[eachDayNum]['reg_file_list_idx']]

            numOrganizers = 0
            data = pd.read_csv(cur_file_path)
            meetup_df = pd.DataFrame(data, columns=gc.MEETUP_CSV_COLUMNS)

            # There is a naming bug in MeetUp csvs that have a space before "Name" field which is corrected after reading from csv file!
            meetup_df.rename(columns={' Name': 'Name'}, inplace=True)

            for index, row in meetup_df.iterrows():
                curEmail = meetup_df.loc[index, 'Email']
                if curEmail not in self.organizer_emails:
                    if curEmail not in participants_email_list:

                        if meetup_df.loc[index, 'Waitlist'] == "WAITLISTED":
                            # Current guest is waitlisted
                            self.messagebox_write(END, f"Waitlisted guest: {curEmail}" + "\n")
                            days_waitlisted_guest_count += 1
                        else:
                            # Guest is registered and is NOT waitlisted

                            participants_email_list.append(curEmail)

                            temp_dict = {'Last & First Name': meetup_df.loc[index, 'Name'],\
                                                  'WWID': meetup_df.loc[index, 'WWID'],\
                                                  'Email': meetup_df.loc[index, 'Email'],\
                                                  'IDFs to date': str(0),\
                                                  'Filed patents to date': str(0)}

                            for everyDay in self.registration_day_dict:
                                temp_dict[self.registration_day_dict[everyDay]['alias']] = ''  # empty string field for each available day

                            attdf = attdf.append(temp_dict, ignore_index=True)

                            days_unique_guest_count += 1  # Excludes WAITLISTED guests
                    else:
                        returningGuests += 1  # Excludes WAITLISTED guests

                    days_guest_count += 1  # Includes WAITLISTED guests

                else:
                    # An organizer found in list
                    self.messagebox_write(END, f"Mentor found: {curEmail} in day {eachDayNum}" + "\n")
                    numOrganizers += 1

            # end for index, row

            self.messagebox_write(END, f"Found {days_guest_count} total guests (registered + waitlisted) this day" + "\n")
            self.messagebox_write(END, f"Found {days_waitlisted_guest_count} waitlisted guests this day" + "\n")
            self.messagebox_write(END, f"Found {days_unique_guest_count} new guests this day" + "\n")
            self.messagebox_write(END, f"Found {numOrganizers} organizers/mentors this day" + "\n")
            self.messagebox_write(END, f"Found {returningGuests} previously seen guests this day" + "\n")

            # Log the above info to relevant data frame
            # Stick to the following column order: ['Registered','Waitlisted','Patent101 Admins','Unique Visitors']
            profileDf.loc[self.registration_day_dict[eachDayNum]['alias']] = [str(days_guest_count - days_waitlisted_guest_count),
                                                                              str(days_waitlisted_guest_count), str(numOrganizers),
                                                                              str(days_unique_guest_count)]

            days_guest_count = 0
            days_unique_guest_count = 0
            days_waitlisted_guest_count = 0
            returningGuests = 0
            self.messagebox_write(END, f"Found {len(participants_email_list)} unique guests so far" + "\n")

        #end for eachDay

        return participants_email_list, attdf, profileDf

    def teams_member_file_button_callback(self):
        self.teams_member_csv_file = filedialog.askopenfilename()  # selects a file

        # Next check to make sure user selected a csv file
        file_extension = self.teams_member_csv_file.split('.')[-1]
        if file_extension.lower() == 'csv':
            self.messagebox_write(END, "Selected Teams member list file: " + self.teams_member_csv_file + "\n")
        else:
            self.messagebox_write(END, "User selection: " + self.teams_member_csv_file + "\n")
            self.messagebox_write(END, "ERROR: Please select a valid *.csv file " + "\n")
            self.teams_member_csv_file = ''  # invalidate file variable

    def teams_member_list_gen_button_callback(self):
        self.participant_emails = self.get_teams_participant_members_only()

        # Create the relevant output files.
        # Write emails to remove from Teams in a new file
        filepath = os.path.join(self.output_folder_dir, gc.DEFAULT_CONFIG_DICT["EXTRACTED_TEAMS_PARTICIPANTS_CSV_FILENAME"])
        fTeamsCsv = open(filepath, 'w')
        filepath = os.path.join(self.output_folder_dir, gc.DEFAULT_CONFIG_DICT["EXTRACTED_TEAMS_PARTICIPANTS_TEXT_FILENAME"])
        fTeamsTxt = open(filepath, 'w')
        fTeamsCsv.write('email\n')  # this is the column name assigned to the csv file (this is needed in PowerShell command!)
        for eachEntry in self.participant_emails:
            fTeamsCsv.write(eachEntry + '\n')  # csv file that will be sent to Teams to remove participants when needed
            fTeamsTxt.write(eachEntry + ';')  # semicolon separated emails in text file for Outlook To field
        fTeamsCsv.close()
        fTeamsTxt.close()

    def get_teams_participant_members_only(self):
        '''
        ASSUMPTIONS: self.teams_member_csv_file (the list of current members on Teams received using
        Power Shell interface) has the following column names: UserId, UseName, Role
        Before the above column names there is one row that needs to be ignored and reads
        "#TYPE Microsoft.TeamsCmdlets.PowerShell.Custom.GetTeamUser+GetTeamUserResponse"
        '''

        data = pd.read_csv(self.teams_member_csv_file, skiprows=[0])  # The first row is to be ignored in the input csv file!
        teams_members_dataframe = pd.DataFrame(data, columns=gc.TEAMS_MEMBERS_LIST_COLUMNS)

        participant_emails = [] # removal_email_list = []
        numOrganizers = 0
        numParticipantEmails = 0  #numEmailsToRemove = 0
        numTotalRecords = 0
        for index, row in teams_members_dataframe.iterrows():
            curEmail = teams_members_dataframe.loc[index, 'User']  # email is listed under column "User" in dataframe
            numTotalRecords += 1
            if curEmail not in self.organizer_emails:
                participant_emails.append(curEmail)
                numParticipantEmails += 1
            else:
                # An organizer found in list
                numOrganizers += 1

        self.messagebox_write(END, f"Found {numOrganizers} organizers and {numParticipantEmails} participants in {numTotalRecords} Teams members" + "\n")

        return participant_emails

    def teams_member_addition_instructions_button_callback(self):
        self.messagebox_write(END, f"To ADD members from a list in a csv file to a space/group in Teams do the following:" + "\n")
        self.messagebox_write(END, f"-"*157 + "\n")
        self.messagebox_write(END, f"Step 1 - Start Power Shell in Windows" + "\n\n")
        self.messagebox_write(END, f"Step 2 - Type the following command and authenticate yourself:\nConnect-MicrosoftTeams" + "\n\n")
        self.messagebox_write(END, f"Step 3 - Type the following command to get the details of Teams you belong to:\nGet-Team -User <your email address>" + "\n\n")
        self.messagebox_write(END, f"Step 4 - Locate the GroupId of the Team (where you want to ADD members to) and copy it (e.g. 884157e4-b389-472c-b7c9-938ba47d0873)" + "\n\n")
        next_command = "Import-Csv -Path <enter path to TEAMS_INPUT_PARTICIPANTS_FILENAME> | foreach{Add-TeamUser -GroupId <Enter Group Id from Step 4> -user $_.email}"
        self.messagebox_write(END, f"Step 5 - Type the following command to ADD a list of participants (from a csv file) as members to that team:\n{next_command}" + "\n\n")
        self.messagebox_write(END, f"PLEASE NOTE: After invoking command in Step 5, depending on the number of members in the list, member addition operation can take some time.")
        self.messagebox_write(END, f" You can watch the progress of the addition (i.e. via the increase in the total number of members in the space) in real time in Teams after invoking the command in Step 5." + "\n\n")

    def teams_member_removal_instructions_button_callback(self):
        self.messagebox_write(END, f"To REMOVE members from a Teams space/group listed in a csv file do the following:" + "\n")
        self.messagebox_write(END, f"-"*157 + "\n")
        self.messagebox_write(END, f"Step 1 - Start Power Shell in Windows" + "\n\n")
        self.messagebox_write(END, f"Step 2 - Type the following command and authenticate yourself:\nConnect-MicrosoftTeams" + "\n\n")
        self.messagebox_write(END, f"Step 3 - Type the following command to get the details of Teams you belong to:\nGet-Team -User <your email address>" + "\n\n")
        self.messagebox_write(END, f"Step 4 - Locate the GroupId of the Team (from which you want to REMOVE a subset of members) and copy it (e.g. 884157e4-b389-472c-b7c9-938ba47d0873)" + "\n\n")
        next_command = "Import-Csv -Path <enter path to EXTRACTED_TEAMS_PARTICIPANTS_CSV_FILENAME> | foreach{Remove-TeamUser -GroupId <Enter Group Id from Step 4> -user $_.email}"
        self.messagebox_write(END, f"Step 5 - Type the following command to REMOVE a list of participants (in a csv file) from that team:\n{next_command}" + "\n\n")
        self.messagebox_write(END, f"PLEASE NOTE: After invoking command in Step 5, depending on the number of members in the list, member removal operation can take some time.")
        self.messagebox_write(END, f" You can watch the progress of the removal (i.e. via the decrease in the total number of members in the space) in real time in Teams after invoking the command in Step 5." + "\n\n")

    def teams_member_retrieval_instructions_button_callback(self):
        self.messagebox_write(END, f"To RETRIEVE members from a Teams space/group into a csv file do the following:" + "\n")
        self.messagebox_write(END, f"-"*157 + "\n")
        self.messagebox_write(END, f"Step 1 - Start Power Shell in Windows" + "\n\n")
        self.messagebox_write(END, f"Step 2 - Type the following command and authenticate yourself:\nConnect-MicrosoftTeams" + "\n\n")
        self.messagebox_write(END, f"Step 3 - Type the following command to get the details of Teams you belong to:\nGet-Team -User <your email address>" + "\n\n")
        self.messagebox_write(END, f"Step 4 - Locate the GroupId of the Team (from which you want to RETRIEVE ALL listed members) and copy it (e.g. 884157e4-b389-472c-b7c9-938ba47d0873)" + "\n\n")
        next_command = "Get-TeamUser -GroupId <Enter Group Id from Step 4> -Role Member | export-csv -path <enter path to a csv file to write to>"
        self.messagebox_write(END, f"Step 5 - Type the following command to RETRIEVE all the members in that team (into a csv file):\n{next_command}" + "\n\n")
        self.messagebox_write(END, f"PLEASE NOTE: After invoking command in Step 5, depending on the number of members in the team, member retrieval operation can take some time.")
        self.messagebox_write(END, f" Retrieval is a read only operation and will not affect the number of total members in a Teams group/space." + "\n\n")
