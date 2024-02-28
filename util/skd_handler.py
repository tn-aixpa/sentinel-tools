
import os
import digitalhub_core as dh
def list_artifact(path:str):
    return os.listdir(path)

def upload_artifact(artifact_name="",src_path="",project_name= "", bucket_name="",endpoint_ur="",core_endpoint="",aws_key="",aws_secret=""):
    # Crea progetto, togliere local quando useremo backend
    project = dh.get_or_create_project(project_name) # , local=True for testing in local

    # Crea nuovo artefatto con src_path (locale) e target_path (remoto) di destinazione
    ssrc_path = os.path.join(src_path,artifact_name)
    art = dh.new_artifact(project=project_name,
                        name=artifact_name,
                        kind="artifact",
                        src_path=ssrc_path,
                        target_path=f"s3://{bucket_name}/{artifact_name}")
    art.upload()

def load_all_artifacts_from_custom(path,json_sdk):
    project_name= json_sdk["PROJECT_NAME"]
    bucket_name=json_sdk["S3_BUCKET_NAME"]
    endpoint_url=json_sdk["S3_ENDPOINT_URL"]
    aws_key = json_sdk["AWS_ACCESS_KEY_ID"]
    aws_secret = json_sdk["AWS_SECRET_ACCESS_KEY"]
    core_endpoint =json_sdk["DIGITALHUB_CORE_ENDPOINT"]
    # set_environment_var(project_name=project_name,bucket_name=bucket_name,endpoint_url=endpoint_url,core_endpoint=core_endpoint,aws_key=aws_key,aws_secret=aws_secret)
    load_all_artifacts(path,project_name=project_name,bucket_name=bucket_name,endpoint_url=endpoint_url,core_endpoint=core_endpoint,aws_key=aws_key,aws_secret=aws_secret)

def set_environment_var(project_name= "", bucket_name="",endpoint_url="",core_endpoint="",aws_key="",aws_secret=""):
    os.environ["PROJECT_NAME"] = project_name
    os.environ["S3_BUCKET_NAME"] = bucket_name
    os.environ["S3_ENDPOINT_URL"] = endpoint_url
    os.environ["DIGITALHUB_CORE_ENDPOINT"] = core_endpoint
    os.environ["AWS_ACCESS_KEY_ID"] = aws_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret

def set_environment_var_from_json(json):
    if 'PROJECT_NAME' in json:
        os.environ["PROJECT_NAME"] = json["PROJECT_NAME"]
    if 'S3_BUCKET_NAME' in json:
        os.environ["S3_BUCKET_NAME"] = json["S3_BUCKET_NAME"]
    if 'S3_ENDPOINT_URL' in json:
        os.environ["S3_ENDPOINT_URL"] = json["S3_ENDPOINT_URL"]
    if 'DIGITALHUB_CORE_ENDPOINT' in json:
        os.environ["DIGITALHUB_CORE_ENDPOINT"] = json["DIGITALHUB_CORE_ENDPOINT"]
    if 'AWS_ACCESS_KEY_ID' in json:
        os.environ["AWS_ACCESS_KEY_ID"] = json["AWS_ACCESS_KEY_ID"]
    if 'AWS_SECRET_ACCESS_KEY' in json:
        os.environ["AWS_SECRET_ACCESS_KEY"] = json["AWS_SECRET_ACCESS_KEY"]
    if 'CDSETOOL_ESA_USER' in json:
        os.environ["CDSETOOL_ESA_USER"] = json["CDSETOOL_ESA_USER"]
    if 'CDSETOOL_ESA_PASSWORD' in json:
        os.environ["CDSETOOL_ESA_PASSWORD"] = json["CDSETOOL_ESA_PASSWORD"]

def load_all_artifacts(path:str,project_name= "", bucket_name="",endpoint_url="",core_endpoint="",aws_key="",aws_secret=""):
    artifacts = list_artifact(path)
    print(f"parameters from env: project_name: {project_name}, bucket_name: {bucket_name}, endpoint_url:{endpoint_url}, core_endpoint:{core_endpoint}")
    print(f"list artifacts to load:")
    for i in artifacts:
        print(f"{i}")
    for i in artifacts:
        full_path = os.path.join(path,i)
        if not os.path.isdir(full_path):
            upload_artifact(artifact_name=i,src_path=path,project_name=project_name,bucket_name=bucket_name,endpoint_ur=endpoint_url,core_endpoint=core_endpoint,aws_key=aws_key,aws_secret=aws_secret)
        else:
            #preprocessing directory
            directory_preprocess = os.path.join(path,i)
            new_list = list_artifact(directory_preprocess)
            for preprocess in new_list:
                upload_artifact(artifact_name=preprocess,src_path=directory_preprocess,project_name=project_name,bucket_name=bucket_name,endpoint_ur=endpoint_url,core_endpoint=core_endpoint,aws_key=aws_key,aws_secret=aws_secret)

def create_json_from_env():
    result = {}
    result['PROJECT_NAME'] = os.environ["PROJECT_NAME"]
    result['S3_BUCKET_NAME'] = os.environ["S3_BUCKET_NAME"]
    result['S3_ENDPOINT_URL'] = os.environ["S3_ENDPOINT_URL"]
    result['DIGITALHUB_CORE_ENDPOINT'] = os.environ["DIGITALHUB_CORE_ENDPOINT"]
    result['AWS_ACCESS_KEY_ID'] = os.environ["AWS_ACCESS_KEY_ID"]
    result['AWS_SECRET_ACCESS_KEY'] = os.environ["AWS_SECRET_ACCESS_KEY"]
    return result

def get_environment_variable_username_password():
    return os.environ["CDSETOOL_ESA_USER"],os.environ["CDSETOOL_ESA_PASSWORD"]

def set_environment_variable_username_password(user,password):
    os.environ["CDSETOOL_ESA_USER"] = user
    os.environ["CDSETOOL_ESA_PASSWORD"] = password