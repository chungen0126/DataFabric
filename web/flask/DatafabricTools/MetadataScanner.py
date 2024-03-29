from DBMSAccessor import DBMSAccessor
from DatafabricManager import TableManager

def scan(username: str, password: str, ip: str, port: str, dbms: str, db: str = None, tables: list = None) -> list:
    """Scan all the tables in dbms. Then import result to datafabric.TableInfo

    Args:
        username (str): Username of DBMS
        password (str): Password of DBMS
        ip (str): IP/Hostname of DBMS
        port (str): Port of DBMS. Note that for Oracle it can be like '1521/sid'
        dbms (str): Name of DBMS, e.g. 'MySQL', will be converted to lowercase.
        db (str): Desired DB in DBMS. If set to None, then scan all possible DBs.
        tables (list): Desired Tables in DBs. If set to None, then scan all possible Tables.

    Returns:
        list: The scanned table infos
    """

    dbms = dbms.lower()

    scanned = []

    if db is None:
        try:
            dbs = DBMSAccessor.list_dbs(username, password, ip, port, dbms)
        except:
            return scanned
    else:
        dbs = [db]

    if tables is None:
        for db in dbs:
            try:
                tables = DBMSAccessor.list_tables(username, password, ip, port, dbms, db)
            except:
                continue
            for table in tables:
                try:
                    columns = DBMSAccessor.list_columns(username, password, ip, port, dbms, db, table)
                    columns = ','.join(columns)
                    scanned.append({
                        'Connection' : f'{ip}:{port}',
                        'DBMS' : dbms,
                        'DB' : db,
                        'TableName' : table,
                        'Columns' : columns
                    })
                except:
                    continue
    else:
        for db in dbs:
            for table in tables:
                try:
                    columns = DBMSAccessor.list_columns(username, password, ip, port, dbms, db, table)
                    columns = ','.join(columns)
                    scanned.append({
                        'Connection' : f'{ip}:{port}',
                        'DBMS' : dbms,
                        'DB' : db,
                        'TableName' : table,
                        'Columns' : columns
                    })
                except:
                    continue
    
    return scanned


def scan_and_import(username: str, password: str, ip: str, port: str, dbms: str, db: str = None, tables: list = None) -> list:
    """Scan all the tables in dbms. Then import result to datafabric.TableInfo

    Args:
        username (str): Username of DBMS
        password (str): Password of DBMS
        ip (str): IP/Hostname of DBMS
        port (str): Port of DBMS. Note that for Oracle it can be like '1521/sid'
        dbms (str): Name of DBMS, e.g. 'MySQL', will be converted to lowercase.
        db (str): Desired DB in DBMS. If set to None, then scan all possible DBs.
        tables (list): Desired Tables in DBs. If set to None, then scan all possible Tables.

    Returns:
        list: The table_id of added table infos
    """

    dbms = dbms.lower()

    added_ids = []
    scanned   = scan(username, password, ip, port, dbms, db, tables)
    for table_info in scanned:
        added_ids.append(
            TableManager.add_table_info(
                table_info['Connection'], table_info['DBMS'], table_info['DB'], table_info['TableName'], table_info['Columns']
            )
        )

    return added_ids
