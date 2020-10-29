
#rm(list=ls())
library(lubridate)
library(raster)
library(exactextractr)
library(sf)

#loading population data and shapefile
popraster = raster("cod_ppp_2020_1km_Aggregated.tif")
drc_shp = read_sf(dsn="./data/geo_drc/",layer="RDC_Micro_ZonesDeSante_Regroupees")

#st_read("./data/geo_drc/RDC_Micro_ZonesDeSante_Regroupees.shp",stringsAsFactors=F)

drc_shp$pop <-exactextractr::exact_extract(popraster, drc_shp, fun="sum")

#Reading infecteous data

epidata = read_csv('./data/epidata.csv')
patNames = epidata$patNames  
patIDs = epidata$patIDs

pat_locator = data.frame(patIDs , patNames)

#we will set the population numbers using the population variable from the shapefile
pat_locator$pop = apply(pat_locator, 1, FUN=function(x){drc_shp$pop[which(drc_shp$Zone.Peupl == x[2])]})


mvt_red = read_csv('./data/mvt_red.csv')

mobmat = read_csv('./data/mobmat.csv')

movement_data = mobmat

recrate = 1/6 #daily probability of recovery
exposerate = 2.68/6 # R0 of 2.68, 5.8 days till seeking treatment # How many people a single person potentially infects per day -- can be calculated from R0 estimate if you divide R0 by infectious period
exposepd = 3 # incubation period






###################################################################################


# dates = seq.Date(from = as.Date("2020-01-01"), to = as.Date("2020-02-01"),by="day")
# 
# drc_shp$IDs = 1:dim(drc_shp)[1]
# 
# ##This part is making up a mobility dataset. Here you wouldn't need to process anything, but you would want to have proportions of people who move from A to B (with no self connections needed)
# # Feel free to ask me how to make this fit your data!
# movement_data_all = data.frame()
# 
# prophome = .8
# for (i in 1:length(dates)){
#   movement_data = expand.grid(fr_pat=drc_shp$IDs,to_pat=drc_shp$IDs)
#   movement_data$move = 0
#   
#   dailymove = matrix(runif(0,1,n=length(drc_shp$IDs)*length(drc_shp$IDs)),length(drc_shp$IDs), length(drc_shp$IDs))
#   diag(dailymove) = prophome
#   for (j in 1:dim(dailymove)[1]){
#     dailymove[j,-j] = dailymove[j,-j] / sum(dailymove[j,-j]) * (1-prophome)
#   }
#   
#   for (m in 1:dim(dailymove)[1]){
#     for (n in 1:dim(dailymove)[2]){
#       movement_data$move[which(movement_data$fr_pat == m & movement_data$to_pat == n)] = dailymove[m,n]
#     }
#   }
#   
#   movement_data$date = as.Date(dates[i])
#   movement_data_all = rbind(movement_data_all,movement_data)
# }
# 
# movement_data_all$move_prop = movement_data_all$move
# movement_data_all = subset(movement_data_all, fr_pat != to_pat)
# 
# movement_data <- movement_data_all
# 
# patNames = drc_shp$NAME_1
# patIDs = drc_shp$IDs
# pat_locator = data.frame(patNames,patIDs)
# 
# recrate = 1/6 #daily probability of recovery
# exposerate = 2.68/6 # R0 of 2.68, 5.8 days till seeking treatment # How many people a single person potentially infects per day -- can be calculated from R0 estimate if you divide R0 by infectious period
# exposepd = 3 # incubation period