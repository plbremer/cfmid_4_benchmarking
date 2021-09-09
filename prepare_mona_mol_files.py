import pandas

import os

def parse_sdf_into_numerically_named_mol_files(sdf_address,base_mol_address):

    mol_file_counter=0
    start_new_file=True
    sdf_file=open(sdf_address,'r')

    #add on to make my life easier
    inchistring_list=list()

    for line in sdf_file:

        if start_new_file:
            temp_mol_file=open(base_mol_address+'mol_file_'+str(mol_file_counter)+'.mol','w')
            start_new_file=False
            #hold=input('hold')

        if 'InChI=InChI=' in line[0:12]:
            inchistring_list.append(line)

        if '$$$$' not in line:
            temp_mol_file.write(line)
        elif '$$$$' in line:
            temp_mol_file.close
            start_new_file=True
            mol_file_counter+=1

    return inchistring_list

def get_parallel_list_of_inchikey(lookup_table_address,temp_inchistring_list):
    lookup_panda=pandas.read_csv(lookup_table_address,sep='¬',quoting=3,usecols=['InChIKey','Comments'])

    lookup_panda['inchistring']=(lookup_panda['Comments'].str.split(n=1,expand=True))[0]
    
    

    inchikey_list=list()

    for temp_inchistring in temp_inchistring_list:

        if 'computed' in temp_inchistring:
            temp_inchistring_sans_computed=temp_inchistring[9:]
        else:
            temp_inchistring_sans_computed=temp_inchistring


        temp_panda_subset=lookup_panda.loc[ lookup_panda['inchistring'] == ('\"'+(temp_inchistring_sans_computed.strip())+'\"')]
        temp_corresponding_inchikey=temp_panda_subset.iloc[0,0]
        inchikey_list.append(temp_corresponding_inchikey)

    return inchikey_list

def rename_mol_files(base_mol_address,temp_inchikey_list):

    for i in range(0,len(temp_inchikey_list)):
        os.system('mv '+base_mol_address+'mol_file_'+str(i)+'.mol'+' '+base_mol_address+temp_inchikey_list[i]+'.mol')

if __name__ == "__main__":

    sdf_file_address='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/starting_files/MoNA-export-VF-NPL_QExactive.sdf'

    mol_file_directory_address='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/mol_files/'

    inchistring_list=parse_sdf_into_numerically_named_mol_files(sdf_file_address,mol_file_directory_address)

    lookup_table_address='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/mona_vfnpl_csv.csv'

    inchikey_list=get_parallel_list_of_inchikey(lookup_table_address,inchistring_list)

    rename_mol_files(mol_file_directory_address,inchikey_list)

