#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:49:05 2020

@author: larry
"""

from weather_Handler import *
import datetime
import os
import time
import json
from flask import render_template,session,url_for,redirect
from flask import Flask ,request



app = Flask(__name__)
app.secret_key= b'asdfgbjfr'

@app.route('/',methods=['POST','GET'])
def index():
    if request.method =='POST':
        
        render_template('index.html')
    return render_template('index.html')

@app.route('/upload/',methods=['GET','POST'])
def upload():	
    basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
    dirs=os.listdir(os.path.join(basepath,session.get('username')))
    timenow = datetime.datetime.now()
    stringtime = str(timenow.year)+str(timenow.month)+str(timenow.day)
    if stringtime not in dirs:
        dirs.insert(0,stringtime)
    else:
        dirs.insert(0,'choose the folder below')
    dirs.insert(0,'Not Choose')
    
    if request.method == 'POST':
    	flist = request.files.getlist("file[]")

    	for f in flist:
    		try:
    			basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
    			format=f.filename[f.filename.index('.'):]
    			fileName=time.time()
    			if format in ('.jpg','.png','.jpeg'):
    				format='.jpg'
    			
    			

    			if request.values['folder']=='0':
    				return render_template('upload.html',alert='Please choose a folder',dirs=dirs)

    			elif request.values['folder']=='1':
    				if not os.path.isdir(os.path.join(basepath,session.get('username'),stringtime)):
    					os.mkdir(os.path.join(basepath,session.get('username'),stringtime))
    					os.mkdir(os.path.join(basepath,session.get('username'),stringtime,'text'))
    					os.mkdir(os.path.join(basepath,session.get('username'),stringtime,'photo'))
					
    				if format == '.jpg':
    					upload_path = os.path.join(basepath,session.get('username'),stringtime,'photo',str(fileName).replace('.','')+str(format))
    				
    			else:
    				
    				upload_path = os.path.join(basepath,session.get('username'),dirs[int(request.values['folder'])],'photo',str(fileName).replace('.','')+str(format))
    				
				
				
    			f.save(upload_path)
    		except:
    			return render_template('upload.html',alert='你沒有選擇要上傳的檔案',dirs=dirs)

    	return redirect(url_for('upload'))
    return render_template('upload.html',dirs=dirs)
@app.route('/logged',methods=['POST','GET'])
def logged():
    if request.method =='POST':
        render_template('logged.html')
             
    return render_template('logged.html')

@app.route('/register',methods=['POST','GET'])
def register():
	with open('./member.json','r') as file_object:
		member = json.load(file_object)
	if request.method=='POST':
		
		if request.values['username'] in member:				
			return render_template('register.html',alert='this account is used.')
		else:				
			member[request.values['username']]={'password':request.values['userpw']}
			with open('./member.json','w') as f:
				json.dump(member, f)
				basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
				os.mkdir(os.path.join(basepath,request.values['username']))
			return redirect( url_for ('index'))
	return render_template('register.html')
  

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method== 'POST' :
        with open('./member.json','r') as file_object:
            member = json.load(file_object)

        if request.values['username'] in member:
            if member[request.values['username']]['password']==request.values['userpw']:
                session['username']=request.values['username']
                return redirect( url_for ('logged'))
            else:
                return render_template('login.html',alert="Your password is wrong, please check again!")
        else:
            return render_template('login.html',alert="Your account is unregistered.")
    return render_template('login.html')

@app.route('/write', methods = ['GET','POST'])
def write():
    basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
    dirs=os.listdir(os.path.join(basepath,session.get('username')))
    timenow = datetime.datetime.now()
    stringtime = str(timenow.year)+str(timenow.month)+str(timenow.day)
    fileName=time.time()
    if stringtime not in dirs:
        os.mkdir(os.path.join(basepath,session.get('username'),stringtime))
        os.mkdir(os.path.join(basepath,session.get('username'),stringtime,'text'))
        os.mkdir(os.path.join(basepath,session.get('username'),stringtime,'photo'))
        
    if request.method== 'POST':
        content = request.values['text']
        save_path = os.path.join(basepath,session.get('username'),stringtime,'text',str(fileName)+'.txt')
        with open(save_path, "w") as text_file:
            text_file.write(content)
                
    return render_template('write.html')

@app.route('/write_dream', methods = ['GET','POST'])
def write_dream():
    basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
    dream_dir = os.listdir(os.path.join(basepath,session.get('username')))
    if 'dream' not in dream_dir:
        os.mkdir(os.path.join(basepath,session.get('username'),'dream'))
    dream_path = os.listdir(os.path.join(basepath,session.get('username'),'dream'))
    timenow = datetime.datetime.now()
    stringtime = str(timenow.year)+str(timenow.month)+str(timenow.day)
    fileName=time.time()
    if stringtime not in dream_path:
        os.mkdir(os.path.join(basepath,session.get('username'),'dream',stringtime))
        
        
    if request.method== 'POST':
        content = request.values['text']
        save_path = os.path.join(basepath,session.get('username'),'dream',stringtime,str(fileName)+'.txt')
        with open(save_path, "w") as text_file:
            text_file.write(content)
                
    return render_template('write_dream.html')

@app.route('/check', methods = ['GET','POST'])
def check():
    basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
    dirs=os.listdir(os.path.join(basepath,session.get('username')))
    if '.DS_Store' in dirs:
        dirs.remove('.DS_Store')
    if 'dream' in dirs:
        dirs.remove('dream')
    
    dirs.insert(0,'Not Choose')
    if request.method== 'POST':
        try:
            basepath = os.path.join(os.path.dirname(__file__), 'static','uploads')
        
            if request.values['folder']=='0':
                	return render_template('check.html',alert='Please choose a folder',dirs=dirs)

            	
            else:
                content_file = os.listdir(os.path.join(basepath,session.get('username'),dirs[int(request.values['folder'])],'text'))
                if '.DS_Store' in content_file:
                    	content_file.remove('.DS_Store')
                
                text_path = os.path.join(basepath,session.get('username'),dirs[int(request.values['folder'])],'text/')
                photo_file = os.listdir(os.path.join(basepath,session.get('username'),dirs[int(request.values['folder'])],'photo'))
                if '.DS_Store' in photo_file:
                    	photo_file.remove('.DS_Store')
                photo_path = os.path.join('static','uploads',session.get('username'),dirs[int(request.values['folder'])],'photo/')
            
        except:
            return render_template('check.html',dirs=dirs)
        str_article = ""
        for i in range(0,len(content_file)):
            str_content = ""
            
            with open(text_path + content_file[i], "r") as text_file:
                contents = text_file.readlines()
            for j in range(0,len(contents)):
                str_content += contents[j]
            str_article += str_content
            str_article += "</br></br>"
        
        img = ""
        for i in range(0,len(photo_file)):
            img += "<img src='../"
            img += photo_path+photo_file[i]
            img += "' width='300'>"
            img += "</br>"
                     
        return  "<h1>Dairy</h1>" \
                "<body>" \
                "<ul>" \
                "<li><a href='../check'>上一頁</a></li>" \
                "<li><a href='../'>登出</a></li>" \
                "</ul>" \
                "<p> Your diary: </p>" \
                " {} ".format(str_article) + img + \
                "</body>"         
                      
    return render_template('check.html',dirs=dirs)

@app.route('/check_dream', methods = ['GET','POST'])
def check_dream():
    basepath = os.path.join(os.path.dirname(__file__), 'static','uploads',session.get('username'))
    dream_dir=os.listdir(os.path.join(basepath,'dream'))
    if '.DS_Store' in dream_dir:
        dream_dir.remove('.DS_Store')
    
    dream_dir.insert(0,'Not Choose')
    if request.method== 'POST':
        try:
            basepath = os.path.join(os.path.dirname(__file__), 'static','uploads',session.get('username'))
        
            if request.values['folder']=='0':
                	return render_template('check_dream.html',alert='Please choose a folder',dream_dir=dream_dir)

            	
            else:
                content_file = os.listdir(os.path.join(basepath,'dream',dream_dir[int(request.values['folder'])]))
                if '.DS_Store' in content_file:
                    	content_file.remove('.DS_Store')
                text_path = os.path.join(basepath,'dream',dream_dir[int(request.values['folder'])])
                
            
        except:
            return render_template('check_dream.html',dream_dir=dream_dir)
        str_article = ""
        for i in range(0,len(content_file)):
            str_content = ""
            
            with open(text_path +'/'+ content_file[i], "r") as text_file:
                contents = text_file.readlines()
            for j in range(0,len(contents)):
                str_content += contents[j]
            str_article += str_content
            str_article += "</br></br>"
        
                             
        return "<h1>Dairy</h1>" \
                "<body>" \
                "<ul>" \
                "<li><a href='../check'>上一頁</a></li>" \
                "<li><a href='../'>登出</a></li>" \
                "</ul>" \
                "<p> Your dream: </p>" \
                " {} ".format(str_article) + \
                "</body>"         
                      
    return render_template('check_dream.html',dream_dir=dream_dir)

@app.route('/send', methods = ['GET','POST'])
def send():
    
    if request.method== 'POST':
        basepath = os.path.join(os.path.dirname(__file__), 'static','send')

        to_address = request.values['username']
        Subject = '%s' % request.values['subject']
        contents = request.values['text'] 
        date = request.form['bday']
        
        
        mail = [to_address,Subject,contents]    
        
        
        
        with open(basepath + '/' + date + '.txt','w') as m:
            for i in mail:
                m.write(str(i) + '\n')
        
    return render_template('send.html')

@app.route('/weather', methods = ['GET','POST'])
def weather():
    if request.method== 'POST' :
        town = request.values['town']
        wh = weather_Handler(town)
        wh.save_pickle()
        return  "<h1>Weather</h1>" \
                "<body>" \
                "<ul>" \
                "<li><a href='../write'>上一頁</a></li>" \
                "<li><a href='../'>登出</a></li>" \
                "</ul>" \
                "</body>" \
               "日期:{}".format(wh.get_Date()) + "</br>" +\
               "天氣狀況:{}".format(wh.get_Wx()) + "</br>" +\
               "降雨機率:{}".format(wh.get_PoP()) + "</br>" +\
               "最低溫:{}".format(wh.get_MinT()) + "</br>" +\
               "最高溫:{}".format(wh.get_MaxT()) + "</br>" +\
               "天氣舒適度:{}".format(wh.get_CI())
        
    return render_template('weather.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=True)

