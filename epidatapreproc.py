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

%matplotlib inline

# Renaming some elements to match with those in  Geo data
def renamed_zs(zs, els):
    zrn = zs
    for vtr in els:
        zrn = zrn.replace(vtr[0], vtr[1])
    return zrn


def main():
    ## Geo Data Processsing
    gpdzs = gpd.read_file('../../data/GEO DRC/RDC_ZonesDeSante.shp')[['PROVINCE','Nom','geometry']]
    gpdzsg = gpd.read_file('../../data/GEO DRC/RDC_Micro_ZonesDeSante_Regroupees.shp')[['PROVINCE','Zone+Peupl','geometry']]
    gpdzsg = gpdzsg.rename({'Zone+Peupl':'Nom'}, axis=1)

    ### Dictionnary of zones as grouped by FV
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
    
    zone_gd = gpdzsg
    #Filter geo data
    zone_filtered_gd = zone_gd[zone_gd['PROVINCE'].isin(
    ['Bas-Uele',
     'Equateur',
     'Haut-Katanga',
     'Haut-Lomami',
     'Haut-Uele',
     'Ituri',
     'KasaÃ¯',
     'KasaÃ¯-Central',
     'KasaÃ¯-Oriental',
     'Kinshasa',

     'Kwango',
     'Kwilu',
     'Lomami',
     'Lualaba',
     'Maniema',
     'MaÃ¯-Ndombe',
     'Mongala',
     'Nord-Kivu',
     'Nord-Ubangi',
     'Sankuru',
     'Sud-Kivu',
     'Sud-Ubangi',
     'Tanganyika',
     'Tshopo',
     'Tshuapa']) ]
    
    list_filtered_zones = list(zone_filtered_gd['Nom'])
    
    ## Epidemiological Data Processing
    
    # read csv file
    df_epi = pd.read_csv('./data/inrbdata.csv',sep = ',')
    df_epi_agg = df_epi.groupby(['Zone de Santé','Provinces'], as_index=False).sum()
    
    ### Renaming and  matching
    list_zone_de_sante_inrb = list(df_epi_agg.groupby('Zone de Santé').groups.keys())
    for idx in list(df_epi_agg.index[df_epi_agg['Zone de Santé'].str.contains('1|2')]):
        df_epi_agg.at[idx,'Zone de Santé'] = renamed_zs(df_epi_agg.iloc[idx]['Zone de Santé'], [('1','I'),('2','II')])
    
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
    
    
    ### Matching epi data zone names to zones names as provided by FV
    for idx in list(df_epi_agg.index[df_epi_agg['Zone de Santé'].isin(groupedzs_inv.keys())]):
    #     print((df_epi_agg.iloc[idx]['Zone de Santé'],groupedzs_inv[df_epi_agg.iloc[idx]['Zone de Santé']]))
        df_epi_agg.at[idx,'Zone de Santé'] = groupedzs_inv[df_epi_agg.iloc[idx]['Zone de Santé']]
    
    df_epi_agg = df_epi_agg.groupby(['Zone de Santé','Provinces'], as_index=False).sum()
    list_zone_de_sante_inrb = list(df_epi_agg.groupby('Zone de Santé').groups.keys())
    
    ### Zones in Epi data but not in Zones FV shp
    #Check mismatching zones
    missingzones = [l for l  in list_zone_de_sante_inrb if l not in list(gpdzs['Nom'])]
    print(missingzones)
    
    #### Cases in those zones
    
    df_epi[df_epi['Zone de Santé'].isin(missingzones)].groupby(['Zone de Santé','Provinces'],as_index = False).sum()
    
    ### Drop those zones for now
    
    df_epi_agg = df_epi_agg.drop(df_epi_agg.index[df_epi_agg['Zone de Santé'].isin(missingzones)])
    
    ### Check zones left
    #Check mismatching zones
    list_zone_de_sante_inrb = list(df_epi_agg.groupby('Zone de Santé').groups.keys())
    
    ### Zones with 0 case
    zs_none_touched = [l for l  in list_filtered_zones if l not in list_zone_de_sante_inrb]
    
    df_zs_none_touched = gpdzsg[~gpdzsg.Nom.isin(list_zone_de_sante_inrb)][['PROVINCE','Nom']]
    df_zs_none_touched['Cas confirmés'] = 0
    df_zs_none_touched = df_zs_none_touched.rename({'Nom':'Zone de Santé','PROVINCE':'Provinces'},axis=1)
    
    df_epi_agg = pd.concat([df_epi_agg,df_zs_none_touched], ignore_index=True)
    
    ### Save Epidata to csv
    df_epi_agg = df_epi_agg.groupby(['Zone de Santé'], as_index=False).sum()
    
    #### Save only filtered zones
    df_epi_agg_fil = df_epi_agg[df_epi_agg['Zone de Santé'].isin(list_filtered_zones)][['Zone de Santé','Cas confirmés']]
    df_epi_agg_fil = pd.DataFrame(df_epi_agg_fil)
    # df_epi_agg_fil['patIDs'] = [i+1 for i in range(len(list_filtered_zones))]#df_epi_agg_fil.shape[0])]
    df_epi_agg_fil['patIDs'] = [i+1 for i in range(df_epi_agg_fil.shape[0])]#df_epi_agg_fil.shape[0])]
    df_epi_agg_fil = df_epi_agg_fil.rename(columns={'Zone de Santé':'patNames'})
    
    #save to csv
    # './epidemiological model/BEARmod/DRCexample/data/epidata.csv'
    df_epi_agg_fil.to_csv('./epidemiological_model/BEARmod_DRC/data/epidata.csv')
    
    df_pats = df_epi_agg_fil[['patIDs', 'patNames']]
    # df_pats = df_pats.rename(columns={'Zone de Santé':'patNames','ids':'patIDs'})
    df_pats


if __name__ == "__main__":
    main()