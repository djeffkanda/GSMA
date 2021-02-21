#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib as mpl 
import seaborn as sns
# sns.set()
sns.set(context='notebook', style='whitegrid', palette='deep', font='sans-serif', font_scale=1.3, color_codes=True, rc=None)
import matplotlib.pyplot as plt
import geopandas as gpd
import geoplot as gpl
import json
import mapclassify
import matplotlib.ticker as ticker
from datetime import timedelta

# get_ipython().run_line_magic('matplotlib', 'inline')


# ## Geo Data Processsing
# 
# Reading the initial zone shapefile and grouped zone (by FV)

# In[2]:


#Handle naming and grouping
gpdzs = gpd.read_file('../../data/GEO DRC/RDC_ZonesDeSante.shp')[['PROVINCE','Nom','geometry']]
gpdzsg = gpd.read_file('../../data/GEO DRC/RDC_Micro_ZonesDeSante_Regroupees.shp')[['PROVINCE','Zone+Peupl','geometry']]

gpdzsg = gpdzsg.rename({'Zone+Peupl':'Nom'}, axis=1)
# gpdzsg['Nom'] =  gpdzsg['Nom']+'_g'



# gpdzm = gpd.GeoDataFrame(pd.concat([gpdzs,gpdzsg], ignore_index=True), crs=gpdzsg.crs)


# In[3]:


gpdzsg


# ### Checking for data issues

# There are two zones with name `Lubunga`, but belonging to two provinces `Kasai-Central and Tshopo`

# In[4]:


gpdzsg[gpdzsg.Nom == 'Lubunga']


# In[5]:


# gpdzm.to_file('merged_zones', driver='ESRI Shapefile')


# In[6]:


# gpdzs_merged = gpd.read_file('data/merged_zones/merged_zones.shp')


# In[7]:


# gpdzs_merged


# In[8]:


# gpdzm


# ### Dictionnary of zones as grouped by FV

# In[9]:


