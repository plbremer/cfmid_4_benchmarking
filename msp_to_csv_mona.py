#this function receives an msp file and reads through it and isolates individual spectra based on blank lines in the file
#it sends a spectrum to parse_spectrum for parsing and writing to the csv file
def isolate_spectra(library_headers):

    #declare empty list for lines from file
    current_spectrum_text_chunk=[]

    #check if we have reached a break
    break_line_reached=0

    #go through each line in the msp file
    #if the line is not a breakline, set the break_line_reached value to false
    #if the line is the first break line, call the parser, update the break line reached to true, clear the chunk
    #if the line is the a second or more break line, do nothing (no if statement)
    for line in msp_file_object:
        if(line != '\n' ):
            break_line_reached=0
            #note that trailing \n removed
            current_spectrum_text_chunk.append(line.rstrip())
        elif(line == '\n' and break_line_reached==0):
            parse_spectrum(current_spectrum_text_chunk,library_headers)
            break_line_reached=1
            current_spectrum_text_chunk.clear()
        
#receives: spectrum chunk of text, list of headers
#outputs: nothing returned, write to file
#this function receives a single spectrum chunk of text
#it creates a dictionary where the keys are the current .msp file's attributes and the values are null
#it goes through the text chunk and assigns values to they keys where it finds the keys
#after that, it creates a list for the mass/intensity peaks
#it then writes the dictionarys values followed by the list to an CSV
def parse_spectrum(spectrum_text, library_headers):

    #create dictionary from NIST headers
    this_spectrums_dictionary={key: None for key in library_headers}
    
    #create empty peak list
    mass_intensity_annotation_list=[]

    #scroll through each line in this spectrum's text
    #if the first character is non-numeric, do a dictionary attribute action (split, assign value)
    #if the first character is numeric, append mass, spectrum, and annotation to peak list
    for line in spectrum_text:
        if not line[0].isdigit():
            #everything after the first colon is the value, so we set the max occurence to 1
            key,value=line.split(': ',1)
            this_spectrums_dictionary[key]=value
        else:
            this_peak=line.split()
            #append mperz then append intensity
            #add a noise filter right now
            if float(this_peak[1]) > 5.0:
                mass_intensity_annotation_list.append(this_peak[0])
                mass_intensity_annotation_list.append(this_peak[1])

    #write the values to file
    #if a dictionary value is None, write it as null
    for header in library_headers:
        if (this_spectrums_dictionary[header]==None):
            csv_file_object.write('null¬')
        else:
            csv_file_object.write(this_spectrums_dictionary[header]+'¬')
    #write the mass, relative intensities, and annotations to file, keep remaining ones empty
    for element in mass_intensity_annotation_list:
        csv_file_object.write(element+'¬')
    csv_file_object.write('\n')

#a list of all possible attributes for a spectrum collected from the nist17 and nist20 databases respectively
#nist_17_headers=['CAS#', 	'Collision_energy', 	'Collision_gas', 	'DB#', 	'ExactMass', 	'Formula', 	'InChIKey', 	'Instrument', 	'Instrument_type', 	'Ion_mode', 	'Ionization', 	'MW', 	'NIST#', 	'Name', 	'Notes', 	'Num Peaks', 	'PrecursorMZ', 	'Precursor_type', 	'Sample_inlet', 	'Spectrum_type', 	'Synon']
#nist_20_headers=['CASNO', 	'Collision_energy', 	'Collision_gas', 	'Comment', 	'ExactMass', 	'Formula', 	'ID', 	'In-source_voltage', 	'InChIKey', 	'Instrument', 	'Instrument_type', 	'Ion_mode', 	'Ionization', 	'Link', 	'MW', 	'NISTNO', 	'Name', 	'Notes', 	'Num peaks', 	'PrecursorMZ', 	'Precursor_type', 	'Related_CAS#', 	'Sample_inlet', 	'Spectrum_type', 	'Synon', 	'msN_pathway']
mona_headers=['Name', 'Synon', 'DB#', "InChIKey", "Precursor_type","Spectrum_type","PrecursorMZ","Instrument_type","Instrument","Ion_mode","Collision_energy","Formula","MW","ExactMass","Comments","Num Peaks"]

#a list of mass, intensity headers
peak_headers=[]
for i in range(0,1000):
    peak_headers.append('mperz'+str(i))
    peak_headers.append('intensity'+str(i))

#file to be parsed
msp_file_object=open('/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/starting_files/MoNA-export-VF-NPL_QExactive.msp','r')

#file to be written to
#append mode
csv_file_object=open('/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/mona_vfnpl_csv.csv','a')

#add headers to csv file
for header in mona_headers:
    csv_file_object.write(header+'¬')
for header in peak_headers:
    csv_file_object.write(header+'¬')
csv_file_object.write('\n')

#start
isolate_spectra(mona_headers)