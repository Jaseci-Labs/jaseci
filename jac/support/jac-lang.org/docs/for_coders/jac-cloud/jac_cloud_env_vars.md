# **Supported Environment Variable**

| **NAME**                      | **DESCRIPTION**                                                                                                                | **DEFAULT**                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| HOST                          | FastAPI's host argument                                                                                                        | 0.0.0.0                                          |
| PORT                          | FastAPI's port argument                                                                                                        | 8000                                             |
| DATABASE_HOST                 | MongoDB connection string                                                                                                      | mongodb://localhost/?retryWrites=true&w=majority |
| DATABASE_PATH                 | Local path for DB                                                                                                              | mydatabase                                       |
| DATABASE_NAME                 | MongoDB database name                                                                                                          | jaseci                                           |
| REDIS_HOST                    | Redis connection host                                                                                                          | redis://localhost                                |
| REDIS_PORT                    | Redis connection port                                                                                                          | 6379                                             |
| REDIS_USER                    | Redis connection username                                                                                                      | null                                             |
| REDIS_PASS                    | Redis connection password                                                                                                      | null                                             |
| REDIS_MAX_RETRY               | Redis maximum retry on connection/timeout error                                                                                | 5                                                |
| REDIS_RETRY_BACKOFF_BASE      | Redis retry initial backoff time                                                                                               | 1                                                |
| REDIS_RETRY_BACKOFF_CAP       | Redis retry maximum backoff time                                                                                               | 10                                               |
| DISABLE_AUTO_CLEANUP          | Disable auto deletion of nodes that doesn't connect to anything                                                                | false                                            |
| SINGLE_QUERY                  | Every edge_ref will trigger query per anchor if not already cached instead of consolidating non cached anchor before querying. | false                                            |
| SESSION_MAX_TRANSACTION_RETRY | MongoDB's transactional retry                                                                                                  | 1                                                |
| DISABLE_AUTO_ENDPOINT         | Disable auto convertion of walker to api. It will now require inner class **specs** or @specs decorator.                       | false                                            |
| SHOW_ENDPOINT_RETURNS         | Include per visit return on api response                                                                                       | false                                            |
| SESSION_MAX_COMMIT_RETRY      | MongoDB's transaction commit retry                                                                                             | 1                                                |
| RESTRICT_UNVERIFIED_USER      | Rstrict user's login until it has verified                                                                                     | false                                            |
| TOKEN_SECRET                  | Random string used to encrypt token                                                                                            | 50 random characters                             |
| TOKEN_ALGORITHM               | Algorithm used to encrypt token                                                                                                | HS256                                            |
| TOKEN_TIMEOUT                 | Token expiration in hours                                                                                                      | 12                                               |
| VERIFICATION_CODE_TIMEOUT     | Verification code expiration in hours                                                                                          | 24                                               |
| RESET_CODE_TIMEOUT            | Password reset code expiration in hours                                                                                        | 24                                               |
| SENDGRID_HOST                 | Sendgrid host used for hyperlinking verification/reset code                                                                    | http://localhost:8000                            |
| SENDGRID_API_KEY              | Sendgrid api key                                                                                                               | null                                             |
| LOGGER_NAME                   | Specified logger name                                                                                                          | app                                              |
| LOGGER_LEVEL                  | Control log level                                                                                                              | debug                                            |
| LOGGER_FILE_PATH              | Log directory and name                                                                                                         | /tmp/jac_cloud_logs/jac-cloud.log                |
| LOGGER_ROLLOVER_INTERVAL      | M = every minute, H = hourly, D = daily, W = weekly                                                                            | D                                                |
| LOGGER_MAX_BACKUP             | Maximum number of backup files before it will deletes old file. Non positive value will not have maximum                       | -1                                               |
| LOGGER_ROLLOVER_MAX_FILE_SIZE | Maximum file size in bytes before it will rollover to new file                                                                 | 10000000                                         |
| LOGGER_USE_UTC                | If logger will use UTC                                                                                                         | false                                            |
| SCHEDULER_MAX_THREAD          | Maximum thread workers for scheduled workers                                                                                   | 5                                                |
| SCHEDULER_MAX_PROCESS         | Maximum process workers for scheduled workers                                                                                  | 1                                                |
| TASK_CONSUMER_CRON_SECOND     | Task consumer cron trigger in seconds                                                                                          | N/A                                              |
| TASK_CONSUMER_MULTITASK       | Task consumer max running task simultaneously                                                                                  | 1                                                |

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

| **NAME**                               | **DESCRIPTION**                                |
| -------------------------------------- | ---------------------------------------------- |
| SSO\_`{PLATFORM}`\_CLIENT_ID           | platform's client id                           |
| SSO\_`{PLATFORM}`\_CLIENT_SECRET       | platform's client secret                       |
| SSO\_`{PLATFORM}`\_ALLOW_INSECURE_HTTP | set if platform allow insecure http connection |
| SSO_GITLAB_BASE_ENDPOINT_URL           | gitlab base endpoint url                       |
| SSO_MICROSOFT_TENANT                   | microsoft tenant                               |

## Apple Client Secret Auto Generation

- for certificate: Just use either SSO_APPLE_CLIENT_CERTIFICATE_PATH or SSO_APPLE_CLIENT_CERTIFICATE

| **NAME**                          | **DESCRIPTION**                        |
| --------------------------------- | -------------------------------------- |
| SSO_APPLE_CLIENT_ID               | apple's client id                      |
| SSO_APPLE_CLIENT_TEAM_ID          | apple's client team id                 |
| SSO_APPLE_CLIENT_KEY              | apple's client key                     |
| SSO_APPLE_CLIENT_CERTIFICATE_PATH | apple's client certificate path        |
| SSO_APPLE_CLIENT_CERTIFICATE      | apple's client certificate raw content |
