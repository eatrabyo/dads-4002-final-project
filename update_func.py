from sqlalchemy import exc, text


def update_email(engine,cus_id,email):
    try:
        if email != '':
            with engine.begin() as conn:
                sql = f"""
                UPDATE customer SET email = '{email}'
                WHERE id = {cus_id}
                """
                
                conn.execute(text(sql))
            print('Finished update new email.')
        else:
            with engine.begin() as conn:
                sql = f"""
                UPDATE customer SET email = NULL
                WHERE id = {cus_id}
                """
                
                conn.execute(text(sql))
            print('Finished update new email.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_phone(engine,cus_id,phone):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE customer SET phone_number = '{phone}'
            WHERE id = {cus_id}
            """
            
            conn.execute(text(sql))
        print('Finished update new phone number.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_stock(engine,product_id,stock):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE product SET stock = {stock}
            WHERE id = '{product_id}'
            """
            
            conn.execute(text(sql))
        print('Finished update new stock.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_prod_cost(engine,product_id,cost):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE product SET product_cost = {cost}
            WHERE id = '{product_id}'
            """
            
            conn.execute(text(sql))
        print('Finished update new cost.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_product_main(engine,row_id,product_id):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE main SET product_id = '{product_id}'
            WHERE id = {row_id}
            """
            
            conn.execute(text(sql))
        print('Finished revised product id.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_customer_main(engine,trans_id,cus_id):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE main SET customer_id = '{cus_id}'
            WHERE transaction_id = '{trans_id}'
            """
            
            conn.execute(text(sql))
        print('Finished revised customer id.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)
def update_purchasing_time_main(engine,trans_id,purchasing_time):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE main SET purchasing_time = '{purchasing_time}'
            WHERE transaction_id = '{trans_id}'
            """
            
            conn.execute(text(sql))
        print(f'Finished revised purchasing time for {trans_id}.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_product_price_main(engine,row_id,product_price):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE main SET price_per_unit = {product_price}
            WHERE id = {row_id}
            """
            
            conn.execute(text(sql))
        print('Finished revised product price.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_product_unit_main(engine,row_id,product_unit):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE main SET unit = {product_unit}
            WHERE id = {row_id}
            """
            
            conn.execute(text(sql))
        print("Finished revised product's selling unit.")
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_address(engine,trans_id,postal,district,province):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE main SET destination_district = '{district}',
            destination_province = '{province}', postal_code = '{postal}'
            WHERE transaction_id = '{trans_id}'
            """
            
            conn.execute(text(sql))
        print("Finished revised postal code, district, and province.")
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)