#Grouped Zone de Sante (By FV)
groupedzs = {
    'Tshela':['Tshela','Kizu'],
    'Matadi':['Matadi', 'Nzanza'],
    'Mbanza-Ngungu':['Mbanza-Ngungu','Gombe-Matadi'],
    'Kisantu':['Kisantu','Nselo'],
    'Ngidinga':['Ngidinga','Kimvula'],
    'Maluku I': ['Maluku I','Maluku II'],
    'Kikimi':['Kikimi', 'Biyela'],
    'Kimbanseke':['Kimbanseke', 'Kingasani'],
    'Lemba':['Lemba','Ngaba'],
    'Kokolo': ['Kokolo','Bandalungwa'],
    'Police':['Police','Lingwala'],
    'Boko': ['Boko','Popokabaka','Kimbau'],
    'Kahemba':['Kahemba','Kajiji','Kisanji'],
    'Gungu':['Gungu','Mungindu','Kingandu'],
    'Idiofa':['Idiofa','Koshibanda','Mukedi'],
    'Mokala': ['Mokala','Kimputu','Ipamu'],
    'Kikwit-Sud':['Kikwit-Nord', 'Kikwit-Sud','Lusanga'],
    'Vanga':['Yasa-Bonga','Mosango','Pay Kongila','Masi-Manimba','Moanza','Vanga'],
    'Bolobo':['Bolobo','Kwamouth'],
    'Mushie':['Yumbi','Mushie','Banjow Moke'],
    'Bokoro':['Inongo','Penjwa','Kiri','Bokoro','Bosobe','Mimia','Oshwe'],
    'Kitangwa': ['Kitangwa', 'Nyanga'],
    'Kamonia':['Kamonia', 'Kanzala'],
    'Luebo': ['Luebo','Ndjoko-Mpunda'],
    'Ilebo': ['Dekese','Ilebo','Mushenge','Bulape','Kakenge'],
    'Bena Tshiadi': ['Bena Tshiadi','Muetshi','Katende'],
    'Kananga':['Kananga','Katoka','Lukonga','Bobozo','Tshikaji','Tshikula'],
    'Luambo' : ['Luambo','Kalomba','Tshibala'],
    'Manika' : ['Manika','Panda','Kilela Balanda'],
    'Likasi' : ['Kambove','Likasi'],
    'Kampemba':['Kampemba','Mumbunda','Kisanga',"Katuba",'Kenya'],
    'Lubumbashi':['Lubumbashi','Vangu','Kowe','Kamalondo'],
    'Rwashi': ['Rwashi','Kafubu'],
    'Kikula':['Kikula','Lukafu','Kasenga'],
    'Mufunga Sampwe': ['Mufunga Sampwe','Mitwaba'],
    'Kamina':['Kamina','Songa'],
    'Kabongo': ['Kayamba','Kabongo'],
    'Moba': ['Kiyambi','Kansimba','Moba'],
    'Kongolo': ['Kongolo','Mbulula'],
    'Ngandajika':['Ngandajika','Kalambayi Kabanga'],
    'Mwene Ditu': ['Mwene Ditu', 'Makota'],
    'Kalenda': ['Kalenda','Wikong'],
    'Diulu': ['Diulu','Mpokolo','Bipemba','Nzaba','Kansele','Lubilanji','Dibindi','Muya','Lukelenge','Tshitenge','Bonzola'],
    'Ototo': ['Ototo','Lusambo','Pania Mutombo'],
    'Omendjadi': ['Omendjadi', 'Tshudi Loto','Bena Dibele'],
    'Kunda': ['Kunda','Kibombo','Tunda'],
    'Kampene': ['Kampene','Pangi'],
    'Kindu' : ['Kindu','Alunguli'],
    'Punia': ['Punia','Ferekeni','Obokote'],
    'Shabunda': ['Shabunda','Lulingu','Mulungu'],
    'Fizi':['Fizi','Kimbi Lulenge'],
    'Mwenga': ['Mwenga','Mwana'],
    'Walungu': ['Walungu','Kaniola','Mubumbano'],
    'Nyangezi': ['Nyangezi', 'Kaziba','Nyantende'],
    'Ibanda': ['Bagira', 'Kadutu', 'Ibanda'],
    'Idjwi' : ['Idjwi','Miti-Murhesa'],
    'Minova': ['Minova','Kalehe',],
    'Bikoro': ['Bikoro','Lukolela','Irebu','Ntondo','Iboko','Ingende'],
    'Wangata': ['Wangata','Bolenge','Mbandaka'],
    'Bolomba': ['Bolomba','Lotumbe','Monieka','Basankusu','Djombo','Lolanga Mampoko','Makanza','Bomongo','Lilanga Bobangi'],
    'Boende': ['Djolu','Ikela','Bosanga','Yalifafo','Bokungu','Wema','Befale','Monkoto','Lingomo','Boende','Mompono'],
    'Basoko': ['Basoko', 'Basali','Yalimbongo'],
    'Yaleko':['Yaleko','Yahisuli','Opala','Lowa'],
    'Makiso-Kisangani': ['Makiso-Kisangani','Mangobo'],
    'Kabondo': ['Kabondo','Tshopo'],
    'Bafwasende': ['Bafwasende','Bafwagbogbo', 'Opienge'],
    'Itebero': ['Itebero','Walikale','Kibua'],
    'Masisi': ['Masisi','Katoyi'],
    'Rutshuru': ['Rutshuru','Bambo'],
    'Kayna':['Kayna','Pinga'],
    'Katwa': ['Butembo','Katwa'],
    'Beni':['Beni','Mabalako','Kalunguta'],
    'Tandala': ["Boto",'Mawuya','Kungu','Bwamanda','Bogosenubia','Bokonzi','Libenge','Tandala'],
    'Bangabola': ['Budjala','Bangabola'],
    'Gemena': ['Bulu', 'Gemena'],
    "Ndage": ['Mbaya','Ndage'],
    "Bili": ['Bili','Bosobolo'],
    'Loko': ['Loko','Mbaya','Yakoma','Mobayi Mbongo','Wasolo','Ndage'],
    'Businga': ['Businga','Abuzi','Wapinda'],
    'Yambuku': ['Yambuku','Yamaluka','Boso Manzi'],
    'Buta': ['Buta','Titule','Aketi','Bili','Ganga'],
    'Poko': ["Ango",'Poko','Viadana'],
    'Isiro':['Boma-Mangbetu','Pawa','Isiro'],
    'Aba':['Makoro','Aba','Faradje'],
    'Komanda': ['Boga','Komanda','Mandima','Lolwa'],
    'Bunia':['Lita','Rwampara','Kilo','Nizi','Bambu','Bunia'],
    'Mongbalu':['Mongbalu','Damas'],
    'Drodro': ['Jiba','Drodro','Tchomia','Fataki'],
    'Angumu': ['Angumu','Linga'],
    'Logo': ['Logo','Rimba','Rethy'],
    'Aru': ['Aru','Biringi','Aungba','Kambala'],
    'Ariwara': ['Ariwara','Laybo','Adja'],
    'Businga': ['Businga','Abuzi'],
    'Loko':['Mobayi Mbongo','Loko','Wasolo','Yakoma'],
    'Bili': ['Bili','Bosobolo'],
    'Kikongo': ['Bandundu','Kikongo','Bagata','Sia'],
    'Karisimbi':['Karisimbi','Goma']
}

#inverse of here above dictionnary
groupedzs_inv = { nk:k for k,v in groupedzs.items() for nk in groupedzs[k]}


# In[10]:


# groupedzs_inv


# In[11]:


len(list(groupedzs.keys()))


# In[12]:


# gpdzsg
# list(groupedzs.values())


# In[13]:


# gpdzs[gpdzs['Nom'].str.contains('lolanga Mampoko')]


# ### Checking that names are identical between grouped and initial zones names

# In[14]:


dict_values = groupedzs.values()
[ll for l in dict_values for ll in l if ll not in list(gpdzs['Nom'])]


# In[15]:


[l for l in list(groupedzs.keys()) if l not in list(gpdzs['Nom'])]


# In[16]:


gpdzs[gpdzs['Nom'].isin(list(groupedzs.keys()))]


# In[17]:


# gpdzs_merged[gpdzs_merged['Nom'] == 'Makala'].iloc[0]['geometry']


# In[18]:


# gpdzs_merged[gpdzs_merged['Nom'].isin(['Nsele','Nsele_g'])]['geometry']


# In[19]:


# gpdzs_merged[gpdzs_merged['Nom'].isin(['Nsele'])].plot()
# gpdzs_merged[gpdzs_merged['Nom'].isin(['Nsele_g'])].plot()


