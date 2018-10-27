from prettytable import PrettyTable
class database():
    """
    Database class for storing the database
    """

    def __init__(self, metafile_name):
        self.metafile_name = metafile_name
        self.table_names = []
        self.column_names = []
        self.tables = {}
        lines = []
        with open(metafile_name) as f:
            for line in f:
                lines.append(line.rstrip())
        i = 0
        while i != len(lines):
            if lines[i] == "<begin_table>":
                i += 1
                current_table_name = lines[i]
                self.table_names.append(lines[i])
                i += 1
                columns = []
                while lines[i] != "<end_table>":
                    columns.append(current_table_name + "." + lines[i])
                    self.column_names.append(current_table_name + "." + lines[i])
                    i += 1
                self.tables[current_table_name] = table(current_table_name, columns, ".csv")
            i += 1

    def add_table(self, newtable):
        self.table_names.append(newtable.table_name)
        self.tables[newtable.table_name] = newtable

class table():
    """
    Table class
    """
    def __init__(self, table_name, columns, file_extention):
        self.table_name = table_name
        self.columns = columns
        self.column_storage = {}
        self.number_of_records = 0
        for col_name in columns:
            self.column_storage[col_name] = []
        if file_extention != '':
            self.insert_records(file_extention)

    def insert_records(self, file_extention):
        file_name = self.table_name + file_extention
        print(file_name)
        records = []
        with open(file_name) as f:
            for line in f:
                record = line.rstrip().replace("\'", "").replace("\"", "").split(",")
                record = [int(i) for i in record]
                records.append(record)
        f.close()
        self.number_of_records = len(records)
        i = 0
        for col_name in self.columns:
            column_record = [records[j][i] for j in range(self.number_of_records)]
            self.column_storage[col_name] = column_record
            i += 1

    def has_column(self, column_name):
        if column_name in self.column_storage:
            return True
        else:
            return False

    def get_column(self, column_name):
        return self.column_storage[column_name]

    def print_table(self, operator):
        t = PrettyTable()
        operator = operator * len(self.columns)
        print("Table Name : " + self.table_name)
        i = 0
        for col in self.columns:
            t.add_column(self.table_name + "-" + col, operator[i](self.column_storage[col]))
            i += 1
        print(t)









#
# database1 = database('metadata.txt')
#
# print(database1.tables['table1'].table_name)
