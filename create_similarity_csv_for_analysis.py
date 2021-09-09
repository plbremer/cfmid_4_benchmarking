import numpy
import pandas
#this is the file that contains our dot product code
import Daphnis.distance_methods.methods

#input parameters
cfmid_csv_address='/home/rictuar/coding_projects/fiehn_work/text_files/_cfmid_4_point_0_spectra_for_experimental_comparison/cfmid_output_csv_nist20_only_adduct_[M+H]+_msrb_relaced.csv'
empirical_csv_address='/home/rictuar/coding_projects/fiehn_work/text_files/nist20_hr_csv.txt'
adduct_of_interest='[M+H]+'
instrument_of_interest='_null_'
#the list of inchikeys the the experimental spectra must be in (nist20 only)
inchikey_nist20_only_address='/home/rictuar/coding_projects/fiehn_work/text_files/_attribute_values_and_counts/set_comparison_nist_20_only_InChIKey.txt'
number_of_metadata_columns=26
distance_method='dot_product'
classyfire_results_address='/home/rictuar/coding_projects/fiehn_work/text_files/_cfb_classyfire_results/classy_fire_results_csv.csv'
output_dataset_address='/home/rictuar/coding_projects/fiehn_work/text_files/_orthogonal_analysis_similarity_only/overall_similarity_result_dot_product_[M+H]+.csv'
cfmid_energy_list=['energy0','energy1','energy2']

#build the dict that will hold our new panda
#read in the experimental panda, 1 row to get columns
experimental_panda_one_row=pandas.read_csv(empirical_csv_address,sep='@@@',usecols=range(0,number_of_metadata_columns),nrows=1)
#declare dictionary using columns in experimental panda
output_dictionary={key: [] for key in experimental_panda_one_row.columns}
#add the classyfire, cfmid energy, and distance output keys
output_dictionary['energy#']=[]
output_dictionary['Superclass']=[]
output_dictionary[distance_method]=[]




#receives a link to a file that is single row after single row, returns set of entries
def read_single_list_to_set(file_address):

    temp_file=open(file_address,'r')

    line_set=set()

    for line in temp_file:
        line_set.add(line.rstrip())

    return line_set

inchikey_set_nist_20=read_single_list_to_set(inchikey_nist20_only_address)

#read in the cfmid panda
cfmid_panda=pandas.read_csv(cfmid_csv_address,sep='¬',header=0)

#set of things cfmid fragmented
cfmid_fragmented_set=set(cfmid_panda['InChIKey'])

#ready in the classyfire_panda
classyfire_panda=pandas.read_csv(classyfire_results_address,sep='\t',header=0,usecols=['InChIKey','Superclass'])

#this function receives a spectrum with mperz/intensity followed by NaN
#returns an array of [mass, intensity] pairings
def prepare_row_for_daphnis(received_spectrum):
    is_nan=~numpy.isnan(received_spectrum)
    received_spectrum_no_nan=received_spectrum[is_nan]
    received_spectrum_pair_list=list()
    for i in range(0,len(received_spectrum_no_nan),2):
        received_spectrum_pair_list.append([received_spectrum_no_nan[i],received_spectrum_no_nan[i+1]])
    received_spectrum_pair_array=numpy.array(received_spectrum_pair_list)
    return received_spectrum_pair_array

#normalize an empircal spectrum to 100
def normalize_daphnis_spectrum(raw_spectrum):
    normalization_constant=max(raw_spectrum[:,1])
    for mass_intensity_pair in raw_spectrum:
        mass_intensity_pair[1]=100*(mass_intensity_pair[1])/normalization_constant
    
    return raw_spectrum

#takes a cfmid panda, an inchikey and an energy, returns a spectrum
#the spectrum is a numpy array [mperz intensity mperz intensity mperz intensity]
def lookup_spectrum_on_cfmid_panda(cfmid_panda, inchikey, energy):
    #get the row that we care about
    temp_row=cfmid_panda.loc[ (cfmid_panda['InChIKey']==inchikey) & (cfmid_panda['energy#']==energy) ]

    spectrum_extracted=numpy.array( temp_row.iloc[0,2:62] , dtype=float )

    return spectrum_extracted

#read in the experimental panda
#experimental_panda_iterator=pandas.read_csv(empirical_csv_address,sep='@@@',chunksize=5000,nrows=10000)
experimental_panda_iterator=pandas.read_csv(empirical_csv_address,sep='@@@',chunksize=5000)
chunk_counter=0
for chunk in experimental_panda_iterator:
    
    chunk_counter+=1

    #go through each row
    for index,row in chunk.iterrows():
       
        if (row['Precursor_type'] != adduct_of_interest ):        
            continue
        
        if (row['InChIKey'] not in inchikey_set_nist_20):
            continue

        #check to see if CFMID fragmented
        if (row['InChIKey'] not in cfmid_fragmented_set):

            print(row['InChIKey'])

            continue

        #extract spectrum from row
        experimental_spectrum_extracted=numpy.array( row.iloc[number_of_metadata_columns:] , dtype=float )

        #prepare experimental spectrum for daphnis
        experimental_spectrum_for_daphnis=prepare_row_for_daphnis(experimental_spectrum_extracted)

        #normalize experimental spectrum
        experimental_spectrum_for_daphnis_normalized=normalize_daphnis_spectrum(experimental_spectrum_for_daphnis)

        #extract inchikey so that we can get experimental spectrum
        temp_inchikey=row['InChIKey']
        
        #iterate through all three energies of cfmid for each experimental row
        for temp_energy in cfmid_energy_list:
        
            #find equivalent cfmid spectrum (this is only an inchikey match)
            #extract cfmid spectrum
            matching_cfmid_spectrum=lookup_spectrum_on_cfmid_panda(cfmid_panda, temp_inchikey, temp_energy)

            #prepare cfmid spectrum for daphnis
            matching_cfmid_spectrum_daphnis=prepare_row_for_daphnis(matching_cfmid_spectrum)


            #SOMETHING TO APPEND
            #send both spectra to daphnis to get similarity score
            temp_dist = Daphnis.distance_methods.methods.distance(experimental_spectrum_for_daphnis_normalized, 
                                            matching_cfmid_spectrum_daphnis, method=distance_method,
                                            normalize_result=True, spectrum_refined=False,
                                            ms2_ppm=10)

            #SOMETHING TO APPEND
            #get classyfire class
            classy_fire_row_panda=classyfire_panda.loc[  classyfire_panda['InChIKey']==temp_inchikey  ]
            temp_class=classy_fire_row_panda['Superclass'].item()

            #add this row to the dictionary that we will typecast to panda
            #go through columns, add value
            for column_name in experimental_panda_one_row.columns:
                output_dictionary[column_name].append(row[column_name])
            #add the three things that are new
            output_dictionary['energy#'].append(temp_energy)
            output_dictionary['Superclass'].append(temp_class)
            output_dictionary[distance_method].append(temp_dist)



#typecast dict to panda
output_panda=pandas.DataFrame.from_dict(output_dictionary)
output_panda.to_csv(output_dataset_address,sep='¬',index=False)