# In[20]:


# gpdzs_merged[gpdzs_merged['Nom'] == 'Makala_g'].iloc[0]['geometry'].interiors.


# In[21]:


# gpdzm


# In[22]:


# gpdzs_merged[gpdzs_merged['Nom'] == 'Makala'].iloc[0]['geometry'].covers(gpdzs_merged[gpdzs_merged['Nom'] == 'Makala'].iloc[0]['geometry'])


# In[23]:


# gpdzs[gpdzs['Nom'] == 'Kikimi'].iloc[0]['geometry'].covers(gpdzsg[gpdzsg['Zone+Peupl'] == 'Kikimi'].iloc[0]['geometry'])


# In[24]:


# gpdzsg


# In[25]:


# gdf_intersects = gpd.overlay(gpdzs,gpdzsg)


# In[26]:


# gdf_intersects[gdf_intersects.Nom_1 == 'Boende']


# In[27]:


# gpdzsg.covered(gpdtouches[gpdtouches['Zone+Peupl'] == 'Kokolo'].iloc[0]['geometry'])


# In[28]:


# gdf_intersects = gpd.overlay(gpdzs,gpdzsg)


# In[29]:


# gpd_dict = dict()
# for index, z in gpdzsg.iterrows():
#     gsz = gpd.GeoSeries(z['geometry'])
#     gpd_dict [z['Zone+Peupl']] = list()
#     for index2, zz in gdf_intersects[gdf_intersects['Zone+Peupl'] == z['Zone+Peupl']].iterrows():
#         gszz = gpd.GeoSeries(zz['geometry'])
# #         print(gsz.covers(gszz))
#         if (gsz.covers(gszz)):
#             print(True)
# #             gpd_dict [z['Zone+Peupl']].append(z['Nom'])


# In[30]:


# gdf_intersects


# In[31]:


# gdf_intersects[(gdf_intersects.PROVINCE_1 == 'Kinshasa') & (gdf_intersects['Zone+Peupl'] == 'Kokolo')]


# In[32]:


# gpdtouches


# In[33]:


# # gpdzsg.touches(gpdzsg[gpdzsg['Zone+Peupl'] == 'Kokolo']['geometry'])
# gpdtouches = gpdzsg
# mask = gpdtouches.touches(gpdtouches[gpdtouches['Zone+Peupl'] == 'Kokolo'].iloc[0]['geometry'])
# gpdtouches[mask]


# In[ ]:





# In[34]:


# gpd_dict = dict()
# for z in gdf_intersects.groupby('Zone+Peupl').groups.keys():
#     gdf_intersects_z = gdf_intersects[(gdf_intersects['Zone+Peupl'] == z)]
#     mask = gpdtouches.touches(gpdtouches[gpdtouches['Zone+Peupl'] == z].iloc[0]['geometry'])
#     gpd_dict[z] = set(list(gdf_intersects_z['Nom'])) - set(list(gpdtouches[mask]['Zone+Peupl']))
#     print(z)


# In[35]:


# gpd_dict['Masina II']


# In[36]:


# gpdzs


# In[37]:


# mask = gpdzs.touches(gpdzsg.loc[71,'geometry'])
# gpdzs[mask]


# In[38]:


# mask = gpdzs.intersects(gpdzsg.loc[71,'geometry'])
# gpdzs[mask]


# In[39]:


# gpdzsg[(gpdzsg.PROVINCE == 'Kinshasa') & (gpdzsg['Zone+Peupl'] == 'Kokolo')]


# In[40]:


#read Geo Data
# ./data/GEO DRC/RDC_Micro_ZonesDeSante_Regroupees.shp
# gpd.read_file('../../data/GEO DRC/RDC_ZonesDeSante.shp')
zone_gd = gpdzsg
zone_gd


# In[352]:


(set(zone_gd['PROVINCE']))


# ### Filter a subset of zones for analysis

# In[616]:


#Filter geo data
zone_filtered_gd = zone_gd[zone_gd['PROVINCE'].isin(
    [
    'KasaÃ¯-Oriental',
  'Kinshasa',
 'Kongo-Central',
  'Kwango',
  'Kwilu',
  'Equateur',
   'MaÃ¯-Ndombe',
   'Tshuapa',
 'Haut-Katanga',
 'Haut-Lomami',
 'Haut-Uele',
 'Ituri',
'Nord-Kivu',
'Sud-Kivu',
'Lomami',
 'Lualaba',
 'Maniema',
 'Bas-Uele',
'Nord-Ubangi',
'Sud-Ubangi',
'Tanganyika',
 'Mongala',

 
  # 'KasaÃ¯',
# 'Sankuru',
 # 'Tshopo',

  #'KasaÃ¯-Central', 
  
 ]) ]
# zone_filtered_gd[zone_filtered_gd['PROVINCE'] == 'Sud-Kivu']


# In[617]:


list_filtered_zones = list(zone_filtered_gd['Nom'])
print(list_filtered_zones,'size:',len(list_filtered_zones))


# ## Epidemiological Data Processing

# In[618]:


# read csv file
df_epi = pd.read_csv('./data/inrbdata.csv',sep = ',')
df_epi


# Grouping epi data by `Zones` and `Provinces`

