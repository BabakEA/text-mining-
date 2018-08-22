"""
Babak Emami
Read text file and extract the words and theirs frequency to the Sqlite dataset

"""

import pandas as pd
import numpy as np
import re
import collections
import os
import sys
from collections import Counter
from datetime import datetime
import sqlite3
import argparse
start=datetime.now()

databasename= 'word.db'
db = sqlite3.connect(databasename)
# load Dataset for proccess     
c = db.cursor()
c1 = db.cursor()
# monitor the input file 

def create_arg_parser():
    #Creates and returns the ArgumentParser object.
    """
    
    parser.add_argument('inputDirectory',
                    help='Path to the input directory. EX : python start.py 1.txt')
    parser.add_argument('--outputDirectory',
                    help='Path to the output that contains the Database, and serach engine\
                           to exit the search engine please einter: eof.')

   """
    parser = argparse.ArgumentParser() 
    #print ('Number of arguments:', len(sys.argv), 'arguments.')
    nfile=str([sys.argv][0][1])
    #print (nfile)
    #print ('Argument List:', str(sys.argv))
    
    return nfile


# Flag table , monitor dataset to protect from over writting

def gurdinupdate():
    
    c.execute('CREATE TABLE if not exists GURDIAN \
             (TFLAG       INT(1)     DEFAULT 0);')

    c.execute("select TFLAG from GURDIAN")
    
    #secflag=[c][0]         
    #return c
    secflag = c.fetchall()

    return secflag

# update Flag table, to omite ignore updationg functions    
def gurdininsert():
    
    c.execute('''INSERT INTO GURDIAN (TFLAG)
                     VALUES(:update)''',
                    {'update':1})

# Creat datatable to calculate IDF and sum (TF*IDF) for each book  
def createtablew():
    c.execute('CREATE TABLE if not exists W \
             (WORD       VARCHAR(200)     NOT NULL, \
              IDF        REAL                 NULL);')
    c.execute('CREATE TABLE if not exists  BOOK \
             (BOOKID     INT                  NULL,\
              SUMTFIDF   REAL                 NULL);')
              
    c.execute('CREATE TABLE if not exists  AUTHORS \
             (BOOKID     INT              NOT NULL, \
              BOOKTITLE  VARCHAR(400)         NULL, \
              AUTHOR     VARCHAR(400)         NULL );')
    
    c.execute('CREATE TABLE if not exists WORDS\
             (ID        INTEGER PRIMARY KEY    AUTOINCREMENT NOT NULL,\
              WORD       VARCHAR(200)     NOT NULL,\
              TF         INT              NOT NULL,\
              IDF        REAL             NULL,\
              TFIDF      REAL             NULL,\
              BOOKID     INT              NOT NULL );')
    db.commit()



def WordCount(filename):
    
    # skip the break lines
    with open(filename) as f:
        for line in f:
            if len(line)<4 :
                continue
            l=line
            l=l.replace('\n','')
            bokid=line.split('\t')
            
            l = re.sub('[ \( \) \[ \] !@#$.:;?%&*"\d \t, \s - _ ]',  ' ', l)
          
            l=l.replace('  ',' ')
            l=Counter(l.lower().strip().split(' '))
            
            for a,b in l.items():
                
                # insert data to Dataset
                c.execute('''INSERT INTO WORDS (WORD, TF, IDF,TFIDF, BOOKID)
                                VALUES(:WORD, :TF, :IDF, :TFIDF, :BOOKID)''',
                                {'WORD':a, 'TF':b, 'IDF':1,'TFIDF':1, 'BOOKID':bokid[0]})
            c1.execute('''INSERT INTO AUTHORS (BOOKID, BOOKTITLE, AUTHOR)
                                VALUES(:BOOKID, :BOOKTITLE, :AUTHOR)''',
                                {'BOOKID':bokid[0],'BOOKTITLE':bokid[1],'AUTHOR':bokid[2]})

        db.commit()
    # print the proccesing time for keywork extraction


def RECORDCOUNT():
    c.execute("select count(BOOKID) from AUTHORS")
    
    #return c
    secflag = c.fetchall()
    
    TOTALRECORDS=secflag[0][0]  
    print("Records =:", TOTALRECORDS)         
    return TOTALRECORDS


def Calculate_IDF0():
    c.execute ("INSERT INTO W (WORD, IDF)\
        SELECT WORD, none, np.log(nrecord/sum(IDF))\
        FROM WORDS  group by WORD;")

    db.commit()

def Calculate_IDF(a):
    TOTALRECORD=a
    c.execute("select WORD, sum(IDF) from WORDS group by WORD ")
    all_rows = c.fetchall()
    for r in all_rows:
        a= np.log(TOTALRECORD/(r[1]))
        b=r[0]
        #print(a, ":",b)
        c.execute('''INSERT INTO W (WORD, IDF)
                     VALUES(:WORD,:IDF)''',
                    {'WORD':b, 'IDF':a})
    db.commit()



def updatedb():
    c.execute(" UPDATE WORDS\
    SET\
    (IDF, TFIDF) = (SELECT W.IDF, WORDS.TF * W.IDF\
                                FROM W\
                                WHERE WORDS.WORD = W.WORD )")
    db.commit(); #
    


def BOOKIDF():
    c.execute(" INSERT INTO \
        BOOK (BOOKID, SUMTFIDF)\
        SELECT BOOKID, sum(TFIDF) \
        FROM WORDS \
        group by BOOKID; ")
    db.commit()
# creat a view table for search 
def CREATVIEW():
    c.execute("    CREATE VIEW if not exists BSEARCH AS SELECT \
                    BOOK.BOOKID, BOOK.SUMTFIDF ,\
                    WORDS.BOOKID, WORDS.TFIDF, WORDS.WORD, \
                    AUTHORS.BOOKTITLE , AUTHORS.AUTHOR \
                    FROM BOOK ,WORDS ,AUTHORS \
                    WHERE (WORDS.BOOKID = BOOK.BOOKID) AND \
                    (BOOK.BOOKID=AUTHORS.BOOKID)")
    db.commit()


#a = [input('Please Enter your keywords: ')]
#print('Hello', person)

def WORDSEARCH(a):
    st=datetime.now()
    print ("\n")
    print ("START:",datetime.now())
    #a=a.split('\t')
    
    for f in [a]:
        
        
        


        c.execute("select BOOKID,BOOKTITLE,AUTHOR, SUMTFIDF,WORD,TFIDF from BSEARCH \
                    WHERE WORD like ? \
                  group by BOOKID \
                  ORDER by TFIDF DESC, BOOKID ASC limit 10 ", (f+'%',) )

        rows = c.fetchall()
    j=0
    for line in rows :
        j+=1
        print ("search rank :" , j) 
        
        #print ("\n")
        print (" BOOKID :", line[0],'\t',line[3],'\t', "Title : ",line[1],'\t',"Authors:", line[2] )
        #print ("Authors:", line[2])
        #print ("TF*IDF :", line[3])
        #print ("\n")
        print ("...........................")
    
    
    print ("\n")
    print ("Search proccess was :",datetime.now()-st)

def main():
    databasename= 'word.db'
    db = sqlite3.connect(databasename)
            
    c = db.cursor()
   
    arg_parser = create_arg_parser()
    filename= arg_parser

    
    #parsed_args = arg_parser.parse_args(sys.argv[1:])
    if os.path.exists(filename):
        print("File exist")
        #parse_Database file 
        if os.path.exists(databasename):
            print("Database is exist")
            db = sqlite3.connect(databasename)
            
            c = db.cursor()
            
        else:
            db = sqlite3.connect(databasename)
            
            c = db.cursor()
            #creat DB
            
        securityflag = gurdinupdate()
        
        if len(securityflag) > 0 :
              a= 'start'
              #a=input('Please Enter your keywords:  ').lower()
              while a != 'eof':
                  a=input('Please Enter your keywords:  ')
                  if len(a)>1 :
                      
                      WORDSEARCH(a)
                  #WORDSEARCH(a)
              c.close()
              print (datetime.now()-start)

            
        else:

              gurdininsert()
              print ("1st step:",datetime.now()-start)
              createtablew()
              print ("2nd step:",datetime.now()-start)
              WordCount(filename)
              print ("3Rd step:",datetime.now()-start)
              numberofrecord=RECORDCOUNT()
              print ("4th step:",datetime.now()-start)
              Calculate_IDF(numberofrecord)
              print ("5th step:",datetime.now()-start)
              updatedb()
              print ("6th step:",datetime.now()-start)
              BOOKIDF()
              print ("7th step:",datetime.now()-start)
              CREATVIEW()
              print ("8th step, Ready for search",datetime.now()-start)

              a='start'
              #a=input('Please Enter your keywords:  ').lower()
              while a != 'eof':
                  a=input('Please Enter your keywords:  ')
                  if len (a) >1 :
                      
                      WORDSEARCH(a)
              
              c.close()
              print (datetime.now()-start)
            
    else:
        print("File Not Exist!")

if __name__ == '__main__':
    main()


                 
#db.commit()





