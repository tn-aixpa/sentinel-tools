
import os
import digitalhub as dh
def list_artifact(path:str):
    return os.listdir(path)

def upload_artifact(artifact_name = "",
                    src_path = "",
                    project_name = ""): 
    
    print(f"Loading artifact: {artifact_name}, {artifact_name}")
    
    # Crea progetto, togliere local quando useremo backend
    project = dh.get_or_create_project(project_name) # , local=True for testing in local

    project.log_artifact(name=artifact_name, kind="artifact", source=src_path)
   
def load_all_artifacts_from_custom(path_current_data,artifact_name):
    project_name= os.environ["PROJECT_NAME"]
    upload_artifact(artifact_name=artifact_name,src_path=path_current_data,project_name=project_name)

    
def get_environment_variable_username_password():
    return os.environ["CDSETOOL_ESA_USER"],os.environ["CDSETOOL_ESA_PASSWORD"]

def set_environment_variable_username_password(user,password):
    os.environ["CDSETOOL_ESA_USER"] = user
    os.environ["CDSETOOL_ESA_PASSWORD"] = password