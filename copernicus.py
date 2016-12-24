#!/usr/bin/python3
# coding: utf8
from argparse import ArgumentParser
from google import search
from google import get_random_user_agent
from bs4 import BeautifulSoup
from unidecode import unidecode
from functools import wraps
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
import errno
import imageGwall
import os
import sys
import signal
import urllib.request, urllib.parse, urllib.error
import random
import itertools
import datetime
import PyPDF2
import time
import json

#some vars

time = "New search at : " ,datetime.datetime.now()

lang = []

resultats = []

pdflink = []

variation1= []
variation2= []
variation3= []
variation4= []
variation5= []
variation6= []

ActualImages = []
family = ""
joinvar = []
allcomb = ""
finalres = []

finalink = []

finalinkchance =[]

specialres = []

specialreslink = []

splecialreslinkchance = []

searcharglist = []

pdfinal = []

pdfinalink = []

pdfinalinkchance =[]

allcombparsedfinal = []
allcombparsed = []
tmpchance = []

alllng = ['af','ar','hy','be','bg','ca','zh-CN','hr','cs','da','nl','en','et','tl','fi','fr','de','el','hi','hu','is','id','it','ja','ko','lv','lt','no','fa','pl','pt','ro','ru','sr','sk','sl','es','sv','th','tr','uk','vi']
#lng = ['en','zh-CN','es','ar','pt','ja','ru','fr','de']
#lng = ['en','fr','ru','es']
#lng = ['en','fr','es']
lng = []


#some def




class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator



def get_soup(url,header):
	

	
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

def fetchurl(language,searcharg,cityarg,addarg):

     global resultats

     for boka in language:
            print()
            print("===")
            print(("Fetching Result in : ",boka))
            print("===")
            print()


            if cityarg == "none":
                print("without cityarg")
                try:
                        for url in search(searcharg, lang=boka, pause=random.randint(30,60), num=100, stop=400, only_standard=False):

                                print(url)

                                if not url in resultats:
                                    resultats.append(url)
                                else:
                                     print("Already Saved !"),resultats
                                     pass
                except Exception as e:
                
                    print(("error : ",e))
                    pass
            if cityarg != "none":
                     print("with cityarg")
                     searchargcity = searcharg + " " + cityarg
                     try:

                             for url in search(searchargcity, lang=boka, pause=random.randint(30,60), num=100, stop=400, only_standard=False):

                                 print(url)

                                 if not url in resultats:

                                     resultats.append(url)
                                 else:
                                     print("Already Saved !")
                                     pass
                     except Exception as e:
                             print(("error : ",e))
                             pass



     print()
     print("===")
     print("Results found :")
     print("===")
     print()

     for item in resultats:

             print(item)



     try:
                                        filelog = open("./Data/Search.log","r")
                                        filelog.close()
     except:
                                        print("==")
                                        print("filelog does not exist Search.log")
                                        print("Creating filelog")
                                        print("==")
                                        filelog = open("./Data/Search.log","w")
                                        filelog.write("")
                                        filelog.close()


     filelog = open("./Data/Search.log","a")
     filelog.write("\n"+str(time)+"\n"+"For : "+str(searcharg)+"\nIn :"+str(cityarg)+"\nMay Contain :"+str(addarg)+"\n")

     for item in resultats:

             filelog.write("\n"+str(item))
     filelog.close










def catch(url):

     catch = ["watch?v",".pdf","dailymotion",".asp",".doc",".gz",".zip",".tar",".bz2",".rar",".7zip",".jsp",".ppt"]

     for ext in catch:
          if ext.lower() in url:
               return 1
def getimg(query,cityarg):

    global ActualImages

    if cityarg != "none":
           query = query+ " "+cityarg

    query = unidecode(query)
    image_type="osint"
    query= query.split()
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    print()
    print("Searching for pictures first : ")
    print(url)
    print()

    #add the directory for your image here
    DIR="./Data/Pictures/"

    fakeua = get_random_user_agent()
    #print(fakeua)
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    header2={'User-Agent':str(fakeua)}
    soup = get_soup(url,header)

    ActualImages=[]# contains the link for Large original images, type of  image
    #print(ActualImages)
    for a in soup.find_all("div",{"class":"rg_meta"}):
        #print(a)
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImages.append((link,Type))
    print()
    print("there are total" , len(ActualImages),"images")
    print()
    if not os.path.exists(DIR):
                os.mkdir(DIR)
                #print("pasglop")
    DIR = os.path.join(DIR, query.split()[0])

    if not os.path.exists(DIR):
            os.mkdir(DIR)

    print(DIR)

    ###print images
    for i , (img , Type) in enumerate( ActualImages):
        try:
            req = urllib.request.Request(img, headers={'User-Agent' : str(header2)})
            raw_img = urllib.request.urlopen(req).read()
            cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
            #print(cntr)
            if len(Type)==0:
                f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
            else :
                f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')

            f.write(raw_img)
            f.close()

        except Exception as e:
            pass
            #print()
            #print("could not load : "+img)
            #print(e)



   


    onlyfiles = [f for f in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, f))]

    for imgs in onlyfiles:

                try:
                    print(imageGwall.Image(str(DIR+"/"+imgs)))
                except Exception as e:
                    print(e)


