import pandas

input_file_location='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/mona_vfnpl_csv.csv'
output_file_location_pos='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/inchikey_list_flattened_m+h.txt'
output_file_location_neg='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/inchikey_list_flattened_m-h.txt'



inchikey_panda=pandas.read_csv(input_file_location,sep='¬',usecols=['InChIKey','Precursor_type'],quoting=3)

pos_panda=inchikey_panda[ inchikey_panda['Precursor_type'] == '[M+H]+' ]

neg_panda=inchikey_panda[ inchikey_panda['Precursor_type'] == '[M-H]-' ]


def flatten_inchikey_list(list_3d):
    flattened_list=list()
    for key in list_3d:
        blocks=key.split('-')
        flattened_list.append(blocks[0]+'-UHFFFAOYSA-N')
    return flattened_list

#set to remove dupes then list to make list
inchikey_3d_list_pos=list(set(pos_panda['InChIKey'].tolist()))
inchikey_3d_list_neg=list(set(neg_panda['InChIKey'].tolist()))

inchikey_2d_list_pos=flatten_inchikey_list(inchikey_3d_list_pos)
inchikey_2d_list_neg=flatten_inchikey_list(inchikey_3d_list_neg)

output_file=open(output_file_location_pos,'w')
for inchikey in inchikey_2d_list_pos:
    output_file.write(inchikey+'\n')
output_file.close()

output_file=open(output_file_location_neg,'w')
for inchikey in inchikey_2d_list_neg:
    output_file.write(inchikey+'\n')
output_file.close()