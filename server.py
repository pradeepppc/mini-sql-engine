from database import *
import re, sys

class query():
    """
    class for query
    """
    def __init__(self, db, sql_query):
        self.sql_query = sql_query
        self.db = db
        self.query_table_names = []
        self.query_column_names = []
        self.query_where_dict = {}

    def check_col_name(self, column_name):
        colname_list = column_name.split(".")

        if column_name in self.db.column_names and colname_list[0] in self.db.table_names and column_name in self.db.tables[colname_list[0]].columns:
            return column_name
        else:
            return None


    def get_columns(self, Q):
        select_str = re.search('select(.*)from', Q).group(1).strip()
        selected_columns = []
        if select_str == "*":
            return selected_columns
        else:
            m = re.search(r"\((.*)\)", select_str)
            if m is None:
                col_list_parser = select_str.split(",")
                for col in col_list_parser:
                    if self.check_col_name(col) is not None:
                        selected_columns.append(self.check_col_name(col))
                    else:
                        print('Column does not exist or invalid sql syntax')
                        sys.exit(0)
            else:
                col_name = m.group(1)
                if self.check_col_name(col_name) is not None:
                    selected_columns.append(self.check_col_name(col_name))
                else:
                    print('Invalid select statement or error in column name')
                    sys.exit(0)

        return selected_columns

    def get_tables(self, Q):
        selected_tables = []
        if re.search('where', Q) is None:
            query = re.search('from(.*)', Q).group(1).strip().split(",")
        else:
            query = re.search('from(.*)where', Q).group(1).strip().split(",")
        for table in query:
            if table in self.db.table_names:
                selected_tables.append(table)
            else:
                print('Invalid select statement or error in table name')
                sys.exit(0)

        return selected_tables

    def strip_column_name(self, col_name):
        col_name = col_name.split(".")
        if len(col_name) == 2:
            return col_name[1]
        else:
            return col_name[0]

    def mergetables(self, table_names):
        if len(table_names) == 1:
            return self.db.tables[table_names[0]]
        else:
            two_names = table_names[:2]
            table1_col_names = self.db.tables[two_names[0]].columns
            table2_col_names = self.db.tables[two_names[1]].columns
            table1_name = self.db.tables[two_names[0]].table_name
            table2_name = self.db.tables[two_names[1]].table_name
            all_column_names = table1_col_names + table2_col_names
            total_records = self.db.tables[table1_name].number_of_records * self.db.tables[table2_name].number_of_records
            merged_table_name = '_'.join(two_names)
            merged_table = table(merged_table_name, all_column_names, '')
            merged_table.number_of_records = total_records
            k = 0
            for i in range(self.db.tables[two_names[0]].number_of_records):
                for j in range(self.db.tables[two_names[1]].number_of_records):
                    for col_name in table1_col_names:
                        merged_table.column_storage[col_name].append(self.db.tables[two_names[0]].column_storage[col_name][i])
                    for col_name in table2_col_names:
                        merged_table.column_storage[col_name].append(self.db.tables[two_names[1]].column_storage[col_name][j])
                    k += 1
            self.db.add_table(merged_table)
            if len(table_names) != 2:
                l1 = [merged_table_name]
                l2 = table_names[2:]
                return self.mergetables(l1 + l2)
            else:
                return merged_table

    def check_where_in_record(self, merge_table, index, evalstring):
        if eval(evalstring):
            return True
        else:
            return False

    def select_columns(self, big_table, columns, eval_string):
        if len(columns) == 0:
            columns = big_table.columns
        totalRecords = big_table.number_of_records
        result_table = table(big_table.table_name, columns, '')
        for i in range(totalRecords):
            if self.check_where_in_record(big_table, i, eval_string):
                for col_name in columns:
                    result_table.column_storage[col_name].append(big_table.column_storage[col_name][i])
                result_table.number_of_records += 1

        return result_table

    def get_where_string(self, query):
        if re.search('where', query) is None:
            return "False"
        else:
            q_str = re.search('where(.*)', query).group(1).strip()
            return q_str

    def check_column_name_query(self, columnname):
        columnname = columnname.split(".")
        if columnname[0] in self.query_table_names:
            return True
        else:
            return False

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def remove_extra_columns(self, columns):
        new_columns = columns.copy()
        for col in new_columns:
            if col in self.query_where_dict.keys():
                if self.query_where_dict[col] in columns:
                    columns.remove(col)
        return columns

    def check_column_table(self, columns, tables):
        for col in columns:
            table_name = col.split(".")[0]
            if table_name not in tables:
                return False
        return True

    def eval_where_string(self, query):
        query = query.split(" ")
        i = 0
        condition = []
        while i != len(query):
            if query[i] in self.db.column_names:
                if i+2 < len(query):
                    if query[i+1] not in self.db.column_names and query[i+2] in self.db.column_names and query[i+1] != "and" and query[i+1] != "or":
                        self.query_where_dict[query[i]] = query[i+2]
                if self.check_column_name_query(query[i]):
                    condition.append('merge_table.column_storage[\'' + query[i] + '\'][index]')
                else:
                    print('error in column names in where statement')
                    sys.exit(0)
            elif query[i] == '=':
                condition.append('==')
            elif query[i] == 'and':
                condition.append('and')
            elif query[i] == 'or':
                condition.append('or')
            elif query[i] == '>=':
                condition.append('>=')
            elif query[i] == '>':
                condition.append('>')
            elif query[i] == '<=':
                condition.append('<=')
            elif query[i] == '<':
                condition.append('<')
            elif self.RepresentsInt(query[i]):
                condition.append(query[i])
            else:
                print('error in where condition')
                sys.exit(0)
            i += 1
        final_eval_string = ' '.join(condition)
        return final_eval_string

