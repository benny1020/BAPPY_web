def list_to_str(li):
    if len(li)==1:
        return str(li[0])
    for i in range(len(li)):
        li[i]=str(li[i])
    return ','.join(li)
# "1,2,3,4"->[1,2,3,4]
def str_to_li(db_str):
    return db_str.split(',')




li = []
print(list_to_str(li)=="")
li = [1,2]
print(list_to_str(li))
li = ["1","2"]
print(list_to_str(li))

str = "1,2,3"
print(str_to_li(str))
str="1"
print(str_to_li(str))
str=""
print(str_to_li(str))
