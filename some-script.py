#!/usr/bin/env python
import web
import csv
import difflib
import re
import operator
import Levenshtein
import datetime
import time

import logging

FMT = '%m/%d/%y %H:%M:%S'

logging_level=6

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)




episode_dir="episode2.txt"
feature_dir="feaseries2.txt"
season_dir="season2.txt"
german_dir="german2.txt"
avail_dir="avails3.txt"

episode=[]
with open(episode_dir,"rb") as k:
             for row in k:
                row=row.split("\t")
                if len(row)==8:
                  episode.append(row)

k.close()

feature=[]
with open(feature_dir,"rb") as j:
             for row in j:
                row=row.split("\t")
                if len(row)==4:
                  feature.append(row)

j.close()


season=[]
with open(season_dir,"rb") as s:
             for row in s:
                row=row.split("\t")
                if len(row)==5:
                   season.append(row)
s.close()

german=[]
with open(german_dir,"rb") as gs:
             for row in gs:
                row=row.split("\t")
                if len(row)==8:
                  german.append(row)
gs.close()

avails=[]
with open(avail_dir,"rb") as avs:
             for row in avs:
                  row=row.split("\t")
                  if len(row)==7:
                     avails.append(row)
avs.close()

episode_dic={}
feature_dic={}
season_dic={}
german_dic={}
avails_dic={}


def substitute1(s2):
             s2=re.sub(r'"','',s2)
             s2=re.sub(r'Part III','Part 3',s2)
             s2=re.sub(r'Part II','Part 2',s2)
             s2=re.sub(r'Part I','Part 1',s2)
             s2=re.sub(r'Part One','Part 1',s2)
             s2=re.sub(r'Part Two','Part 2',s2)
             s2=re.sub(r'Part Three','Part 3',s2)
             s2=re.sub(r' III',' 3',s2)
             s2=re.sub(r' II',' 2',s2)
             s2=re.sub(r' I',' 1',s2)
             s2=re.sub(r'12:00 Midnight','12:00 A.M',s2)
             s2=re.sub(r'Dr\.','Doctor',s2)
             return(s2)
def substitute2(s2):
             matchO=re.match(r'(.*):(.*)',s2)
             matchOb=re.match(r'(.*), The',s2)
             if matchO:
               matchO1=re.match(r'(.*), The',matchO.group(1))
               matchO2=re.match(r'(.*), The',matchO.group(2))
               if matchO1 and not matchO2:
                     group1="The"+matchO1.group(1)
                     s2=group1+matchO.group(2)
               if matchO2 and not matchO1:
                     group2="The"+matchO2.group(1)
                     s2=matchO.group(1)+group2
               if matchO1 and matchO2:
                      group1="The"+matchO1.group(1)
                      group2="The"+matchO2.group(1)
                      s2=group1+group2
             elif matchOb:
                 s2="The"+matchOb.group(1)
             return(s2)



def substitute3(s2):
             s2=s2.lower()
             s2=re.sub(r'series',' ',s2)
             s2=re.sub(r'episode',' ',s2)
             s2=re.sub(r'season',' ',s2)
             s2=re.sub(r'"',' ',s2)
             s2=re.sub(r'-',' ',s2)
             s2=re.sub(r':',' ',s2)
             s2=re.sub(r' ','',s2)
             s2=re.sub(r'\&','and',s2)
             s2=re.sub(r'\.','',s2)
             s2=re.sub(r'\*','',s2)
             return(s2)
