[<< back to main](../README.md)
# **Logger**
> Default logger follows elastic formatting. This is to support filebeat integration.

## **Enable Filebeat**
- [Download](https://www.elastic.co/downloads/beats/filebeat) and install filebeat.
- setup yml based on your setup
```yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /tmp/jac_cloud_logs/*-jac-cloud-*.log
    - /tmp/jac_cloud_logs/jac-cloud.log
  json:
    keys_under_root: true
    overwrite_keys: true
    add_error_key: true
    expand_keys: true

output.elasticsearch:
  hosts: ["localhost:9200"]
  protocol: https
  api_key: "id:api_key"
  index: "filebeat-testing"

setup.template.name: "filebeat"
setup.template.pattern: "filebeat-*"
```
- to run without restriction, run filebeat as root
    - sudo cp filebeat.yml /etc/filebeat/filebeat.yml
    - sudo filebeat -e
- normal run
    - filebeat -e -c filebeat.yml
- for complete documentation
    - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-search-use-cases-python-logs.html
    - https://www.elastic.co/guide/en/beats/filebeat/current/configuring-howto-filebeat.html

## Logger Configurations
| **NAME**  | **DESCRIPTION**   | **DEFAULT**   |
|-----------|-------------------|---------------|
| LOGGER_NAME   | Specified logger name | app   |
| LOGGER_LEVEL  | Control log level     | debug |
| LOGGER_FILE_PATH | Log directory and name | /tmp/jac_cloud_logs/jac-cloud.log |
| LOGGER_ROLLOVER_INTERVAL | M = every minute, H = hourly, D = daily, W = weekly | D |
| LOGGER_MAX_BACKUP | Maximum number of backup files before it will deletes old file. Non positive value will not have maximum | -1 |
| LOGGER_ROLLOVER_MAX_FILE_SIZE | Maximum file size in bytes before it will rollover to new file | 10000000 |
| LOGGER_USE_UTC | If logger will use UTC | false |