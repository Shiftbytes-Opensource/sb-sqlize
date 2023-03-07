import argparse, json, re

alternateDValueNames = {
    "boolean" : [ "yes", "no", "true", "false", "y", "n", "t", "f", "none", "null", "undefined", 1, 0 ]
}

dTypeConversionMap = {
    "boolean" : "string",
    "float" : "string",
    "integer" : "string"
}

def get_keys(j_ob, tablename):
    column_name_set = set()
    for item in j_ob:
        print(item)
        for cname in item.keys():
            column_name_set.add(cname)
    return column_name_set

def getDtype(dtype):
    print (dtype)
    varlen = None
    vartype =  dtype.split('(')[0]

    d = re.search('\((.*)\)', dtype)

    if not d:
        if vartype in ["string", "varchar"]:
            varlen = 50
    else:
        varlen = d.group(1)
    
    if vartype == "string":
        vartype = "varchar"

    return vartype, varlen 

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
            
            vartype, varlen = getDtype(jf["data_type_map"][column_name])
            
            if not varlen:
                varlen = ""
            else:
                varlen = f"({varlen})"

            dataType = f"{vartype}{varlen}"
            
            sql_string = f"{column_name} {dataType} {nullable} {unique}"
            sql_string_list.append(sql_string)

        sql_statement = f"create table if not exists {tablename} ({','.join(sql_string_list)});"
    
    return(sql_statement)