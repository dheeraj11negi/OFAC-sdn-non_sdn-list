import re
import os

class htmlhelper:
    def returnformatedhtml(content:str):
        result = re.sub("\\s+", " ", content).replace(" \"", "\"").replace("\" >", "\">").replace(" >", ">").replace("> <","><").replace("\" />", "\"/>").replace(" =", "=").replace("= ", "=")
        return result

    def formatstring(content : str):
        return re.sub("<(.|\n)*?>", " ", content).strip()



    def returnvalue(content: str, start: str, end: str):
        result = ""
        pattern = re.compile(re.escape(start) + "(.*?)" + re.escape(end))
        match = pattern.search(content)
        if match:
             result = match.groups()[0].strip()
        return result


    def collecturl(content:str, start: str, end: str):
        result = []
        pattern = re.compile(re.escape(start) + "(.*?)" + re.escape(end))
        match = pattern.findall(content)
        if match:
            result = [sub.strip() for sub in match]
        return result



