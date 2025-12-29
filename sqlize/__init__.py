
import json
from utils import clogs

class RequiredParamsNotFound(Exception):
    pass

class DataTypeNotSupported(Exception):
    pass

class FiltersNeededToDelete(Exception):
    pass

class Sqlize(clogs):

    allowedConditions = ["and", "or"]

    def __init__(self,logger = None):
        clogs.__init__(self, logger = logger)
        # self.logger = logger
        self.log("Initializing SQL Query Generator.")

    # def print(self, message):
    #     if not self.logger:
    #         print("Logger not initialized.")
    #         print(message)
    #         return
    #     self.logger.info(message)

    def getDatatype(self, _var):
        if _var in ["string", "email", "mobile_number", "apikey"]:
            return "varchar(100)"
        
        if _var in ["password"]:
            return "bytea"
        
        if _var == "uid":
            return "varchar(64)"
        
        if _var in ["nested_object", "list"]:
            return "jsonb"
        
        if _var == "text":
            return "text"
        
        if _var == "datetimetz":
            return "timestamptz"
        
        if _var == "bool":
            return "boolean"
        
        if _var in ["price", "percent"]:
            return "decimal"
    
    def generate_where_statements(self, filter_attributes, condition = "and"):
        # conditions = [f"{key} = '{val}'" for key, val in filter_attributes.items()]
        if not condition in self.allowedConditions:
            self.log(f"condition {condition} not in allowed list {self.allowedConditions}")
            return False
        conditions = []
        for key, val in filter_attributes.items():
            if isinstance(val, str):
                c = f"{key} = '{val}'"

            if isinstance(val, list):
                qvals = [f"'{sval}'" for sval in val]
                c = f"{key} in ({','.join(qvals)})"

            if val in ["null", None]:
                c = f"({key} is null or {key}='')"

            conditions.append(c)

        if condition == "and":
            where_statement = f'where {" and ".join(conditions)}'
        elif condition == "or":
            where_statement = f'where {" or ".join(conditions)}'
        return where_statement

    def database_exists(self, dbname):
        sql_statement = f"select datname from pg_database where datname = '{dbname}';"
        self.log(f"Generated Query : {sql_statement}")
        return sql_statement
    
    def create_database(self, dbname):
        sql_statement = f"create database {dbname};"
        self.log(f"Generated Query : {sql_statement}")
        return sql_statement

    def table_exists(self, tablename):
        sql_statement = f"select table_name from information_schema.tables where table_name = '{tablename}';"
        self.log(f"Generated Query : {sql_statement}")
        return sql_statement
    
    def get_entries(self, tablename, columns, filter_attributes = {}, condition = "and", limit = 100):
        where_statement = ""

        if filter_attributes:
            where_statement = self.generate_where_statements(filter_attributes, condition)
        
        limitquery = f"limit {limit}"

        sql_statement = f"select {','.join(columns)} from {tablename} {where_statement} {limitquery};"
        
        self.log(f"Generated Query : {sql_statement}")
        return sql_statement
        
    def insert_entry_in_table(self, tablename, jd):
        vals = ','.join(f"{w}" if isinstance(w, bytes) or isinstance(w, dict) else f"'{w}'" for w in [json.dumps(val) if type(val) == dict or type(val) == list else val for val in list(jd.values())])
        sql_statement = f"insert into {tablename}({','.join(list(jd.keys()))}) values ({vals});"
        self.log(f"Generated Query : {sql_statement}")
        return sql_statement

    def delete_entries_in_table(self, tablename, filter_attributes ={}):
        if not filter_attributes:
            raise FiltersNeededToDelete("No filters provided to delete from table.")
        
        sql_statement = f"delete from {tablename} {self.generate_where_statements(filter_attributes)}"
        self.log(f"Generated Query : {sql_statement}")
        return sql_statement
    
    def update_entry_in_table(self, tablename, jd, filter_attributes = {}):
        where_statement = ""

        vals = ",".join([f"{key} = '{value}'" for key, value in jd.items() ])

        if filter_attributes:
            where_statement = self.generate_where_statements(filter_attributes)

        sql_statement = f"update {tablename} set {vals} {where_statement};"

        self.log(f"Generated Query : {sql_statement}")
        return sql_statement

    def create_table(self, jd, create_pkey = True):
        tablename = jd["name"]
        attributes = jd["attributes"]
        sql_string_list = []
 
        for attribute in attributes:
            
            unique = ""
            nullable = ""

            if not "name" in attribute or not "type" in attribute:
                raise RequiredParamsNotFound("Required params not found in one of the attributes")

            attr_name = attribute["name"]
            attr_type = attribute["type"]

            if "unique" in attribute:
                if attribute["unique"]:
                    unique = "unique"

            if not "nullable" in attribute:
                attribute["nullable"] = False
            
            if not attribute["nullable"]:
                nullable = "not null"

            dataType = self.getDatatype(attr_type)

            if not dataType:
                raise DataTypeNotSupported(f"data type not supported for {attr_name} - {attr_type}")

            sql_string = f"{attr_name} {dataType} {nullable} {unique}"
            sql_string_list.append(sql_string)

        if create_pkey:
            sql_string_list.append('id serial primary key')

        sql_statement = f"create table if not exists {tablename} ({','.join(sql_string_list)});"
        self.log(f"Generated Query : {sql_statement}")
        return sql_statement


# def database_exists(dbname):
#     s = Sqlize()
#     q = s.database_exists(dbname)
#     return q

# def create_database(dbname):
#     s = Sqlize()
#     return s.create_database(dbname)

# def table_exists(tablename):
#     s = Sqlize()
#     return s.table_exists(tablename)

# def create_table_sql(jd):
#     s = Sqlize()
#     return s.create_table(jd)

# def insert_entry_in_table_sql(tablename, jd):
#     s = Sqlize()
#     return s.insert_entry_in_table(tablename, jd)

# def get_entries_sql(tablename, columns, filter_attributes, condition, limit):
#     s = Sqlize()
#     return s.get_entries(tablename, columns, filter_attributes, condition, limit)

# def delete_entries_sql(tablename, filter_attributes):
#     s = Sqlize()
#     return s.delete_entries_in_table(tablename, filter_attributes)

# def update_entries_sql(tablename, data, filter_attributes={}):
#     s = Sqlize()
#     return s.update_entry_in_table(tablename, data, filter_attributes)
