###DRC hypothetical example
rm(list=ls())
library(data.table) 
library(lubridate)
library(tictoc)
#library(pryr)
#library(sf)
#library(maps)
#library(magick)
library(janitor)
library(gifski)
#library(tidyverse)
library(readr)
library(ggplot2)
library(gganimate)
library(dplyr)

source("bearmod_fx_dev.R")
source("preprocess_DRC_example.R")

recprob = 1/5
recrate = 1-exp(-1/5) #daily probability of recovery
exposerate = 1 # R0 of 2.68, 5.8 days till seeking treatment # How many people a single person potentially infects per day -- can be calculated from R0 estimate if you divide R0 by infectious period
exposepd = 4 # incubation period

r0vals = read.csv("data/rt.csv")
r0vals = subset(r0vals,country == "Congo - Kinshasa")


#Some initial parameters
NPat = length(patNames)
patnInf = rep(0,NPat)
patnExp = c(rep(0,NPat) )


#pat_locator$pop = drc_shp$pop

#start infection in Kinshasa, with 500 cases
#patnInf[which(patNames == "Kinshasa")] = 500

patnInf = epidata$`Cas confirmés`
patnExp = c(rep(0,NPat))





dates = as.Date(as.character(r0vals$date),format = "%d/%m/%Y")
#relative_move_data is a data frame that includes relative_move, and relative_contact.
#This data frame is intended to simulate potential interventions that lead to reductions in mobility (travel restrictions) and reductions in contact rates (social distancing)
#.01 means 1% of normal, .5 mean 50% of normal, etc.
# Ideally every day should be represented (a row has a day a patch and a relative_move and relative_contact value).

relative_move_data=expand.grid(date =  as.Date(r0vals$date,format = "%d/%m/%Y"),from = patNames,relative_move = 0,relative_contact = 0)
#relative_move_data = mvt_red
relative_move_data$relative_contact = r0vals$mean * recrate
#relative_move_data$relative_move[which(relative_move_data$date > as.Date("2020-01-20"))] = .01
#relative_move_data$relative_contact[which(relative_move_data$date > as.Date("2020-01-20"))] = .01
#### Running the model  ####

#create the initial human population
HPop = InitiatePop(pat_locator,patnInf,patnExp)
###dates of simulation. should be bounded by the dates where mobility data are available

input_dates =  dates  #seq.Date(from = as.Date("2020-01-01"), to = as.Date("2020-02-01"),by="day")
 


#run the simulation
HPop_update = runSim(HPop,pat_locator,relative_move_data, relative_move_data,movement_data,input_dates,recrate,exposerate,exposepd,exposed_pop_inf_prop = 0,TSinday = 1,prob_move_per_TS=0) 
   
 
newHPop = HPop_update$HPop
epidemic_curve = HPop_update$epidemic_curve
all_spread = HPop_update$all_spread


ggplot() + geom_line(data=epidemic_curve,mapping=aes(x=Date,y=inf))



cases_on_days = data.frame()#as.data.frame(t(all_spread[which(all_spread$runday==day_chosen),3:dim(all_spread)[2]]))
#cases_on_days$day = day_chosen
for (day_chosen in 1:length(input_dates)) {
   cases_on_day = as.data.frame(t(all_spread[which(all_spread$runday==day_chosen),3:dim(all_spread)[2]]))
   names(cases_on_day) = "cases"
   cases_on_day$day = day_chosen
   cases_on_day$date = input_dates[day_chosen]
   cases_on_day$province = rownames(cases_on_day)
   cases_on_days <- rbind(cases_on_days,cases_on_day)
}


#merge the number of cases into the shapefile
drc_shp_with_cases = merge(drc_shp,cases_on_days,by.x="Zone.Peupl",by.y="province")

#Formatting the df for plots
drc_shp_with_cases_formatted = drc_shp_with_cases%>% 
   group_by(day)%>%   
   mutate(rank = rank(-cases), 
          Value_rel = cases/cases[rank==1], 
          Value_lbl = paste0(" ",cases))
drc_shp_with_cases_formatted$cases = floor(drc_shp_with_cases_formatted$cases)


#nc <- sf::st_read(system.file("shape/nc.shp", package = "sf"), quiet = TRUE)

