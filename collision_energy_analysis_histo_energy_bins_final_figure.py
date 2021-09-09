import numpy
import pandas
import seaborn
import matplotlib.pyplot
import re
import sys

adduct=sys.argv[1]
instrument=sys.argv[2]
cfmid_energy_list=['energy0','energy1','energy2']
instrument_brand='Orbitrap Fusion Lumos'
bin_count=int('200')
base_output_path='/home/rictuar/coding_projects/fiehn_work/text_files/_figures_for_publication/collision_energy/output_files'

column_labels=["999 to 950","949 to 900","899 to 850","849 to 800",
"799 to 750","749 to 700","699 to 650","649 to 600",
"599 to 550","549 to 500","499 to 450","449 to 400",
"399 to 350","349 to 300","299 to 250","249 to 200",
"199 to 150","149 to 100","99 to 50","49 to 0"]


def transform_collision_energy_column(temp_panda,temp_instrument,temp_instrument_brand):
    if (temp_instrument=='qtof'):
        return temp_panda, 'Collision_energy'
    
    elif (temp_instrument=='itft'):
        temp_panda.insert(loc=len(temp_panda.columns),column='Collision_energy_itft',value=35)
        return temp_panda, 'Collision_energy_itft'

    elif ((temp_instrument=='hcd') and (temp_instrument_brand=='Orbitrap Fusion Lumos')):
        temp_panda.insert(loc=len(temp_panda.columns),column='Collision_energy_hcd_lumos_NCE_only',value=-1)

        for index,row in temp_panda.iterrows():
            #if the collision energy column contains eV, skip it
            if 'eV' in row['Collision_energy']:
                continue
            else:

                temp_panda.loc[index,'Collision_energy_hcd_lumos_NCE_only']=float((re.findall(r'[0-9]+',row['Collision_energy']))[0])

        #############################if lumos and hcd##################################
        #subset panda to make rest of script still work
        ##############################################################################
        temp_panda=temp_panda.loc[temp_panda['Collision_energy_hcd_lumos_NCE_only'] != -1]
        #############################if lumos and hcd##################################
        #divide column by precursor mz to figure out normalization
        ##############################################################################        
        temp_panda['Collision_energy_hcd_lumos_NCE_only']=temp_panda['Collision_energy_hcd_lumos_NCE_only'].multiply(temp_panda['PrecursorMZ'])
        return temp_panda, 'Collision_energy_hcd_lumos_NCE_only'


def bin_column(temp_panda, temp_column_name, temp_bin_count):
    column_bin_integers=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count,labels=False)
    column_bin_edges=pandas.cut(x=temp_panda[temp_column_name],bins=temp_bin_count)
    
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bins',value=column_bin_integers)
    temp_panda.insert(loc=len(temp_panda.columns),column=temp_column_name+'_bin_edges',value=column_bin_edges)
    return temp_panda[temp_column_name+'_bin_edges'].cat.categories
    #return column_bin_edges


# get the averages of each bin
def get_average_of_bin_column(temp_panda,temp_column_name, temp_bin_count,temp_cfmid_energy):
    temp_bin_value_list=list()
    temp_subset_population_list=list()
    
    for i in range(0,temp_bin_count):
        subset_experimental_collision=temp_panda.loc[temp_panda[temp_column_name+'_bins'] == i]
        subset_cfmid_energy=subset_experimental_collision.loc[subset_experimental_collision['energy#'] == temp_cfmid_energy]

        temp_average=subset_cfmid_energy['dot_product'].mean()

        temp_subset_population=len(subset_cfmid_energy.index)

        if numpy.isnan(temp_average):
            temp_average=1.
        if numpy.isnan(temp_subset_population):
            temp_subset_population=0

        temp_bin_value_list.append(1-temp_average)
        temp_subset_population_list.append(temp_subset_population)
    return temp_bin_value_list,temp_subset_population_list

LABEL_LIST=list()
LIST_OF_AVERAGES=list()
HIST_LABELS='to_be_replaced'

