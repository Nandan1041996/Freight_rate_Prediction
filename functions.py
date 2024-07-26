import pandas as pd
import numpy as np
from exception import MissingColumnError


def validate_columns(df, df_name, required_columns):
    """
    Validate if DataFrame `df` contains all `required_columns`.

    Args:
    - df (pd.DataFrame): DataFrame to validate.
    - df_name (str): Name of the DataFrame (for error messages).
    - required_columns (list): List of column names that must be present in `df`.

    Raises:
    - ValueError: If any required column is missing in `df`.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    print('misssing column',missing_columns)
    if missing_columns:
        raise   ValueError(f"{df_name} is missing the following required columns: {', '.join(missing_columns)}")





# def diesel_inc_dec_percentage(new_price,old_price,add_perc = 10):
#     diff = new_price-old_price
    
#     percentage_increase = (diff * 1.1)/old_price
#     return percentage_increase



def fraight_rate_calculation(current_fraight_file,dest_dict_file,main_file,perc_increase):
    try:
        # to read excel file "Current Freight Rate.XLSX"
        current_freight_df = pd.read_excel(current_fraight_file)

        c_frt_not_avail_col_lst =[]
        required_cols = ['Plant','Final Destination','Dest. Desc.','MODE','Direct Road Freight']
        for col in required_cols:
            if not col in  current_freight_df.columns:
                c_frt_not_avail_col_lst.append(col)

        if len(c_frt_not_avail_col_lst) !=0:
            raise MissingColumnError(c_frt_not_avail_col_lst,'Current Freight Rate File')
        # current_freight_df = pd.read_excel("Current Freight Rate.XLSX")
        # get unique final destinations
        lst = current_freight_df['Final Destination'].unique()

        # read excel file "Destination Distance.XLSX"
        dest_dict_df = pd.read_excel(dest_dict_file)

        dest_frt_not_avail_col_lst =[]
        required_cols = ['Direct Road Freight Rate','Description','Plant','Mode of Transport','Distance in KM']
        for col in required_cols:
            if not col in  dest_dict_df.columns:
                dest_frt_not_avail_col_lst.append(col)

        if len(dest_frt_not_avail_col_lst) !=0:
            raise MissingColumnError(dest_frt_not_avail_col_lst,'Destination Freight Rate File')

        # merge Two df to calculate the operation 
        final_df = current_freight_df.merge(dest_dict_df,left_on=['Final Destination','Dest. Desc.','Plant','MODE'],right_on=['Direct Road Freight Rate','Description','Plant','Mode of Transport'])

        # took required columns 
        final_df1 = final_df[['Plant','Dest. Desc.','Final Destination','MODE','Distance in KM','Direct Road Freight']]

        # to get per Km Price
        final_df1['per_km_price'] =final_df1['Direct Road Freight']/final_df1['Distance in KM']

        # read excel 25 Gujarat Frt from 01.04.2024_Propose.xlsx
        main_df = pd.read_excel(main_file)

        main_frt_not_avail_col_lst =[]
        required_cols = ['Sr. No.','Destination','State','Route','Kms / Ex Sutrapada','Final Freight from 19.08.2021','Freight per Ton/KM','Proposed Final Freight incrd/ decrd per MT from 15.03.2024','Proposed Final Freight/MT  from 15.03.2024','Freight per Ton/KM','Increased/ Decreased in %']
        for col in required_cols:
            if not col in  main_df.columns:
                main_frt_not_avail_col_lst.append(col)

        if len(main_frt_not_avail_col_lst) !=0:
            raise MissingColumnError(main_frt_not_avail_col_lst,'Old Freight Rate File')

        # to get unique destination
        unique_destination = main_df['Destination'].unique()

        # some destination has two value saperated by '/'
        lst =[]
        for i in unique_destination:
            if '/' in i:
                lst.append(i)

        # for mapping values for main df 
        dest_dict = {}
        for i in lst:
            dest_dict[i] = i.split('/')

        # df_lst contains list of dataframe 
        df_lst =[]
        for k,v in dest_dict.items():
            aa = main_df[main_df['Destination']==k]
            for i in v:
                print(i)
                b = aa.copy()
                b.loc[:,'Destination'] = i
            df_lst.append(b)

        # perform join operation     
        sep_dictmain_df = pd.concat(df_lst)

        # combine sep_dictmain_df with main_df1
        main_df1 = pd.concat([main_df,sep_dictmain_df],axis=0)

        # remove all 'Nan' destination 
        for i in lst:
            main_df1.replace({'Destination':{i:np.nan}},inplace=True)

        # set 'Sr. No.' as index
        main_df1.set_index('Sr. No.',inplace=True)
        main_df1.reset_index(drop=True,inplace=True)


        # remove all Nan values from destination column
        main_df1.dropna(subset=['Destination'],inplace=True)
        main_df1.reset_index(drop=True,inplace=True)

        # get all unique destination lst
        main_df1_lst = main_df1['Destination'].unique()

        unique_dest_lst  = final_df1['Dest. Desc.'].unique()

        for i in main_df1_lst:
            if i in unique_dest_lst:
                print(i)

        # perc_increase = diesel_inc_dec_percentage(92,91.86)

        final_df1['proposed_price'] = final_df1['Direct Road Freight']+final_df1['Direct Road Freight']* perc_increase
        final_df1['Proposed_per_km_price'] = final_df1['proposed_price']/final_df1['Distance in KM']
        final_df1['Diff_bw_old_propose_rate'] = final_df1['proposed_price'] - final_df1['Direct Road Freight']

        


        return final_df1
    except MissingColumnError as e:
        return e