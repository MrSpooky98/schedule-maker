import sys
import random

class Week():
    def __init__(self,days = 5,hours = 12):
        self.hours = hours
        self.days = days
        self.week = self.generateMatrix(days,hours)
        self.nrcs = []

    def generateMatrix(self,columns,rows):
        matrix = []

        for i in range(rows):
            matrix.append(self.listSizeOf(columns))

        return matrix

    def listSizeOf(self,size,item = '     '):
        l = []

        for i in range(size):
            l.append(item)

        return l

    def getRowHeader(self):
        rowHeader = []

        for i in range (self.hours):
            begin = (7 + i) % 12
            if (begin == 0):
                begin = 12

            end = (7 + i + 1) % 12
            if (end == 0):
                end = 12

            rowHeader.append('%02i-%02i' % (begin,end))

        return rowHeader

    def toString(self,sep = ' '):
        columnHeader = ['     ','  L  ','  M  ','  M  ','  J  ','  V  ']
        rowHeader = self.getRowHeader()
        s = ''

        for col in columnHeader:
            s = s + ('%s%s' % (col,sep))
        s = s[:-1] + '\n'

        rowInd = 0
        for row in self.week:
            s = s + ('%s%s' % (rowHeader[rowInd],sep))
            for column in row:
                s = s + ('%s%s' % (column,sep))
            s = s[:-1] + '\n'
            rowInd = rowInd + 1

        return s

    def toHTMLTable(self,subjectNames,subjectsList):
        columnHeader = ['     ','  L  ','  M  ','  M  ','  J  ','  V  ']
        rowHeader = self.getRowHeader()
        s = '<tr>\n'

        for col in columnHeader:
            s = s + '<th>' + ('%s' % (col)) + '</th>'
        s = s + '\n</tr>'

        week = list(self.week)

        rowInd = 0
        for row in week:
            s = s + '<tr>\n<td>' + ('%s' % (rowHeader[rowInd])) + '</td>\n'

            colInd = 0
            for column in row:
                c = 0
                found = False

                while (not found and c < len(subjectNames)):
                    cl = subjectsList[subjectNames[c]]

                    for x in cl:
                        if (x.nrc == column):
                            found = True
                            break

                    if (not found): c = c + 1

                s = s + ('<td class="m%i">' % (c)) + ('%s' % (column)) + '</td>'

                colInd = colInd + 1

            s = s + '</tr>\n'
            rowInd = rowInd + 1

        return '<table>\n' + s + '\n</table>'

    def merge(self,week1,week2):
        response = {}
        
        for row in range(len(week1)):
            for column in range(len(week1[0])):
                if (week2[row][column] != '     '):
                    if (week1[row][column] != '     '):
                        
                        response['good'] = False
                        return response
                    
                    week1[row][column] = week2[row][column]

        response['good'] = True
        response['week'] = week1

        return response

class Class():
    def __init__(self,code,name):
        self.week = Week()
        self.nrc = code
        self.name = name

    def printClass(self):
        print('%s %s' % (self.name,self.nrc))
        print(self.week.toString())

def parse(filename = 'classes.csv'):
    if (len(sys.argv) == 2):
        filename = sys.argv[1]

    reader = open(filename,'r')

    classes = []
    cls = Class('00000','holder')
    hourInd = 0
    for line in reader:
        cells = line.split(',')
        cells[len(cells) - 1] = str(cells[len(cells) - 1])[:-1]
        
        if (cells[0] == ''):
            classes.append(cls)
            cls = Class('00000','holder')
            hourInd = 0
            continue

        if (cells[0] == 'HORA'):
            cls.name = cells[len(cells) - 1]
            cls.nrc = cells[len(cells) - 2]
            continue

        x = 1
        for x in range(cls.week.days + 1):
            if (cells[x] == ''):
                cells[x] = ' ' * 5
            cls.week.week[hourInd][x - 1] = cells[x]

        hourInd = hourInd + 1
    classes.append(cls)

    reader.close()

    return classes

def mergingPossibilities(subjectNames,subjectsList):
    possibilities = []

    times = []

    for key in subjectsList:
        times.append(len(subjectsList[key]))

    for first in range(times[0]):
        for second in range(times[1]):
            for third in range(times[2]):
                for fourth in range(times[3]):
                    for fifth in range(times[4]):
                        for sixth in range(times[5]):
                            ind = [first,second,third,fourth,fifth,sixth]
                            week = Week()
                            good = True
                            for i in range(len(subjectNames)):
                                response = week.merge(week.week,subjectsList[subjectNames[i]][ind[i]].week.week)
                                if (response['good'] == False):
                                    good = False
                                    break

                                week.week = response['week']

                            if (good == True):
                                possibilities.append(week)

    return possibilities

def printSubjectsWithNRC(subjectNames,subjectsList):
    for name in subjectNames:
        print(name)
        for cls in subjectsList[name]:
            print(cls.nrc)
        print()

def printSubjectsWithNRCHTML(subjectNames,subjectsList):
    tables = ''
    c = 0
    for name in subjectNames:
        tables = tables + ('<div>\n<table class = "mat">\n<th>%s</th>' % (name))
        for cls in subjectsList[name]:
            tables = tables + ('\n<td class="m%i">%s</td>' % (c,cls.nrc))
        tables = tables + '\n</table>\n</div>\n'
        c = c + 1
    return tables

def generateCSV(possibilities):
    writer = open('posibilities.csv','w+')

    for week in possibilities:
        s = week.toString(sep=',')
        writer.write(s)
        writer.write(',\n')

    writer.close()

def generateHTML(possibilities,subjectNames,subjectsList):
    subjectClasses = ''
    
    c = 0
    for name in subjectNames:
        subjectClasses = subjectClasses + '\n.m%i {background: hsl(%i,%i%%,%i%%);}' % (c,c * (360 // len(subjectNames)),100,50)
        c = c + 1

    style = '<style>\ntable, th, td {\nborder: 1px solid black;\nborder-collapse: collapse;} \nth, td {\npadding: 5px;\ntext-align: center;} \ndiv {\nfloat: left; \nmargin-right: 50px;\nmargin-bottom: 50px;} \n' + subjectClasses + '\n</style>'
    table = ''
    subjectTables = printSubjectsWithNRCHTML(subjectNames,subjectsList)

    for week in possibilities:
        table = table + '\n<div>' + week.toHTMLTable(subjectNames,subjectsList) + '</div>\n'
    
    html = '<html>\n<head>\n<title>\nPossibilities\n</title>\n%s\n</head>\n<body>\nThere are %i possible schedules\n</br></br>\n%s\n</br></br>\n%s\n</body>\n</html>' % (style,len(possibilities),subjectTables,table)
    with open('possibilities.html','w+') as f:
        f.write(html)

def main():
    classes = parse()

    subjectsList = {}
    subjectNames = []

    for cls in classes:
        if cls.name not in subjectNames:
            subjectNames.append(cls.name)

        try:
            old = subjectsList[cls.name]
            old.append(cls)
            subjectsList[cls.name] = old
        except KeyError:
            subjectsList[cls.name] = [cls]

    printSubjectsWithNRC(subjectNames,subjectsList)

    possibilities = mergingPossibilities(subjectNames,subjectsList)

    generateCSV(possibilities)
    generateHTML(possibilities,subjectNames,subjectsList)

    # for week in possibilities:
    #     print(week.toString())
    
    print('%i results' % (len(possibilities)))

if (__name__ == '__main__'):
    main()