def permutation(searcharg):

     global joinvar
     global searcharglist
     global allcomb
     global allcombparsed


     searcharglist = searcharg.lower()
     searchsave = searcharglist
     asclify = unidecode(searcharglist).split(" ")
     searcharglist = searcharglist.split(" ")

     if all(ord(char) < 128 for char in searchsave) == True:

         for i in range(0,len(searcharglist)):
             variation1.append(searcharglist[i])
             variation2.append(searcharglist[i].title())
             variation3.append(searcharglist[i].upper())

         joinvar = variation1+variation2+variation3

         print(joinvar)



         allcomb = list(itertools.permutations(joinvar, len(searcharglist)))

         print("==")
         print("loading all permutations")
         print("==")


         for item in allcomb:

             allcombparsed.append(str(item).replace(",","").replace("(","").replace("'","").replace(")",""))
             print((str(item).replace(",","").replace("(","").replace("'","").replace(")","")))

         for item in allcombparsed:

            print(item)

     #sys.exit()
     else:

         for i in range(0,len(searcharglist)):
             variation1.append(searcharglist[i])
             variation2.append(searcharglist[i].title())
             variation3.append(searcharglist[i].upper())
             variation4.append(asclify[i])
             variation5.append(asclify[i].title())
             variation6.append(asclify[i].upper())
         joinvar = variation1+variation2+variation3+variation4+variation5+variation6

         

         print(joinvar)



         allcomb = list(itertools.permutations(joinvar, len(searcharglist)))

         print("==")
         print("loading all permutations")
         print("==")


         for item in allcomb:

             allcombparsed.append(str(item).replace(",","").replace("(","").replace("'","").replace(")",""))
             #print((str(item).replace(",","").replace("(","").replace("'","").replace(")","")))

         for item in allcombparsed:

            print(item)
         



@timeout(121)
def lastchance(res,link,searcharg,addarg,cityarg):
     global tmpchance
     
     tmpchance = []
     min = []

     if type(res) == list:
          res = [chunk.lower() for chunk in res]
     if type(res) == str:
          res = res.lower()


     searcharg = searcharg.lower()
     addarg = addarg.lower()
     cityarg = cityarg.lower()

     for item in searcharg.split(' '):
          if len(item) > 2:
               min.append(item)


     if cityarg != "none":
          min.append(cityarg)






     if len(addarg.split(",")) > 0:
          

          if family != "none" and family.lower() in res:
               #print("Family Name detected",family)
               cnt = 0
               required = 0
               roundmin = int(round(len(min)/3))
               if roundmin < 1:
                    roundmin = 1
               good = len(min)+ roundmin

               for item in min:

                     if item.lower() in res:
                           required = required + 1
                           cnt = cnt + 1
#                           print("Found required word : ",item)
                           tmpchance.append(item)

               for item in addarg.split(","):

                     if item.lower() in res:

                           cnt = cnt + 1
#                           print("Found additional word : ",item)
                           tmpchance.append(item)

               

               if cnt >= good and required >= 1:

#                     if link not in finalink:

#                           if link not in pdflink:
                                        tmpchance = " ".join(tmpchance)
                                        return 1




