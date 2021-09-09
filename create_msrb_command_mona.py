#the motivation for this script is to create several giant command that will get the msrb docker
#tool to print every single compound when possible
#the reason for this is that the msrb docker does not accept .sdf files

import os
mol_files_path='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/mol_files'
list_of_files_to_try=os.listdir(mol_files_path)

os.chdir(mol_files_path)

#we want to run all of the predictions in convenient sets
#conveniently, for both Nist20-only and vfnpl, the number
#of compounds has a pleasant breakdown of factors (not prime)
#2286 files, 18*127
#there are 15958 .mol files, 79*202=15958
for i in range(0,18):
    command='sudo docker run --rm=true -v $("pwd"):/root/output -it wishartlab/cfmid:latest sh -c "cd /root/output; '
    for j in range (0,127):
        current_index=i*127+j
        command=command+'java -jar /opt/msrb/msrb-fragmenter.jar -isdf '+list_of_files_to_try[current_index]+' -o /root/output >> output_from_msrb.txt; '
    command=command+'\"'
    print(command)
    os.system(command)

