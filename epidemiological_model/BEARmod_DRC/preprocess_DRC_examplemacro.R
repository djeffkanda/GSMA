
#rm(list=ls())
library(lubridate)
library(raster)
library(exactextractr)
library(sf)
library(stringr)

library("ggrepel")
library("googleway")

#loading population data and shapefile
popraster = raster("cod_ppp_2020_1km_Aggregated.tif")
#drc_shp = read_sf(dsn="./data/geo_drc/",layer="RDC_Micro_ZonesDeSante_Regroupees")
drc_shp = read_sf(dsn="./data/geo_drc/",layer="RDC_Macro_Provinces")



drc_shp =cbind(drc_shp, st_coordinates(st_centroid(drc_shp)))
#AIzaSyAPvoRJKdAc9uDNPt3dzSxACd1dcStNXRc

#drc_shp$Zone.Peupl

ggplot(drc_shp) + 
  stat_sf_coordinates()+
  geom_sf() + 
  scale_fill_distiller(palette="RdYlBu",direction=-1)#+ 
  #geom_sf_label(aes(label = Zone.Peupl))#+
  #geom_text_repel(data = drc_shp, aes(x = X, y = Y, label = Zone.Peupl),fontface = "bold")
  

# , nudge_x = c(1, -1.5, 2, 2, -1), nudge_y = c(0.25,
#                                               -0.25, 0.5, 0.5, -0.5)
#geom_point(data=drc_shp,drc_shp_point,aes(X,Y))
#+geom_text_repel()

#st_read("./data/geo_drc/RDC_Micro_ZonesDeSante_Regroupees.shp",stringsAsFactors=F)

#drc_shp$pop <-exactextractr::exact_extract(popraster, drc_shp, fun="sum")

drc_shp$pop <- as.numeric(apply(drc_shp, 1, FUN=function(x){str_replace_all(x[6], " ", "")}))#(as.character(drc_shp$Population,collapse=""))
#Reading infecteous data

epidata = read_csv('./data/epidatamacro.csv')
patNames = epidata$patNames  
patIDs = epidata$patIDs

pat_locator = data.frame(patIDs , patNames)

#we will set the population numbers using the population variable from the shapefile
pat_locator$pop = apply(pat_locator, 1, FUN=function(x){drc_shp$pop[which(drc_shp$PROVINCE == x[2])]})


mvt_red = read_csv('./data/mvt_redmacro.csv')

mobmat = read_csv('./data/mobmatmacro.csv')

movement_data = mobmat

#recrate = 1/6 #daily probability of recovery
#exposerate = 2.68/6 # R0 of 2.68, 5.8 days till seeking treatment # How many people a single person potentially infects per day -- can be calculated from R0 estimate if you divide R0 by infectious period
#exposepd = 3 # incubation period





