from bs4 import BeautifulSoup
import requests
import arabic_reshaper
from bidi.algorithm import get_display
from urllib.parse import unquote
import subprocess
def arabic_fix(text): #reshapes arabic and fixes it
    try:
        return get_display(arabic_reshaper.reshape(text))
    except:
        return text

def arabic_url(text): #fixes links in arabic
    try:
        return arabic_fix(unquote(text).encode('latin1').decode('utf-8'))
    except:
        return text
    

def get_obj():#search for movie in site
    movie =(input("Enter The movie Title: "))
    url_search = f"https://ak.sv/search?q={movie}"
    return url_search

def get_movie():
    url_search = get_obj()
    response =  requests.get(url_search)
    soup = BeautifulSoup(response.text , 'html.parser')
    h3_main_tags =soup.find_all('h3' , class_='entry-title font-size-14 m-0') #search for h3 listing movies
    a_list_main= []
    for h3_main_tag in h3_main_tags:
        a_main_tags= h3_main_tag.find_all('a') #find all <a> values
        a_list_main.extend(a_main_tags) # add all <a> values in main search page to an array
        # for a_tag:
    # print(a_list_main)
    links = []
    titles = []
    for a_tag_main in a_list_main:
        links.append(a_tag_main['href']) #extract all movies links 
        titles.append(a_tag_main.text) #extract titles of movies
    movie_index = 1

    #print each movie title with an index to select which one
    print("Titles available:")
    for title in titles:
        print(f"[{movie_index}]{arabic_fix(title)}")
        movie_index +=1
    choice = int(input("Enter Your choice (e.g: 3): "))-1

    return links[choice]

def get_episode_link_site(link , num ,i , saved_quality , start):
    response =  requests.get(link)
    soup = BeautifulSoup(response.text , 'html.parser')
    qualities= []
    qualities_links= []
    tab_content_1080p =soup.find('div' , class_='tab-content quality' , id="tab-5") #search for div containing 1080p quality tab
    if tab_content_1080p:
        qualities.append('1080p')
        links_1080p = (tab_content_1080p.find_all('a'))
        for link in links_1080p:
            # print(f"linka {link['href']}")
            if 'link' in link['href'] and 'watch' not in link['href']:
                qualities_links.append(link['href'])
    
    tab_content_720p =soup.find('div' , class_='tab-content quality' , id="tab-4") #search for div containing 720p quality tab
    if tab_content_720p:
        qualities.append('720p')
        links_720p = (tab_content_720p.find_all('a'))
        for link in links_720p:
            # print(f"linka {link['href']}")
            if 'link' in link['href'] and 'watch' not in link['href']:
                qualities_links.append(link['href'])

# def get_episode_link_site(link , num ,i , saved_quality , start):
#     response =  requests.get(link)
#     soup = BeautifulSoup(response.text , 'html.parser')
#     qualities_dict = {}

#     tab_content_720p =soup.find('div' , class_='tab-content quality' , id="tab-4") #search for div containing 720p quality tab
#     if tab_content_720p:
#         links = [

#         ]
#         qualities.append('720p')
#         links_720p = (tab_content_720p.find_all('a'))
#         for link in links_720p:
#             # print(f"linka {link['href']}")
#             if 'link' in link['href'] and 'watch' not in link['href']:
#                 qualities_links.append(link['href'])
                

        # qualities_links.append(tab_content_720p.find('a')['href'])
        
    tab_content_480p =soup.find('div' , class_='tab-content quality' , id="tab-3") #search for div containing 480p quality tab
    if tab_content_480p:
        qualities.append('480p')
        links_480p = (tab_content_480p.find_all('a'))
        for link in links_480p:
            if 'watch' in link['href']:
                continue
            elif 'link' in link['href']:
                qualities_links.append(link['href'])
                break
            
        
    quality_choice = 1
    if (num == 'ranged' and i == start) or (num == 'one'):
        print("available qualities: ")
        for quality in qualities:
            print(f"[{(quality_choice)}]{quality}")
            quality_choice +=1
        
        quality_choice -=1    
        specified_quality = int((input("Enter The quality you want (e.g: 2): ")))-1
        # print(f"i is {i} and start is {start}")
    elif num == 'ranged' and i != start :
        # print(f"i is {i} and start is {start}")
        specified_quality = saved_quality
    return qualities_links[specified_quality] , specified_quality


def get_semi_final_download_link(link):
    response =  requests.get(link)
    soup = BeautifulSoup(response.text , 'html.parser')
    semi_final_link_a =soup.find('a' , class_='download-link') 
    if semi_final_link_a:
        semi_final_link = semi_final_link_a['href']
        # print(f"Semi_final link is:{semi_final_link}")
        return semi_final_link

def get_final_download_link(link):
    response =  requests.get(link)
    soup = BeautifulSoup(response.text , 'html.parser')
    final_link_a =soup.find('a' , class_='link btn btn-light')
    if final_link_a:
        final_link = final_link_a['href']
        # print(f"final link is:{final_link}")
        return final_link


def download_fdm(link):
    fdm_location = r"C:\Program Files\Softdeluxe\Free Download Manager\fdm.exe"
    cmd = f'"{fdm_location}" "{link}"'
    # print(f"The command is: {cmd}")
    subprocess.run(cmd)

def download_adm(link):
    fdm_location = r"C:\Program Files\Ant Download Manager (x64)\AntDM.exe"
    cmd = f'"{fdm_location}" "{link}"'
    # print(f"The command is: {cmd}")
    subprocess.run(cmd)
