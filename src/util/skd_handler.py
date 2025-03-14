
import os
import digitalhub as dh
def list_artifact(path:str):
    return os.listdir(path)

def upload_artifact(artifact_name = "",
                    src_path = "",
                    s3_path=None,
                    project_name = "",
                    bucket_name = ""):
    
    #artifact_name_new = artifact_name.replace(".zip","").lower()
    #source = os.path.join(src_path, artifact_name)
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
    bucket_name=json_sdk["S3_BUCKET_NAME"]
    endpoint_url=json_sdk["S3_ENDPOINT_URL"]
    aws_key = json_sdk["AWS_ACCESS_KEY_ID"]
    aws_secret = json_sdk["AWS_SECRET_ACCESS_KEY"]
    core_endpoint =json_sdk["DHCORE_ENDPOINT"]
    # set_environment_var(project_name=project_name,bucket_name=bucket_name,endpoint_url=endpoint_url,core_endpoint=core_endpoint,aws_key=aws_key,aws_secret=aws_secret)
    load_all_artifacts(path_current_data,artifact_name=artifact_name,project_name=project_name,bucket_name=bucket_name,s3_path=s3_path)

def set_environment_var(project_name= "", bucket_name="",endpoint_url="",core_endpoint="",aws_key="",aws_secret="",aws_session_key=""):
    os.environ["PROJECT_NAME"] = project_name
    os.environ["S3_BUCKET_NAME"] = bucket_name
    os.environ["S3_ENDPOINT_URL"] = endpoint_url
    os.environ["DHCORE_ENDPOINT"] = core_endpoint
    os.environ["AWS_ACCESS_KEY_ID"] = aws_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret
    os.environ["AWS_SESSION_TOKEN"] = aws_session_key

def set_environment_var_from_json(json):
    if 'PROJECT_NAME' in json:
        os.environ["PROJECT_NAME"] = json["PROJECT_NAME"]
    if 'S3_BUCKET_NAME' in json:
        os.environ["S3_BUCKET_NAME"] = json["S3_BUCKET_NAME"]
    if 'S3_ENDPOINT_URL' in json:
        os.environ["S3_ENDPOINT_URL"] = json["S3_ENDPOINT_URL"]
    if 'DHCORE_ENDPOINT' in json:
        os.environ["DHCORE_ENDPOINT"] = json["DHCORE_ENDPOINT"]
    if 'AWS_ACCESS_KEY_ID' in json:
        os.environ["AWS_ACCESS_KEY_ID"] = json["AWS_ACCESS_KEY_ID"]
    if 'AWS_SECRET_ACCESS_KEY' in json:
        os.environ["AWS_SECRET_ACCESS_KEY"] = json["AWS_SECRET_ACCESS_KEY"]
    if 'AWS_SESSION_TOKEN' in json:
        os.environ["AWS_SESSION_TOKEN"] = json["AWS_SESSION_TOKEN"]
    if 'CDSETOOL_ESA_USER' in json:
        os.environ["CDSETOOL_ESA_USER"] = json["CDSETOOL_ESA_USER"]
    if 'CDSETOOL_ESA_PASSWORD' in json:
        os.environ["CDSETOOL_ESA_PASSWORD"] = json["CDSETOOL_ESA_PASSWORD"]

def load_all_artifacts(path_current_data:str,artifact_name:str,s3_path:str=None,project_name= "", bucket_name=""):
    upload_artifact(artifact_name=artifact_name,src_path=path_current_data,s3_path=s3_path,project_name=project_name,bucket_name=bucket_name)
    # old implementations
    # artifacts = list_artifact(path_current_data)
    # print(f"parameters from env: project_name: {project_name}, bucket_name: {bucket_name}, endpoint_url: {endpoint_url}, core_endpoint: {core_endpoint}")
    # for i in artifacts:
    #     full_path = os.path.join(path_current_data,i)
    #     if not os.path.isdir(full_path):
    #         upload_artifact(artifact_name=i,src_path=path_current_data,project_name=project_name,bucket_name=bucket_name)
    #     else:
    #         #preprocessing directory
    #         directory_preprocess = os.path.join(path_current_data,i)
    #         new_list = list_artifact(directory_preprocess)
    #         for preprocess in new_list:
    #             upload_artifact(artifact_name=preprocess,src_path=directory_preprocess,project_name=project_name,bucket_name=bucket_name)

def create_json_from_env():
    result = {}
    result['PROJECT_NAME'] = os.environ["PROJECT_NAME"]
    result['S3_BUCKET_NAME'] = os.environ["S3_BUCKET_NAME"]
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