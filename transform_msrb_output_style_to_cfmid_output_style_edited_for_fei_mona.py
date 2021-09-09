#the motivation for this script is to transform the msrb raw output log files to be like the
#cfmid raw output log files
#i wrote a parser, parse_cfmid_logs_to_csv.py that will take all of the cfmid raw output .log files
#and sew them together into a .csv
#this script takes one place for the unedited files, one place for the edited files

from os import listdir
from shutil import move
from os import rename

#the purpose of this functin is to receive the two paths, and call the editor for each file.
#the editor wil create a copy that is edited and leave it in the same directory
#after going through all the raw files, the guide_transformation function will move all of the files to the
#new directory
#new files will be have _edited appended to their filename, the file will be moved, and then the _edited will
#be removed
def guide_transformation_of_files(path_to_unedited,path_to_edited):

    msrb_raw_file_list=listdir(path_to_unedited)

    for file_name in msrb_raw_file_list:
        truncate_spectral_file(path_to_unedited+file_name)
        move(path_to_unedited+file_name+'_edited',path_to_edited+file_name+'_edited')
        rename(path_to_edited+file_name+'_edited',path_to_edited+file_name)


#this method receives a single msrb log file and cuts off information that wasnt present in the 
#cfmid-like log files. it puts _edited onto the end of the new file
def truncate_spectral_file(path_to_file):
    raw_file=open(path_to_file,'r')
    edited_file=open(path_to_file+'_edited','w+')


    #the first four lines are comments and are handled on a custom basis
    #the adduct type and inchikey lines are deleted as they are in the title
    #the msrb version and smile are kept
    #skip the first and fourht lines
    i=0
    for line in raw_file:
        if i==0:
            i+=1
            continue
        elif i==3:
            i+=1
            continue
        #if the first character is still #, its one of the comments that we want
        elif line[0] == '#':
            edited_file.write(line)
        #if the first character is 'e' i.e. energy0, write the whole line
        elif line[0] == 'e':
            edited_file.write(line)
        #if the line is numeric, aka an mperz and an intensity, copy it
        #but drop the annotations
        elif line[0].isnumeric():
            edited_file.write(line.split()[0]+' '+line.split()[1]+'\n')
        #if we get to an empty line, then the file is done
        elif line == '\n':
            break
        i+=1
    edited_file.write("\n")
    raw_file.close()
    edited_file.close()




directory_of_edited_files=('/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/msrb_results/like_cfmid_log_files/')
directory_of_unedited_files=('/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/msrb_results/original_log_files/')

guide_transformation_of_files(directory_of_unedited_files,directory_of_edited_files)