@timeout(242)
def searchhtml(item,addarg,searcharg,cityarg):
     global finalres
     global finalink
     global specialres
     global pdflink


     if catch(item) != 1:

          try:

                     done = 0
                     fakeua = get_random_user_agent()
                     
                     
                     opener = urllib.request.build_opener()
                     opener.addheaders = [('User-Agent', fakeua)]           

                     html = opener.open(item)

                     soup = BeautifulSoup(html,'lxml')
     
                     titre = str(soup.title.string).replace("\n","")
                     result = soup.get_text()
                     print()
                     print()
                     print("############")
                     print(("Scanning  : ",item))
                     print("############")
                     print("title: ",titre)
                     print()
                     print()
                     for comb in allcombparsed:
                          splitemcase = []
                          Dbl = 0
                          splitem = comb.split(' ')
                          for case in splitem:
                                     splitemcase.append(case.lower())
     
                          for word in splitemcase:
                             if Dbl == 0:

                                  if splitemcase.count(word.lower()) > 1:
                                              Dbl = Dbl + 1



                          if Dbl == 0:
     
                                             if comb in result:
                                                     print()
                                                     print()
                                                     print()
                                                     print()
                                                     print("SUCH WOW !")
                                                     print()
                                                     print()
                                                     print(("FOUND : ", comb))
                                                     print()
                                                     print(("In : ", item))


                                                     pos = result.find(comb)
                                                     samplemin = pos - 70
                                                     samplemax = pos + 70

                                                     echantillon = result[samplemin:samplemax]
                                                     print()
                                                     echantillon = str(echantillon).replace("\n"," ")
                                                     print("Description : ",echantillon)
                                                     print()
                                                     finalres.append(item+" "+comb)
                                                     finalink.append(titre+"#***#"+item+"#***#"+echantillon)
                                                     done = 1
                                                     print()
                                                     print()
                                                     print()


     
                          else:
     
     
                                            pass

                     if lastchance(result,item,searcharg,addarg,cityarg) == 1 and addarg != "none":
                              
                              if done == 0:
                                                     print()
                                                     print()
                                                     print()
                                                     print()
                                                     print("May found Something interesting...")
                                                     print()
                                                     print("In : ", item)

                                                     print()
                                                     print("Contains :",tmpchance)


                                                     finalres.append(item+" "+"lastchance")
                                                     finalinkchance.append(titre+"#***#"+item+"#***#"+"Contains : "+tmpchance)
                                                     print()
                                                     print()
                                                     print()
                                                     print()
 


          except Exception as e:
                                     print()
                                     print()
                                     print(("Error : ",e))
                                     print()
                                     print()
                                     pass
     else:
     
                     print()
                     special = "\nFound special item : " + str(item)
                     print()
                     if ".pdf" in item:
     
                             pdflink.append(item)
                     else:
                             specialres.append(str(special))
                             specialreslink.append(str(item))



@timeout(242)
def searchpdf(pdf,addarg,searcharg,cityarg):
             global pdfinal

             print()
             print(("Searching in pdf file : ",pdf))
             print()

             try: 

                     done = 0
                     save = "./Data/Pdf/"+str(pdf.split("/")[-1])
                     urllib.request.urlretrieve (str(pdf), str(save))
                     Pdtxt = getPDFContent(save)

                     for comb in allcombparsed:

                          splitemcase = []
                          Dbl = 0
                          splitem = comb.split(' ')
                          for case in splitem:
                                     splitemcase.append(case.lower())

                          for word in splitemcase:
                             if Dbl == 0:

                                  if splitemcase.count(word.lower()) > 1:
                                             Dbl = Dbl + 1


                          if Dbl == 0:

                             if comb in Pdtxt:


                                     print()
                                     print()
                                     print()
                                     print("SUCH WOW !!!")
                                     print()
                                     print(("Found : ",str(comb)))
                                     print()
                                     print(("In : ", str(pdf)))


                                     pos = Pdtxt.find(comb)
                                     samplemin = pos - 70
                                     samplemax = pos + 70

                                     echantillon = Pdtxt[samplemin:samplemax]
                                     print()
                                     echantillon = str(echantillon).replace("\n"," ")
                                     print("Description : ",echantillon)
                                     print()

                                     pdfinal.append(str(pdf)+" "+"Confirmed")
                                     pdfinalink.append(str(pdf)+"#***#"+echantillon)
                                     done = 1
                                     print()
                                     print()
                                     print()


                    
                     if lastchance(Pdtxt,pdf,searcharg,addarg,cityarg) == 1 and addarg != "none":
                         if done == 0:

                                     print()
                                     print()
                                     print()
                                     print("May have found Something interesting...")
                                     print()
                                     print("In : ", str(pdf))
                                     print()
                                     print()
                                     print("Description",tmpchance)
                                     print()

                                     pdfres = "Confirmed Last Chance: ",str(pdf)
                                     pdfinal.append(str(pdfres))
                                     pdfinalinkchance.append(str(pdf)+"#***#"+"Contains : "+tmpchance)


             except Exception as e:
                     print(e)
                     pass







             try:
                                        filelog = open("./Data/Final.log","r")
                                        filelog.close()
             except:
                                        print("==")
                                        print("filelog does not exist Final.log)")
                                        print("Creating filelog")
                                        print("==")
                                        filelog = open("./Data/Final.log","w")
                                        filelog.write("")
                                        filelog.close()


             filelog = open("./Data/Final.log","a")
             filelog.write("\n"+str(time)+"\n"+"For : "+str(argsname)+"\n")

             for item in finalres:
                  filelog.write("\n"+str(item))

             for item in specialres:
                  filelog.write("\n"+str(item))

             for item in pdfinal:
                  filelog.write("\n"+str(item))

             filelog.close





