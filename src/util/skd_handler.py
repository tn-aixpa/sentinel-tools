
import os
import digitalhub as dh
def list_artifact(path:str):
    return os.listdir(path)

def upload_artifact(artifact_name = "",
                    src_path = "",
                    s3_path=None,
                    project_name = "",
                    bucket_name = ""):
    
    print(f"Loading artifact: {artifact_name}, {artifact_name}")
    
    # Crea progetto, togliere local quando useremo backend
    project = dh.get_or_create_project(project_name) # , local=True for testing in local

    if s3_path is None:
        project.log_artifact(name=artifact_name,
                             kind="artifact",
                             source=src_path)
    else:
        project.log_artifact(name=artifact_name,
                               kind="artifact",
                               path= s3_path,
                               source=src_path)

def load_all_artifacts_from_custom(path_current_data,json_sdk,artifact_name,s3_path=None):
    project_name= json_sdk["PROJECT_NAME"]
    bucket_name=json_sdk["S3_BUCKET"]
    endpoint_url=json_sdk["S3_ENDPOINT_URL"]
    aws_key = json_sdk["AWS_ACCESS_KEY_ID"]
    aws_secret = json_sdk["AWS_SECRET_ACCESS_KEY"]
    core_endpoint =json_sdk["DHCORE_ENDPOINT"]
    load_all_artifacts(path_current_data,artifact_name=artifact_name,project_name=project_name,bucket_name=bucket_name,s3_path=s3_path)

def load_all_artifacts(path_current_data:str,artifact_name:str,s3_path:str=None,project_name= "", bucket_name=""):
    upload_artifact(artifact_name=artifact_name,src_path=path_current_data,s3_path=s3_path,project_name=project_name,bucket_name=bucket_name)
    
def create_json_from_env():
    result = {}
    result['PROJECT_NAME'] = os.environ["PROJECT_NAME"]
    result['S3_BUCKET'] = os.environ["S3_BUCKET"]
    result['S3_ENDPOINT_URL'] = os.environ["S3_ENDPOINT_URL"]
    result['DHCORE_ENDPOINT'] = os.environ["DHCORE_ENDPOINT"]
    result['AWS_ACCESS_KEY_ID'] = os.environ["AWS_ACCESS_KEY_ID"]
    result['AWS_SECRET_ACCESS_KEY'] = os.environ["AWS_SECRET_ACCESS_KEY"]
    result['AWS_SESSION_TOKEN'] = os.environ["AWS_SESSION_TOKEN"]
    
    return result

def get_environment_variable_username_password():
    return os.environ["CDSETOOL_ESA_USER"],os.environ["CDSETOOL_ESA_PASSWORD"]

def set_environment_variable_username_password(user,password):
    os.environ["CDSETOOL_ESA_USER"] = user
    os.environ["CDSETOOL_ESA_PASSWORD"] = password