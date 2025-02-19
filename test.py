from flask import Flask, redirect, url_for, render_template, request, session,flash
from datetime import timedelta
from predict import transform
import codecs
import json
import os
import uuid

app = Flask(
    __name__, static_folder="./static", template_folder="./templates")
app.secret_key = "ljc18376334"
app.permanent_session_lifetime = timedelta(days=7)

@app.route("/", methods=["POST", "GET"])
def home():
   if request.method == "GET":
      return render_template("index.html")
   else:
      text = request.form["text"]
      print(text)
      language = request.form["language"]
      model = request.form['model']
      input = {}
      input['text'] = text
      uid = uuid.uuid1()
      id = uid.hex
      input['id'] = id
      inputJson = json.dumps(input)
      result = {}         
      output = predict(inputJson, model=model, language=language)
      result['text'] = output
      types = {}
      print(output)
      if not output: # 处理识别不出的事件
         output = [{'event_type': '未能识别'}]

      for item in output:
         type = item['event_type']
         if type not in types.keys():
            args = set()
            types[type] = args
         
         if 'arguments' in item:
            for it in item['arguments']:
               types[type].add(it['role'] + '--' + it['argument'])

      result['event'] = types        
      return render_template("index.html", result=result)

#这里扩展模型和语言
def predict(inputJson, model, language):
   if model == "" or language == "":
      return ""
   if model == "EE":
      if language == "Chinese":
         return transform(inputJson)
      else:
         return ""
   else:
      return ""



if __name__ == "__main__":
   app.run(debug=True)