# In[619]:


df_epi_agg = df_epi.groupby(['Zone de Santé','Provinces'], as_index=False).sum()
df_epi_agg


# In[620]:


# Sum cases
df_epi_agg.sum()


# ### Renaming and  matching

# In[621]:


# Renaming some elements to match with those in  Geo data
def renamed_zs(zs, els):
    zrn = zs
    for vtr in els:
        zrn = zrn.replace(vtr[0], vtr[1])
    return zrn


# In[622]:


list_zone_de_sante_inrb = list(df_epi_agg.groupby('Zone de Santé').groups.keys())


# In[623]:


for idx in list(df_epi_agg.index[df_epi_agg['Zone de Santé'].str.contains('1|2')]):
    df_epi_agg.at[idx,'Zone de Santé'] = renamed_zs(df_epi_agg.iloc[idx]['Zone de Santé'], [('1','I'),('2','II')])
    


# ### Spelling Correction 

# In[624]:



corrected_list = [('Kokolo (Ndolo)','Kokolo'),
                  ('Mont-Ngafula I','Mont Ngafula I'), 
                  ('Mont-Ngafula II','Mont Ngafula II'),  
                  ('N\'sele','Nsele'), ('Binza Méteo','Binza Meteo'), 
                  ('Kasavubu','Kasa-Vubu'), ('N\'djili','Ndjili'), 
                  
                 ('Boko Kivulu','Boko-Kivulu'),
                  ('Bonga Yasa','Yasa-Bonga'),
                  ('Sonabata','Sona-Bata'),
                  ('Sekebanza','Seke-Banza'),
                  ('Nyirangongo','Nyiragongo'),
                  ('Nyankunde','Nyakunde'),
                  ('Mumbanda','Mumbunda'),
                  ('Miti Murhesa','Miti-Murhesa'),
                  ('Miti murhesa','Miti-Murhesa'),
                  ('Mbanza ngungu','Mbanza-Ngungu'),
                  ('Mbanza Ngungu','Mbanza-Ngungu'),
                  ('Kwilu Ngongo','Kwilu-Ngongo'),
                  ('Kwilungongo','Kwilu-Ngongo'),
                  ('Makiso','Makiso-Kisangani'),
                  ('Kinsenso','Kisenso'),
                  ('Muanda','Moanda')
                 ]
correction_dict = {k:v for k,v in corrected_list}
# .str.contains('|'.join(['Mont','sele','Binza','djili','Kasa','Kokolo']))
for idx in list(df_epi_agg.index[df_epi_agg['Zone de Santé'].isin([el[0] for el in corrected_list])]):
    df_epi_agg.at[idx,'Zone de Santé'] = correction_dict[df_epi_agg.iloc[idx]['Zone de Santé']]
#     renamed_zs(df_epi_agg.iloc[idx]['Zone de Santé'], corrected_list)


# ### Matching epi data zone names to zones names as provided by FV

# In[625]:


for idx in list(df_epi_agg.index[df_epi_agg['Zone de Santé'].isin(groupedzs_inv.keys())]):
#     print((df_epi_agg.iloc[idx]['Zone de Santé'],groupedzs_inv[df_epi_agg.iloc[idx]['Zone de Santé']]))
    df_epi_agg.at[idx,'Zone de Santé'] = groupedzs_inv[df_epi_agg.iloc[idx]['Zone de Santé']]


# In[626]:


df_epi_agg = df_epi_agg.groupby(['Zone de Santé','Provinces'], as_index=False).sum()
df_epi_agg


# In[627]:


list_zone_de_sante_inrb = list(df_epi_agg.groupby('Zone de Santé').groups.keys())


# ### Zones in Epi data but not in Zones FV shp

# In[628]:


#Check mismatching zones
missingzones = [l for l  in list_zone_de_sante_inrb if l not in list(gpdzs['Nom'])];missingzones


# #### Cases in those zones

# In[629]:


df_epi[df_epi['Zone de Santé'].isin(missingzones)].groupby(['Zone de Santé','Provinces'],as_index = False).sum()


# ### Drop those zones for now
# 
# `TODO` see what to do with those later on

# In[630]:


df_epi_agg = df_epi_agg.drop(df_epi_agg.index[df_epi_agg['Zone de Santé'].isin(missingzones)])
df_epi_agg


# ### Check zones left

# In[631]:


#Check mismatching zones
list_zone_de_sante_inrb = list(df_epi_agg.groupby('Zone de Santé').groups.keys())
[l for l  in list_zone_de_sante_inrb if l not in list_filtered_zones]


# ### Zones with 0 case

# In[632]:


#Zone with 0 case
zs_none_touched = [l for l  in list_filtered_zones if l not in list_zone_de_sante_inrb]
print(zs_none_touched,len(zs_none_touched))


# In[633]:


df_zs_none_touched = gpdzsg[~gpdzsg.Nom.isin(list_zone_de_sante_inrb)][['PROVINCE','Nom']]
df_zs_none_touched['Cas confirmés'] = 0
df_zs_none_touched = df_zs_none_touched.rename({'Nom':'Zone de Santé','PROVINCE':'Provinces'},axis=1)
df_zs_none_touched


# In[634]:


df_epi_agg = pd.concat([df_epi_agg,df_zs_none_touched], ignore_index=True)
df_epi_agg