def getPDFContent(path):
    content = ""
    pdf = PyPDF2.PdfFileReader(path, "rb")
    for i in range(0, pdf.getNumPages()):
        
        content += pdf.getPage(i).extractText() + "\n"
    content = " ".join(content.strip().split())
    return content





### Some code:


parser = ArgumentParser()


parser.add_argument("-l","--language", dest="lang",default='fr',
                    help="Country : en,zh-CN,es,ar,pt,ja,ru,fr,de...", metavar="'LANG'")

parser.add_argument("-s","--search", dest="name",default='Marcel Menou',
                    help="Name to Search", metavar="'NAME'")

parser.add_argument("-f","--family", dest="family",default='none',
                    help="Specify Family name if any (needed with -a)ex: -s Albert Einstein -f Einstein -a relativity,physics", metavar="FAMILY NAME")

parser.add_argument("-a","--add", dest="add",default='none',
                    help="Additional information to catch more results: \n--add Word1,Word2,Word3", metavar="OPTION")

parser.add_argument("-c","--city", dest="city",default='none',
                    help="Specify city", metavar="CITY")

args = parser.parse_args()

lang = args.lang

argsname = args.name

argscity = args.city

argsfamily = args.family

argsadd = args.add

family = argsfamily

#file = open("arg.txt","w")
#file.write("\n"+argsname+"\n"+argscity+"\n"+argsfamily+"\n"+argsadd)
#file.close

if lang != "none":

     tmpsplit = lang.split(",")
     for split in tmpsplit:
          if split in alllng:
               lng.append(split)
     if len(lng) == 0:
          lng = ['en','fr']
else:

     lng = ['en','fr']

print

if argsadd != "none" and family == "none":
     print()
     print("-f option is missing")
     print()
     print("To use additional information (-a) :")
     print()
     print("Specify Family name (-f) ex: -s Albert Einstein -f Einstein -a relativity,physics")
     print()
     print("")
     sys.exit()

if argsadd == "none" and family != "none":
     print()
     print("-a option is missing")
     print()
     print("The -f option must be used in combination with -a :")
     print()
     print("Specify Additional informations (-a) ex: -s Albert Einstein -f Einstein -a relativity,physics")
     print()
     print("")
     sys.exit()


print()
print()
print("Results Languages : ",lng)
print()

print("Searching for : ",args.name)
print()
print("Family Name : ",args.family)
print()
print("In city : ",args.city)
print()
print("Which may contain : ",args.add)
print()



getimg(argsname,argscity)

fetchurl(lng,argsname,argscity,argsadd)

permutation(argsname)


#searcharglist = searcharg.lower()
#searcharglist = searcharglist.split(" ")
print()
print()
print("================================")
print(("Searching each Url Content for :",args.name))
print("================================")
print()
print()


for link in resultats:

     try:
          searchhtml(link,argsadd,argsname,argscity)
     except Exception as e:
          print(e)
          pass

print()
print()
print("Searching in pdf files")
print()
print(("Pdf Nbr :",len(pdflink)))
print()
print()
print()


for links in pdflink:
     try:
          searchpdf(links,argsadd,argsname,argscity)
     except Exception as e:
          print(e)
          pass



#print()
#print("=the end=")
#print()




googlelink = finalink
googlelinkchance = finalinkchance
googlepdf = pdfinalink
googlepdfchance = pdfinalinkchance
googlespecial = specialreslink
googleimg = ActualImages

db = GraphDatabase("http://localhost:7474")
 

stitle = db.labels.create("Search Sample")  
s0 = db.nodes.create(name=argsname)
stitle.add(s0)


srcheng = db.labels.create("Search Engine")
s1 = db.nodes.create(name="Google")
srcheng.add(s1)
s2 = db.nodes.create(name="Bing")
srcheng.add(s2)