for j in range(len(episode)):
             s2=episode[j][3].strip()+' - '+episode[j][4].strip()+' - '+episode[j][5].strip()
             s2=substitute1(s2)
             matchObj=re.match(r'(.*) - (.*) - (.*)',s2)
             matchO=re.match(r'(.*):(.*)',s2)
             matchOb=re.match(r'(.*), The',s2)
             if matchObj:
                 matchObj1=re.match(r'(.*), The',matchObj.group(1))
                 matchObj3=re.match(r'(.*), The',matchObj.group(3))
                 if matchObj1 and not matchObj3:
                     group1="The"+matchObj1.group(1)
                     s2=group1+matchObj.group(2)+matchObj.group(3)
                 if matchObj3 and not matchObj1:
                     group3="The"+matchObj3.group(1)
                     s2=matchObj.group(1)+matchObj.group(2)+group3
                 if matchObj1 and matchObj3:
                      group1="The"+matchObj1.group(1)
                      group3="The"+matchObj3.group(1)
                      s2=group1+matchObj.group(2)+group3
             elif matchO:
               matchO1=re.match(r'(.*), The',matchO.group(1))
               matchO2=re.match(r'(.*), The',matchO.group(2))
               if matchO1 and not matchO2:
                     group1="The"+matchO1.group(1)
                     s2=group1+matchO.group(2)
               if matchO2 and not matchO1:
                     group2="The"+matchO2.group(1)
                     s2=matchO.group(1)+group2
               if matchO1 and matchO2:
                      group1="The"+matchO1.group(1)
                      group2="The"+matchO2.group(1)
                      s2=group1+group2
             elif matchOb:
                 s2="The"+matchOb.group(1)
             s2=substitute3(s2)
             episode[j].append(s2)
             s3=re.sub(r',',' ',episode[j][3]+episode[j][4]+episode[j][5]).lower()
             episode[j].append(s3)
             episode_dic[episode[j][7].strip()]=s2
for t in range(len(feature)):
             s2=feature[t][1].strip()
             s2=substitute1(s2)
             matchO=re.match(r'(.*):(.*)',s2)
             matchOb=re.match(r'(.*), The$',s2)
             matchOa1=re.match(r'(.*), A$',s2)
             matchOa2=re.match(r'(.*), An$',s2)
             matchOa3=re.match(r'(.*), As$',s2)
             if matchO:
               matchO1=re.match(r'(.*), The',matchO.group(1))
               matchO2=re.match(r'(.*), The',matchO.group(2))
               if matchO1 and not matchO2:
                     group1="The"+matchO1.group(1)
                     s2=group1+matchO.group(2)
               if matchO2 and not matchO1:
                     group2="The"+matchO2.group(1)
                     s2=matchO.group(1)+group2
               if matchO1 and matchO2:
                      group1="The"+matchO1.group(1)
                      group2="The"+matchO2.group(1)
                      s2=group1+group2
             elif matchOb:
                s2="The"+matchOb.group(1)
             elif matchOa1:
                s2="A"+matchOa1.group(1)
             elif matchOa2:
                s2="An"+matchOa2.group(1)
             elif matchOa3:
                s2="As"+matchOa3.group(1)
             s2=substitute3(s2)
             s2=s2
             feature[t].append(s2)
             feature_dic[feature[t][2].strip()]=s2
for q in range(len(season)):
             s2=season[q][2].strip()+" "+season[q][3].strip()
             s2=substitute1(s2)
             s2=substitute2(s2)
             s2=re.sub(r',',' ',s2)
             s2=substitute3(s2)
             season[q].append(s2)
             season_dic[season[q][4].strip()]=s2
for q in range(len(german)):
             s2=german[q][3].strip()
             s2=substitute1(s2)
             s2=re.sub(r'Akte X','AkteX',s2)
             s2=re.sub(r'\[Ov\]',' ',s2)
             s2=re.sub(r'Omu',' ',s2)
             s2=re.sub(r'Staffel',' ',s2)
             s2=re.sub(r'AkteX','X-Files',s2)
             s2=substitute2(s2)
             s2=re.sub(r',',' ',s2)
             s2=substitute3(s2)
             s2=s2+german[q][4]+german[q][6]
             german[q].append(s2)
             german_dic[german[q][7].strip()]=s2
for q in range(len(avails)):
             s2=avails[q][5].strip()
             s2=substitute1(s2)
             matchO=re.match(r'(.*) - (.*)',s2)
             matchOb=re.match(r'(.*), The',s2)
             if matchO:
               matchO1=re.match(r'(.*), The',matchO.group(1))
               matchO2=re.match(r'(.*), The',matchO.group(2))
               if matchO1 and not matchO2:
                     group1="The"+matchO1.group(1)
                     s2=group1+matchO.group(2)
               if matchO2 and not matchO1:
                     group2="The"+matchO2.group(1)
                     s2=matchO.group(1)+group2
               if matchO1 and matchO2:
                      group1="The"+matchO1.group(1)
                      group2="The"+matchO2.group(1)
                      s2=group1+group2
             elif matchOb:
                 s2="The"+matchOb.group(1)
             s2=re.sub(r',',' ',s2)

             s2=substitute3(s2)
             s2=s2
             avails[q].append(s2)
             avails_dic[avails[q][6].strip()]=[avails[q][0],avails[q][2],s2]

def clean_input_data(level1):
          level1=re.sub(r'Part III','Part 3',level1)
          level1=re.sub(r'Part II','Part 2',level1)
          level1=re.sub(r'Part I','Part 1',level1)
          level1=re.sub(r'Part One','Part 1',level1)
          level1=re.sub(r'Part Two','Part 2',level1)
          level1=re.sub(r'Part Three','Part 3',level1)
          level1=re.sub(r' III',' 3',level1)
          level1=re.sub(r' II',' 2',level1)
          level1=re.sub(r' I',' 1',level1)
          level1=re.sub(r'12:00 Midnight','12:00 A.M',level1)
          level1=re.sub(r'Dr\.','Doctor',level1)
          level1=re.sub(r'\[Ov\]',' ',level1)
          level1=re.sub(r'Omu',' ',level1)
          level1=re.sub(r'Staffel',' ',level1)
          level1=re.sub(r'Vol.','Season',level1)
          matchOb=re.match(r'(.*), The$',level1)
          matchOa1=re.match(r'(.*), A$',level1)
          matchOa2=re.match(r'(.*), An$',level1)
          matchOa3=re.match(r'(.*), As$',level1)
          if matchOb:
                level1="The"+matchOb.group(1)
          if matchOa1:
                level1="A"+matchOa1.group(1)
          if matchOa2:
                level1="An"+matchOa2.group(1)
          if matchOa3:
                level1="As"+matchOa3.group(1) 
          level1=re.sub(r'Akte X','AkteX',level1)
          level1=re.sub(r'AkteX','X-Files',level1)
          level1=level1.lower()
          level1=re.sub(r'series',' ',level1)
          level1=re.sub(r'season',' ',level1)
          level1=re.sub(r'episode',' ',level1)
          level1=re.sub(r'"',' ',level1)
          level1=re.sub(r'-',' ',level1)
          level1=re.sub(r':',' ',level1)
          level1=re.sub(r' ','',level1)
          level1=re.sub(r'\&','and',level1)
          level1=re.sub(r'\.','',level1)
          level1=re.sub(r'\*','',level1)
          return(level1)

def selection(my_list, avai1):
             my_list1=dict(my_list)
             my_list_zip=zip(*my_list)[0]
             inter=set(my_list_zip).intersection(set(avai1.keys()))
             if set(my_list_zip) & set(avai1.keys()):
                sub_dic=dict((k, my_list1[k]) for k in inter)

             if set(my_list_zip) & set(avai1.keys()) and max(sub_dic.values())>0.8:
                    max_va=max(sub_dic.iteritems(),key=operator.itemgetter(1))
                    a=datetime.date.today()
                    date_object_start=datetime.datetime.strptime(avai1[max_va[0].strip()][0],"%m/%d/%Y %H:%M:%S").date()
                    date_object_end=datetime.datetime.strptime(avai1[max_va[0].strip()][1],"%m/%d/%Y %H:%M:%S").date()
                    delta=datetime.timedelta(days=-14)
                    u=a+delta
                    start=u-date_object_start
                    start=start.days
                    end=date_object_end-u
                    end=end.days
                    if  start>=0 and end>=0:
                       match=max_va[0].strip()+","+str(min((int(float(max_va[1])*100)+30),100))
                       return match
                    else:
                       match=max_va[0].strip()+","+str(min((int(float(max_va[1])*100)+20),100))
                       return match
             else:
                      match=my_list[0][0].strip()+","+str(int(float(my_list[0][1])*100))
                      return match

urls = ('/title_matching2','title_matching2')
app1 = web.application(urls,globals())


 
class title_matching2:

     

    def GET(self):
      try:
       step1=time.strftime("%x %X")
       if logging_level>4:
              print "The starting time is: "+step1
       getInput = web.input(level1="level1",level2="level2",level3="level3",WPR_ID="WPR",htype1="TYPE1",htype2="TYPE2")
       htype1=getInput.htype1.encode("utf-8","ignore")
       htype2=getInput.htype2.encode("utf-8","ignore")
       WPR_ID=str(getInput.WPR_ID.encode("utf-8","ignore"))
       if htype1=="SALES" and htype2=="BCAST":
        
          level1=getInput.level1
          level2=getInput.level2
          level3=getInput.level3
          level1=level1.encode("utf-8","ignore")
          level2=level2.encode("utf-8","ignore")
          level3=level3.encode("utf-8","ignore")
          level1=str(level1)
          level2=str(level2)
          level3=str(level3)
          if logging_level>3:
              print "The input parameters are %s,%s,%s,%s,%s,%s:" % (level1,level2,level3,WPR_ID,htype1,htype2)
          level1=clean_input_data(level1)
          level3=clean_input_data(level3)

          WPR_ID=str(getInput.WPR_ID.encode("utf-8","ignore"))
          if WPR_ID=="":
               WPR_ID="NULL"

          

          if level1=="" and level2=="" and level3=="" and WPR_ID=="":
           my_list="Error"+","+"0"
           return my_list 
          if WPR_ID=="NULL":
           
           if level2!='UNK' and level3!='unk' and level1!='unk':
             level2=clean_input_data(level2)
             level=level1+level2+level3
             ff={}
             for j in range(len(episode)):
                k1=float(Levenshtein.ratio(str(level),episode[j][len(episode[j])-2]))
                ff[str(episode[j][7].strip())]=k1
             my_list=sorted(ff.items(),key=lambda x:x[1],reverse=True)[:5]
             match=selection(my_list,avails_dic)
             if logging_level>5:
                       print "returned value : % s" % match
             step2=time.strftime("%x %X")

             tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
             if logging_level>4:
               print "first step ending time   is:"+step2
               print "first step used time is %s:" % tdelta

             return match


 


           if level2=='UNK' and level3=='unk' and level1!='unk':
             ee={}
             level=level1
             for e in range(len(feature)):
               d2=float(Levenshtein.ratio(str(level),feature[e][len(feature[e])-1]))
               ee[str(feature[e][2].strip())]=d2
             my_list=sorted(ee.items(), key=lambda x: x[1],reverse=True)[:5]
             match=selection(my_list,avails_dic)
             if logging_level>5:
                       print "returned value : % s" % match
             step2=time.strftime("%x %X")

             tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
             if logging_level>4:
               print "first step ending time   is:"+step2
               print "first step used time is %s:" % tdelta
             return match
       
           level2=getInput.level2
           level2=level2.encode("utf-8","ignore")
           level2=str(level2)
           matchK=re.match(r'(.*)Episode ()',level2)
           matchK1=re.match(r'(.*)Episode  ',level2)
           matchK2=re.match(r'(.*)Episode \d',level2)
           

           if level3=='unk' and level2!='UNK' and level1!='unk':
            if not matchK and not matchK1 and not matchK2: 
             level2=clean_input_data(level2)
             cc={}
             level=level1+level2
             for r in range(len(season)):
                d3=float(Levenshtein.ratio(str(level),season[r][len(season[r])-1]))
                cc[str(season[r][4].strip())]=d3
             my_list=sorted(cc.items(),key=lambda x:x[1], reverse=True)[:5]
             match=selection(my_list,avails_dic)
             if logging_level>5:
                       print "returned value : % s" % match
             step2=time.strftime("%x %X")

             tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
             if logging_level>4:
               print "first step ending time   is:"+step2
               print "first  step used time is %s:" % tdelta
             return match
            elif matchK or matchK1 or matchK2:
                   level2=clean_input_data(level2)
                   cc={}
                   level=level1+level2
                   for r in range(len(german)):
                     d3=float(Levenshtein.ratio(str(level),german[r][len(german[r])-1]))
                     cc[str(german[r][7].strip())]=d3
                   my_list=sorted(cc.items(),key=lambda x:x[1],reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                     print "first  step ending time   is:"+step2
                     print "first  step used time is %s:" % tdelta
                   return match
           else:
              match="NULL"+","+"0"
              return match 
          elif WPR_ID!="NULL":
        #   if WPR_ID in avai1.keys():
        #        level=level1+level2+level3
        #        level=re.sub(r'unk','',level)
        #        level=re.sub(r'UNK','',level)
        
        #        if float(Levenshtein.ratio(str(level),avai1[WPR_ID][2]))>=0.95:
        #             rr=float(Levenshtein.ratio(str(level),avai1[WPR_ID][2]))
        #             rr=int(100*rr)
        #             my_list=WPR_ID.strip()+","+str(rr)
        #             return my_list
        #        elif float(Levenshtein.ratio(str(level),avai1[WPR_ID][2]))<0.7:
        #            ff={}
        #            for j in range(len(avai)):
        #               k1=float(Levenshtein.ratio(str(level),avai[j][len(avai[j])-1]))
        #               ff[str(avai[j][6].strip())]=k1
        #            my_list=max(ff.iteritems(), key=operator.itemgetter(1))
        #            if my_list[1]>=0.95:
        #               my_list=my_list[0].strip()+","+str(int(my_list[1]*100))
        #               return my_list
        #  step2=time.strftime("%x %X")

           if   WPR_ID in episode_dic.keys():
             level=level1+level2+level3           
             rr=float(Levenshtein.ratio(str(level),episode_dic[WPR_ID]))
             rr=int(100*rr)
             if rr>95:
                my_list=WPR_ID.strip()+","+str(rr)
                return my_list
             else:
                 if level2!='UNK' and level3!='unk' and level1!='unk':
                  level2=clean_input_data(level2)
                  level=level1+level2+level3
                  ff={}
                  for j in range(len(episode)):
                    k1=float(Levenshtein.ratio(str(level),episode[j][len(episode[j])-2]))
                    ff[str(episode[j][7].strip())]=k1
                  my_list=sorted(ff.items(),key=lambda x:x[1],reverse=True)[:5]
                  match=selection(my_list,avails_dic)
                  if logging_level>5:
                       print "returned value : % s" % match
                  step2=time.strftime("%x %X")

                  tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                  if logging_level>4:
                     print "first  step ending time   is:"+step2
                     print "first  step used time is %s:" % tdelta
                  return match

                 elif level2=='UNK' and level3=='unk' and level1!='unk':
                   ee={}
                   level=level1
                   for e in range(len(feature)):
                     d2=float(Levenshtein.ratio(str(level),feature[e][len(feature[e])-1]))
                     ee[str(feature[e][2].strip())]=d2
                   my_list=sorted(ee.items(),key=lambda x:x[1],reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                      print "first  step ending time   is:"+step2
                      print "first  step used time is %s:" % tdelta
                   return match

                 


                 level2=getInput.level2
                 level2=level2.encode("utf-8","ignore")
                 level2=str(level2)                 
                 matchK=re.match(r'(.*)Episode ()',level2)
                 matchK1=re.match(r'(.*)Episode  ',level2)
                 matchK2=re.match(r'(.*)Episode \d',level2)
                 if level3=='unk' and level2!='UNK' and level1!='unk':
                  if not matchK and not matchK1 and not matchK2:
                   level2=clean_input_data(level2)
                   level=level1+level2
                   cc={}
                   level=level1+level2
                   for r in range(len(season)):
                     d3=float(Levenshtein.ratio(str(level),season[r][len(season[r])-1]))
                     cc[str(season[r][4].strip())]=d3
                   my_list=sorted(cc.items(),key=lambda x:x[1], reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                      print "first  step ending time   is:"+step2
                      print "first  step used time is %s:" % tdelta
                   return match

                  elif  matchK or matchK1 or matchK2:
                    level2=clean_input_data(level2)
                    kk={}
                    level=level1+level2
                    for e in range(len(german)):
                          d2=float(Levenshtein.ratio(str(level),german[e][len(german[e])-1]))
                          kk[str(german[e][7].strip())]=d2
                    my_list=sorted(kk.items(),key=lambda x:x[1],reverse=True)[:5]
                    match=selection(my_list,avails_dic)
                    if logging_level>5:
                       print "returned value : % s" % match
                    step2=time.strftime("%x %X")

                    tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                    if logging_level>4:
                        print "first  step ending time   is:"+step2
                        print "first  step used time is %s:" % tdelta
                    return match
                
                 else:
                    match="NULL"+","+"0"
                    return match
                
           elif  WPR_ID not in episode_dic.keys() and WPR_ID in feature_dic.keys():
             level=level1
             rr=float(Levenshtein.ratio(str(level),feature_dic[WPR_ID]))
             rr=int(100*rr)
             if rr>95:
                my_list=WPR_ID+","+str(rr)
                return my_list
             else:
                  if level2!='UNK' and level3!='unk' and level1!='unk':
                   level=level1+level2+level3
                   ff={}
                   for j in range(len(episode)):
                    k1=float(Levenshtein.ratio(str(level),episode[j][len(episode[j])-2]))
                    ff[str(episode[j][7].strip())]=k1
                   my_list=sorted(ff.items(),key=lambda x:x[1],reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                      print "first  step ending time   is:"+step2
                      print "first  step used time is %s:" % tdelta
                   return match

                  if level2=='UNK' and level3=='unk' and level1!='unk':
                   ee={}
                   level=level1
                   for e in range(len(feature)):
                     d2=float(Levenshtein.ratio(str(level),feature[e][len(feature[e])-1]))
                     ee[str(feature[e][2].strip())]=d2
                   my_list=sorted(ee.items(),key=lambda x:x[1],reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                      print "first  step ending time   is:"+step2
                      print "first  step used time is %s:" % tdelta
                   return match
    
                  level2=getInput.level2
                  level2=level2.encode("utf-8","ignore")
                  level2=str(level2)
                  matchK=re.match(r'(.*)Episode ()',level2)
                  matchK1=re.match(r'(.*)Episode  ',level2)
                  matchK2=re.match(r'(.*)Episode \d',level2)
                  if level3=='unk' and level2!='UNK' and level1!='unk':
                   if not matchK and not matchK1 and not matchK2:
                    level2=clean_input_data(level2)
                    level=level1+level2
                    cc={}
                    level=level1+level2
                    for r in range(len(season)):
                     d3=float(Levenshtein.ratio(str(level),season[r][len(season[r])-1]))
                     cc[str(season[r][4].strip())]=d3
                    my_list=sorted(cc.items(),key=lambda x:x[1],reverse=True)[:5]
                    match=selection(my_list,avails_dic)
                    if logging_level>5:
                       print "returned value : % s" % match
                    step2=time.strftime("%x %X")

                    tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                    if logging_level>4:
                       print "first  step ending time   is:"+step2
                       print "first  step used time is %s:" % tdelta
                    return match

                   elif  matchK or matchK1 or matchK2 and level3=='unk':
                    level2=clean_input_data(level2)
                    kk={}
                    level=level1+level2
                    for e in range(len(german)):
                          d2=float(Levenshtein.ratio(str(level),german[e][len(german[e])-1]))
                          kk[str(german[e][7].strip())]=d2
                    my_list=sorted(kk.items(),key=lambda x:x[1],reverse=True)[:5]
                    match=selection(my_list,avails_dic)
                    if logging_level>5:
                       print "returned value : % s" % match
                    step2=time.strftime("%x %X")

                    tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                    if logging_level>4:
                       print "first  step ending time   is:"+step2
                       print "first  step used time is %s:" % tdelta
                    return match
                  else:
                     match="NULL"+","+"0"
                     return match

           elif  WPR_ID not in feature_dic.keys() and WPR_ID not in episode_dic.keys() and WPR_ID  in season_dic.keys():
             level=level1+level2
             rr=float(Levenshtein.ratio(str(level),season_dic[WPR_ID]))
             rr=int(100*rr)
             if rr>95:
                my_list=WPR_ID+","+str(rr)
                return my_list
             else:
                 if level2!='UNK' and level3!='unk' and level1!='unk':
                  level=level1+level2+level3
                  ff={}
                  for j in range(len(episode)):
                    k1=float(Levenshtein.ratio(str(level),episode[j][len(episode[j])-2]))
                    ff[str(episode[j][7].strip())]=k1
                  my_list=sorted(ff.items(),key=lambda x:x[1],reverse=True)[:5]
                  match=selection(my_list,avails_dic)
                  if logging_level>5:
                       print "returned value : % s" % match
                  step2=time.strftime("%x %X")

                  tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                  if logging_level>4:
                     print "first  step ending time   is:"+step2
                     print "first  step used time is %s:" % tdelta
                  return match




                 if level2=='UNK' and level3=='unk' and level1!='unk':
                   ee={}
                   level=level1
                   for e in range(len(feature)):
                     d2=float(Levenshtein.ratio(str(level),feature[e][len(feature[e])-1]))
                     ee[str(feature[e][2].strip())]=d2
                   my_list=sorted(ee.items(),key=lambda x:x[1],reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                        print "first  step ending time   is:"+step2
                        print "first  step used time is %s:" % tdelta
                   return match
        
                 level2=getInput.level2
                 level2=level2.encode("utf-8","ignore")
                 level2=str(level2)
                 matchK=re.match(r'(.*)Episode ()',level2)
                 matchK1=re.match(r'(.*)Episode  ',level2)
                 matchK2=re.match(r'(.*)Episode \d',level2)
                 if level3=='unk' and level2!='UNK' and level1!='unk':
                  if not matchK and not matchK1 and not matchK2:
                   level2=clean_input_data(level2)
                   level=level1+level2
                   cc={}
                   level=level1+level2
                   for r in range(len(season)):
                     d3=float(Levenshtein.ratio(str(level),season[r][len(season[r])-1]))
                     cc[str(season[r][4].strip())]=d3
                   my_list=sorted(cc.items(),key=lambda x:x[1],reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                       print "first  step ending time   is:"+step2
                       print "first  step used time is %s:" % tdelta
                   return match

                  elif  matchK or matchK1 or matchK2:
                    level2=clean_input_data(level2)
                    kk={}
                    level=level1+level2
                    for e in range(len(german)):
                          d2=float(Levenshtein.ratio(str(level),german[e][len(german[e])-1]))
                          kk[str(german[e][7].strip())]=d2
                    my_list=sorted(kk.items(),key=lambda x:x[1],reverse=True)[:5]
                    match=selection(my_list,avails_dic)
                    if logging_level>5:
                       print "returned value : % s" % match
                    step2=time.strftime("%x %X")

                    tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                    if logging_level>4:
                      print "first  step ending time   is:"+step2
                      print "first  step used time is %s:" % tdelta
                    return match

                 else:
                   match="NULL"+","+"0"
                   return match
      

           elif  WPR_ID not in episode_dic.keys() and WPR_ID not in feature_dic.keys() and WPR_ID not in season_dic.keys():
                 if level2!='UNK' and level3!='unk' and level1!='unk':
                  level=level1+level2+level3
                  ff={}
                  for j in range(len(episode)):
                    k1=float(Levenshtein.ratio(str(level),episode[j][len(episode[j])-2]))
                    ff[str(episode[j][7].strip())]=k1
                  my_list=sorted(ff.items(),key=lambda x:x[1],reverse=True)[:5]
                  match=selection(my_list,avails_dic)
                  if logging_level>5:
                       print "returned value : % s" % match
                  step2=time.strftime("%x %X")

                  tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                  if logging_level>4:
                     print "first  step ending time   is:"+step2
                     print "first  step used time is %s:" % tdelta
                  return match




                 if level2=='UNK' and level3=='unk' and level1!='unk':
                   ee={}
                   level=level1
                   for e in range(len(feature)):
                     d2=float(Levenshtein.ratio(str(level),feature[e][len(feature[e])-1]))
                     ee[str(feature[e][2].strip())]=d2
                   my_list=sorted(ee.items(),key=lambda x:x[1],reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                      print "first  step ending time   is:"+step2
                      print "first  step used time is %s:" % tdelta
                   return match


                 level2=getInput.level2
                 level2=level2.encode("utf-8","ignore")
                 level2=str(level2)
                 matchK=re.match(r'(.*)Episode ()',level2)
                 matchK1=re.match(r'(.*)Episode  ',level2)
                 matchK2=re.match(r'(.*)Episode \d',level2)
                 if level3=='unk' and level2!='UNK' and level1!='unk':
                  if not matchK and not matchK1 and not matchK2:
                   level2=clean_input_data(level2)
                   cc={}
                   level=level1+level2
                   for r in range(len(season)):
                     d3=float(Levenshtein.ratio(str(level),season[r][len(season[r])-1]))
                     cc[str(season[r][4].strip())]=d3
                   my_list=sorted(cc.items(),key=lambda x:x[1],reverse=True)[:5]
                   match=selection(my_list,avails_dic)
                   if logging_level>5:
                       print "returned value : % s" % match
                   step2=time.strftime("%x %X")

                   tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                   if logging_level>4:
                       print "first  step ending time   is:"+step2
                       print "first  step used time is %s:" % tdelta
                   return match
 
                  elif  matchK or matchK1 or matchK2:
                    level2=clean_input_data(level2)
                    kk={}
                    level=level1+level2
                    for e in range(len(german)):
                          d2=float(Levenshtein.ratio(str(level),german[e][len(german[e])-1]))
                          kk[str(german[e][7].strip())]=d2
                    my_list=sorted(kk.items(),key=lambda x:x[1],reverse=True)[:5]
                    match=selection(my_list,avails_dic)
                    if logging_level>5:
                       print "returned value : % s" % match
                    step2=time.strftime("%x %X")

                    tdelta = datetime.datetime.strptime(step2, FMT) - datetime.datetime.strptime(step1, FMT)
                    if logging_level>4:
                       print "first  step ending time   is:"+step2
                       print "first  step used time is %s:" % tdelta
                    return match
                 
                 else:
                      match="NULL"+","+"0"
                      return match    
      except Exception,e:
          if logging_level>1:
             logging.error(e)



          
if __name__ == "__main__":
         app1.run()
         