# In[635]:


df_epi_agg[df_epi_agg.duplicated()]


# In[636]:


# df_epi_agg[df_epi_agg['Zone de Santé'] == 'Bandalungwa']


# In[637]:


# zone_filtered_gd[zone_filtered_gd.PROVINCE == 'Kinshasa'][['PROVINCE','Zone+Peupl']].sort_values('Zone+Peupl')


# In[638]:


len([l for l in list_zone_de_sante_inrb if l in list_filtered_zones])


# In[639]:


len(list_filtered_zones)


# In[640]:


# [l for l  in list(df_epi_agg['Zone de Santé']) if l not in  list_filtered_zones]


# ### Save Epidata to csv

# In[641]:


df_epi_agg = df_epi_agg.groupby(['Zone de Santé'], as_index=False).sum()
df_epi_agg


# In[642]:


check_list = list()
for el in list_filtered_zones:#list(df_epi_agg['Zone de Santé']):
    if (el in check_list):
        print(el)
    else:
        check_list.append(el)


# In[643]:


len(list_filtered_zones),len(list(df_epi_agg['Zone de Santé']))


# In[644]:


set(list_filtered_zones) == set(list(df_epi_agg['Zone de Santé']))


# In[645]:


len(set(list_filtered_zones))


# In[646]:


len(set(list(df_epi_agg['Zone de Santé'])))


# In[647]:


[ el for el in list_filtered_zones if el not in  list(df_epi_agg['Zone de Santé'])]


# #### Save only filtered zones

# In[648]:


df_epi_agg_fil = df_epi_agg[df_epi_agg['Zone de Santé'].isin(list_filtered_zones)][['Zone de Santé','Cas confirmés']]
df_epi_agg_fil = pd.DataFrame(df_epi_agg_fil)
# df_epi_agg_fil['patIDs'] = [i+1 for i in range(len(list_filtered_zones))]#df_epi_agg_fil.shape[0])]
df_epi_agg_fil['patIDs'] = [i+1 for i in range(df_epi_agg_fil.shape[0])]#df_epi_agg_fil.shape[0])]
df_epi_agg_fil = df_epi_agg_fil.rename(columns={'Zone de Santé':'patNames'})
df_epi_agg_fil


# In[649]:


#save to csv
# './epidemiological model/BEARmod/DRCexample/data/epidata.csv'
df_epi_agg_fil.to_csv('./epidemiological_model/BEARmod_DRC/data/epidata.csv')


# In[650]:


df_epi_agg_fil.to_clipboard(True)


# In[651]:


#['Destination','deltaVolume_x_plus_y_x_y']
# df_obs_agg_merge

# df_epi_reduc_agg_fil = df_epi_agg_fil.merge(df_obs_agg_merge[['Destination','deltaVolume_x_plus_y_x_y']], left_on='Zone de Santé', right_on='Destination')
# df_epi_reduc_agg_fil.rename(columns={'deltaVolume_x_plus_y_x_y'})


# In[652]:


df_epi_agg_fil


# In[653]:


df_epi_agg_fil['Cas confirmés'].sum()


# In[654]:


df_pats = df_epi_agg_fil[['patIDs', 'patNames']]
# df_pats = df_pats.rename(columns={'Zone de Santé':'patNames','ids':'patIDs'})
df_pats


# ### Population movement data Processing

# In[655]:


# read csv file

df = pd.read_csv('../../data/export_csv/Flux_24h.csv',sep = ';')

# Date Conversion
df['Date'] = pd.to_datetime(df['Date'])
df['Date_day'] = df['Date'].dt.weekday


# In[656]:


#Filter data for only 3h of Immobility and exclude hors-zone
df = df[(df.Immobility == '3h') & (df.Origin != 'Hors_Zone')]
df


# ### Remove duplicated data

# In[657]:


df = df.drop_duplicates()
df


# In[658]:


# Only consider zone Globale (not hotspots)
df_g = df[df.Observation_Zone == 'ZoneGlobale'].groupby(by=['Date','Origin','Destination','Observation_Zone','Date_day'], as_index=0).sum()
df_g


# ### Filter movement data by selected zones

# In[659]:


df_filtered_both = df_g[(df_g['Origin'].isin(list_filtered_zones)) & (df_g['Destination'].isin(list_filtered_zones))]
df_filtered_both


# In[660]:


#Computing Totals Volume for each Origin per day
# df_filtered_both_agg = df_filtered_both.groupby(by = ['Date','Date_day',"Origin"], as_index=False).sum()
# df_filtered_both_agg


# In[661]:


# df_filtered_both_mg = df_filtered_both.merge(df_filtered_both_agg,left_on=['Date','Origin'], right_on=['Date','Origin'])
# df_filtered_both_mg


# In[662]:


# df_filtered_both_mg['VolumeProp'] = df_filtered_both_mg['Volume_x']/df_filtered_both_mg['Volume_y']
# df_filtered_both_mg#[(df_filtered_both_mg.Origin == 'Kinshasa') & (df_filtered_both_mg.Date == '2020-01-31')]


# In[ ]:





# # Net Mobility

# In[663]:


# df_filtered_both = df_g[(df_g['Origin'].isin(list_filtered_zones)) & (df_g['Destination'].isin(list_filtered_zones))]
# df_filtered_both


# In[664]:


def filter_df_from_to(start_date, end_date, df):
    mask_base = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    return df.loc[mask_base]


# ### Net Mobility for each Zone per day

# In[665]:


df_filtered_agg_in = df_filtered_both.groupby(by=['Date','Destination','Date_day'],as_index=0).sum()
#df_filtered_agg_in[(df_filtered_agg_in.Destination == 'Gombe') & (df_filtered_agg_in.Date == '2020-02-02')]
df_filtered_agg_out = df_filtered_both.groupby(by=['Date','Origin','Date_day'],as_index=0).sum()
#df_filtered_agg_out
df_filtered_agg_in_out = pd.merge(df_filtered_agg_in,df_filtered_agg_out, left_on=['Date','Destination','Date_day'], right_on=['Date','Origin','Date_day'])

#Sum volume inbound and outbound for each zone
df_filtered_agg_in_out['Volume_x_plus_y'] = df_filtered_agg_in_out['Volume_x'] + df_filtered_agg_in_out['Volume_y']
df_filtered_agg_in_out


# ### Splitting data (ref/obs)

# In[666]:


# mobility with baseline  (the starting date of lockdown in DRC)
ref_start_date = '2020-02-01'
ref_end_date = '2020-03-18'

# mask_base = (df_filtered_agg_in_out['Date'] >= ref_start_date) & (df_filtered_agg_in_out['Date'] <= ref_end_date)

obs_start_date = '2020-03-19'
obs_end_date = '2020-06-29'

# mask_obs = (df_filtered_agg_in_out['Date'] >= obs_start_date) & (df_filtered_agg_in_out['Date'] <= obs_end_date)

df_ref = filter_df_from_to(ref_start_date, ref_end_date,df_filtered_agg_in_out)#df_agg_gen_mob.loc[mask_base]
df_obs = filter_df_from_to(obs_start_date, obs_end_date,df_filtered_agg_in_out)#df_agg_gen_mob.loc[mask_obs]


# In[667]:


df_ref_agg = df_ref.groupby(by=['Date','Destination','Date_day'],as_index=0).sum().groupby(by=['Destination'],as_index=0).median()
df_obs_agg = df_obs.groupby(by=['Date','Destination','Date_day'],as_index=0).sum().groupby(by=['Destination'],as_index=0).median()


# In[668]:


df_ref_agg.head()


# In[669]:


df_obs_agg.head()


# In[670]:


# df_obs_agg_merge = pd.merge(df_ref_agg, df_obs_agg,left_on='Destination', right_on='Destination')
# df_obs_agg_merge['diffVolume_x_plus_y_x_y'] = df_obs_agg_merge['Volume_x_plus_y_y'] - df_obs_agg_merge['Volume_x_plus_y_x']

# df_obs_agg_merge['deltaVolume_x_plus_y_x_y'] = df_obs_agg_merge['diffVolume_x_plus_y_x_y']/df_obs_agg_merge['Volume_x_plus_y_x']*100
# df_obs_agg_merge = df_obs_agg_merge.sort_values('deltaVolume_x_plus_y_x_y')
# df_obs_agg_merge = df_obs_agg_merge[df_obs_agg_merge.Destination.isin(list_filtered_zones)]

# #['Destination','deltaVolume_x_plus_y_x_y']
# df_obs_agg_merge
# # df_obs_agg_merge['Destination','deltaVolume_x_plus_y_x_y']


# ### Movement Reduction

# In[671]:


df_ref_agg_date_day = df_ref.groupby(by=['Date','Destination','Date_day'],as_index=0).sum().groupby(by=['Destination','Date_day'],as_index=0).median()
df_ref_agg_date_day[df_ref_agg_date_day.Destination == 'Gombe']


# In[672]:


df_obs_agg_date_dest_dd = df_obs.groupby(by=['Date','Destination','Date_day'],as_index=0).sum()
# df_obs_agg_date_dest_dd[df_obs_agg_date_dest_dd.Destination == 'Gombe']


# In[673]:


df_trend = pd.merge(df_obs_agg_date_dest_dd,df_ref_agg_date_day,left_on=['Destination','Date_day'],right_on=['Destination','Date_day']).sort_values(by='Date')
# df_trend[df_trend.Destination == 'Gombe']
df_trend


# In[674]:


df_trend['deltaV'] = (df_trend['Volume_x_plus_y_x'])/df_trend['Volume_x_plus_y_y'] #- df_trend['Volume_x_plus_y_y']
# df_trend = df_trend[df_trend.Destination == 'Gombe']

# df_trend[(df_trend.Destination == 'Ngiri-Ngiri') & (df_trend.Date == '2020-03-30')]
df_trend


# In[675]:


df_trend.describe()


# ### Save Movement Reduction data to csv

# In[676]:


df_mvt_red = df_trend[['Date','Destination','deltaV']].merge(df_pats, left_on='Destination', right_on='patNames').rename(columns={'Destination':'from','Date':'date','patIDs':'name', 'deltaV':'relative_move'})
#Save to csv
df_mvt_red.to_csv('./epidemiological_model/BEARmod_DRC/data/mvt_red.csv')
df_mvt_red


# In[677]:


df_mvt_red.describe()


# In[678]:


selected_zones = ['Kinshasa','Gombe','Barumbu']