s0.relationships.create("Query", s1)
s0.relationships.create("Query", s2)


 
labelwebsite = db.labels.create("Website")
labelFile = db.labels.create("File")
labelspecial = db.labels.create("Special")
labelsiteverified = db.labels.create("Verified")
labelsitechance = db.labels.create("Interresting")
labelpdfverified = db.labels.create("Verified")
labelpdfchance = db.labels.create("Interresting")


GoogleurlPlus = db.nodes.create(name="url verified")
GoogleurlMinus = db.nodes.create(name="url interesting")

BingurlPlus = db.nodes.create(name="url verified")
BingurlMinus = db.nodes.create(name="url interesting")

s1.relationships.create("Link Website", GoogleurlPlus)
s1.relationships.create("Link Website", GoogleurlMinus)
s2.relationships.create("Link Website", BingurlPlus)
s2.relationships.create("Link Website", BingurlMinus)


GooglepdfPlus = db.nodes.create(name="pdf verified")
GooglepdfMinus = db.nodes.create(name="pdf interresting")

BingpdfPlus = db.nodes.create(name="pdf verified")
BingpdfMinus = db.nodes.create(name="pdf interresting")

s1.relationships.create("Link Pdf", GooglepdfPlus)
s1.relationships.create("Link Pdf", GooglepdfMinus)
s2.relationships.create("Link Pdf", BingpdfPlus)
s2.relationships.create("Link Pdf", BingpdfMinus)


Googleimgnode = db.nodes.create(name="Imgs")
Bingimgnode = db.nodes.create(name="Imgs")

s1.relationships.create("Image File", Googleimgnode)
s2.relationships.create("Image File", Bingimgnode)

Googlespecialnode = db.nodes.create(name="Link not parsed yet")

Bingspecialnode = db.nodes.create(name="Link not parsed yet")

s1.relationships.create("Not verified", Googlespecialnode)
s2.relationships.create("Not verified", Bingspecialnode)


labelwebsite.add(GoogleurlPlus, GoogleurlMinus, BingurlPlus, BingurlMinus)

labelFile.add(BingpdfPlus,BingpdfMinus,GooglepdfPlus, GooglepdfMinus,Bingimgnode,Googleimgnode)

labelspecial.add(Googlespecialnode,Bingspecialnode)

print()
print()
print("##############################################")
print("##############Writing Graph###################")
print("##############################################")

print()
print("Glink")
print()

for glink in googlelink:

  try:
    glink = glink.split("#***#")
    print(glink)
    item = db.nodes.create(Title=glink[0], Link=glink[1], Sample=glink[2])
    GoogleurlPlus.relationships.create("Verified Link",item)
    labelsiteverified.add(item)
    print(item)
    #s1.relationships.create("Source Url", item)
  except Exception as e:
          print(e)


print()
print("Glinkchance")
print()



for glink in googlelinkchance:

  try:
    glink = glink.split("#***#")
    print(glink)
    item = db.nodes.create(Title=glink[0], Link=glink[1], Sample=glink[2])
    GoogleurlMinus.relationships.create("Interesting Link",item)
    labelsitechance.add(item)
    print(item)
    #s1.relationships.create("Source Url", item)
  except Exception as e:

          print(e)

print()
print("pdf")
print()

for pdf in googlepdf:
  try:
    pdf = pdf.split("#***#")
    print(pdf)
    item = db.nodes.create(Title=pdf[1],Link=pdf[0], Sample=pdf[1])
    GooglepdfPlus.relationships.create("Verified Pdf",item)
    labelpdfverified.add(item)
    print(item)
    #s1.relationships.create("Source File", item)
  except Exception as e:
          print(e)

print()
print("pdfchance")
print()


for pdf in googlepdfchance:
  try:
    pdf = pdf.split("#***#")
    print(pdf)
    item = db.nodes.create(Title=pdf[1],Link=pdf[0], Sample=pdf[1])
    GooglepdfMinus.relationships.create("Interesting Pdf",item)
    labelpdfchance.add(item)
    print(item)
    #s1.relationships.create("Source File", item)
  except Exception as e:
     print(e)

for spec in googlespecial:
  try:
    item = db.nodes.create(name=spec)
    Googlespecialnode.relationships.create("Not handled",item)
    labelspecial.add(item)
    #s1.relationships.create("Source item", item)
  except Exception as e:
          print(e)

for fileimg in googleimg:

  try:
    item = db.nodes.create(name=fileimg)
    Googleimgnode.relationships.create("Interesting Picture",item)
    labelFile.add(item)
    #s1.relationships.create("Source File", item)
  except Exception as e:
          print(e)

