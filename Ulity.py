import pandas as pd
import numpy as np
import joblib
import sklearn
import catboost
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import streamlit as st
import os
from joblib import load
Den=pd.read_csv('Density.csv',header=0)
Gdpd=pd.read_csv('gdpd.csv',header=0)
scaler1 = joblib.load('Model/scaler1.pkl')
scaler2 = joblib.load('Model/scaler2.pkl')



directory = 'Model'
#for filename in os.listdir(directory):
#    if filename.endswith('.pkl'):
#        model = load(os.path.join(directory, filename))
#        model_name = os.path.splitext(filename)[0]
def Find_Density(quanhuyen, tinhthanhpho):
    if tinhthanhpho=='TP Hồ Chí Minh': tinhthanhpho='Thành phố Hồ Chí Minh'

    temp = Den[(Den['Tên đơn vị hành chính'] == quanhuyen) & (Den['Tỉnh/Thành phố'] == tinhthanhpho)]
    if not temp.empty:
        value = temp['Mật độ dân số (người/km²)'].iloc[0]
        return value
    else:
        return None
def Find_GDPD(tinhthanhpho):
    if tinhthanhpho == 'TP Hồ Chí Minh': tinhthanhpho = 'Thành phố Hồ Chí Minh'
    temp = Gdpd[(Gdpd['Tên tỉnh / thành phố'] == tinhthanhpho)]
    value = temp['Tăng trưởng 2023']
    value=value.str.replace('%','').str.replace(',','.')
    value=float(value)
    return value


#Xử lý dataframe
train=pd.read_csv('Train_set_v1.csv')
test=pd.read_csv('Test_set_v1.csv')
df = pd.concat([train, test], axis=0)
df.reset_index(drop=True, inplace=True)
All_mean_0=df.loc[df['Loại BDS']==0]['Giá(Tỷ)'].mean()
All_mean_1=df.loc[df['Loại BDS']==1]['Giá(Tỷ)'].mean()
All_mean_2=df.loc[df['Loại BDS']==2]['Giá(Tỷ)'].mean()
HN_mean_0=df.loc[(df['Loại BDS']==0)&(df['Tỉnh/ Thành phố']==3)]['Giá(Tỷ)'].mean()
HN_mean_1=df.loc[(df['Loại BDS']==1) &(df['Tỉnh/ Thành phố']==3)]['Giá(Tỷ)'].mean()
HN_mean_2=df.loc[(df['Loại BDS']==2) & (df['Tỉnh/ Thành phố']==3)]['Giá(Tỷ)'].mean()
SG_mean_0=df.loc[(df['Loại BDS']==0)&(df['Tỉnh/ Thành phố']==7)]['Giá(Tỷ)'].mean()
SG_mean_1=df.loc[(df['Loại BDS']==1)&(df['Tỉnh/ Thành phố']==7)]['Giá(Tỷ)'].mean()
SG_mean_2=df.loc[(df['Loại BDS']==2)&(df['Tỉnh/ Thành phố']==7)]['Giá(Tỷ)'].mean()

def Prediction(sample,vung, method, model_n):
    def Select_model_name(vung, method, model_n):
        if vung == 'Việt Nam':
            v = 'all'
        elif vung == 'Hà Nội':
            v = 'hn'
        else:
            v = 'sg'
        me = ''.join([char for char in method if char.isnumeric()])
        words = model_n.split()
        mo = words[0].lower()
        model_name = mo + "_" + v + '_' + me
        return model_name
    model_name = Select_model_name(vung, method, model_n)
    if method=='Alternative 1':X_new = scaler1.transform(sample)
    else: X_new=scaler2.transform(sample)
    model_path = os.path.join(directory, f"{model_name}.pkl")
    if os.path.exists(model_path):
        model = load(model_path)
        y_new = model.predict(X_new)
        return y_new
    else:
        raise FileNotFoundError(f"Model '{model_name}' not in '{directory}'.")
    return y_predict
def Compare_kq(pred,mean,vung):
    # So sánh giá dự đoán với giá trung bình toàn quốc
    price_diff = np.round(abs(pred - mean), 3)
    if pred >= mean:
        compare_text = 'higher than'
    elif pred < mean:
        compare_text = 'lower than'
    st.sidebar.write(f"+ {compare_text} average price {vung} is: ", str(price_diff), " (B)")
