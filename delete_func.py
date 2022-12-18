from sqlalchemy import exc, text


def delete_trans(engine,row_id):
    try:
        with engine.begin() as conn:
            sql = f"""
            delete from main
            WHERE id = {row_id}
            """
            
            conn.execute(text(sql))
        print(f'Finished delete row: {row_id}.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)