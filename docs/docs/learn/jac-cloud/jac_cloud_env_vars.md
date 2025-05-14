# **Supported Environment Variable**

| **NAME**  | **DESCRIPTION**   | **DEFAULT**   |
|-----------|-------------------|---------------|
| DATABASE_HOST | MongoDB connection string | mongodb://localhost/?retryWrites=true&w=majority |
| DATABASE_PATH | Local path for DB | mydatabase |
| DATABASE_NAME | MongoDB database name | jaseci |
| REDIS_HOST | Redis connection host | redis://localhost |
| REDIS_PORT | Redis connection port | 6379     |
| REDIS_USER | Redis connection username | null |
| REDIS_PASS | Redis connection password | null |
| DISABLE_AUTO_CLEANUP | Disable auto deletion of nodes that doesn't connect to anything | false |
| SINGLE_QUERY | Every edge_ref will trigger query per anchor if not already cached instead of consolidating non cached anchor before querying. | false |
| SESSION_MAX_TRANSACTION_RETRY | MongoDB's transactional retry | 1 |
| DISABLE_AUTO_ENDPOINT | Disable auto convertion of walker to api. It will now require inner class __specs__ or @specs decorator. | false |
| SESSION_MAX_COMMIT_RETRY | MongoDB's transaction commit retry | 1 |
| RESTRICT_UNVERIFIED_USER | Rstrict user's login until it has verified | false |
| TOKEN_SECRET | Random string used to encrypt token | 50 random characters |
| TOKEN_ALGORITHM | Algorithm used to encrypt token | HS256 |
| TOKEN_TIMEOUT | Token expiration in hours | 12 |
| VERIFICATION_CODE_TIMEOUT | Verification code expiration in hours | 24 |
| RESET_CODE_TIMEOUT | Password reset code expiration in hours | 24 |
| SENDGRID_HOST | Sendgrid host used for hyperlinking verification/reset code | http://localhost:8000 |
| SENDGRID_API_KEY | Sendgrid api key | null    |
| LOGGER_NAME   | Specified logger name | app   |
| LOGGER_LEVEL  | Control log level     | debug |
| LOGGER_FILE_PATH | Log directory and name | /tmp/jac_cloud_logs/jac-cloud.log |
| LOGGER_ROLLOVER_INTERVAL | M = every minute, H = hourly, D = daily, W = weekly | D |
| LOGGER_MAX_BACKUP | Maximum number of backup files before it will deletes old file. Non positive value will not have maximum | -1 |
| LOGGER_ROLLOVER_MAX_FILE_SIZE | Maximum file size in bytes before it will rollover to new file | 10000000 |
| LOGGER_USE_UTC | If logger will use UTC | false |

# **SSO Supported Enviroment Variable**
## Supported Platform
 - APPLE
 - FACEBOOK
 - FITBIT
 - GITHUB
 - GITLAB
 - GOOGLE
 - KAKAO
 - LINE
 - LINKEDIN
 - MICROSOFT
 - NAVER
 - NOTION
 - TWITTER
 - YANDEX

| **NAME**  | **DESCRIPTION**   |
|-----------|-------------------|
| SSO_`{PLATFORM}`_CLIENT_ID | platform's client id |
| SSO_`{PLATFORM}`_CLIENT_SECRET | platform's client secret |
| SSO_`{PLATFORM}`_ALLOW_INSECURE_HTTP | set if platform allow insecure http connection |
| SSO_GITLAB_BASE_ENDPOINT_URL | gitlab base endpoint url |
| SSO_MICROSOFT_TENANT | microsoft tenant |

## Apple Client Secret Auto Generation
- for certificate: Just use either SSO_APPLE_CLIENT_CERTIFICATE_PATH or SSO_APPLE_CLIENT_CERTIFICATE

