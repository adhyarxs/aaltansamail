#########################################
## EMAILS SENDER BASED ON SPREADSHEET  ##
#########################################
## Dedicated to altansa ##
##########################

###########################
### IMPORTING DEPENCIES ###
###########################
try:
    import httplib2
    import os
    import sys
    import time
    import requests
    import lib.TerminalControl as TC
    import lib.CSVParsing as CSVP
    import csv
    import time
    import base64
    from email import encoders
    from email.message import EmailMessage
    import mimetypes
    import google.auth
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from datetime import datetime
except:
    exit("Please install the depencies")
###                     ###
###########################

def clearTerm(anim=False):
    TC.clearTerm()
    if anim:
        TC.animText("\033[0;32m=== Altansa Mail Sender ===\033[0m\n")
        TC.animText("\033[0;32m================\033[0m")
        TC.animText("\r\033[0;31m====== === =====\033[0m\n\n")
    else:
        print("\033[0;32m=== Altansa Mail Sender ===\033[0m")
        print("\033[0;31m====== === =====\033[0m\n\n")
def main():
    ##########################
    ## VARIABLE DECLARATION ##
    ##########################

    SPREADSHEETURL=""
    RESPONSEHANDSHAKE=""
    DATACSV=""
    _senderEmail="aaltansa@gmail.com"
    _emailList=[]
    _preSubject="Subject"
    _preText="This is default text"
    attachmentFile=[]
    SCOPES='https://www.googleapis.com/auth/gmail.send'
    CLIENTSECRETFILE='credentials.json'
    APPLICATIONNAME='Altansa Gmail Sender'

    for argvCont in sys.argv:
        #print(argvCont)
        if(argvCont.lower()=="noanim"):
            ANIMATIONBOOL=False
            break
    if ANIMATIONBOOL:
        clearTerm(True)
    else:
        clearTerm(False)
    #exit()
    _importMassListDefault = input("Import mass list of receiver from default spreadsheets(y/n): ")
    if(_importMassListDefault.lower()=='y'):
        SPREADSHEETURL='https://docs.google.com/spreadsheets/d/1u5TXUs2hLkDksrf6lCE6DilIFqatga7962WYuGYGTsc/export?format=csv&id=1u5TXUs2hLkDksrf6lCE6DilIFqatga7962WYuGYGTsc'
        try:
            dataRAW=CSVP.getFromURL(SPREADSHEETURL)
            print("\033[0;32m[+]Spreadsheet successfully loaded\033[0m")
        except:
            exit("Can requests GET to the url, try again or contact the developer")
        semiParsed=CSVP.parseToColumn(dataRAW,'\n',2)
        for eachEmAng in semiParsed:
            _emailList+=CSVP.parseColumn(eachEmAng,',',3,5)
        #exit(_emailList)
    elif(_importMassListDefault.lower()=='n'):
        while 1:
            _optionOfReceiver=input("\r[1] Type each receivers manually\n[2] CSV File URL\n\nYour Option: ")
            if(_optionOfReceiver=='1' or _optionOfReceiver=='2'):
                break;
        #exit(_optionOfReceiver)
        if(_optionOfReceiver=='1'):
            while 1:
                clearTerm();
                print("Input EACH of the receiver email\n(input 'done' to stop inputing)\n(input 'clear' to re-input)\n(input 'remove' to remove one email inputed rigth before the remove input)\n(input 'export <filename>' to export from txt file)\n")
                print("[Inputed Email]\n");
                i=0
                for eachEmail in _emailList:
                    i=i+1
                    print(str(i)+"."+eachEmail+"\n");
                _tempEmail = str(input("Receiver Email: "))
                if "@" not in _tempEmail:
                    if _tempEmail.lower()=="done" or _tempEmail.lower()=="remove" or _tempEmail.lower()=="clear" or 'export ' in _tempEmail.lower():
                        if _tempEmail.lower()=="done":
                            break
                        else:
                            if _tempEmail.lower()=="remove":
                                _emailList.pop(-1)
                            else:
                                if _tempEmail.lower()=="clear":
                                    _emailList.clear()
                                else:
                                    if 'export ' in _tempEmail.lower():
                                        filename=_tempEmail[len('export '):]
                                        try:
                                            with open(os.path.basename(filename),"r") as fpr:
                                                for fpreachCon in fpr.read().split('\n'):
                                                    if '@' in fpreachCon:
                                                        _emailList.append(fpreachCon)
                                        except:
                                            print("Missing arguments: File Not Found!")
                                            time.sleep(0.5)
                    else:
                        print("[-] Enter a valid email!")
                        time.sleep(1);
                if "@" in _tempEmail:
                    _emailList.append(_tempEmail)
            clearTerm();
        elif(_optionOfReceiver=='2'):
            #exit("got IN")
            while 1:
                clearTerm();
                _CSVURL=input("Input link to CSV File: ")
                try:
                    csvCustomDat=CSVP.parseToColumn(CSVP.getFromURL(_CSVURL))
                    print("\033[0;32m[+]Spreadsheet successfully loaded\033[0m")
                except:
                        exit("Can requests GET to the url, try again or contact the developer")
                _CSVDelim=input("Input the delimeter(default:','): ")
                if len(_CSVDelim)==0:
                    _CSVDelim=','
                _CSVIdent=input("Identifier for email parser(default:'@'): ")
                if len(_CSVIdent)==0:
                    _CSVIdent='@'
                for eachData in csvCustomDat:
                    _emailList+=CSVP.parseColumnAuto(CSVP.parseColumn(eachData))
                clearTerm();
                print("Current array of emails:\n")
                lchM=0
                for eachM in _emailList:
                    lchM+=1
                    print(f"{lchM}.{eachM}")
                breakOrNo=input("you sure(y/n): ");
                if(breakOrNo.lower()=='y'):
                    break;
                _emailList.clear()
    else:
        exit("Input a valid answer!")
    clearTerm();
    while 1:
        _messageChoices=input("[1]Use in-code message\n[2]Manually input the message\n\nChoices:")
        if(_messageChoices=='1' or _messageChoices=='2'):
            break;
    if(_messageChoices=='2'):
        clearTerm();
        print("-( When input body text or attachment file )-\n-( Use '|done|' if done )-\n( In inputing body )-\n-(Use '|export| <htmlFile>' to export )-")
        _preSubject=input("Input the subject: ");
        while 1:
            _preInput=input("Input the body Text(html): ");
            if "|done|" in _preInput.strip().lower() or "|export|" in _preInput.strip().lower():
                if "|done|" in _preInput.strip().lower():
                    if _preInput.strip().lower() == "|done|":
                        break;
                    else:
                        print("Wrong Syntax!")
                else:
                    if "|export|" in _preInput.strip().lower() and len(_preInput.strip())!=len("|export| "):
                        filename=_preInput.strip()[len('|export| '):]
                        with open(os.path.basename(filename),"r") as fpr:
                            for fpreachCon in fpr.read().split('\n'):
                                _preText+=(fpreachCon)
                    else:
                        print("Wrong syntax: Missing Filename")
            else:
                _preText+=_preInput
        while 1:
            inputFile=input("Input the path of attachment Fil: ")
            if "|done|" in inputFile.strip().lower():
                if "|done|" in inputFile.strip().lower():
                    break;
            if not open(inputFile,"r"):
                print("File not found!")
            else:
                attachmentFile.append(inputFile)
    clearTerm();
    print("[FINAL]\n")
    print("Sender: " + _senderEmail)
    print("[Receiver]\n")
    for eachMailForFINAL in _emailList:
        print(eachMailForFINAL)
    print("Subject: " + _preSubject)
    print("Body   : " + _preText)
    for eacHatC in attachmentFile:
        print("AttachmentFile : " + eacHatC)
    sureOrNo=input("\nAre you sure(y/n, 'exit' to cancel): ")
    if(sureOrNo.lower()=="exit"):
        exit()
    #else(sureOrNo.lower()=="y"):
    #    break
    ##################
    # IMPORTANT PART #
    ##################
    """for eachEmailForSent in _emailList:
        sendMessage(_senderEmail,eachEmailForSent,_preSubject,_preText,"")"""
    creds=None
    if os.path.exists('token.json'):
        creds=Credentials.from_authorized_user_file('token.json',SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds=flow.run_local_server(port=0)
        with open('token.json','w') as token:
            token.write(creds.to_json())
    try:
        _preText=MIMEText(_preText,"html")
        serviceX=build('gmail','v1',credentials=creds)
        for eachEmail in _emailList:
            #print(eachEmail)
            #print(_emailList)
            #print(len(_emailList))
            #exit()
            structMSSG=MIMEMultipart()
            structMSSG.attach(_preText)
            structMSSG['To'] = eachEmail
            structMSSG['From'] = _senderEmail
            structMSSG['Subject'] = _preSubject
            if attachmentFile:
                for eachAttach in attachmentFile:
                    with open(eachAttach,'rb') as fp:
                        #type_subtype,encoding=mimetypes.guess_type(os.path.basename(attachmentFile))
                        #maintype,subtype=type_subtype.split('/',1)
                        #partM=MIMEBase(maintype,subtype)
                        partM=MIMEBase("application","octet-stream")
                        partM.set_payload((fp).read())
                        encoders.encode_base64(partM)
                        partM.add_header("Content-Disposition","attachment; filename={}".format(os.path.basename(eachAttach)))
                        structMSSG.attach(partM)
            encoded_message=base64.urlsafe_b64encode(structMSSG.as_bytes()).decode()
            create_message={'raw':encoded_message}
            send_message=(serviceX.users().messages().send(userId="me",body=create_message).execute())
            print(send_message)
    except HttpError as error:
        return 'An error occured:' + error

if __name__ == "__main__":
    main()

