
CONFIGURATION_FILENAME='config.json'  # tool expects to find this exact configuration file
APPLICATION_VERSION_STRING='v1.0'
TOOL_NAME_STRING="Patent 101 Workshop Management Tool"
TITLE_ICON_FILE="Patent101_OR.ico"
TITLE_STRING=TOOL_NAME_STRING + " - " + APPLICATION_VERSION_STRING

MESSAGE_BOX_ATTRIBS={'x_offset': 10, 'y_offset': 80, 'box_height': 200}
OUTPUT_FOLDER_BUTTON_POS={'x': 90, 'y': 30}
MENTORS_DIR_BUTTON_POS={'x': OUTPUT_FOLDER_BUTTON_POS['x'], 'y': OUTPUT_FOLDER_BUTTON_POS['y'] + 60}

MEETUP_CSV_COLUMNS = ['Attendance', 'Waitlist', 'Guests', 'Name', 'WWID', 'IDSID', 'Email', 'Shift', 'Site', 'Campus',
                  'Building', 'Title', 'Business Group', 'Business Division', 'Business Organization',
                  'Months of Service', 'Class', 'Status', 'Timestamp']

REGISTRATION_PROFILE_COLUMNS = ['Registered', 'Waitlisted', 'Patent101 Admins', 'Unique Visitors']
TEAMS_MEMBERS_LIST_COLUMNS = ["UserId", "User", "Name", "Role"]

DEFAULT_CONFIG_DICT={"TEAMS_GROUPID": "abcdef123456", \
                     "SUPPORTING_MENTORS_FILENAME": "supporting_mentor_emails.txt",
                     "REGISTRATION_PROFILE_FILENAME": " workshop_registration_profile.csv",
                     "TEAMS_INPUT_PARTICIPANTS_FILENAME": "participants_to_add_to_teams.csv",
                     "SEMICOLON_DELIMITED_PARTICIPANTS_FILENAME": "meetup_registered_participants.txt",
                     "ATTENDANCE_TRACKING_LIST_FILENAME": "attendance_tracker.csv",
                     "EXTRACTED_TEAMS_PARTICIPANTS_TEXT_FILENAME": "teams_participant_members.txt",
                     "EXTRACTED_TEAMS_PARTICIPANTS_CSV_FILENAME": "teams_participant_members.csv"
}

SUPPORTING_MENTORS_FILENAME = 'supporting_mentor_emails.txt'
REGISTRATION_PROFILE_FILENAME = 'workshop_registration_profile.csv'
TEAMS_INPUT_PARTICIPANTS_FILENAME = 'participants_to_add_to_teams.csv'
SEMICOLON_DELIMITED_PARTICIPANTS_FILENAME = 'meetup_registered_participants.txt'
ATTENDANCE_TRACKING_LIST_FILENAME = 'attendance_tracker.csv'
EXTRACTED_TEAMS_PARTICIPANTS_TEXT_FILENAME = 'teams_participant_members.txt'
EXTRACTED_TEAMS_PARTICIPANTS_CSV_FILENAME = 'teams_participant_members.csv'

##############################
CANVAS_DIM={'w': 400, 'h': 300}
TXTBOX1_POS={'x': 75, 'y': 25}
WORKING_DIR_BUTTON_POS={'x': 150, 'y': 150}
LABEL1_POS={'x': WORKING_DIR_BUTTON_POS['x'], 'y': WORKING_DIR_BUTTON_POS['y'] + 30}
DROPDOWN1_OPTIONS_LIST=["Create Participant Team List", "Create Mentors List"]
DROPDOWN1_POS={'x': LABEL1_POS['x'], 'y': LABEL1_POS['y'] + 30}
EXEC_BUTTON_POS={'x': DROPDOWN1_POS['x'], 'y': DROPDOWN1_POS['y'] + 30}