import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.ProcessesModel import processModel

class ProcessController:
    def __init__(self, user_uid):
        self.processModel = processModel
    
    def create(self, userUid, process):
        try:
            processPid = self.processModel.create(userUid, process)
            
            return processPid
        
        except Exception as e:
            raise e         
        
    def update(self, process, processPid, userUid):
        try:
            process = self.processModel.update(process, processPid)
            
            return process
        
        except Exception as e:
            raise e     
        
    def list(self, userUid):
        try:
            processes = self.processModel.list(userUid)
            return processes
        except Exception as e:
            raise e   
        
    def delete(self, processPid, userUid):
        try:
            self.processModel.delete(processPid)
            return {}
        except Exception as e:
            raise e   
        
    def getProcesso(self, proccesPid):
        try:
            process = self.processModel.getProcess(proccesPid)
            return process
        except Exception as e:
            raise e   
        
    
    def mudarEstadosDosProcessos(self, user_uid):
        self.processModel.update_state(user_uid)
            
        
    def deleteAll(self):
        self.processModel.deleteAll()