import textract
import os
import requests


supported = ['.csv','.docx','.eml','.epub','.json','.msg','.odt','.pdf','.pptx','.xls','.txt','.xlsx',".html"]

supportedLangs = ["czech","danish","dutch","english","estonian","finnish","french","german","greek","italian","norwegian","polish","portuguese","russian","spanish","swedish","turkish"]
spacedLangs = ["japanese","korean","chinese (simplified)","lao","myanmar (burmese)",'chinese (traditional)',"greek"]
allsupported = supportedLangs + ["japanese","chinese (simplified)","chinese (traditional)"]

def get_text(path):
        text = textract.process(path,encoding="utf-8")
        return (text.decode('utf-8'))

def web(url):
    with open("website.html","wb") as web:
        res = requests.get(url)
        web.write(res.content)

    text = textract.process("website.html",encoding="utf-8")
    text = text.decode("utf-8")
    os.remove("website.html")
    return (text)




