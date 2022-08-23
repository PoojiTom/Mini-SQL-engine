#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import math
d={}
e={}
me=open('metadata.txt','r')
line=me.readlines()
flag=0
count=0
l=1
mine=[]
#print(line[0],end="")
for row1 in line:
    row=row1[0:len(row1)-1].lower()
    #print(row,end="")
    if(row=="<end_table>"):
        e[temp]=mine
        continue
    if(row=="<begin_table>"):
        mine=[]
        flag=1
        l=1
        #print('*')
        continue
    if(flag==1):
        temp=row
        flag=0
        continue
    d[row]=(temp,l)
    mine.append(row)
    l=l+1
    #print(d[row],row)
    #print(e)


# In[2]:


#print(d)
#print(e)


# In[3]:


def read_table(tab):
    red = open('{0}.csv'.format(tab), 'r')
    cs=csv.reader(red,delimiter=',')
    l=[]
    for i in cs:
        te=[]
        for j in i :
            hi=(j.split('"'))
            hi=hi[0]
            #print(hi)
            te.append(int(hi))
        l.append(te)
        #print(te)
    return l
def join_table(tab1,tab2):
    l=[]
    #print(tab1)
    #print(tab2)
    for i in range(len(tab1)):
        for j in range(len(tab2)):
            me1=tab1[i].copy()
            me1.extend(tab2[j])
            #print(me1)
            l.append(me1)
    return l
def make_table(tab):
    if(len(tab)==1):
        return read_table(tab[0]),e[tab[0]]
    ta=read_table(tab[0])
    tem=e[tab[0]]
    #print(temp)
    for i in range(1,len(tab)):
        #print(e[tab[i]])
        ta=join_table(ta,read_table(tab[i]))
        tem.extend(e[tab[i]])
    return ta,tem
def extract_table(tab,cols,req):
    tab1=[[row[i] for row in tab] for i in range(len(tab[0]))]
    me=[]
    #print(req)
    #print(cols)
    for i in range(len(req)):
        for j in range(len(cols)):
            if(cols[j]==req[i]):
                me.append(tab1[j])
                break
    req=[x for x in req if x]
    if(len(me)!=len(req)):
        print("not every column is present in table")
        sys.exit()
    tab1=[[row[i] for row in me] for i in range(len(me[0]))]
    #print(tab1)
    return tab1


# In[4]:


def integer(a,arr,cols):
    try : 
        int(a)
        return int(a)
    except :
        for i in range(len(cols)):
            if(cols[i]==a):
                return arr[i]
        print('column not exist')
        sys.exit()
def cond(a,b,op,arr,cols):
    #print('hi--',integer(a,arr,cols),integer(b,arr,cols))
    if(op=='<='):
        if(integer(a,arr,cols)<=integer(b,arr,cols)):
            return True
        else :
            return False
    if(op=='<'):
        if(integer(a,arr,cols)<integer(b,arr,cols)):
            return True
        else :
            return False
    if(op=='>='):
        if(integer(a,arr,cols)>=integer(b,arr,cols)):
            return True
        else :
            return False
    if(op=='>'):
        if(integer(a,arr,cols)>integer(b,arr,cols)):
            return True
        else :
            return False
    if(op=='='):
        if(integer(a,arr,cols)==integer(b,arr,cols)):
            return True
        else :
            return False
