from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Before modifying scopes, delete credentialss stored at ~/.credentials/classroom.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/classroom.coursework.students.readonly', \
    'https://www.googleapis.com/auth/classroom.courses.readonly', \
    'https://www.googleapis.com/auth/classroom.coursework.me.readonly', \
    'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Classroom API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'classroom.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    
def parse_classes(classes):
    final = []
    classes = classes.get('courses')
    for course in classes:
        final.append([course.get('name'), course.get('id')])
    return final
    
def parse_assignments(assignments):
    final = []
    assignments = assignments.get('courseWork')
    for work in assignments:
        final.append([work.get('title'), work.get('id')])
    return final
    
def parse_submissions(submissions):
    final = []
    submissions = submissions.get('studentSubmissions')
    for assignment in submissions:
            temp = assignment.get('assignmentSubmission')
            if type(temp) is dict:
                temp = temp.get('attachments')
                if type(temp) is list:
                    temp = temp[0]
                    if type(temp) is dict:
                        temp = temp.get('driveFile')
                        if type(temp) is dict:
                            title = parse_name(temp.get('title'))
                            link = parse_link(temp.get('alternateLink'))
                            final.append([title, link])
    return final
    
def parse_name(name):
    if '.' in name:
        ind = name.index('.')
        return name[:ind]
    else:
        return name

def parse_link(link):
    if 'id=' in link:
        ind = link.index('id=')
        return link[(ind + 3):]
    else:
        return link
        
def download_file(drive_service, name, id):
#Add way to create student file if there is more than one submission and keep titles as is
#Add more file type specific endings and implement .export() for google Docs and such
    type = drive_service.files().get(fileId=id).execute()
    type = type.get('mimeType')
    if 'image' in type:
        name += '.jpg'
    data = drive_service.files().get_media(fileId=id).execute()
    img = open(name, 'wb')
    img.write(data)
    img.close()

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    classroom_service = discovery.build('classroom', 'v1', http=http)
    drive_service = discovery.build('drive', 'v3', http=http)
    
    course_select = True
    assignment_select = True
    
    class_list = parse_classes(classroom_service.courses().list().execute())
    num1 = -1
    courseid = 0
        
    while course_select:
        for x in range(len(class_list)):
            print(str(x) + ': ' + str(class_list[x][0]))
        num1 = int(input('\nEnter the corresponding number for a class: '))
        if (num1 >= 0) and (num1 < len(class_list)):
            courseid = class_list[num1][1]
            course_select = False
    
    assignment_list = parse_assignments(classroom_service.courses().courseWork().list(courseId=courseid).execute())
    num2 = -1
    assignmentid = 0
    
    while assignment_select:
        for x in range(len(assignment_list)):
            print(str(x) + ': ' + str(assignment_list[x][0]))
        num2 = int(input('\nEnter the corresponding number for an assignment: '))
        if (num2 >= 0) and (num2 < len(class_list)):
            assignmentid = assignment_list[num2][1]
            assignment_select = False

    path = os.getcwd()
    path += '\\' + class_list[num1][0]
    if not os.path.exists(path):
        os.makedirs(path)
    path += '\\' + assignment_list[num2][0]
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)
    
    submissions = parse_submissions(classroom_service.courses().courseWork().studentSubmissions().list(courseId=courseid, courseWorkId=assignmentid).execute())
    for work in submissions:
        download_file(drive_service, work[0], work[1])
    print('Finished.')
    
if __name__ == '__main__':
    main()