#ggplot(head(nc, 3)) +
#   geom_sf(aes(fill = AREA)) +
#  geom_sf_label(aes(label = NAME))


# Plot map with cases per by zone
#myPlot<- ggplot() + geom_sf(data=drc_shp_with_cases_formatted,aes(fill=cases))
   #geom_sf_label(aes(label = "Zone.Peupl"))
#myPlot

# Plot map with cases per by zone
myPlot<- ggplot() + geom_sf(data=drc_shp_with_cases_formatted,aes(fill=cases))+
   #geom_sf_label(aes(label = "Zone.Peupl"))+
labs(title = 'Day: {frame_time}') +#+ scale_fill_distiller(trans="log10",palette="YlOrRd",direction=1)
   scale_fill_distiller(palette="YlOrRd",direction=1)+
   transition_time(day)+
   ease_aes()


#animate map as gif
map_animated_plot <- animate(myPlot,
                             duration = 60,
                             fps = 2,
                             width = 1200,
                             height = 1000, 
                             renderer = gifski_renderer("simulation_map.gif"))

map_animated_plot
#animate map as mp4
map_animated_plot_mp4 = animate(myPlot, 102, fps = 3,  width = 1200, height = 1000,
        renderer = ffmpeg_renderer()) -> for_mp4
anim_save("simulation_map.mp4", animation = for_mp4 )

map_animated_plot


#myPlot <- ggplot() + geom_sf(data=drc_shp_with_cases) 
#myPlot


#,mapping=aes(fill=cases, frame=date)
#      + scale_fill_distiller(trans="log10",palette="YlOrRd",direction=1)
# +
#    # gganimate specific bits:
#   # labs(title = 'Day: {frame_time}') +
#    #transito(date) +
#    ease_aes('linear')
# 
# animate(myPlot, duration = 5, fps = 20, width = 400, height = 400, renderer = gifski_renderer())
# #anim_save("output.gif")
# # Save at gif:
# anim_save("covidspread_drc.gif")



# Barchart of cases by zone de santes (ranked)
staticplot = ggplot(drc_shp_with_cases_formatted, aes(rank, group = Zone.Peupl, 
                                       fill = as.factor(Zone.Peupl), color = as.factor(Zone.Peupl))) +
   geom_tile(aes(y = cases/2,
                 height = cases,
                 width = 0.9), alpha = 0.8, color = NA) +
   geom_text(aes(y = 0, label = paste(Zone.Peupl, " ")), vjust = 0.2, hjust = 1) +
   geom_text(aes(y=cases,label = cases, hjust=0)) +
   coord_flip(clip = "off", expand = FALSE) +
   scale_y_continuous(labels = scales::comma) +
   scale_x_reverse() +
   guides(color = FALSE, fill = FALSE) +
   theme(axis.line=element_blank(),
         axis.text.x=element_blank(),
         axis.text.y=element_blank(),
         axis.ticks=element_blank(),
         axis.title.x=element_blank(),
         axis.title.y=element_blank(),
         legend.position="none",
         panel.background=element_blank(),
         panel.border=element_blank(),
         panel.grid.major=element_blank(),
         panel.grid.minor=element_blank(),
         panel.grid.major.x = element_line( size=.1, color="grey" ),
         panel.grid.minor.x = element_line( size=.1, color="grey" ),
         plot.title=element_text(size=25, hjust=0.5, face="bold", colour="grey", vjust=-1),
         plot.subtitle=element_text(size=18, hjust=0.5, face="italic", color="grey"),
         plot.caption =element_text(size=8, hjust=0.5, face="italic", color="grey"),
         plot.background=element_blank(),
         plot.margin = margin(2,2, 2, 4, "cm"))


anim = staticplot + transition_states(date, transition_length = 4, state_length = 1) +
   view_follow(fixed_x = TRUE)  +
   labs(title = 'Cases by zone : {closest_state}',  
        subtitle  =  "Kinshasa"
        )



animate(anim, 102, fps = 3,  width = 1200, height = 1000, 
        renderer = gifski_renderer("simulation_bar.gif"))


animate(anim, 102, fps = 5,  width = 1200, height = 1000,
        renderer = ffmpeg_renderer()) -> for_mp4
anim_save("simulation_bar.mp4", animation = for_mp4 )



