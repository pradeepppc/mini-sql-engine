# import sqlparse
# sql = 'select ppc from table1 where id = 1'
# res = sqlparse.parse(sql)
# stmt = res[0]
# print(stmt.get_real_name())
import re

# table_names = ['ppc', 'pradeep', 'cool']
# tab = table_names[:2]
# print(tab)

# str = 'ppca'
# lis = str.split(".")
# print(lis)
# sql = 'select  distinct table1.A,table2.B from table1'
# ag_op = re.search('select(.*)from', sql).group(1).strip()
# s = re.search("select(.*)from",sql)
# sq_st = re.search(r"\((.*)\)", sql)
# if sq_st is not None:
#     print(sq_st.group(1))
# print(s.group(1).strip() + "ppc")
# sel_col_strs = [x.strip() for x in ag_op.split(",")]
# print(sel_col_strs)

# l = []
#
# if True:
#     l = [1,2,3]
# else:
#     pass
#
# print(l)



# sql = "select table1.A from table1 where table1.A = 20 and table1.B = 30"
# q_str = []
# if re.search('where',sql) == None:
#     q_str = "True"
# else:
#     q_str = re.search('where(.*)', sql).group(1).strip()
#     q_str = q_str.split(" ")
#     print(q_str)
#     # cond_split = re.split('(\W)', q_str)
#     # print(cond_split)

# colname = 'table1.A'
# colname = colname.split(".")
# print(colname)


# sql = '1 == 1 and 2 == 2'
# if eval(sql):
#     print("hurray")
# else:
#     print("fail")

# lis = ['a','b','c']
# stri = 'ppc'
# lis2 = [stri]
# l = lis2 + lis
# print(l)

q = {}
q['ppc'] = 'll'
print(q['ppc'])