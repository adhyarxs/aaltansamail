import requests

def parseColumnAuto(csvContent=[],parser="@",cont=False):
    _result=[]
    if len(csvContent)!=0:
        if parser:
            for eachDat in csvContent:
                if parser in str(eachDat):
                    _result.append(str(eachDat))
                    if not cont:
                        break
    return _result

def parseColumn(csvContentSTR=None,delim=None,part=0,end=None):
    if not delim:
        delim=','
    if end:
        if end==-1:
            return csvContentSTR.split(delim)[part:]
        else:
            return csvContentSTR.split(delim)[part:end]
    else:
        return csvContentSTR.split(delim)[part:]  
def parseToColumn(csvRAW=None,delim=None,start=0,end=None):
    if not delim:
        delim='\n'
    if end:
        if end==-1:
            return csvRAW.split(delim)[start:]
        else:
            return csvRAW.split(delim)[start:end]
    else:
        return csvRAW.split(delim)[start:]
def getFromURL(URL):
    h4ndsh4k3=requests.get(URL)
    return h4ndsh4k3.content.decode('utf-8')

