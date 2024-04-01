from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from enum import Enum


class Environment(str, Enum):
    production = "production"
    development = "development"
    test = "test"


class Config(BaseModel):
    NODE_ENV: Environment = Field(default=Environment.development)
    EVENT_STORAGE_BASE_URL: HttpUrl
    ROUTING_SERVICE_BASE_URL: HttpUrl
    OCP_APIM_SUBSCRIPTION_KEY: str
    AUTH_TOKEN_URL: HttpUrl
    AUTH_TOKEN_CLIENT_ID: str
    AUTH_TOKEN_CLIENT_SECRET: str
    AUTH_TOKEN_SCOPE: str
    AUTH_TOKEN_CACHE_KEY: str = Field(default="authToken")
    AUTH_TOKEN_CACHE_TTL: int = Field(default=3600)
    GET_OFFERS_PATH: str = Field(default="/api/events/{partyId}")
    GET_EVENT_BY_ID_PATH: str = Field(default="/api/events/{partyId}/{resourceId}")
    ROUTING_SERVICE_GET_BROKER_DATA_PATH: str = Field(default="/api/brokers?client_uuid={clientId}")
    ROUTING_SERVICE_GET_VISIBLE_PARTIES_PATH: str = Field(default="/api/insurers/{productUuid}?brokerUuid={brokerUuid}")
    ROUTING_SERVICE_GET_PRODUCTS_PATH: str = Field(default="/api/products")
    ROUTING_SERVICE_SUBSCRIPTION_PATH: str = Field(default="/api/subscriptions")
    SUBMISSION_TOPIC: str = Field(default="")
    SUBMISSION_TYPE_ENUM_VALUE: str = Field(default="Submission")
    SUBMISSION_ERROR_TYPE_ENUM_VALUE: str = Field(default="SubmissionError")
    SUBMISSION_DECLINE_TYPE_ENUM_VALUE: str = Field(default="SubmissionDecline")
    SUBMISSION_REFER_TYPE_ENUM_VALUE: str = Field(default="SubmissionRefer")
    SUBMISSION_BOUND_TYPE_ENUM_VALUE: str = Field(default="SubmissionBound")
    SUBMISSION_BOUND_ERROR_TYPE_ENUM_VALUE: str = Field(default="SubmissionBoundError")
    SUBMISSION_NTU_TYPE_ENUM_VALUE: str = Field(default="SubmissionNTU")
    SUBMISSION_NTU_ERROR_TYPE_ENUM_VALUE: str = Field(default="SubmissionNTUError")
    OFFER_TYPE_ENUM_VALUE: str = Field(default="SubmissionOffer")
    EQDBB_PRODUCT_NAME: str = Field(default="EQDBB")
    SENTRY_ENABLED: bool = Field(default=False)
    SENTRY_AUTH_TOKEN: Optional[str] = None
    SENTRY_DSN: Optional[str] = None
    SENTRY_ORG: Optional[str] = None
    SENTRY_PROJECT: Optional[str] = None
    SENTRY_RELEASE: Optional[str] = None
    SENTRY_ENV: str = Field(default="production")

    class Config:
        extra = "forbid"
