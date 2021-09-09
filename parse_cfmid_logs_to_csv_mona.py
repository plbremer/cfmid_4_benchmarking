#this script reads a directory's worth of log files (spectra at three energies) from cfmid
#and puts them into a large csv vile
#InChIKey   Energy  mperz0  intensity0  ... ... mperz1040   intensity1040
#1040 was the max number of peaks observed for any spectrum for nist20
#so we also have a counter to count the max number of peaks observed in any cfmid spectrum
#this is just printed to output

import os
import pandas as pd


#starts with a directory full of log files
#iterates
#outputs a csv with the headers
#InChIKey   Energy  mperz0  intensity0  ... ... mperz1040   intensity1040



log_file_directory=('/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/cfmid_operated_on_mona/[M+H]+/myout/')

cfmid_output_csv=open('/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/cfmid_operated_on_mona/mona_cfmid_final_output_[M+H]+.csv','w')

#list of headers
peak_headers=list()
for i in range(0,1041):
    peak_headers.append('mperz'+str(i))
    peak_headers.append('intensity'+str(i))

#print headers to csv file
cfmid_output_csv.write('InChIKey¬')
cfmid_output_csv.write('energy#¬')
for header in peak_headers:
    cfmid_output_csv.write(header+'¬')
cfmid_output_csv.write('\n')

#keeps track of max number of spectra
max_peak_count_so_far=0

#iterate through all log files
for log_file in os.listdir(log_file_directory):
    
    log_file_inchikey=log_file[:-4]
    temp_logfile=open(log_file_directory+log_file,'r')

    #skip the first two lines in each log file
    next(temp_logfile)
    next(temp_logfile)
    #only for vfnpl predictions
    #next(temp_logfile)
    #next(temp_logfile)    


    #we know that the first line we care about is energy0, so fake read it and go to next line
    #then set the rest of the variables that are for one particular energy/spectrum to "empty"
    current_energy='energy0'
    next(temp_logfile)
    current_mperz_list=list()
    current_intensity_list=list()
    current_peak_count=0

    #for the rest of the file
    #read through
    for line in temp_logfile:
        #if we hit a new energy
        if 'energy' in line:
            #write the current spectrum to file
            cfmid_output_csv.write(log_file_inchikey+'¬')
            cfmid_output_csv.write(current_energy+'¬')
            for i in range(0,len(peak_headers)):
                if i < len(current_mperz_list):
                    cfmid_output_csv.write(current_mperz_list[i]+'¬')
                    cfmid_output_csv.write(current_intensity_list[i]+'¬')
                else:
                    cfmid_output_csv.write('¬')
            cfmid_output_csv.write('\n')
            
            #check if the current peak count is greater than the global max, if so, update it and print it (for fun)
            if (current_peak_count>max_peak_count_so_far):
                max_peak_count_so_far=current_peak_count

            #reset all the current stuff
            current_mperz_list=list()
            current_intensity_list=list()
            current_peak_count=0        

            #get the energy from the line        
            current_energy=line.strip('\n')
        
        #if the line is the last line which is always blank, do the same thing as reaching a new energy
        #except for reassinging the energy
        elif line=='\n':
            #write the current spectrum to file
            cfmid_output_csv.write(log_file_inchikey+'¬')
            cfmid_output_csv.write(current_energy+'¬')
            for i in range(0,len(peak_headers)):
                if i < len(current_mperz_list):
                    cfmid_output_csv.write(current_mperz_list[i]+'¬')
                    cfmid_output_csv.write(current_intensity_list[i]+'¬')
                else:
                    cfmid_output_csv.write('¬')
            cfmid_output_csv.write('\n')
                     
            #check if the current peak count is greater than the global max, if so, update it and print it (for fun)
            if (current_peak_count>max_peak_count_so_far):
                print(current_peak_count)
                max_peak_count_so_far=current_peak_count

            #reset all the current stuff
            current_mperz_list=list()
            current_intensity_list=list()
            current_peak_count=0        

        #if we arent at a new energy or the "end of file blank line", if we are just at another peak
        #add the peak to the current spectrum/energy peak list
        #increase the current peak counter
        else:
            current_mperz_list.append(line.split()[0])
            current_intensity_list.append(line.split()[1])
            current_peak_count+=1