# g = sns.FacetGrid(df_trend[df_trend.Destination.isin(selected_zones)], row="Destination",aspect=3,height=6,sharey=False,sharex=False)
# # g.map(sns.lineplot, x='Date',y='deltaV', alpha=.7)
# g.map(plt.plot, "Date", "deltaV", alpha=.7)
# # sns.lineplot(x='Date',y='deltaV',data=df_trend)
# g.add_legend();


# # Presence Data

# In[679]:


# reading csv file
dfp = pd.read_csv('../../data/export_csv/Presence_24h.csv',sep = ';')
dfp


# In[680]:


#Duplicates check
dfp[dfp.duplicated()]


# In[681]:


#Convert to Date

dfp['Date'] = pd.to_datetime(dfp['Date'])


# In[682]:


#filter by selected zones

dfp_filtered = dfp[dfp['Zone'].isin(list_filtered_zones)]
dfp_filtered


# In[683]:


df_agg_dzp = dfp_filtered.groupby(["Date","Zone",'PresenceType'],as_index=0).sum()
df_agg_dzp


# In[684]:


dfp_agg_f_day = df_agg_dzp#[df_agg_dzp.PresenceType == 'Nuit']
dfp_agg_date_zone = dfp_agg_f_day.groupby(by=['Date','Zone'],as_index=0).sum()
dfp_agg_date_zone


# In[685]:


# dfp_agg_f_night = df_agg_dzp[df_agg_dzp.PresenceType == 'Nuit']
# dfp_agg_f_day = df_agg_dzp[df_agg_dzp.PresenceType == 'Day']


# In[686]:


# dfp_agg_f_night


# ### Merging Presence and Movement

# In[687]:


df_mvt_pres = df_filtered_both.merge(dfp_agg_date_zone,left_on=['Origin','Date'], right_on=['Zone','Date'])
df_mvt_pres['move_prop'] = df_mvt_pres['Volume_x']/ df_mvt_pres['Volume_y']
# df_mvt_pres[(df_mvt_pres.Date == '2020-02-02') & (df_mvt_pres.Origin == 'Gombe')].sum()
# df_mvt_pres[(df_mvt_pres.Origin == 'Gombe') ]
df_mvt_pres


# In[688]:


df_mvt_epi = df_mvt_pres.merge(df_pats, left_on='Origin', right_on='patNames')
df_mvt_epi = df_mvt_epi.merge(df_pats, left_on='Destination', right_on='patNames')
df_mvt_epi.drop(['patNames_x','patNames_y','Observation_Zone','Zone'],axis=1, inplace=True) #,'Date_day'
#"fr_users","movers"
df_mvt_epi.rename(columns={'Date':'date','Volume_x':'movers','patIDs_x':'fr_pat','patIDs_y':'to_pat','Volume_y':'fr_users'}, inplace=True)
df_mvt_epi


# Trying to repeate mobility pattern for missing date

# In[689]:


df_mvt_epi_wo_npi = df_mvt_epi[df_mvt_epi.date<'2020-03-18']
df_mvt_epi_wo_npi


# ### Check for missing dates

# In[690]:


# pd.date_range('2020-01-31','2020-03-17',)
def check_missing_dates(df,start,end):
    return set([d.strftime('%Y-%m-%d') for d in pd.date_range(start,end,)]) - set(df.date.dt.date.astype(str))


# In[691]:


# df_mvt_epi[df_mvt_epi.date == '2020-03-18']


# In[692]:


df_mvt_epi_wo_npi[df_mvt_epi_wo_npi.date == '2020-02-05']


# In[693]:


check_missing_dates(df_mvt_epi_wo_npi,'2020-01-31','2020-03-17')


# In[694]:


def slide_df(df,interval, unit):
    df_copy = pd.DataFrame(df, copy=True)
    df_copy['date'] = df_copy['date'] + pd.Timedelta(interval, unit)
    df_copy_slid = df_copy[df_copy.date > df.date.max()]
    return pd.concat([df,df_copy_slid], axis=0)


# In[695]:


df_mvt_epi_wo_npi_slid = pd.DataFrame(df_mvt_epi_wo_npi, copy=True)
df_mvt_epi_wo_npi_slid['date'] = df_mvt_epi_wo_npi_slid ['date'] + pd.Timedelta(6, 'W')
df_mvt_epi_wo_npi_slid


# In[696]:


# df_mvt_epi_slid = df_mvt_epi_slid[df_mvt_epi_slid.date > df_mvt_epi_wo_npi.date.max()] #>= df_mvt_epi_wo_npi.date.max()
# df_mvt_epi_slid


# In[697]:


#Sliding data until december 2020

df_mvt_wo_npi_slid = slide_df(df_mvt_epi_wo_npi,6, 'W')
df_mvt_wo_npi_slid = slide_df(df_mvt_wo_npi_slid,12, 'W')
df_mvt_wo_npi_slid = slide_df(df_mvt_wo_npi_slid,16, 'W')
df_mvt_wo_npi_slid


# In[698]:


check_missing_dates(df_mvt_wo_npi_slid,'2020-01-31','2020-12-08')


# In[699]:


# df_mvt_epi[(df_mvt_epi.Origin == 'Gombe')].mean()


# In[700]:


df_mvt_wo_npi_slid[(df_mvt_wo_npi_slid.Origin == 'Gombe')&(df_mvt_wo_npi_slid.date == '2020-11-08')].describe()


# In[701]:


# df_mvt_epi[(df_mvt_epi.Origin == 'Kinshasa') & (df_mvt_epi.date == '2020-03-27')]['move_prop'].sum()


# ### Save OD matrix to csv

# In[702]:


df_mvt_wo_npi_slid[(df_mvt_wo_npi_slid.date >= '2020-07-04')&((df_mvt_wo_npi_slid.date <= '2020-11-09'))][['date','Origin','Destination','fr_pat', 'to_pat','movers','fr_users','move_prop']].to_csv('./epidemiological_model/BEARmod_DRC/data/mobmat.csv')


# In[ ]:





# # BEARmod
# Basic Epidemic, Activity, and Response COVID-19 model
# 
# This model implements a basic SEIR simulation model, accounting for variable daily movement patterns, recovery rates, and contact rates. Demonstration of this model can be seen in a recent Nature paper [1]
# 
# For a placeholder dummy dataset and example simulation run, please see "run_model_small.R", which uses a dummy movement dataset "testmove.csv"
# 
# ## Overall model
# This model is a metapopulation model of COVID-19 transmission, based on an SEIR modeling framework. Within each patch, this model follows a fairly simple SEIR framework. The primary complexities this model is designed to describe are daily movement patterns, and spatially and temporally heterogeneous reductions in movement and contact rates. Specifically, this model is particularly suited for data that generally come from mobile phone companies.
# 
# ### Baseline patch-level processes
# Within each patch, this model first calculates the number of infected people who recovered or were otherwise removed from the infectious population (ie. through self-isolatuion) at an average rate r, where r is equal to the inverse of the average infectious period. This is explicitly incorporated as a Bernoulli trial for each infected person with a probability of recovering 1-exp⁡(-r). 
# Then, the model converts exposed people to infectious by similarly incorporating a Bernoulli trial for each exposed individual, where the daily probability of becoming infectious 1-exp⁡(-ε), where ε was the inverse of the average time spent exposed but not infectious. 
# Finally, to end the exposure, infection, and recovery step of the model, newly exposed people are calculated for each city based on the number of infectious people in the city I_i, and the average number of daily contacts that lead to transmission that each infectious person has c. This model then simulates the number of newly exposed people through a random draw from a Poisson distribution for each infectious person where the mean number of new infections per person was c, which was then multiplied by the fraction of people in the patch who are susceptible.
# The infection processes within each patch therefore approximate the following deterministic, continuous-time model, where c and r varied through time:
# dS/dt=S-c SI/N
# dE/dt=c SI/N-εE
# dI/dt=εE-rI
# dR/dt=rI
# 
# ### Movement between patches
# After completing the infection-related processes, the model moves infectious people between cities, using the proportion of people who went from each patch to each other patch measured in the input OD matrix. Infectious people are moved from their current location to each possible destination (including remaining in the same place) using Bernoulli trials for each infectied person, and each possible destination city. 
# Through this model, stochasticity in the numbers and places where COVID-19 appears between simulation runs in this model through variance in numbers of people becoming exposed, infectious, and removed/recovered, as well as variance in numbers of people moving from one city to another.
# 
# ## Input options and formats
# Note: These parameter specifications are relevant for v 0.92, denoted at the top of the bearmod_fx.R file.
# 
# First, you will create an empty population list HPop, using InitiatePop(). This function takes as inputs:
# - pat_locator: A data frame with variables "patNames", "patIDs" (numeric; sequential from 1:number of patches), and "pop" (population per patch)
# - initialInf: A vector of initially infected people per patch, length equal to the number of patches
# - initialExp: A vector of initially exposed people per patch, length equal to the number of patches
# 
# The initial HPop is then fed into the runSim function, which has the following inputs:
# - HPop
# - pat_info: This is the same as pat_locator
# - movement_reduction_df: a data frame with 3 variables, "date", "name", and "relative_movement". "name" corresponds to the patNames ID for the patch, and "relative_movement" indicates the relative proportion of movement for that day--.3 means all movement for that patch in that day (both incoming and outgoing) will be 30% of the baseline value (specified in mobmat later). This is specified on a per-day basis, and does not have to be complete--any missing day/patch pairs will have 100% of the baseline movement patterns
# - contact_reduction_df: a data frame with 3 variables, "date", "name", and "relative_contact". Same as movement_reduction_df except this refers to the relative contact rate within a patch for a given day--ie. .5 means half as many contacts per person
# - mobmat: A data frame with variables "date", "fr_pat", "to_pat", "move_prop". fr_pat and to_pat refer to the patch IDs of the origin and destination patches (see patIDs from pat_locator), and move_prop is the proportion of people who move from each origin to each destination on the given day in "date". If stayers are not denoted (origin = destination), then the model will designate this as 1 - sum(movement elsewhere) for a given patch. 
# 
# --more parameter definitions coming soon--
# 
# Contact:
# Nick W Ruktanonchai; 
# nrukt00 at gmail.com
# 
# [1] Lai, S., Ruktanonchai, N.W., Zhou, L. et al. Effect of non-pharmaceutical interventions to contain COVID-19 in China. Nature (2020). https://doi.org/10.1038/s41586-020-2293-x
# 

# In[ ]:




