#usage
#specify an input csv (nist 20)
#specify an output csv
#specify the location of n number of text files, one for each metadata attribute, that contain the set of attribute values that are acceptable
#specify a parallel list of metadata headers
import numpy as np
import pandas as pd

#receives a list of locations of csv files
#returns a list of sets
#always chooses first column
#assumes no header as there is a parallel header list and it does no harm to have an extra element in the set
#assumes comma sep
def make_list_of_sets(sets_locations):

    list_of_sets=[]

    for set_location in sets_locations:
        temp_column_panda=pd.read_csv(set_location, header=None, sep=',', usecols=[0],squeeze=True)
        list_of_sets.append(set(temp_column_panda))

    return list_of_sets


#receives an input and output csv location
#receives a list of sets to check and a parallel list of headers
#goes through the first csv in chunks
def construct_abridged_csv(nist_csv_location,abridged_csv_location,list_of_sets,list_of_headers):

    input_csv_iterator=pd.read_csv(nist_csv_location,engine='python',chunksize=1000,sep='@@@')

    subset_counter=0

    #the way that it has to work is we will have nested for loops for each condition
    #we break up the incoming csv into chunks for memory purposes
    for chonk in input_csv_iterator:
        
        print(subset_counter)
        subset_counter+=1
        #we have to initialize the tmp panda once outside the nested loop so we can use it mutliple times
        temp_panda=chonk
        #we do a subset reduction for each condition that we have. we could do one if we had a static set of conditions
        #instead we have nested reductions
        for i in range (0,len(list_of_sets)):
        #    temp_panda=
            temp_panda=temp_panda.loc[temp_panda[list_of_headers[i]].isin(list_of_sets[i])]

        #clean up temp panda, drop index, drop last row
        temp_panda.drop(temp_panda.columns[[-1]],axis=1,inplace=True)

        #write chunk to file, if this is the first time writing to file, include headers    
        with open(abridged_csv_location, 'a') as f:
            temp_panda.to_csv(f, index=None, mode='a', header=f.tell()==0, sep='¬')

#this is a list of the sets of values that a particular metadata type must have in order to be included
must_contain_sets_locations=[
'/home/rictuar/coding_projects/fiehn_work/text_files/_attribute_values_and_counts/attribute_values_inchikey_msrbONLY.txt',
#'/home/rictuar/coding_projects/fiehn_work/text_files/attribute_values_instrument_type_qtof.txt']
#'/home/rictuar/coding_projects/fiehn_work/text_files/attribute_values_ion_mode_negative.txt']
#'/home/rictuar/coding_projects/fiehn_work/text_files/attribute_values_precursor_type_+.txt',
'/home/rictuar/coding_projects/fiehn_work/text_files/_attribute_values_and_counts/attribute_values_spectrum_type_ms2.txt']

#this is the parallel list of headers for the sets that we narrow down by
#list_of_headers=['InChIKey','Instrument_type','Ion_mode','Precursor_type','Spectrum_type']
list_of_headers=['InChIKey','Spectrum_type']

nist_csv_location='/home/rictuar/coding_projects/fiehn_work/text_files/nist20_hr_csv.txt'
abridged_csv_location='/home/rictuar/coding_projects/fiehn_work/text_files/subset_inchikey_msrb.txt'

#call set list maker
list_of_sets=make_list_of_sets(must_contain_sets_locations)


construct_abridged_csv(nist_csv_location,abridged_csv_location,list_of_sets,list_of_headers)