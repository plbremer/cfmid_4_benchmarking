import pandas

#this file takes an msrb file and a cfmid file
#it goes through the msrb file, and, if the adduct matches the specified adduct
#and the mass/intensity row is not null
#it replaces the mass/intensity values in the cfmid panda


##############################################
#####MUST SET ADDUCT TO MATCH CFMID FILE######
###############################################
cfmid_address='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/cfmid_operated_on_mona/mona_cfmid_final_output_[M+H]+.csv'
msrb_address='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/msrb_results/mona_msrb_results.csv'
adduct_we_want='[M+H]+'
output_address='/home/rictuar/coding_projects/fiehn_work/text_files/mona_vfnpl/cfmid_operated_on_mona/mona_cfmid_final_output_[M+H]+_msrb_replaced.csv'

msrb_panda=pandas.read_csv(msrb_address,delimiter='¬',index_col=False)


cfmid_panda=pandas.read_csv(cfmid_address,delimiter='¬',index_col=False)
cfmid_column_list=cfmid_panda.columns


####ADDED FOR MONA
msrb_panda.drop(labels='Unnamed: 2085',axis='columns',inplace=True)
cfmid_panda.drop(labels='Unnamed: 2084',axis='columns',inplace=True)

for index,row in msrb_panda.iterrows():

    
    if (pandas.notnull(row['mperz0']) and row['adduct']==adduct_we_want):   

        #find the index of the cfmid panda with the same inchikey and energy
        temp_index=cfmid_panda.index[ (cfmid_panda['InChIKey']==row['InChIKey']) & (cfmid_panda['energy#']==row['energy#'])   ]
        #so we make a temp series, drop the adduct column
        #temp_series=msrb_panda.iloc[index]
        temp_series=row.copy(deep=True)
        temp_series.drop(labels='adduct',inplace=True)

        cfmid_panda.iloc[temp_index[0]]=temp_series

#print the updated panda
cfmid_panda.to_csv(output_address,sep='¬',index=False)
