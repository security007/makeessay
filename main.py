from flask import Flask,render_template,request
import requests
import json
import wikipedia
import html
import datetime
import translators as ts

app = Flask(__name__)

def tanggal():
    tanggall = datetime.datetime.now()
    bulan = str(tanggall.month)
    form = '{"1":"Januari","2":"Februari","3":"Maret","4":"April","5":"Mei","6":"Juni","7":"Juli","8":"Agustus","9":"September","10":"Oktober","11":"November","12":"Desember"}'
    form = json.loads(form)
    format = str(tanggall.day)+" "+str(form[bulan])+" "+str(tanggall.year)
    return format

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = "http://www.essaytyper.com/lookup"
        essay = request.form['essay']
        res = requests.post(url,data={'subject':ts.google(essay,to_language='en')})
        if res.status_code == 200:
            go = json.loads(res.text)
            result = """<div class="t-area">Ucup Setiawan<br>[jurusan/mata kuliah],Semester II, Class 2A<br>Bambang Suratman S.Sos <br>Institute Teknologi Surabaya<br>"""+tanggal()+"""<br><br><center>"""+html.escape(essay).upper()+"""</center><br>&emsp;&emsp;&emsp;"""+go['text']+"""<div>"""
            return render_template('index.html',result=result)
        else:
            try:
                wikipedia.set_lang("id")
                result = """<div class="t-area">Ucup Setiawan<br>[jurusan/mata kuliah],Semester II, Class 2A<br>Bambang Suratman S.Sos <br>Institute Teknologi Surabaya<br>"""+tanggal()+"""<br><br><center>"""+html.escape(essay).upper()+"""</center><br>&emsp;&emsp;&emsp;"""+wikipedia.summary(essay)+"""
            <div>"""
                return render_template('index.html',result=result)
            except:
                result = """<div class="t-area">
                <div class="alert alert-danger" role="alert">OOops sorry we don't find anything about """+html.escape(essay)+"""</div><div>"""
                return render_template('index.html',result=result)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)