def Show_answer(pred,loaibds_value):
    st.sidebar.text('Prediction price is: '+str(pred)+' (B)')
    if loaibds_value ==0:
        Compare_kq(pred, All_mean_0,'Vietnam')
        Compare_kq(pred, HN_mean_0,'Hanoi')
        Compare_kq(pred, SG_mean_0,'Ho Chi Minh city')
    if loaibds_value ==1:
        Compare_kq(pred, All_mean_1,'Vietnam')
        Compare_kq(pred, HN_mean_1,'Hanoi')
        Compare_kq(pred, SG_mean_1,'Ho Chi Minh city')
    if loaibds_value ==2:
        Compare_kq(pred, All_mean_2,'Vietnam')
        Compare_kq(pred, HN_mean_2,'Hanoi')
        Compare_kq(pred, SG_mean_2,'Ho Chi Minh city')

city_districts = {
    'Hà Nội': {
        'Hà Đông': ['Phúc La', 'La Khê', 'Yên Nghĩa', 'Văn Quán', 'Vạn Phúc', 'Đồng Mai', 'Biên Giang', 'Phú Lãm', 'Phú Lương', 'Lê Lợi', 'Lê Trọng Tấn', 'Hòa Bình', 'Yết Kiêu', 'Quang Trung', 'Văn Khê', 'Vạn Yên'],
        'Hai Bà Trưng': ['Bách Khoa', 'Thành Công', 'Đống Mác', 'Đồng Tâm', 'Vĩnh Tuy', 'Bạch Đằng', 'Thanh Lương', 'Thanh Nhàn', 'Cầu Dền', 'Bạch Mai', 'Lê Đại Hành', 'Đồng Nhân', 'Phạm Đình Hổ', 'Nguyễn Du'],
        'Cầu Giấy': ['Nghĩa Tân', 'Nghĩa Đô', 'Quan Hoa', 'Dịch Vọng', 'Dịch Vọng Hậu', 'Yên Hòa', 'Trung Hoà', 'Nghĩa Phát', 'Mai Dịch', 'Trung Yên'],
        'Hoàn Kiếm': ['Phan Chu Trinh', 'Hàng Bông', 'Tràng Tiền', 'Trần Hưng Đạo', 'Phúc Tân', 'Hàng Bài', 'Cửa Đông', 'Lý Thái Tổ', 'Hàng Trống', 'Trần Quốc Toản', 'Tràng Thi', 'Hàng Đào'],
        'Hoàng Mai': ['Vĩnh Hưng', 'Yên Sở', 'Trường Lâm', 'Tân Mai', 'Thanh Trì', 'Phương Liệt', 'Định Công', 'Mai Động', 'Hồng Hà', 'Giáp Bát', 'Lĩnh Nam', 'Hoàng Văn Thụ', 'Hoàng Liệt', 'Tam Trinh', 'Thịnh Liệt'],
        'Đống Đa': ['Láng Hạ', 'Ô Chợ Dừa', 'Quang Trung', 'Trung Liệt', 'Phương Liên', 'Thổ Quan', 'Nam Đồng', 'Trung Tự', 'Quốc Tử Giám', 'Trung Phụng', 'Cát Linh', 'Văn Chương', 'Trung Vĩnh', 'Khâm Thiên'],
        'Ba Đình': ['Ngọc Hà', 'Điện Biên', 'Trúc Bạch', 'Vĩnh Phúc', 'Cống Vị', 'Liễu Giai', 'Ngọc Khánh', 'Kim Mã', 'Nguyễn Trung Trực', 'Quán Thánh', 'Thành Công', 'Trúc Bạch', 'Đội Cấn', 'Ngọc Khánh'],
        'Tây Hồ': ['Quảng An', 'Tứ Liên', 'Xuân La', 'Tây Hồ', 'Bưởi', 'Nhật Tân', 'Phú Thượng', 'Thụy Khuê', 'Yên Phụ'],
        'Nam Từ Liêm': ['Mễ Trì', 'Mỹ Đình 1', 'Mỹ Đình 2', 'Tây Mỗ', 'Trung Văn', 'Xuân Phương', 'Phú Đô', 'Cầu Diễn', 'Tây Tựu', 'Thanh Xuân Trung', 'Phương Canh'],
        'Long Biên': ['Gia Thụy', 'Ngọc Lâm', 'Phúc Đồng', 'Sài Đồng', 'Thạch Bàn', 'Thượng Thanh', 'Bồ Đề', 'Cự Khối', 'Đức Giang', 'Giang Biên'],
        'Thanh Trì': ['Lĩnh Nam', 'Ngũ Hiệp', 'Ngọc Hồi', 'Tả Thanh Oai', 'Tam Hiệp', 'Yên Mỹ', 'Vĩnh Quỳnh', 'Duyên Hà', 'Hữu Hòa', 'Vạn Phúc', 'Tả Thanh Oai'],
        'Thanh Xuân': ['Khương Trung', 'Khương Mai', 'Thanh Xuân Bắc', 'Thanh Xuân Trung', 'Thanh Xuân Nam', 'Nhân Chính', 'P Trung', 'Thượng Đình', 'Phương Liệt', 'Khương Đình', 'Hạ Đình', 'Kim Giang', 'Thịnh Liệt'],
        'Hoài Đức': ['Trạm Trôi', 'Đức Thượng', 'Đức Giang', 'Cát Quế', 'Kim Chung', 'Yên Sở', 'Vân Canh', 'Xuân Mai', 'Đông La', 'Phúc La'],
        'Đông Anh': ['Phú Cường', 'Đông Hội', 'Xuân Nộn', 'Thuỵ Lâm', 'Tiên Dương', 'Uy Nỗ', 'Vân Hà', 'Vĩnh Ngọc', 'Võng La', 'Xuân Canh'],
        'Bắc Từ Liêm': ['Thượng Cát', 'Liên Mạc', 'Đông Ngạc', 'Thụy Phương', 'Tây Tựu', 'Xuân Đỉnh', 'Minh Khai', 'Cổ Nhuế 1', 'Cổ Nhuế 2', 'Phú Đô', 'Phúc Diễn'],
        'Mê Linh': ['Mê Linh', 'Quang Minh', 'Thạch Đà', 'Tiền Phong', 'Tiền Phong', 'Tiền Phong', 'Tiền Phong', 'Tiền Phong', 'Tiền Phong'],
        'Thường Tín': ['Thường Tín', 'Ninh Sở', 'Nhị Khê', 'Duyên Thái', 'Khánh Hà', 'Văn Bình', 'Hiền Giang', 'Hòa Bình', 'Tân Minh', 'Tả Thanh Oai', 'Vạn Điểm'],
        'Gia Lâm': ['Trâu Quỳ', 'Yên Viên', 'Yên Thường', 'Yên Viên', 'Ninh Hiệp', 'Đình Xuyên', 'Cổ Bi', 'Văn Lâm', 'Việt Hưng', 'Đình Xuyên', 'Phù Đổng'],
        'Sóc Sơn': ['Bắc Sơn', 'Tân Minh', 'Mai Đình', 'Phù Linh', 'Hiền Ninh', 'Mỹ Hưng', 'Tân Uyên', 'Phú Cường', 'Tân Tiến', 'Quang Tiến', 'Đông Xuân'],
        'Thanh Oai': ['Thanh Oai', 'Cao Dương', 'Thanh Mai', 'Đông Xuân', 'Đông La', 'Thạch Thán', 'Duyên Hà', 'Kim An', 'Cát Quế', 'Bích Hòa', 'Xuân Dương'],
        'Đan Phượng': ['Phùng', 'Thọ An', 'Trung Châu', 'Hồng Hà', 'Liên Hà', 'Liên Hồng', 'Liên Trung', 'Phương Đình', 'Đan Phượng', 'Đồng Tháp', 'Song Phượng'],
        'Chương Mỹ': ['Chúc Sơn', 'Quốc Oai', 'Tiên Phương', 'Xuân Mai', 'Trung Hòa', 'Hoàng Diệu', 'Thượng Vực', 'Thạch Thán', 'Đồng Phú', 'Thanh Bình', 'Đồng Lạc', 'Minh Châu', 'Đồng Lạc'],
        'Thạch Thất': ['Liên Quan', 'Bình Yên', 'Bình Phú', 'Hữu Bằng', 'Kim Quan', 'Yên Bình', 'Dị Nậu', 'Cẩm Yên', 'Lại Thượng', 'Phùng Xá', 'Canh Nậu'],
        'Quốc Oai': ['Quốc Oai', 'Cấn Hữu', 'Hòa Thạch', 'Sài Sơn', 'Phú Cát', 'Nghĩa Hương', 'Ngọc Liệp', 'Thạch Thán', 'Yên Sơn', 'Đông Xuân', 'Phú Mãn'],
        'Ba Vì': ['Ba Vì', 'Ba Trại', 'Ba Cường', 'Thái Hòa', 'Đồng Thái', 'Tân Xã', 'Minh Châu', 'Cẩm Lĩnh', 'Sơn Đà', 'Phú Châu', 'Tản Hồng', 'Đông Quang', 'Cam Thượng', 'Tản Lĩnh', 'Vân Hòa']
    },
    'TP Hồ Chí Minh': {
        'Quận 1': ['Bến Nghé', 'Bến Thành', 'Cầu Kho', 'Cầu Ông Lãnh', 'Cô Giang', 'Đa Kao', 'Nguyễn Cư Trinh', 'Nguyễn Thái Bình', 'Phạm Ngũ Lão', 'Tân Định', 'Võ Thị Sáu', 'Võ Văn Kiệt'],
        'Quận 2': ['An Phú', 'Bình An', 'Bình Khánh', 'Bình Trưng Đông', 'Bình Trưng Tây', 'Cát Lái', 'Thạnh Mỹ Lợi', 'Thảo Điền', 'Thủ Thiêm'],
        'Quận 3': ['Bến Thành', 'Cô Giang', 'Cầu Ông Lãnh', 'Đa Kao', 'Nguyễn Thị Minh Khai', 'Nguyễn Đình Chiểu', 'Phạm Ngũ Lão', 'Võ Văn Tần', 'Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6', 'Ward 7', 'Ward 8', 'Ward 9', 'Ward 10', 'Ward 11', 'Ward 12', 'Ward 13', 'Ward 14'],
        'Quận 4': ['Bến Nghé', 'Bến Thành', 'Hiệp Tân', 'Phú Mỹ', 'Thạnh Mỹ Lợi', 'Thạnh Xuân', 'Tân Hương', 'Tân Kiểng', 'Vĩnh Hội'],
        'Quận 5': ['Bàu Sen', 'Bến Nghé', 'Chợ Lớn', 'Vĩnh Lộc', 'Vĩnh Nguyên', 'Vĩnh Hải'],
        'Quận 6': ['1', '10', '11', '12', '13', '14', '2', '3', '4', '5', '6', '7', '8', '9', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Cái Khế', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo A', 'Tân Tạo B', 'Tân Thới Hiệp'],
        'Quận 7': ['Bến Nghé', 'Phú Mỹ', 'Phú Mỹ Hưng', 'Phú Thuận', 'Tân Kiểng', 'Tân Phong', 'Tân Phú', 'Tân Quy', 'Tân Thuận Đông', 'Tân Thuận Tây', 'Bình Thuận', 'Phước Kiển', 'Phước Lợi', 'Phước Trung', 'Phước An'],
        'Quận 8': ['Bến Nghé', 'Hiệp Bình Chánh', 'Hiệp Bình Phước', 'Tân Thới Hiệp', 'Tân Thới Nhất', 'Tân Thới Trung', 'Vĩnh Lộc', 'Vĩnh Ông'],
        'Quận 9': ['Hiệp Phú', 'Long Bình', 'Long Phước', 'Long Thạnh Mỹ', 'Long Trường', 'Phú Hữu', 'Phước Long A', 'Phước Long B', 'Tân Phú', 'Tăng Nhơn Phú A', 'Tăng Nhơn Phú B', 'Trường Thạnh', 'Việt Kiểu'],
        'Quận 10': ['1', '10', '11', '12', '13', '14', '2', '3', '4', '5', '6', '7', '8', '9', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Cái Khế', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo A', 'Tân Tạo B', 'Tân Thới Hiệp'],
        'Quận 11': ['Bến Nghé', 'Hiệp Bình Chánh', 'Hiệp Bình Phước', 'Tân Thới Hiệp', 'Tân Thới Nhất', 'Tân Thới Trung', 'Vĩnh Lộc', 'Vĩnh Ông'],
        'Quận 12': ['Hiệp Thành', 'Tân Chánh Hiệp', 'Tân Hưng Thuận', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tân Thới Đông', 'Tân Thới Tây', 'Thạnh Lộc', 'Thạnh Xuân', 'Thái Thịnh', 'An Phú Đông', 'Đông Hưng Thuận', 'Tân Hưng Thuận'],
        'Bình Tân': ['An Lạc', 'An Lạc A', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo B', 'Tân Kỳ Tân Quý', 'Tân Qúy', 'Tân Sơn Nhì', 'Tân Thành', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tây Thạnh', 'Hòa Thạnh', 'Hòa Thạnh'],
        'Bình Thạnh': ['1', '10', '11', '12', '13', '14', '2', '3', '4', '5', '6', '7', '8', '9', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Cái Khế', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo A', 'Tân Tạo B', 'Tân Thới Hiệp'],
        'Gò Vấp': ['Hiệp Bình Chánh', 'Hiệp Bình Phước', 'Tân Thới Hiệp', 'Tân Thới Nhất', 'Tân Thới Trung', 'Vĩnh Lộc', 'Vĩnh Ông'],
        'Phú Nhuận': ['1', '10', '11', '12', '13', '14', '2', '3', '4', '5', '6', '7', '8', '9', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Cái Khế', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo A', 'Tân Tạo B', 'Tân Thới Hiệp'],
        'Tân Bình': ['Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo B', 'Tân Kỳ Tân Quý', 'Tân Qúy', 'Tân Sơn Nhì', 'Tân Thành', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tây Thạnh', 'Hòa Thạnh', 'Hòa Thạnh'],
        'Tân Phú': ['Hiệp Thành', 'Tân Chánh Hiệp', 'Tân Hưng Thuận', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tân Thới Đông', 'Tân Thới Tây', 'Thạnh Lộc', 'Thạnh Xuân', 'Thái Thịnh', 'An Phú Đông', 'Đông Hưng Thuận', 'Tân Hưng Thuận'],
        'Thủ Đức': ['An Lạc', 'An Lạc A', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo B', 'Tân Kỳ Tân Quý', 'Tân Qúy', 'Tân Sơn Nhì', 'Tân Thành', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tây Thạnh', 'Hòa Thạnh', 'Hòa Thạnh'],
        'Bình Chánh': ['An Lạc', 'An Lạc A', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo B', 'Tân Kỳ Tân Quý', 'Tân Qúy', 'Tân Sơn Nhì', 'Tân Thành', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tây Thạnh', 'Hòa Thạnh', 'Hòa Thạnh'],
        'Cần Giờ': ['An Lạc', 'An Lạc A', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo B', 'Tân Kỳ Tân Quý', 'Tân Qúy', 'Tân Sơn Nhì', 'Tân Thành', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tây Thạnh', 'Hòa Thạnh', 'Hòa Thạnh'],
        'Củ Chi': ['An Lạc', 'An Lạc A', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo B', 'Tân Kỳ Tân Quý', 'Tân Qúy', 'Tân Sơn Nhì', 'Tân Thành', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tây Thạnh', 'Hòa Thạnh', 'Hòa Thạnh'],
        'Hóc Môn': ['An Lạc', 'An Lạc A', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo B', 'Tân Kỳ Tân Quý', 'Tân Qúy', 'Tân Sơn Nhì', 'Tân Thành', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tây Thạnh', 'Hòa Thạnh', 'Hòa Thạnh'],
        'Nhà Bè': ['An Lạc', 'An Lạc A', 'Bình Hưng Hòa', 'Bình Hưng Hòa A', 'Bình Hưng Hòa B', 'Bình Trị Đông', 'Bình Trị Đông A', 'Bình Trị Đông B', 'Tân Tạo', 'Tân Tạo A', 'Tân Tạo B', 'Tân Kỳ Tân Quý', 'Tân Qúy', 'Tân Sơn Nhì', 'Tân Thành', 'Tân Thới Hiệp', 'Tân Thới Nhì', 'Tây Thạnh', 'Hòa Thạnh', 'Hòa Thạnh']
    },
    'Đà Nẵng': {
        'Hải Châu': ['Hải Châu 1', 'Hải Châu 2', 'Thạch Thang', 'Hòa Thuận Đông', 'Hòa Thuận Tây', 'Nam Dương', 'Bình Hiên', 'Hòa Cường Bắc', 'Hòa Cường Nam'],
        'Thanh Khê': ['Thanh Khê Đông', 'Thanh Khê Tây', 'Xuân Hà', 'Vĩnh Trung', 'Thạc Gián', 'An Khê', 'Nam Dương'],
        'Sơn Trà': ['An Hải Bắc', 'An Hải Đông', 'An Hải Tây', 'Mân Thái', 'Nại Hiên Đông', 'Phước Mỹ', 'Thọ Quang'],
        'Ngũ Hành Sơn': ['Mỹ An', 'Khuê Mỹ', 'Hoà Hải', 'Hòa Quý', 'Hòa Hải'],
        'Liên Chiểu': ['Hòa Hiệp Bắc', 'Hòa Hiệp Nam', 'Hòa Khánh Bắc', 'Hòa Khánh Nam', 'Hòa Minh'],
        'Cẩm Lệ': ['Hòa Thọ Đông', 'Hòa Thọ Tây', 'Hòa Xuân', 'Hòa Phát'],
        'Hòa Vang': ['Hòa Liên', 'Hòa Sơn', 'Hòa Ninh', 'Hòa Nhơn', 'Hòa Bắc', 'Hòa Phong', 'Hòa Châu']
    },
    'Lâm Đồng': {
        'Đà Lạt': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'Tà Nung', 'Xuân Trường'],
        'Bảo Lộc': ['Lộc Phát', 'Lộc Tiến', 'Lộc Sơn', 'Lộc Thanh'],
        'Đam Rông': ['Đạ Đờn', 'Ma Đa Guôi', 'Đạ Pal', 'Đạ Tồn'],
        'Đơn Dương': ["Đạ M'ri", 'Đạ Oai', 'Đạ Ploa', 'Đạ Tẻh'],
        'Đức Trọng': ['Đạ Tẻh', 'Đạ Lây', "Đạ K'Nàng", 'Đạ Pal'],
        'Lạc Dương': ['Lạc Dương', 'Lát', 'Đạ Sar', 'Đưng KNớ'],
        'Lâm Hà': ['Liên Đầm', 'Đạ Chais', 'Đạ Nhim', 'Đan Phượng']
    },
    'Hải Phòng': {
        'Hồng Bàng': ['Hạ Lý', 'Trần Nguyên Hãn', 'Quán Trữ', 'Hùng Vương', 'Cầu Đất', 'Phan Bội Châu'],
        'Ngô Quyền': ['Máy Chai', 'Lạc Viên', 'Cầu Tre', 'Lạch Tray', 'Đằng Giang', 'Đông Khê'],
        'Lê Chân': ['Dư Hàng Kênh', 'Đông Hải 1', 'Đông Hải 2', 'Lê Lợi', 'Minh Khai', 'Niệm Nghĩa'],
        'Hải An': ['Đằng Lâm', 'Đằng Hải', 'Nam Hải', 'Cát Dài', 'Tràng Cát', 'Vạn Hương'],
        'Kiến An': ['Cầu Rào 1', 'Cầu Rào 2', 'Lạc Long', 'Nam Sơn', 'Phù Liễn', 'Phạm Thái'],
        'Đồ Sơn': ['Bàng La', 'Minh Đức', 'Ngọc Xuyên', 'Vạn Sơn'],
        'Dương Kinh': ['Đông Sơn', 'Hải Thành', 'Hoà Nghĩa', 'Tân Thành'],
        'An Dương': ['An Đồng', 'An Hòa', 'An Hồng', 'An Cư', 'An Thượng'],
        'An Lão': ['An Lão', 'An Tiến', 'An Tràng', 'Bát Trang', 'Chi Lăng'],
        'Kiến Thuỵ': ['Đa Phúc', 'Đại Thắng', 'Đoàn Xá', 'Kiến Quốc', 'Quốc Tuấn']
    },
    'Khánh Hòa': {
        'Nha Trang': ['Văn Thạnh', 'Vĩnh Hải', 'Vĩnh Phước', 'Vĩnh Trường', 'Vĩnh Thái'],
        'Cam Ranh': ['Cam Hải Đông', 'Cam Hải Tây', 'Cam Hiệp Bắc', 'Cam Hiệp Nam', 'Cam Linh', 'Cam Lộc', 'Cam Phúc Bắc', 'Cam Phúc Nam', 'Cam Thành Bắc', 'Cam Thành Nam', 'Cam Tân'],
        'Ninh Hòa': ['Ninh Diêm', 'Ninh Đông', 'Ninh Hải', 'Ninh Sơn', 'Ninh Thủy', 'Ninh Tân', 'Ninh Thọ', 'Ninh Vân', 'Ninh Xuân'],
        'Diên Khánh': ['Diên An', 'Diên Điền', 'Diên Đồng', 'Diên Phú', 'Diên Sơn', 'Diên Thạnh', 'Diên Toàn', 'Diên Xuân'],
        'Khánh Vĩnh': ['Cầu Bà', 'Sông Cầu', 'Thành Sơn', 'Vĩnh Hòa', 'Vĩnh Lương', 'Vĩnh Phương', 'Vĩnh Trung'],
        'Trường Sa': ['Song Tử Đông', 'Song Tử Tây']
    },
    'Bắc Ninh': {
        'Bắc Ninh': ['Phong Khê', 'Vũ Ninh', 'Hạp Lĩnh', 'Khắc Niệm', 'Đại Phúc', 'Suối Hoa', 'Vệ An', 'Thị Cầu', 'Vân Dương', 'Hòa Long', 'Hương Mạc', 'Kim Chân', 'Kinh Bắc', 'Kim An', 'Thanh Khương', 'Đáp Cầu', 'Phong Khải', 'Khúc Xuyên', 'Hòa An', 'Vân Hội', 'Vân Tử', 'Phù Chẩn', 'Trung Dũng', 'Vĩnh Long', 'Tiền An'],
        'Từ Sơn': ['Đại Xuân', 'Trang Hạ', 'Đình Bảng', 'Đồng Kỵ', 'Phù Khê', 'Tam Sơn', 'Hoàng Đạo', 'Lãng Ngâm', 'Tân Hồng', 'Đại Phúc', 'Tân Lãng', 'Phú Lãm', 'Hoàn Sơn', 'Đại Mạch', 'Tiền Tiến', 'Hàm Rồng', 'Khả Phong', 'Châu Khê', 'Phú Xuân', 'Đồng Nguyên', 'Minh Đạo', 'Tương Giang', 'Ngũ Thái', 'Hòa Long', 'Bình Dương', 'Đông Hòa', 'Trung Kênh', 'Thanh Khương', 'Hương Mạc', 'Kim Chân', 'Kinh Bắc', 'Kim An', 'Thanh Khương', 'Đáp Cầu', 'Phong Khải', 'Khúc Xuyên', 'Hòa An', 'Vân Hội', 'Vân Tử', 'Phù Chẩn', 'Trung Dũng', 'Vĩnh Long', 'Tiền An'],
        'Quế Võ': ['Chờ', 'Ngọc Xá', 'Phố Mới', 'Việt Hùng', 'Phù Lãng', 'Trí Quả', 'Phù Lỗ', 'Ngọc Lâm', 'Châu Phong', 'Đại Đồng', 'Đại Hạnh', 'Đại Phong', 'Hồ', 'Phú Xuân', 'Tiền Tiến', 'Trung Mỹ', 'Việt Thống', 'Yên Lộc']
    },
    'Đồng Nai': {
        'Biên Hòa': ['Tân Biên', 'An Bình', 'Bửu Long', 'Bửu Hòa', 'Bửu Hòa 1', 'Bửu Hòa 2', 'Tam Hiệp', 'Tam Hòa', 'Tam Phước', 'Tam Bình', 'Long Bình', 'Trảng Dài', 'Trung Dũng', 'Tân Hạnh', 'Hố Nai 3', 'Quyết Thắng'],
        'Long Khánh': ['Xuân An', 'Bàu Sen', 'Bàu Trâm', 'Bàu Hàm', 'Xuân Lập', 'Xuân Thạnh', 'Xuân Tân', 'Phú Lý', 'Suối Tre', 'Bảo Quang', 'Phú Đức', 'Phú Sơn', 'Xuân Quế', 'Long An'],
        'Trảng Bom': ['Đồi 61', 'Hưng Thịnh', 'Hưng Lộc', 'Thanh Tuyền', 'Thanh Bình', 'Thanh Hòa', 'Cây Gáo', 'Giang Điền', 'Gia Kiệm', 'Gia Tân 1', 'Gia Tân 2', 'Gia Tân 3', 'Gia Tân 4', 'Sông Thao', 'Phước Thái', 'Xuân Thịnh'],
        'Thống Nhất': ['Thống Nhất', 'Đồng Nai', 'Đồng Khởi', 'Gia Đông', 'Quang Trung', 'Đồng Tâm', 'Bàu Hàm 1', 'Bàu Hàm 2', 'Sông Ray', 'Xuân Thiện', 'Xuân Phong', 'Xuân Thanh']
    },
    'Cần Thơ': {
        'Quận Ninh Kiều': ['Ninh Kiều'],
        'Quận Cái Răng': ['Cái Răng'],
        'Quận Bình Thủy': ['Bình Thủy'],
        'Quận Ô Môn': ['Ô Môn'],
        'Quận Thốt Nốt': ['Thốt Nốt'],
        'Huyện Vĩnh Thạnh': ['Vĩnh Thạnh', 'Tân Hòa', 'Thạnh An', 'Thạnh Lộc', 'Thạnh Lợi', 'Thạnh Mỹ', 'Thạnh Quới', 'Thạnh Thắng', 'Thạnh Tiến', 'Thạnh Trị', 'Thạnh Tân', 'Thạnh Xuân'],
        'Huyện Cờ Đỏ': ['Thới Lai', 'Trung An', 'Trung Hưng', 'Đông Hiệp', 'Đông Thắng', 'Thạnh Phú', 'Thới Đông', 'Thới Hòa', 'Thới Long', 'Thới Thạnh', 'Trường Thành', 'Định Môn']
    },
    'Bà Rịa – Vũng Tàu': {
        'Thành phố Vũng Tàu': ['Thắng Nhất', 'Thắng Nhì', 'Thắng Tam', 'Rạch Dừa', 'Nghĩa Thành', 'Phước Thắng', 'Lê Lợi', 'Vũng Tàu', 'Hưng Phước', 'Trần Phú', '5', '10', '11', '12', '13', '14', '15', '16'],
        'Thị xã Bà Rịa': ['Phước Hiệp', 'Long Toàn', 'Long Hương', 'Kim Dinh', 'Hoà Long', 'Long Tâm', 'An Ngãi', 'An Ngãi Trung', 'An Phước', 'Tân Hưng', 'Hòa Hội', 'Long Hữu', 'Phước Hưng', 'Phước Thái', 'Kim Long'],
        'Huyện Châu Đức': ['Xuân Sơn', 'Ngũ Lão', 'Bàu Chinh', 'Bình Ba', 'Bình Triều', 'Sông Xoài', 'Sơn Bình', 'Suối Nghệ', 'Suối Rao', 'Xà Bang', 'Bàu Lâm', 'Cù Bị', 'Đa Lộc', 'Kim Long', 'Láng Lớn', 'Phước Bình', 'Xuân Tân'],
        'Huyện Xuyên Mộc': ['Hòa Bình', 'Bàu Lâm', 'Bình Châu', 'Bông Trang', 'Hòa Hiệp', 'Hòa Hội', 'Phước Bưu', 'Phước Tân', 'Phước Thuận', 'Sơn Xuyên', 'Xuyên Mộc']
    }
}