| **NAME**  | **DESCRIPTION**   |
|-----------|-------------------|
| SSO_APPLE_CLIENT_ID | apple's client id |
| SSO_APPLE_CLIENT_TEAM_ID | apple's client team id |
| SSO_APPLE_CLIENT_KEY | apple's client key |
| SSO_APPLE_CLIENT_CERTIFICATE_PATH | apple's client certificate path |
| SSO_APPLE_CLIENT_CERTIFICATE | apple's client certificate raw content |

## Uvicorn Configs
- You may check [uvicorn settings](https://www.uvicorn.org/settings/) for more informations relates to their respective purpose and formats
- **All comma separated configs should not have space in between values**
- `UV_RELOAD` and `UV_WORKERS` are currently not supported on `jac serve` as we run it via app object instead of import string.
- As alternative, you can run your jac app using `poetry run standalone` to support `UV_WORKERS`. **This trigger will require you to set `APP_PATH` environment variable to point your `jac file`**

| **NAME**  | **UVICORN KWARGS EQUIVALENT** | **DEFAULT** |
|---|---|---|
| UV_HOST   | host | "127.0.0.1" |
| UV_PORT   | port | 8000 |
| UV_UDS    | uds | None |
| UV_FD     | fd | None |
| UV_LOOP   | loop | "auto" |
| UV_HTTP   | http | "auto" |
| UV_WS     | ws | "auto" |
| UV_WS_MAX_SIZE    | ws_max_size | 16777216 |
| UV_WS_MAX_QUEUE   | ws_max_queue | 32 |
| UV_WS_PING_INTERVAL   | ws_ping_interval | 20.0 |
| UV_WS_PING_TIMEOUT    | ws_ping_timeout | 20.0 |
| UV_WS_PER_MESSAGE_DEFLATE     | ws_per_message_deflate | True |
| UV_LIFESPAN   | lifespan | "auto" |
| UV_INTERFACE  | interface | "auto" |
| ~~UV_RELOAD~~     | reload | False |
| UV_RELOAD_DIRS    | reload_dirs | None |
| UV_RELOAD_INCLUDES    | reload_includes | None |
| UV_RELOAD_EXCLUDES    | reload_excludes | None |
| UV_RELOAD_DELAY   | reload_delay | 0.25 |
| ~~UV_WORKERS~~    | workers | None |
| UV_ENV_FILE   | env_file | None |
| UV_LOG_CONFIG     | log_config | LOGGING_CONFIG |
| UV_LOG_LEVEL  | log_level | None |
| UV_ACCESS_LOG     | access_log | True |
| UV_PROXY_HEADERS  | proxy_headers | True |
| UV_SERVER_HEADER  | server_header | True |
| UV_DATE_HEADER    | date_header | True |
| UV_FORWARDED_ALLOW_IPS    | forwarded_allow_ips | None |
| UV_ROOT_PATH  | root_path | "" |
| UV_LIMIT_CONCURRENCY  | limit_concurrency | None |
| UV_BACKLOG    | backlog | 2048 |
| UV_LIMIT_MAX_REQUESTS     | limit_max_requests | None |
| UV_TIMEOUT_KEEP_ALIVE     | timeout_keep_alive | 5 |
| UV_TIMEOUT_GRACEFUL_SHUTDOWN  | timeout_graceful_shutdown | None |
| UV_SSL_KEYFILE    | ssl_keyfile | None |
| UV_SSL_CERTFILE   | ssl_certfile | None |
| UV_SSL_KEYFILE_PASSWORD   | ssl_keyfile_password | None |
| UV_SSL_VERSION    | ssl_version | SSL_PROTOCOL_VERSION |
| UV_SSL_CERT_REQS  | ssl_cert_reqs | ssl.CERT_NONE |
| UV_SSL_CA_CERTS   | ssl_ca_certs | None |
| UV_SSL_CIPHERS    | ssl_ciphers | "TLSv1" |
| UV_HEADERS    | headers | None |
| UV_USE_COLORS     | use_colors | None |
| UV_APP_DIR    | app_dir | None |
| UV_FACTORY    | factory | False |
| UV_H11_MAX_INCOMPLETE_EVENT_SIZE | h11_max_incomplete_event_size | None |