def wher_split(t,s,stri,arr,cols): 
    st11=''
    st12=''
    st21=''
    st22=''
    op1=''
    op2=''
    #print(t,s)
    for i in range(len(t)):
        if(t[i]=='<' or t[i]=='=' or t[i]=='>'):
            if(t[i]=='='):
                st11=t[:i]
                st12=t[i+1:]
                op1='='
            else :
                if(t[i+1]=='='):
                    st11=t[:i]
                    st12=t[i+2:]
                    op1=t[i]+t[i+1]
                else :
                    st11=t[:i]
                    st12=t[i+1:]
                    op1=t[i]
            break
    for i in range(len(s)):
        if(s[i]=='<' or s[i]=='=' or s[i]=='>'):
            if(s[i]=='='):
                st21=s[:i]
                st22=s[i+1:]
                op2='='
            else :
                if(s[i+1]=='='):
                    st21=s[:i]
                    st22=s[i+2:]
                    op2=s[i]+s[i+1]
                else :
                    st21=s[:i]
                    st22=s[i+1:]
                    op2=s[i]
            break
    l=[] 
    for i in range(len(arr)):
        if(stri=='and'):
            #print('*')
            if(cond(st11,st12,op1,arr[i],cols) and cond(st21,st22,op2,arr[i],cols)):
                l.append(arr[i])
        if(stri=='or'):
            #print('^')
            if(cond(st11,st12,op1,arr[i],cols) or cond(st21,st22,op2,arr[i],cols)):
                l.append(arr[i])
    return l
def wher(comm,arr,cols):
    #print('in wher',comm)
    if( ('and' in comm) or ('or'in comm)):
        t=''
        s=''
        #me <= 3 , me<= 3 , me <= 3 --> me<=3 
        if('and' in comm):
            for j in range(len(comm)):
                if(comm[j]=='and'):
                    break
                t=t+comm[j]
            for j in range(len(comm)):
                if(comm[0]=='and'):
                    comm.pop(0)
                    break
                comm.pop(0)
            for j in range(len(comm)):
                if(comm[j]=='group' or comm[j]=='order'):
                    break
                s=s+comm[j]
            return wher_split(t,s,'and',arr,cols)
        if('or' in comm):
            for j in range(len(comm)):
                if(comm[j]=='or'):
                    break
                t=t+comm[j]
            for j in range(len(comm)):
                if(comm[0]=='or'):
                    comm.pop(0)
                    break
                comm.pop(0)
            for j in range(len(comm)):
                if(comm[j]=='group' or comm[j]=='order'):
                    break
                s=s+comm[j]
            return wher_split(t,s,'or',arr,cols)
    else :
        t=''
        for i in range(len(comm)):
            if(comm[i]=='group' or comm[i]=='order'):
                break
            t=t+comm[i]
        return wher_split(t,t,'or',arr,cols)


# In[5]:


def func(a,b):
    #print(a,b)
    if(b.lower()=='count'):
        return len(a)
    if(b.lower()=='sum'):
        return sum(a)
    if(b.lower()=='avg'):
        return sum(a)/len(a)
    if(b.lower()=='min'):
        return min(a)
    if(b.lower()=='max'):
        #print('here')
        #print(max(a))
        return max(a)
def col_func(cols,aggs):
    temp=[]
    for i in range(len(cols)):
        if(aggs[i]!=''):
            temp.append(aggs[i]+'('+cols[i]+')')
        else:
            temp.append(cols[i])
    return temp
def group(arr,cols,aggs,n):
    gro=[]
    for i in range(n,len(cols)):
        arr=sorted(arr,key = lambda x:x[i])
    while(1):
        if(len(arr)==0):
            break
        temp=arr[0].copy()
        #arr.pop(0)
        me=[]
        l=[[]for i in range(len(cols))]
        #for i in range(len(temp)):
         #   if(aggs[i]!=''):
          #      l[i].append(temp[i])
        for i in range(len(arr)):
            flag_here=0
            for j in range(len(aggs),len(cols)):
                if(temp[j]!=arr[i][j]):
                    flag_here=1
            if(flag_here==0):
                me.append(arr[i])
                for ii in range(len(aggs)):
                    if(aggs[ii]!=''):
                        l[ii].append(arr[i][ii])
        #print('--',me)
        for i in range(len(aggs)):
            if(aggs[i]!=''):
                temp[i]=func(l[i],aggs[i])
            #print('hi madhuri',temp[i])
        for i in range(len(me)):
            for j in range(len(arr)):
                if(me[i]==arr[j]):
                    #print('*',i,end='')
                    arr.pop(j)
                    break
        gro.append(temp)
        #print('--',temp)
    #print(cols,aggs)
    cols[:n]=col_func(cols[:n],aggs)
    gro=extract_table(gro,cols,cols[:n])
    return gro,cols[:n]


# In[6]:


def order(arr,cols,req):
    #print('order by--',arr)
    req.reverse()
    oder=1
    for j in range(len(req)):
        tempoo=0
        if(req[j]=='desc'):
            oder=-1
        if(req[j]=='desc' or req[j]=='asc'):
            continue
        for i in range(len(cols)):
            if(cols[i]==req[j]):
                arr=sorted(arr,key=lambda x:oder*x[i])
                tempoo=1
                oder=1
                break
        if(tempoo==0):
            print('column not found for ordering')
            sys.exit()
        oder=1
    #arr=sorted(arr,key = lambda x : oder*x[req])
    return arr,cols


# In[7]:


def aggregates(arr,cols,req,aggs,mohit):
    aggs=[x for x in aggs if x]
    if(len(aggs)!=0 and len(aggs)!=len(req)):
        print('aggregates found without group by')
    if(len(aggs)==0):
        return [arr,cols],mohit
    extract_table(arr,cols,req)
    arr1=[[row[i] for row in arr] for i in range(len(arr[0]))]
    x=[0 for i in range(len(aggs))]
    for i in range(len(aggs)):
        x[i]=func(arr1[i],aggs[i])
    return [[x],col_func(req,aggs)],col_func(req,aggs)
def print_me(arr,cols,aggs=False):
    if(aggs):
        cols1=col_func(cols,aggs)
        cols1,cols=cols,cols1
    else :
        cols1=cols.copy()
        for i in range(len(cols1)):
            if('(' in cols[i]):
                for j in range(len(cols[i])):
                    if(cols[i][j]=='('):
                        cols1[i]=cols[i][j+1:]
                        break
            cols1[i]=cols1[i].rstrip("()")
    print(d[cols1[0]][0],'.',cols[0],sep='',end='')
    for i in range(1,len(cols)):
        print(',',d[cols1[i]][0],'.',cols[i],sep='',end='')
    print()
    if(len(arr)==0 or len(arr[0])==0):
        print('empty table or no rows')
        sys.exit()
    for i in range(len(arr)):
        print(arr[i][0],end='',sep='')
        for j in range(1,len(arr[i])):
            print(',',arr[i][j],sep='',end='')
        print()
    #print(len(arr))
    sys.exit()


# In[8]:


#import sqlparse
import re
import sys
import copy
def split_own(a):
    temp1=[]
    temp2=[]
    #print(a)
    for i in range(len(a)):
        flag=0
        here=''
        here1=''
        for j in range(len(a[i])):
            if(a[i][j]=='('):
                #print(j)
                here1=a[i][:j]
                here=a[i][j+1:-1]
                flag=1
                break
        if(flag==1):
            temp1.append(here)
            temp2.append(here1)
        else:
            temp1.append(a[i])
            temp2.append('')
    return temp1,temp2
def main():
    com=sys.argv[1]
    com=com.lower()
    com=com.strip()
#com=com.lower()
    save_com=com
    com_store=com
    com_dup=com.lower()
    if(bool(re.match('select.*from.*',com_dup))==False):
    #print('processing :')
        print('wrong command: didnot find select or from or the order followed is some what mistaken')
        sys.exit()
    if(com[-1]!=';'):
        print('semicolon ending is missing')
        sys.exit()
    com=com[:-1]
    com=com.split()
    if(com[0].lower()!='select'):
        print('select not found')
        sys.exit()
    com.pop(0)
    er=0
    l=[]
    for i in com :
        if(i.lower()=='from'):
            er=1
            break
        l.extend(i.split(','))
    n=len(com)
    for i in range(n):
        if(com[0].lower()=='from'):
            com.pop(0)
            break
        com.pop(0)
    col=[x for x in l if x]
    flag_distinct=0
    if(col[0]=='distinct'):
        col.pop(0)
        flag_distinct=1
    col_copy=col.copy()
#print(col_copy)
    col,agg=split_own(col)
    agg_copy=[x for x in agg if x]
#print(col,agg)
    if(len(agg_copy)!=len(col) and 'group' not in com and len(agg_copy)!=0):
        print('group not found in less number of aggregates')
        sys.exit()
    flag_group=0
    if('group' in com):
        flag_group=1
#print(col,agg,agg_copy)
    l=[]
    splitting=['where','group','order']
    for i in com:
        if(i.lower() in splitting):
            break
        l.extend(i.split(','))
    tab=[x for x in l if x]
    n=len(com)
    for i in range(n):
        if(com[0].lower() in splitting):
            break
        com.pop(0)
#print(tab)
    if(er==0):
        print('from not found after any space ie. spacing error')
        sys.exit()
    if(len(set(tab))!=len(tab)):
        print('tables are not unique')
        sys.exit()
#me=sqlparse.parse(com)
#me=sqlparse.format(com, reindent=True, keyword_case='upper')
#print(com)


# In[9]:
    fin=make_table(tab)
    #print(fin)
    star=['*']
    for i in range(len(agg)):
        if(agg[i]=='count'):
            if(col[i]=='*'):
                col[i]=fin[1][0]
#print(col)
#print()
#print()
    if(col[0]=='*'):
        col.pop(0)
        t=fin[1].copy()
        #print(t)
        t.extend(col)
        col=t
        agg1=['' for i in range(len(fin[1])-1)]
        agg1.extend(agg)
        agg=agg1
#print('*',col)
    save=fin[1]
#print(fin[0])
#print(save_com)
    if(len(com)!=0 and com[0].lower()=='where'):
    #print('000')
        fin=[wher(com[1:],fin[0],fin[1]),save]
#print(fin,len(fin[0]))
    if(len(fin[0])==0):
        print_me(fin[0],col_func(col,agg))
        sys.exit()
    #print('hi-tej')
#fin=group_lilly(fin[0],save_com,fin[1])
#print(fin)

    for i in range(len(com)):
        if(com[0]=='group' or com[0]=='order'):
            break
        com.pop(0)
#if(len(com)==0):
#    extract_table(fin[0],fin[1],col)
    if(len(com)!=0 and com[0]=='group'):
        if(com[1]!='by'):
            print('group by not found -> syntax error')
            sys.exit()
        com.pop(0)
        com.pop(0)
        temps=[]
        for i in range(len(com)):
            if(com[0]=='order'):
                break
            temps.extend(com[0].split(','))
            com.pop(0)
        temps=[x for x in temps if x]
    #print(agg)
    #print(col)
    #print(temps)
        for i in range(len(col)):
            if(agg[i]=='' and col[i] not in temps):
            #print(col[i])
                print('group command error , columns in left and right are not same')
                sys.exit()
        gr=len(col)
        temps.reverse()
        col.extend(temps)
        #print(agg)
        fin=extract_table(fin[0],fin[1],col)
        fin=group(fin,col,agg,gr)
        #print(fin)
        col=fin[1]
#print(com)
    if(flag_group==0):
        fin,col=aggregates(fin[0],fin[1],col,agg,col)
    #print('aggregates--',fin)
    if(len(com)!=0 and com[0]=='order'):
        if(com[1]!='by'):
            print('order found but not by -> syntax error')
            sys.exit()
        com.pop(0)
        com.pop(0)
        req=[]
        for i in range(len(com)):
            req.extend(com[0].split(','))
            com.pop(0)
        req=[x for x in req if x]
        fin=order(fin[0],fin[1],req)
    #print(fin[1])
    #print()
    #print()
    #print()
        if(len(com)!=0):
            print('something is mistaken only one column in order by allowed and string is not empty')
            sys.exit()
    #print(fin[0],fin[1],req,oder)
#print(fin)
#fin=extract_table(fin[0],fin[1],col)
#print(fin[1],col)
    fin=[extract_table(fin[0],fin[1],col),col]
#print(flag_distinct)
#print(fin)
    if(flag_distinct==1):
        temp=[]
        for x in fin[0]:
            if(x not in temp):
                temp.append(x)
        fin[0]=temp.copy()
#print_self(fin)
#print()
#print()
#print(fin,len(fin))
    print_me(fin[0],col)
if __name__ == '__main__':
    main()
