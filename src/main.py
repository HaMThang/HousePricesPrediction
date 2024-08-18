import time
import random as rd
import Module01
import pandas as pd

#Khởi tạo biến
home="https://alonhadat.com.vn"
#base_url = "/nha-dat/can-ban/biet-thu-nha-lien-ke/trang--{}.html"
base_url="/can-ban-nha-quang-ninh-t49/trang-{}.htm"
list_page=[]

# Tạo các trang từ 1 đến 20
for page_number in range(1, 4):
    url = base_url.format(page_number)
    list_page.append(home + url)

list_webs = []
list_web = []
for page in list_page:
    links = Module01.get_titles_with_links1(page, list_webs)
    list_webs.extend(links)
print(f"Crawling of {len(list_webs)} webs")

print("Lọc trùng lặp................Start")
for link in list_webs:
    if link not in list_web:
        list_web.append(link)
ii=0
property_info_list = []
for url in list_web:
    ii+=1
    print(f"{ii}/{len(list_web)}")
    property_info = Module01.extract_property_info(url)
    if property_info is not None:
       property_info_list.append(property_info)
    time.sleep(rd.randint(1,4))
#Create a DataFrame from the extracted information

df = pd.DataFrame(property_info_list)
#df.to_csv("dataBT10.csv",sep=';')
#df_old=pd.read_csv('data_tonghop.csv',sep=';')
#df_c=pd.concat([df, df_old],ignore_index=True)
print(df)
#df_c.to_csv('data_tonghop.csv',sep=';',index=False)