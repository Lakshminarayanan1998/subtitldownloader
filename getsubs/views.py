
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import MovieForm
from .models import StoreData
from bs4 import BeautifulSoup
import requests
import simplejson as json
store=StoreData()
def index(request):
    form=MovieForm()
    if request.method=="POST":
        form=MovieForm(request.POST)
        if form.is_valid():
            link_list=[]
            final_download_link=[]
            final_mov_title=[]
            moviename=request.POST.get('movie_name','')
            length = len(moviename.split(" "))
            url = "https://subscene.com/subtitles/title?q="
            if(length==1):
                url=url+moviename+"&l="
            else:
                movie_bits=moviename.split(" ")
                moviename='+'.join(movie_bits)
                url=url+moviename+"&l="


            print(url)
            page=requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            filter=soup.find('div',{"class":"search-result"})
            subtitle_count_class=filter.findAll("div",{"class":"subtle count"})
            # print(subtitle_count_class)
            max=0
            for find in subtitle_count_class:
                val=find.text
                val=val.strip()
                val=val.split(" ")
                val=int(val[0])
                if val>max:
                    max=val

            print(max)
            list_items=filter.findAll("li",{"class":""})
            # print(list_items)
            for items in list_items:
                check=items.find("",{"class":"subtle count"})
                check=(check.text).strip()
                check=check.split(" ")
                check=int(check[0])
                if check==max:
                    target_tag=items.find('a',href=True)
                    target_link=target_tag['href']
                    print(target_link)
                    break



            url="https://subscene.com"
            url=url+target_link+"/english"
            print(url)

            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            filter=soup.body.table

            process=soup.body.table

            for a in process.findAll('a', href=True):
                length=len(a['href'])
                if(length>10):
                    link_list.append(a['href'])
            count=0
            for link in link_list:
                url="https://subscene.com"+link
                page = requests.get(url)
                soup = BeautifulSoup(page.text, "html.parser")
                download_link=soup.find("div",{"class": "download"})
                download_link=download_link.a['href']
                final_download_link.append("https://subscene.com"+download_link)
                count=count+1;
                if(count==20):
                    break
            for link in final_download_link:
                print(link)

            movie_title=filter.findAll("td", {"class": "a1"})
            movie_title=filter.findAll("span", {"class":""})

            count=0
            for link in movie_title:
                link=link.text.strip()
                final_mov_title.append(link)
                print(link)
                count=count+1;
                if(count==20):
                    break
        store.movie_title = json.dumps(final_mov_title)
        store.movie_link = json.dumps(final_download_link)
        store.save()


        return HttpResponseRedirect('/download')

    return render(request,'getsubs/index.html',{'form':form})

def download(request):
    jsonDec = json.decoder.JSONDecoder()
    movie_title = jsonDec.decode(store.movie_title)
    movie_link= jsonDec.decode(store.movie_link)
    finallist = zip(movie_title,movie_link)

    return render(request,'getsubs/display.html',{"movie_info":finallist})
