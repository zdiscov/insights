from flask import Flask, render_template 
from cfpbData import cfpbData
app = Flask(__name__,static_url_path='')


@app.route("/report")
def report():
   return render_template('report.html')

@app.route("/")
def hello():
   return render_template('report1.html') 

@app.route("/cfpb/<clientname>")
def cfpb(clientname):
   c = cfpbData(clientname)
   html_string = ""
   retV = c.getStateComplaintsChartFile()
   try:
   	f = open(retV, 'r')
   	html_string = f.read()
   	f.close()
   except:
	html_string = ""
   return html_string

@app.route("/hello2/<name>")
def hello2(name):
    return render_template("hello.html", name=name)

@app.route("/chloro/<clientname>")
def chloro(clientname):
	c = cfpbData(clientname)
   	c.getStateComplaintsChartFile()
	c.writeToMapViz()
	return app.send_static_file('chloro.html')

@app.route("/ch/<clientname>")
def ch(clientname):
        c = cfpbData(clientname)
        c.getStateComplaintsChartFile()
        c.writeToMapViz()
	return render_template('chloro.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
