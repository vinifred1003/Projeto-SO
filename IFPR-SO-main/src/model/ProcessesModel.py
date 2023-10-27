from model.DatabaseConnection import DatabaseConnection
from model.UsersModel import usersModel
import time
import random
import threading
import sqlite3


class ProcessesModel:
    def __init__(self):
        conecction = DatabaseConnection()
        self.cursor = conecction.getCursor()

        self.usersModel = usersModel
        
    def getProcess(self, processPid):
        self.cursor.execute("SELECT * FROM processes WHERE pid=?", (processPid,))
        dataBaseProcess = self.cursor.fetchone()

        if not dataBaseProcess:
            return
        
        process = {
            "pid": dataBaseProcess[0],
            "user_uid": dataBaseProcess[1],
            "priority": dataBaseProcess[2],
            "cpu_usage": dataBaseProcess[3],
            "state": dataBaseProcess[4],
            "memory_space": dataBaseProcess[5],
            "process_name": dataBaseProcess[6]
        }
        
        return (process)
        
    def create(self, userUid, process):
        user = self.usersModel.getUserByUid(userUid)
        if not user:
            raise Exception("Usuário não autenticado")
        
        if not process["priority"] or not process["cpu_usage"] or not process["process_name"] or not process["memory_space"]:
            raise Exception("Faltando dados obrigatórios") 
        
        self.cursor.execute( 
            '''
            INSERT INTO processes (user_uid, process_name, priority, cpu_usage, state, memory_space) 
            VALUES (?, ?,  ?, ?, "CRIAÇÃO", ?)
            ''', (userUid, process["process_name"], process["priority"], process["cpu_usage"], process["memory_space"],)
        )
        
        self.cursor.connection.commit()
        
        process_id = self.cursor.lastrowid
        
        return process_id
    
    def delete(self, processPid):
        self.cursor.execute( 
            '''
            DELETE FROM processes WHERE pid=? 
            ''', (processPid,)
        )
        self.cursor.connection.commit()
        return {}
        
    def update(self, process, processPid):
        if not process["priority"] or not process["cpu_usage"] or not process["state"] or not process["process_name"] or not process["memory_space"]:
            raise Exception("Faltando dados obrigatórios") 
        
        self.cursor.execute( 
            '''
            UPDATE processes 
            SET priority=?, cpu_usage=?, state=?, memory_space=?, process_name=?
            WHERE pid=?
            ''', (process["priority"], process["cpu_usage"], process["state"], process["memory_space"], process["process_name"], processPid)
        )
        
        self.cursor.connection.commit()
        
        process = self.getProcess(processPid)
        
        return process
    
    def list(self, userUid):
        user = self.usersModel.getUserByUid(userUid)
        if not user:
            raise Exception("Usuário não autenticado")
        
        self.cursor.execute("SELECT pid, process_name, priority, cpu_usage, state, memory_space FROM processes",)
        processes = self.cursor.fetchall()
        return processes
    
    def get_processo_executando(self):
        self.cursor.execute("SELECT * FROM processes WHERE state=?", ("EXECUÇÃO",))
        dataBaseProcess = self.cursor.fetchone()
        return (dataBaseProcess)
    
    def generate_random_process(self, user_uid):
        possiblePrograms = ["Word", "Excel", "Power Point", "Google Chrome", "VS Code"]
        program = random.choice(possiblePrograms)
        
        process = {
            "priority": random.choice(["BAIXA", "MÉDIA", "ALTA"]),
            "cpu_usage": random.randint(1, 100),
            "memory_space": random.randint(1, 100),
            "process_name": program
        }
        process["priority"] or not process["cpu_usage"] or not process["memory_space"]
        
        self.create(user_uid, process)
    
    def deleteAll(self):
        self.cursor.execute("DELETE FROM processes")
        self.cursor.connection.commit()
        
    
    def update_state(self, user_uid):
        possibleStatesExecucao = ['PRONTO', 'ESPERA', 'FINALIZADO']
        possibleStatesPronto = ['EXECUÇÃO', 'PRONTO']
        possibleStatesFinalizacao = ['DELETAR']
        possibleStatesEspera = ['PRONTO', 'ESPERA']
        possibleStateCriacao = ['PRONTO']

        self.cursor.execute("SELECT pid, user_uid, priority, cpu_usage, state, memory_space FROM processes ORDER BY pid")
        processes = self.cursor.fetchall()
        
        pid_do_ultimo_pronto = None
        for process in reversed(processes):
            if process[4] == "PRONTO":
                pid_do_ultimo_pronto = process[0]
        
        print("ENTROU")
        for p in processes:
            process = {
                "pid": p[0],
                "user_uid": p[1],
                "priority": p[2],
                "cpu_usage": p[3],
                "state": p[4],
                "memory_space": p[5],
            }
            
            match process["state"]:
                case "CRIAÇÃO":
                    new_state = random.choice(possibleStateCriacao)
                case "ESPERA":
                    new_state = random.choice(possibleStatesEspera)
                case "PRONTO": 
                    new_state = random.choice(possibleStatesPronto)
                case "EXECUCAO":
                    new_state = random.choice(possibleStatesExecucao)
                case "FINALIZADO":
                    new_state = random.choice(possibleStatesFinalizacao)
                case _:
                    new_state = 'ESPERA'
                
            
            if new_state == 'DELETAR':
                self.delete(process["pid"]) 

            else:
                self.cursor.execute("SELECT * FROM processes WHERE state=?", ("EXECUÇÃO",))
                execucao_exists = self.cursor.fetchone()  
                if new_state == 'EXECUÇÃO' and execucao_exists:
                    self.cursor.execute( 
                        '''
                        UPDATE processes 
                        SET state=? 
                        WHERE pid=?
                        ''', (random.choice(possibleStatesExecucao), execucao_exists[0]))
                
                if process["state"] == 'PRONTO' and not execucao_exists and pid_do_ultimo_pronto == process["pid"]:
                    new_state = 'EXECUÇÃO'  
                               
                process["state"] = new_state
                print(process)
                self.cursor.execute( 
                    '''
                    UPDATE processes 
                    SET state=? 
                    WHERE pid=?
                    ''', (process["state"], process['pid'])
                )

                self.cursor.connection.commit()
                
        
        if (len(processes) < 10): 
            self.generate_random_process(user_uid)

        
    
processModel = ProcessesModel()
