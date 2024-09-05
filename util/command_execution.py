from ast import List
import os

class CommandExecution():

    def __init__(self,list_of_commands):
        if type(list_of_commands) is dict:
            res = []
            for key in list_of_commands.keys:
                if len(list_of_commands[key])>0:
                    res+list_of_commands[key]
            self.list_of_commands = res
            pass
        else:
            self.list_of_commands: List = list_of_commands
    
    def execute(self):
        results = []
        self.set_env()
        for command in self.list_of_commands:
            if command != "":
                res = self.promt_command(command)
                if res == 0:
                    results.append({'command': command,'success': True})
                else:
                    results.append({'command': command,'success': False})
                print(f"Success: {res}")
                #print(command)
            else:
                results.append({'command': 'No commands','success': False})
        return results
    
    def promt_command(self,command):
        #CMD = 'cmd /k' 
        #COMMAND_ = CMD + "\"" + command + "\"" 
        #COMMAND_ = "python3 script1.py"
        result = os.system(command)
        return result
    
    def set_env(self):
        # https://www.freecodecamp.org/news/how-to-set-an-environment-variable-in-linux/
        pass
        # com1 = "export SNAP_HOME=/home/dsl/snap_esa/bin"
        # com2 = "export PATH=$PATH:$SNAP_HOME"
        # com3 = 'echo "Env setted finished!"'
        # os.system(com1)
        # os.system(com2)
        # os.system(com3)
        # os.system('./linux_span_env.sh')