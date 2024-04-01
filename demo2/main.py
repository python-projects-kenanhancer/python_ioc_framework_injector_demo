from config import Config

config = Config(
    EVENT_STORAGE_BASE_URL="https://example.com",
    ROUTING_SERVICE_BASE_URL="https://example-service.com",
    OCP_APIM_SUBSCRIPTION_KEY="your-key-here",
    AUTH_TOKEN_URL="https://auth.example.com",
    AUTH_TOKEN_CLIENT_ID="client-id",
    AUTH_TOKEN_CLIENT_SECRET="client-secret",
    AUTH_TOKEN_SCOPE="scope",
)

if __name__ == '__main__':
    print(config.dict())
