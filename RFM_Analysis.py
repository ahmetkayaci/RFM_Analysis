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

# "Champions" segmentindeki müşterilerin frekans değeri ortalaması en yüksek değer: 12.41.
# Bu frekansı takip eden "cant loose" segmenti 8.38 ile 2. en yüksek frekans değerine sahip. Frekans değeri
# evet yüksek ama ortalama 132 gündür ortalıkta yoklar ve 63 kişiler buna yönelik bir çalıştırma yapar mıydım bilemedim
# fakat kişi sayısı az olduğundan her ne kadar monetary'si yüksekte olsa çok önem vermemekle birlikte bi cross sel yapabilirdim almasını sağlamak amacıyla.

# "Champions" segmenti en prime müşterilerimiz. Her biri çok değerli ve monetary değeriyle de dikkatimizi hemen çekti.
# 819 kişinin de olması da 6857 birimlik para miktarını hızlıca ve kolayca katlanabileceğini gösteriyor.

# "About to sleep" segmenti dikkatimi çekti. 352 kişiler frekansları düşük evet bıraktıkları ücrette düşük ama uyuyan yılan uykudan uyandırılabilir.
# Bu segmentteki kısmada cross-sell ve up-sell uygulamaları yapılarak her şey satılmaya çalışılabilir.

# "CHAMPIONS"
# Bu segmentteki her müşteri bir maden adeta. O yüzden özel fırsatlar, çarkıfelek, baloncuklar, mailler, sms'ler, cross-sell ve up-sell ile
# müşteriye her saniye her gün kendimizi hatırlatarak şirketteki her ürün potansiyelli şekilde bu segmenttekilere pazarlanabilir.

# "LOYAL_CUSTOMERS"
# Ortalama 33 günde bir geliyorlar. Bu segmentteki müşterileri de değerlendirip monetary değeri arttırılabilir hızlı bir şekilde.
# Size özel indirimler, 3 al 2 öde gibi zarara uğratmayacak kampanyalarla birlike pazarlama departmanındaki ekibin büyük çoğunluğunu bu müşterilerle
# ilgilenmesini isterdim. "Champions" segmentine evrilmeye potansiyelli çünkü bu müşteriler.

# "POTENTIAL_LOYALISTS
# Bu müşteri segmenti de oldukça değerli. Büyük potansiyel taşıyorlar. 484 kişi olmaları da cezbedici. Frekansları
# arttırmaya yönelik şöyle bir uygulamaya gidilir: En az 500 birimlik alışveriş yaptığında 1 ay ekstra taksit imkanı ve şimdi aldığın üründen çıkan
# %20'lik indirimi de bundan hemen sonraki alışverişlerinde kullanma imkânı tarzı bir uygulama olabilir.