if __name__ == "__main__":
    db = database('metadata.txt')
    qp = query(db, "")
    print("sql>")
    Q = input()
    while Q != "q":
        query_split = Q.split(";")
        if len(query_split) != 2:
            print("Incorrect syntax")
            sys.exit(0)
        else:
            Q = query_split[0]
        if "select" in Q and "from" in Q:
            selected_columns = qp.get_columns(Q)
            selected_tables = qp.get_tables(Q)
            if qp.check_column_table(selected_columns, selected_tables):
                pass
            else:
                print('selected columns does not belong to selected tables')
                exit(0)
            qp.query_table_names = selected_tables
            qp.query_column_names = selected_columns
            where_string = qp.get_where_string(Q)
            try:
                Big_t = qp.mergetables(selected_tables)
            except IndexError:
                print("Invalid Table names")
                sys.exit(0)
            eval_where_string = []
            if where_string == 'False':
                eval_where_string = "True"
            else:
                eval_where_string = qp.eval_where_string(where_string)
            operator = []
            if len(selected_columns) == 0:
                selected_columns = Big_t.columns
            selected_columns = qp.remove_extra_columns(selected_columns)
            final_table = qp.select_columns(Big_t, selected_columns, eval_where_string)
            aggre_fun_query = re.search(r"\((.*)\)", Q)
            if aggre_fun_query is not None:
                aggre_op_query = re.search("select(.*)from", Q).group(1).strip()
                if aggre_op_query.startswith("max("):
                    operator = [lambda x: [max(x)]]
                elif aggre_op_query.startswith("min("):
                    operator = [lambda x: [min(x)]]
                elif aggre_op_query.startswith("avg("):
                    operator = [lambda x: [sum(x) * 1/len(x)]]
                elif aggre_op_query.startswith("sum("):
                    operator = [lambda x: [sum(x)]]
                elif aggre_op_query.startswith("distinct("):
                    operator = [lambda x: list(set(x))]
                else:
                    print("Syntax Error in select statement")
                    sys.exit(0)
            else:
                operator = [lambda x: x]


            final_table.print_table(operator)

        else:
            print("SQL SYNTAX ERROR")

        print("sql>")
        Q = input()


    print("Good Bye")
