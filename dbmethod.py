import sqlite3

class Joke:
    def __init__(self,id,content,count):
        self.id = id
        self.content = content
        self.count = count


#导出
def exportJoke(conn, filename):
    c = conn.cursor()
    results = c.execute("select * from joke")
    with open(filename, 'a', encoding="utf8") as load_f:
        for row in results:
            load_f.write(row[1]+"|\n")


#导入
def dumpJoke(conn,filename):
    c = conn.cursor()
    with open(filename, 'r',encoding="utf8") as load_f:
        arr = load_f.read().split('|')
        for msg in arr:
            if msg.strip() != "":
                c.execute("insert into joke (content) values (?)",(msg,))
    conn.commit()

#Distinct
def distinctJoke(conn):
    c = conn.cursor()
    #read table data to memory to joke_list
    results = c.execute("select * from joke")
    joke_list = []
    for row in results:
        joke_list.append(Joke(row[0],row[1].replace(' ','').replace('\n',''),row[2]))

    joke_list.sort(key=takeCount, reverse=True)
    #distinct the joke_list
    for index,org in reversed(list(enumerate(joke_list))):
        for j in reversed(range(index)):
            if org.content == joke_list[j].content:
                deleteFromDatabase(conn, org.id)
                break

def takeCount(element):
    return element.count

def deleteFromDatabase(conn, id):
    c = conn.cursor()
    c.execute("DELETE from joke where id=?",(id,))
    conn.commit()

#This function can import for other module
def getJoke():
    conn = sqlite3.connect('wechat_auto.db')
    c = conn.cursor()
    result = c.execute("select * from joke order by count asc").fetchone()
    c.execute("update joke set count=count+1 where id=?",(result[0],))
    conn.commit()
    conn.close()
    return (result[1].strip(),result[2])

def getStatus(conn):
    c = conn.cursor()
    results = c.execute("select count from joke")
    for row in results:
        print(row[0])
    count = c.execute("select count(*) from joke").fetchone()[0]
    print(count)

if __name__ == '__main__':
    conn = sqlite3.connect('wechat_auto.db')
    #先导入
    dumpJoke(conn,'storage/joke')
    #再去重
    distinctJoke(conn)
   
    conn.close()