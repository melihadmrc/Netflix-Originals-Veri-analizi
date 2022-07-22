import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn
from datetime import datetime


document=pd.read_csv("NetflixOriginals.csv", encoding="ISO-8859-1")
print(document.head(5))

#uzun soluklu filmlerin süresini belirlemek için ortalama runtime elde edilir, ortlamanın üstü uzun soluklu film kabul edilir.
ort=document.Runtime.mean()
print(ort)

#ortalamanın üstü değerler yeni bir değişkene aktarılır.
doc_high_run=document[document["Runtime"] > ort]

#diller sadeleştirilir
doc_diller=doc_high_run["Language"].unique()

sbn.set_theme(style="whitegrid")
sbn.set(rc={"figure.figsize": (40,40)})
sbn.barplot(y=doc_diller, x=document["Runtime"] [:len(doc_diller)])
#plt.show()

#2019 Ocak ile 2020 Haziran tarihleri arasında 'Documentary' türünde çekilmiş filmlerin IMDB değerlerini bulup görselleştiriniz.
#veri türlerini elde ederiz
print(document.dtypes)

#premiere kolonunda tarihler belirtilmektedir to_datetime yardımıyla veriyi işlenebilir hale getiririz.
document["Premiere"]=pd.to_datetime(document["Premiere"])
document.sort_values(by="Premiere", inplace=True)

doc_tarih=document[(document["Premiere"] > datetime(2019,1,1)) & (document["Premiere"] < datetime(2020,6,1))]

#2019 2020 tarihleri arasında documentary türündeki filmmleri çekmek için genre de documentary türünde olanları aldık.
doc_newtarih=doc_tarih[doc_tarih["Genre"]== "Documentary"]["IMDB Score"]

#documentary türündeki filmler gösterilmiştir.
sbn.histplot(doc_newtarih)
#plt.show()

#ingilizce çekilen filmler arasında hangi tür en yüksek IMDB puanına sahip
#inglizce olan dilleri değişkene atadık.
doc_english=document.loc[(document["Language"]== "English")]
#IMDB skorunu sıralayarak en yüksek hangisinin olduğu bulundu
doc_english=doc_english.sort_values(by="IMDB Score", ascending= False) [0:5]
print(doc_english)

#Hindi' Dilinde çekilmiş olan filmlerin ortalama 'runtime' suresi nedir?
doc_hindi=document.loc[(document["Language"]=="Hindi")]
hindi_ort=doc_hindi.Runtime.mean()
print("hint filmlerinin runtime ortalaması: ", hindi_ort)

#'Genre' Sütunu kaç kategoriye sahiptir ve bu kategoriler nelerdir? Görselleştirerek ifade ediniz.
doc_genre=document["Genre"].unique()
print("genre kategorileri: ", doc_genre," "," genrenin kategori sayısı: ", len(doc_genre))
doc_genre2=document["Genre"].value_counts()
sbn.barplot(x=doc_genre, y=doc_genre2 [:len(doc_genre)])
plt.show()


#Veri setinde bulunan filmlerde en çok kullanılan 3 dili bulunuz.
three_language=document["Language"].value_counts().head(3)
print(three_language)

#IMDB puanı en yüksek olan ilk 10 film hangileridir?
doc_IMDB=document.sort_values(by="IMDB Score", ascending=False).head(10)
print(doc_IMDB)

#IMDB puanı ile 'Runtime' arasında nasıl bir korelasyon vardır? İnceleyip görselleştiriniz.
plt.figure(figsize=(16,10))
sbn.heatmap(document[["IMDB Score", "Runtime"]].corr(), annot=True, linewidths=0.5)
plt.title('Correlation')
#plt.show()
print("Runtime ile IMDB Score arasında yüksek bir korelasyon yoktur.")

#IMDB Puanı en yüksek olan ilk 10 'Genre' hangileridir? Görselleştiriniz.
doc_IMDBGenre=document.groupby("Genre",as_index=False).agg({"IMDB Score":"max"}).sort_values(by="IMDB Score", ascending= False).head(10)
sbn.lineplot(x=doc_IMDBGenre["IMDB Score"], y=doc_IMDBGenre["Genre"])
#plt.show()

#'Runtime' değeri en yüksek olan ilk 10 film hangileridir? Görselleştiriniz.
doc_runtime=document.sort_values(by="Runtime", ascending=False).head(10)
sbn.barplot(x=doc_runtime["Runtime"][:10], y=doc_runtime["Title"][:10])
#plt.show()

#Hangi yılda en fazla film yayımlanmıştır? Görselleştiriniz.
doc_year=document.copy()
doc_year["Premiere"]=pd.DatetimeIndex(doc_year["Premiere"]).year
doc_yearfilm=doc_year.groupby("Premiere").agg({"Title": "size"}).sort_values(by="Title",ascending=False)
sbn.barplot(x=doc_yearfilm.index, y=doc_yearfilm["Title"])
plt.ylabel="FİLM SAYISI"
#plt.show()

#Hangi dilde yayımlanan filmler en düşük ortalama IMBD puanına sahiptir? Görselleştiriniz.
doc_dusukımdb=document.groupby("Language", as_index=False).agg({"IMDB Score":"mean"}).sort_values(by="IMDB Score",ascending=False).head(10)
sbn.barplot(y=doc_dusukımdb["Language"], x=doc_dusukımdb["IMDB Score"])
#plt.show()

#Hangi yılın toplam "runtime" süresi en fazladır?
doc_yuksekruntime=doc_year.groupby("Premiere",as_index=False).agg({"Runtime": "mean"}).sort_values(by="Runtime", ascending= False)
print(doc_yuksekruntime)

#Her bir dilin en fazla kullanıldığı "Genre" nedir?
doc_enfazlagenre=document.groupby("Language")["Genre"].value_counts().head(10)
print(doc_enfazlagenre)

#Veri setinde outlier veri var mıdır? Açıklayınız.
doc_IMDBoutlier=document["Runtime"]
sbn.boxplot(x=doc_IMDBoutlier)
#plt.show()

doc_Runtimeoutlier=document["Runtime"]
sbn.boxplot(x=doc_Runtimeoutlier)
#plt.show()

print("grafiğe bakıldığınında iki tane dikey çigiyle belirtilmiş alan bizim aykırı verilerimizdir.")

