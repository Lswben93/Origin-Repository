import mysql.connector
import json

DB=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1015",
    database="taipei-attractions",
    charset='utf8'
)
def getData():
    jsonFilePath="D:/wehelp/week8/Origin-Repository/data/taipei-attractions.json"
    with open(jsonFilePath,encoding="utf-8") as file:
        lines=file.readline()
        data=json.loads(lines)
        return data

def dataSave(data):
    try: 
        newdata=data["result"]["results"]
        for needData in newdata:
            name=needData["stitle"]
            category=needData["CAT2"]
            description=needData["xbody"]
            address=needData["address"]
            transport=needData["info"]
            mrt=needData["MRT"]
            latitude=needData["latitude"]
            longitude=needData["longitude"]
            replace=needData["file"].replace('jpghttps','jpg,https').replace('JPGhttps','JPG,https')
            split=replace.split(",")
            image=split[0]
            mycursor=DB.cursor()
            sql="INSERT INTO informations (name,category,description,address,transport,mrt,latitude,longitude,image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql,(name,category,description,address,transport,mrt,latitude,longitude,image))
            DB.commit()
    except Exception as e:
        DB.rollback()
        print(str(e))

if __name__ == "__main__":
    a=getData()
    dataSave(a)
        
