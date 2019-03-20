# schedule-maker
Class Scheduler maker
Schedule maker that takes a CSV file with the classes as input and generates an HTML and a CSV files with all the posibilities 

fixed for 6 courses, but easily modifiable (add or remove for-loop in the mergePossibilities function)

Generate CSV file and html page for easy reading

classes.csv FORMAT
'''

     HORA    ,LUNES,MARTE,MIERC,JUEVE,VIERN,<NRC>,<SUBJECT_NAME>
07:00 – 08:00,     ,     ,     ,     ,     ,     ,     
08:00 – 09:00,     ,     ,     ,     ,     ,     ,     
09:00 – 10:00,     ,     ,     ,     ,     ,     ,     
10:00 – 11:00,     ,     ,     ,     ,     ,     ,     
11:00 – 12:00,     ,     ,     ,     ,     ,     ,     
12:00 – 01:00,     ,     ,     ,     ,     ,     ,     
01:00 – 02:00,<NRC>,     ,     ,     ,     ,     ,     
02:00 – 03:00,<NRC>,     ,     ,     ,     ,     ,     
03:00 – 04:00,     ,     ,<NRC>,     ,     ,     ,     
04:00 – 05:00,     ,     ,<NRC>,     ,     ,     ,     
05:00 – 06:00,     ,     ,     ,     ,     ,     ,     
06:00 – 07:00,     ,     ,     ,     ,     ,     ,     

'''
