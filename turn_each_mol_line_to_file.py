#takes the nist 20 .sdf .json dump and makes n .mol files
nist_20_mol_file=open('/home/rictuar/coding_projects/fiehn_work/text_files/NIST20_msms_moldata.json','r')

for line in nist_20_mol_file:
    inchikey=line.split(sep="\"")[1]
    full_file=line.split(sep="\\n")
    output_mol_file=open('/home/rictuar/coding_projects/fiehn_work/text_files/_nist_20_mol_files/'+inchikey+'.mol','w')
    for sub_line in full_file:
        output_mol_file.write(sub_line+'\n')
    output_mol_file.close()
