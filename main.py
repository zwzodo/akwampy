from bs4 import BeautifulSoup
import requests
from lib import get_movie , arabic_fix , get_episode_link_site , get_semi_final_download_link , get_final_download_link , download_fdm , download_adm

print(r"""
        _                                         
       | |                                        
   __ _| | ____      ____ _ _ __ ___  _ __  _   _ 
  / _` | |/ /\ \ /\ / / _` | '_ ` _ \| '_ \| | | |
 | (_| |   <  \ V  V / (_| | | | | | | |_) | |_| |
  \__,_|_|\_\  \_/\_/ \__,_|_| |_| |_| .__/ \__, |
                                     | |     __/ |
                                     |_|    |___/ 
 """)

movie_url = get_movie()

download_links = []
response =  requests.get(movie_url)
soup = BeautifulSoup(response.text , 'html.parser')

if '/movie/' in movie_url:
     link ,saved_quality = get_episode_link_site(movie_url , 'one' , 0 , 0 , 0)
     download_links.append(link)

else:
    #extract episodes names
    h2_tags = soup.find_all('h2' , class_='font-size-18 text-white mb-2')
    a_list_movie = []

    for h2_tag in h2_tags:
        a_movie_tag = h2_tag.find_all('a')

        a_list_movie.extend(a_movie_tag)

    # for thing in a_list_movie:
    episodes_links = []
    episodes_titles = []
    for ep in a_list_movie:
        title_raw  = ep.text
        try:
             fixed_title = title_raw.encode('latin1').decode('utf-8')
        except:
             fixed_title = title_raw


        episodes_links.append(ep['href'])
        episodes_titles.append(fixed_title)
    episode_index = 1
    print("Episodes:")
    for episode_title in episodes_titles:
        print(f"[{episode_index}]{arabic_fix(episode_title)}")
        episode_index +=1
    ep_choice = (input("Enter Your choice (e.g: 3): "))

    if '-' in ep_choice and '-' not in ep_choice[0]:
        ep_choice = ep_choice.replace(" " , "")
        start , end = map(int , ep_choice.split('-'))
        start -=1
        # end -=1
        # print(f"{start} - {end}")
        for i in range(start , end):
            # print(episodes_links[i])
            if i == start: 
                    link ,saved_quality = get_episode_link_site(episodes_links[i] , 'ranged' , i , '' , start)
                    download_links.append(link)

            else:
                download_links.append(get_episode_link_site(episodes_links[i] , 'ranged' , i , saved_quality , start)[0])



    elif (ep_choice).isdigit() == True and not ep_choice == -1:
        download_links.append(get_episode_link_site(episodes_links[int(ep_choice)-1 ] , 'one' , 0 , 0 , 1 )[0])
        


    elif ep_choice == "-1":
            for i in range(0 , len(episodes_links)):
                # print(episodes_links[i])
                if i == 0: 
                    link ,saved_quality = get_episode_link_site(episodes_links[i] , 'ranged' , i , 0 , 0)
                    download_links.append(link)

                else:
                    download_links.append(get_episode_link_site(episodes_links[i] , 'ranged' , i , saved_quality , 0)[0])


final_links = []
for link in download_links:
    semi_final_link = get_semi_final_download_link(link)
    if semi_final_link:
        final_links.append(get_final_download_link(semi_final_link))
    else:
        print("Couldn't find semi-final link")
methods = ["FDM" , "ADM"]
for index , method in enumerate(methods , start=1):
    print(f"[{index}]{method}")
choice = int(input("Enter The method you want:"))-1
# print(f"links are {final_links}")
for link in final_links:
     if methods[choice] == "FDM":
          download_fdm(link)
     elif methods[choice] == "ADM":
          download_adm(link)
          
     






    # print(f"now: {arabic_fix(unquote(thing['href']).encode('latin1').decode('utf-8'))}") #gooooooood







# for film in films:
#     print(film)
# print(soup.prettify())