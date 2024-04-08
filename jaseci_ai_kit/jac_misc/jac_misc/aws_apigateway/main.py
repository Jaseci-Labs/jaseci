"""
"""

from os import getenv

from boto3.session import Session

from jaseci.jsorc.live_actions import jaseci_action

from mypy_boto3_apigateway import APIGatewayClient
from mypy_boto3_apigateway.type_defs import (
    IntegrationExtraResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    MethodResponseTypeDef,
    ResourceResponseTypeDef,
)

AWS_APIGATEWAY_SESSION: Session = None
AWS_APIGATEWAY_CLIENT: APIGatewayClient = None


def get_client() -> APIGatewayClient:
    global AWS_APIGATEWAY_SESSION, AWS_APIGATEWAY_CLIENT

    if not isinstance(AWS_APIGATEWAY_SESSION, Session):
        AWS_APIGATEWAY_SESSION = Session()

    if not isinstance(AWS_APIGATEWAY_CLIENT, APIGatewayClient):
        AWS_APIGATEWAY_CLIENT = AWS_APIGATEWAY_SESSION.client(
            "apigateway",
            region_name=getenv("AWS_APIGATEWAY_REGION"),
            aws_access_key_id=getenv("AWS_APIGATEWAY_ACCESS_ID"),
            aws_secret_access_key=getenv("AWS_APIGATEWAY_ACCESS_KEY"),
        )

    return AWS_APIGATEWAY_CLIENT


@jaseci_action(act_group=["aws_apigateway"], allow_remote=True)
def setup():
    """"""
    get_client()


# "oft92s6cl0", "4sqg2anl1f", "testing-1"
@jaseci_action(act_group=["aws_apigateway"], allow_remote=True)
def create_resource(
    restApiId: str, parentId: str, pathPart: str
) -> ResourceResponseTypeDef:
    return get_client().create_resource(
        restApiId=restApiId, parentId=parentId, pathPart=pathPart
    )


# POST, requestModels = {"application/json": "AskQuestionModel"}
@jaseci_action(act_group=["aws_apigateway"], allow_remote=True)
def create_method(
    restApiId: str, resourceId: str, httpMethod: str, options: dict = {}
) -> MethodResponseTypeDef:
    return get_client().put_method(
        restApiId=restApiId, resourceId=resourceId, httpMethod=httpMethod, **options
    )


@jaseci_action(act_group=["aws_apigateway"], allow_remote=True)
def put_method_response(
    restApiId: str, resourceId: str, httpMethod: str, options: dict = {}
) -> IntegrationExtraResponseTypeDef:
    return get_client().put_method_response(
        restApiId=restApiId,
        resourceId=resourceId,
        httpMethod=httpMethod,
        **options,
    )


# POST, requestModels = {"application/json": "AskQuestionModel"}
@jaseci_action(act_group=["aws_apigateway"], allow_remote=True)
def put_integration(
    restApiId: str, resourceId: str, httpMethod: str, options: dict = {}
) -> MethodResponseTypeDef:
    return get_client().put_integration(
        restApiId=restApiId, resourceId=resourceId, httpMethod=httpMethod, **options
    )


@jaseci_action(act_group=["aws_apigateway"], allow_remote=True)
def update_integration(
    restApiId: str, resourceId: str, httpMethod: str, options: dict = {}
) -> IntegrationExtraResponseTypeDef:
    return get_client().update_integration(
        restApiId=restApiId,
        resourceId=resourceId,
        httpMethod=httpMethod,
        **options,
    )


@jaseci_action(act_group=["aws_apigateway"], allow_remote=True)
def put_integration_response(
    restApiId: str, resourceId: str, httpMethod: str, options: dict = {}
) -> IntegrationExtraResponseTypeDef:
    return get_client().put_integration_response(
        restApiId=restApiId,
        resourceId=resourceId,
        httpMethod=httpMethod,
        **options,
    )


@jaseci_action(act_group=["aws_apigateway"], allow_remote=True)
def delete_resource(restApiId: str, resourceId: str) -> EmptyResponseMetadataTypeDef:
    return get_client().delete_resource(restApiId=restApiId, resourceId=resourceId)
