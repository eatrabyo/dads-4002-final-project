import os
from query import query_trans_id_list,query_trans_by_id
from delete_func import delete_trans
from engine import main_db

def delete_transaction_tbl():
    while True:
        os.system('clear') # 'clear' on mac, for windows 'cls'
        try:
            # asking user which transaction to update
            trans_id = input('Please enter transaction id: ')
            trans_list = query_trans_id_list(main_db)

            # check if transaction id match from our db
            if trans_id in trans_list:
                #query transaction info base on id
                trans_df = query_trans_by_id(main_db,trans_id)

                # list for store primary key
                main_tbl_id = trans_df.reset_index()['id'].to_list()

                print("\n",trans_df,"\n")

                while True:
                        try:
                            row_id = int(input('\nWhich row would you like to delete: '))
                            if row_id in main_tbl_id:
                                break
                            else:
                                os.system('clear') # 'clear' on mac, for windows 'cls'
                                print(f'Please enter valid row id for {trans_id}.\n')
                                print(trans_df)
                                continue
                        except:
                            os.system('clear') # 'clear' on mac, for windows 'cls'
                            print(f'Please enter valid row id for {trans_id}.\n')
                            print(trans_df)
                            continue
                # delete that row
                delete_trans(engine=main_db,row_id=row_id)
                #show new data
                new_trans_df = query_trans_by_id(main_db,trans_id)
                if len(new_trans_df) == 0:
                    print(f"\nAll data for {trans_id} has been deleted.\n")
                else:
                    print("\n",new_trans_df,"\n")

            else:
                raise
        except:
            print('Please enter valid transaction id.')
            continue

        # loop for asking update more or no
        while True:
            loop_to_main = input("Would you like to delete more? (Y/N): ").lower()
            if loop_to_main in ['y','n']:
                break
            else:
                continue
        if loop_to_main == 'y':
            continue
        elif loop_to_main == 'n':
            break