for cfmid_energy in cfmid_energy_list:
    input_address='/home/rictuar/coding_projects/fiehn_work/text_files/orthogonal_snakemake/'+adduct+'/'+instrument+'/precursor_yes/binned_distances_'+adduct+'_'+instrument+'_precursor_yes.txt'
    input_panda=pandas.read_csv(input_address,sep='¬')
    input_panda,new_collision_energy_name=transform_collision_energy_column(input_panda,instrument,instrument_brand)
    edges=bin_column(input_panda,new_collision_energy_name,bin_count)
    bin_value_list,bin_population_list=get_average_of_bin_column(input_panda,new_collision_energy_name,bin_count,cfmid_energy)
    ###############get histogram labels#################
    histo_labels=list()
    
    x_label_counter=0
    for edge in edges:
        
        #####################MODIFIED FOR HCD########################
        temp_edge=str(edge)
        first_edge=temp_edge.split(', ')[0]
        second_edge=temp_edge.split(', ')[1]
        first_edge=first_edge[1:]
        second_edge=second_edge[:-1]
        first_edge_rounded=round(float(first_edge))
        second_edge_rounded=round(float(second_edge))

        histo_labels.append('('+str(first_edge_rounded)+' '+str(second_edge_rounded)+']')
        x_label_counter+=1



    histo_labels=list(histo_labels)

    #######add shit to global variable carriers#########
    LIST_OF_AVERAGES.append(bin_value_list)
    HIST_LABELS=histo_labels
    LABEL_LIST.append(adduct+' '+instrument+' '+cfmid_energy)
    ####################################################

LABEL_LIST=['CFM-ID Energy 10','CFM-ID Energy 20','CFM-ID Energy 40']


####################prepare histogram image#######################################
matplotlib.rcParams['font.family'] = 'Avenir'
matplotlib.pyplot.rcParams['font.size'] = 18
matplotlib.pyplot.rcParams['axes.linewidth'] = 2

my_figure = matplotlib.pyplot.figure(figsize=(6.69292, 8))

matplotlib.pyplot.xlabel('Experimental Collision Energies')
matplotlib.pyplot.ylabel('Average Dot Product')

#######################modified for HCD###############################3
n,bins,patches=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count) for temp in range(0,3)],weights=LIST_OF_AVERAGES,bins=bin_count,histtype='step',linewidth=3)
#cut to one half
print(bin_count/2)
#n,bins,patches=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count/4) for temp in range(0,3)],weights=[LIST_OF_AVERAGES[0][0:50],LIST_OF_AVERAGES[1][0:50],LIST_OF_AVERAGES[2][0:50]],bins=int(bin_count/4),histtype='step',linewidth=3)
##########################################################################




#transpose for plot
print(LIST_OF_AVERAGES)
LIST_OF_AVERAGES=numpy.array(LIST_OF_AVERAGES)
LIST_OF_AVERAGES=LIST_OF_AVERAGES.T

my_axes=matplotlib.pyplot.gca()


#######################MODIFIED FOR HCD###############################
my_axes.set_xticks(numpy.arange(0,bin_count))
#my_axes.set_xticks(numpy.arange(0,int(bin_count/4)))
my_axes.set_xticklabels(HIST_LABELS,rotation=-90)
#my_axes.set_xticklabels(HIST_LABELS[0:50],rotation=-90)
######################################################################

my_axes.set_yticks(numpy.arange(0,1,0.2))
y_plot_labels=['0','200','400','600','800','999']

matplotlib.pyplot.legend(LABEL_LIST,loc='upper center')

matplotlib.pyplot.savefig('/home/rictuar/collision_energy_'+instrument+'_'+adduct+'.eps',bbox_inches="tight")
matplotlib.pyplot.savefig('/home/rictuar/collision_energy_'+instrument+'_'+adduct+'.png',bbox_inches="tight")
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.show()


#make the population inset
my_figure=matplotlib.pyplot.figure(figsize=(3.5,3))

max_population_value=max(bin_population_list)
bin_population_list=[bin_population_list[i]/max_population_value for i in range(0,len(bin_population_list))]

#######################MODIFIED FOR HCD###############################
n2,bins2,patches2=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count) for temp in range(0,1)],weights=bin_population_list,bins=bin_count,histtype='bar',linewidth=3)
#n2,bins2,patches2=matplotlib.pyplot.hist(x=[numpy.arange(0,bin_count/4) for temp in range(0,1)],weights=bin_population_list[0:50],bins=int(bin_count/4),histtype='bar',linewidth=3)
######################################################################


matplotlib.pyplot.xlabel('Bin')
matplotlib.pyplot.ylabel('Relative Population')
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig('/home/rictuar/collision_energy_'+instrument+'_'+adduct+'_inset.eps')
matplotlib.pyplot.savefig('/home/rictuar/collision_energy_'+instrument+'_'+adduct+'_inset.png')

matplotlib.pyplot.show()
