import pandas as pd
import datetime as dt
pd.set_option('display.max_columns',None)
pd.set_option('display.float_format', lambda x: '%2f' %x)

df_ = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df.head()

df.shape
df.describe().T
df.isnull().sum()

df.dropna(inplace=True)
df.describe().T
df.shape


df["StockCode"].nunique()
df["StockCode"].value_counts()
df["StockCode"].value_counts()

df.groupby("StockCode").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()
df = df[~df["Invoice"].str.contains("C", na=False)]
df.describe().T
df.shape

df["TotalPrice"] = df["Price"] * df["Quantity"]
df.head()

today_date = dt.datetime(2011, 12, 11)

df.groupby("Customer ID").agg({"InvoiceDate" : lambda date : (today_date - date.max()).days,
                               "Invoice" : lambda num : num.nunique(),
                               "TotalPrice" : lambda TotalPrice : TotalPrice.sum()})

rfm = df.groupby("Customer ID").agg({"InvoiceDate" : lambda date : (today_date - date.max()).days,
                               "Invoice" : lambda num : num.nunique(),
                               "TotalPrice" : lambda TotalPrice : TotalPrice.sum()})

rfm.columns = ["recency", "frequency", "monetary"]
rfm = rfm[rfm["monetary"] > 0]

rfm['recency_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm['monetary_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)
rfm.head()

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean","count"])
rfm[rfm["segment"] == "loyal_customers"].head()

rfm[rfm["segment"] == "loyal_customers"].index

loyal_df = pd.DataFrame()
loyal_df["loyal_customer_id"] = rfm[rfm["segment"] == "loyal_customers"].index
loyal_df.head()

loyal_df.to_csv("loyal_customers.csv")

##############################################
            # Y O R U M L A M A
##############################################

# "Champions" segmentindeki m????terilerin frekans de??eri ortalamas?? en y??ksek de??er: 12.41.
# Bu frekans?? takip eden "cant loose" segmenti 8.38 ile 2. en y??ksek frekans de??erine sahip. Frekans de??eri
# evet y??ksek ama ortalama 132 g??nd??r ortal??kta yoklar ve 63 ki??iler buna y??nelik bir ??al????t??rma yapar m??yd??m bilemedim
# fakat ki??i say??s?? az oldu??undan her ne kadar monetary'si y??ksekte olsa ??ok ??nem vermemekle birlikte bi cross sel yapabilirdim almas??n?? sa??lamak amac??yla.

# "Champions" segmenti en prime m????terilerimiz. Her biri ??ok de??erli ve monetary de??eriyle de dikkatimizi hemen ??ekti.
# 819 ki??inin de olmas?? da 6857 birimlik para miktar??n?? h??zl??ca ve kolayca katlanabilece??ini g??steriyor.

# "About to sleep" segmenti dikkatimi ??ekti. 352 ki??iler frekanslar?? d??????k evet b??rakt??klar?? ??crette d??????k ama uyuyan y??lan uykudan uyand??r??labilir.
# Bu segmentteki k??smada cross-sell ve up-sell uygulamalar?? yap??larak her ??ey sat??lmaya ??al??????labilir.

# "CHAMPIONS"
# Bu segmentteki her m????teri bir maden adeta. O y??zden ??zel f??rsatlar, ??ark??felek, baloncuklar, mailler, sms'ler, cross-sell ve up-sell ile
# m????teriye her saniye her g??n kendimizi hat??rlatarak ??irketteki her ??r??n potansiyelli ??ekilde bu segmenttekilere pazarlanabilir.

# "LOYAL_CUSTOMERS"
# Ortalama 33 g??nde bir geliyorlar. Bu segmentteki m????terileri de de??erlendirip monetary de??eri artt??r??labilir h??zl?? bir ??ekilde.
# Size ??zel indirimler, 3 al 2 ??de gibi zarara u??ratmayacak kampanyalarla birlike pazarlama departman??ndaki ekibin b??y??k ??o??unlu??unu bu m????terilerle
# ilgilenmesini isterdim. "Champions" segmentine evrilmeye potansiyelli ????nk?? bu m????teriler.

# "POTENTIAL_LOYALISTS
# Bu m????teri segmenti de olduk??a de??erli. B??y??k potansiyel ta????yorlar. 484 ki??i olmalar?? da cezbedici. Frekanslar??
# artt??rmaya y??nelik ????yle bir uygulamaya gidilir: En az 500 birimlik al????veri?? yapt??????nda 1 ay ekstra taksit imkan?? ve ??imdi ald??????n ??r??nden ????kan
# %20'lik indirimi de bundan hemen sonraki al????veri??lerinde kullanma imk??n?? tarz?? bir uygulama olabilir.