import streamlit as st
import numpy as np
import Ulity as ult
import sklearn

st.title('HOUSE PRICE PREDICTION APPLICATION')
vung = st.sidebar.selectbox('Select region',['Việt Nam','Hà Nội','TP Hồ Chí Minh'])
method = st.sidebar.radio('Select treatment option:',['Alternative 1','Alternative 2(Most Recommended)','Alternative 3','Alternative 4'])
#Chọn phương án xử lý:',['Phương án 1','Phương án 2','Phương án 3','Phương án 4']
if vung=='Hà Nội':model = st.sidebar.selectbox("Select regression model",['XGBoost Regression'])
elif vung=="TP Hồ Chí Minh":
    model = st.sidebar.selectbox("Select regression model",['RandomForest Regression'])
else:
    model = st.sidebar.selectbox("Select regression model",['Catboost Regression'])
button = st.sidebar.button('Prediction')

col1, col2, col3 = st.columns(3)
with col1:
    loaibds = st.selectbox('Type of real estate',['Nhà liền kề, biệt thự','Nhà mặt tiền','Nhà trong hẻm'])#Loại bất động sản'
    loaibds_value = ['Nhà liền kề, biệt thự', 'Nhà mặt tiền', 'Nhà trong hẻm'].index(loaibds)
with col2:
    huong = st.selectbox('The direction of the house',['Bắc','Nam','Tây','Tây Bắc','Tây Nam','Đông','Đông Bắc','Đông Nam'])
    huong_value = ['Bắc','Nam','Tây','Tây Bắc','Tây Nam','Đông','Đông Bắc','Đông Nam'].index(huong)
with col3:
    phaply = st.selectbox('Juridical',['Không','Có'])
    phaply_value=['Không','Có'].index(phaply)

#city=['Hà Nội','Thành phố Hồ Chí Minh','Đà Nẵng','Lâm Đồng','Hải Phòng','Khánh Hòa','Bắc Ninh','Đồng Nai','Cần Thơ','Bà Rịa – Vũng Tàu','Thừa Thiên Huế','Đắk Lắk','Bình Dương']
#[4,8,7,5,10,6,12,3,2,9,0,11,1]

diachi1, diachi2=st.columns(2)
diachi3,diachi4=st.columns(2)
with diachi1:
    if vung=='Việt Nam':
        tinhthanhpho = st.selectbox('Province/City', list(ult.city_districts.keys()))
        index_tinhthanhpho = list(ult.city_districts.keys()).index(tinhthanhpho)
        tinhthanhpho_value = [3,7,6,4,8,5,9,2,1,0][index_tinhthanhpho]
    elif vung == "Hà Nội":
        tinhthanhpho = st.selectbox('Province/City',['Hà Nội'])
        tinhthanhpho_value = 4
    else:
        tinhthanhpho = st.selectbox('Province/City', ['TP Hồ Chí Minh'])
        tinhthanhpho_value = 8

if tinhthanhpho in ult.city_districts:
    with diachi2:
        quanhuyen = st.selectbox('District', list(ult.city_districts[tinhthanhpho].keys()))

if quanhuyen in ult.city_districts[tinhthanhpho]:
    with diachi3:
        xaphuong = st.selectbox('Wards', ult.city_districts[tinhthanhpho][quanhuyen])
with diachi4:diachi = st.text_input('Street')

col4,col5 = st.columns(2)
with col4:
    matdodanso=ult.Find_Density(quanhuyen,tinhthanhpho)
    matdo=st.number_input('Population density(person/km2)',matdodanso,disabled=True)
with col5:
    gdp=ult.Find_GDPD(tinhthanhpho)
    grdp=st.number_input('GRPD(%)',gdp,disabled=True)
col6, col7, col8,col9 = st.columns(4)
with col6:
    dgtrcnha=st.number_input('Road in front of house(m)',step=1)
with col7:
    solau=st.number_input('Number of floors',step=1)
with col8:
    sophgngu=st.number_input('Number of bedroom',step=1)
with col9:
    dientich=st.number_input('Acreage/Area(m2)',step=1)

if button:
    st.snow()
    if dientich!=0 and solau !=0 :
        if method == 'Alternative 1':
            new_record = np.array(
                [dgtrcnha, loaibds_value, phaply_value, solau, sophgngu, dientich, tinhthanhpho_value, matdodanso, grdp])
            sample = new_record.reshape(-1, 9)
        else:
            new_record = np.array(
                [huong_value, dgtrcnha, loaibds_value, phaply_value, solau, sophgngu, dientich, tinhthanhpho_value,
                 matdodanso, grdp])
            sample = new_record.reshape(-1, 10)
        predict = ult.Prediction(sample, vung, method, model)
        ult.Show_answer(predict,loaibds_value)
    else:st.warning('You must type into Area and Number of floor!')
