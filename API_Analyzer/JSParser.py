import re
import sys
def fileOpen(path):
    file = open(path, 'r')
    return file;

def traverseThru(path, findinFile):
    file = fileOpen(path);
    output=[]
    for nmbr,line in enumerate(file):
        for unsfe in findinFile:
            if line.find(unsfe) >= 0:
                output.append([nmbr,unsfe, line])
    return output

def findInValue(apiList):
    inVal=[]
    for element in apiList:
        chrNo = element[2].find(element[1])+element[1].__len__()-1
        if element[2][chrNo] == "(":
            val = ""
            bool = True
            for chr in range(chrNo,element[2].__len__()):
                if bool:
                    val += element[2][chr]
                    if element[2][chr] == ")":
                        bool = False
                        inVal.append([element,val])
    varList = []
    for i in inVal:
        varLen = re.findall('\'.*?\'|".*?"|(\w+)', i[1])
        if varLen.__len__() != 0:
            for j in varLen:
                if j != '' and j != "":
                    varList.append(j)
    return varList



def bracketSearch(path, b, start):
    file = fileOpen(path)
    cntOpn = 0
    cntCls = 0
    lastline = 0
    bracket = {"{": "}", "(": ")", "[": "]"}
    codeBlock=[]
    for cntr, line in enumerate(file):
        if cntr >= start:
            for i in line:
                if cntOpn == cntCls and cntOpn !=0 and cntCls != 0:
                    return codeBlock,start+lastline
                if i == b:
                    cntOpn += 1
                    codeBlock.append(line)
                elif i == bracket[b]:
                    cntCls += 1
                    codeBlock.append(line)
            lastline += 1

def findinFunc(apiList, funcList):
    inFunc = []
    for i in apiList:
        start=-sys.maxsize-1
        end= sys.maxsize
        for j in funcList:
            if i[0] > j[0] and i[0] < j[4]:
                if start < j[0] and end > j[4]:
                    start = j[0]
                    end = j[4]
                    inFunc.append([i,j])
    return inFunc

def printAPI(unsafe,apiInFunc,path):
    print("******************************* Unsafe APIs in file ", path,"******************************")
    for i in apiInFunc:
        print("********* API: ", i[0][1], "*********")
        print()
        for j in unsafe:
            if i[0][1] == j:
                print("Line ", i[0][0], ": ", i[0][2])
                print("In function: ", i[1][2])
                for ele in i[1][3]:
                    print(ele)
def printVariable(variableList,path):
    print("******************************* Variable in unsafe APIs in file ", path,"******************************")
    for j in variableList:
        print("************", j[1], "***************")
        for i in variableList:
            if j[2] == i[2]:
                print("Line ",i[0],": ",i[2])
def main(path):
    unsafe=[sys.argv[2]]
    apiList = traverseThru(path, unsafe)
    varList = findInValue(apiList)
    funcList = traverseThru(path, ["function"])
    #   for i in funcList:
    #     print(i)

    for indx, ele in enumerate(funcList):
        if bracketSearch(path, "{", ele[0]) is not None:
            funcList[indx].append(bracketSearch(path, "{", ele[0])[0])
            funcList[indx].append(bracketSearch(path, "{", ele[0])[1])
    apiInFunc = findinFunc(apiList, funcList)
    variableList = []
    for i in varList:
        if len(i) > 1:
            for j in traverseThru(path,[i+" =",i+"="]):
                variableList.append(j)
    printAPI(unsafe, apiInFunc,path)
    printVariable(variableList,path)

if __name__ == "__main__":
    cmdline_arg = sys.argv[1]
    #for p in cmdline_arg:
    main(cmdline_arg)






