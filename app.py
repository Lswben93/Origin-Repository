from flask import *
import mysql.connector
import decimal
import json
from flask import request
import os
from dotenv import load_dotenv
load_dotenv()

DB=mysql.connector.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    database=os.getenv("database"),
	auth_plugin='mysql_native_password',
    charset='utf8'
)


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        super(JsonEncoder,self).default(obj)

app=Flask(__name__)
app.secret_key="a4d8ad18qf8wf"
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions",methods=["GET"])
def name():
	page=request.args.get("page")
	nextpage=int(page)+1
	name=request.args.get("name")
	mycursor=DB.cursor(dictionary=True)
	
	if name!=None:
		strsql = "SELECT id,name,category,description,address,transport,mrt,latitude,longitude,image FROM informations WHERE name LIKE '%"+ name +"%' LIMIT " + str(12*int(page)) + ",12"
		mycursor.execute(strsql)
		result=mycursor.fetchall()
		if result==[]:
			return {
  				"error": True,
  				"message": "查無資料"
				}
		else:
			
			strj = "{\"nextpage\":"+str(nextpage)+",\"data\":["
			for row in result:
				id=row["id"]
				name=row["name"]
				category=row["category"]
				description=row["description"]
				address=row["address"]
				transport=row["transport"]
				mrt=row["mrt"]
				latitude=json.dumps(row["latitude"], cls=JsonEncoder,ensure_ascii=False)
				longitude=json.dumps(row["longitude"], cls=JsonEncoder,ensure_ascii=False)
				images=row["image"].decode("utf-8")
				newimage=images.replace('jpghttps','jpg,https').replace('JPGhttps','JPG,https')
				newimages=newimage.split(",")
				strj += "  {\"id\":" + str(id) + ","
				strj += "  \"name\":\"" + name + "\","
				strj += "  \"category\":\"" + category + "\","
				strj += "  \"description\":\"" + description + "\","
				strj += "  \"address\":\"" + address + "\","
				strj += "  \"transport\":\"" + transport + "\","
				strj += "  \"mrt\":\"" + mrt + "\","
				strj += "  \"latitude\":" + str(latitude) + ","
				strj += "  \"longitude\":" + str(longitude) + ","
				strj += "  \"image\":" + str(newimages).replace("'","\"") + "},"
				
			strj = strj[:len(strj)-1]
			strj += "]}"
			return strj
	else:
		strsql = "SELECT id,name,category,description,address,transport,mrt,latitude,longitude,image FROM informations  LIMIT " + str(12*int(page)) + ",12"
		mycursor.execute(strsql)
		result=mycursor.fetchall()
		strj = "{\"nextpage\":"+str(nextpage)+",\"data\":["
		for row in result:
			id=row["id"]
			name=row["name"]
			category=row["category"]
			description=row["description"]
			address=row["address"]
			transport=row["transport"]
			mrt=row["mrt"]
			latitude=json.dumps(row["latitude"], cls=JsonEncoder,ensure_ascii=False)
			longitude=json.dumps(row["longitude"], cls=JsonEncoder,ensure_ascii=False)
			images=row["image"].decode("utf-8")
			newimage=images.replace("jpghttps","jpg,https").replace("JPGhttps","JPG,https")
			newimages=newimage.split(",")
			strj += "  {\"id\":" + str(id) + ","
			strj += "  \"name\":\"" + name + "\","
			strj += "  \"category\":\"" + category + "\","
			strj += "  \"description\":\"" + description + "\","
			strj += "  \"address\":\"" + address + "\","
			strj += "  \"transport\":\"" + transport + "\","
			strj += "  \"mrt\":\"" + mrt + "\","
			strj += "  \"latitude\":" + str(latitude) + ","
			strj += "  \"longitude\":" + str(longitude) + ","
			strj += "  \"image\":" + str(newimages).replace("'","\"") + "},"
				
		strj = strj[:len(strj)-1]
		strj += "]}"
		return strj

				
		
		

@app.route("/api/attraction/<id>",methods=["GET"])
def getId(id):
	if id=="":
		return {
  				"error": True,
  				"message": "請輸入景點編號"
				}
	else:
		mycursor=DB.cursor(dictionary=True)
		strsql = "SELECT id,name,category,description,address,transport,mrt,latitude,longitude,image FROM informations WHERE id = "+ str(id) +" "
		mycursor.execute(strsql)
		result=mycursor.fetchall()
		if result==[]:
			return {
  				"error": True,
  				"message": "景點編號不正確"
				}
		else:
			
			strj = "{\"data\":{"
			for row in result:
				id=row["id"]
				name=row["name"]
				category=row["category"]
				description=row["description"]
				address=row["address"]
				transport=row["transport"]
				mrt=row["mrt"]
				latitude=json.dumps(row["latitude"], cls=JsonEncoder,ensure_ascii=False)
				longitude=json.dumps(row["longitude"], cls=JsonEncoder,ensure_ascii=False)
				images=row["image"].decode("utf-8")
				newimage=images.replace('jpghttps','jpg,https').replace('JPGhttps','JPG,https')
				newimages=newimage.split(",")
				strj += "  \"id\":" + str(id) + ","
				strj += "  \"name\":\"" + name + "\","
				strj += "  \"category\":\"" + category + "\","
				strj += "  \"description\":\"" + description + "\","
				strj += "  \"address\":\"" + address + "\","
				strj += "  \"transport\":\"" + transport + "\","
				strj += "  \"mrt\":\"" + str(mrt) + "\","
				strj += "  \"latitude\":" + str(latitude) + ","
				strj += "  \"longitude\":" + str(longitude) + ","
				strj += "  \"image\":" + str(newimages).replace("'","\"") + "}"
		return strj


app.run(host="0.0.0.0",port=3000)