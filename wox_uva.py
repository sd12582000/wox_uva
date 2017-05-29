#encoding=utf8
from wox import Wox
import UvaTools
import sys

#Your class must inherit from Wox base class https://github.com/qianlifeng/Wox/blob/master/PythonHome/wox.py
#The wox class here did some works to simplify the communication between Wox and python plugin.
class Wox_Uva(Wox):
    problemDics = UvaTools.UvaProblems()
    from os.path import abspath, join, dirname
    file_path = join(abspath(dirname(__file__)), "config.json")
    myconfig = UvaTools.lib.GeneralMethod.load_json_data(file_path) 
    userLog = UvaTools.UvaUser(myconfig['userName'])
    
    def __init__(self):
        super().__init__()
        
    def nothingToWork(self,query):
        None
    
    def reloadUserLog(self):
        self.userLog.reload_user_sumbit()

    def creatDicForPro(self,rootPath,num):
        self.problemDics.creat_problem_dir(rootPath , num)

    def query(self, query):
        results = []
       
        if query=="reload":
           results.append({
                "Title": "Uva",
                "SubTitle": "reload {} solved record".format(self.myconfig['userName']),            
                "IcoPath":"onlineJudgeLogo.png",
                "JsonRPCAction":{"method": "reloadUserLog", "parameters": []},
                "dontHideAfterAction":True
            })
        else:
            pro_title = self.problemDics.get_title(query)
            if pro_title!="":
                subTitle=""
                is_pass = self.userLog.is_acept(query)
                if is_pass:
                    subTitle="Problem [ {}- {} ] was solved !".format(query,pro_title)
                else:
                    subTitle="Problem [ {}- {} ] needs solved !".format(query,pro_title)
                
                results.append({
                    "Title": "Uva",
                    "SubTitle": subTitle,            
                    "IcoPath":"onlineJudgeLogo.png",
                    "JsonRPCAction":{"method": "nothingToWork", "parameters": [query]},
                    "dontHideAfterAction":True
                })

                if not is_pass:
                  results.append({
                    "Title": "Uva",
                    "SubTitle": "Creat [ {}- {} ] Dir In {}".format(query, pro_title, self.myconfig['rootPath']),            
                    "IcoPath":"onlineJudgeLogo.png",
                    "JsonRPCAction":{"method": "creatDicForPro", "parameters": [self.myconfig['rootPath'], query]},
                    "dontHideAfterAction":False
                })
            else:
                results.append({
                    "Title": "Uva",
                    "SubTitle": "problem Num?",            
                    "IcoPath":"onlineJudgeLogo.png",
                    "JsonRPCAction":{"method": "nothingToWork", "parameters": [query]},
                    "dontHideAfterAction":True
                })
        return results
        
#Following statement is necessary
if __name__ == "__main__":
    Wox_Uva()