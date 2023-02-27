import argparse, json

def get_keys(j_ob, tablename):
    column_name_set = set()
    for item in j_ob:
        print(item)
        for cname in item.keys():
            column_name_set.add(cname)
    return column_name_set

def getDatatype(_var):
    if type(_var) == str:
        return "varchar(100)"
    elif type(_var) == int:
        return "integer"

def sqlize(jsonfile):
    with open(jsonfile, 'r') as fp:
        jf = json.load(fp)
        tablename = jf["tablename"]
        unique_fields = jf["unique_fields"]
        not_nullable_fields = jf["not_nullable_fields"]
        column_names = get_keys(jf["data"], tablename)
        print(column_names)
        sql_string_list = []

        for column_name in column_names:
            if column_name in unique_fields:
                unique = "unique"
            else:
                unique = ""

            if column_name in not_nullable_fields:
                nullable = "not null"
            else:
                nullable = "" 
            
            dataType = getDatatype(column_name)
            
            sql_string = f"{column_name} {dataType} {nullable} {unique}"
            sql_string_list.append(sql_string)

        sql_statement = f"create table if not exists {tablename} ({','.join(sql_string_list)});"
    
    return(sql_statement)