# Logging
* jac-cloud server logs incoming requests and outgoing responses by default to log files stored in `/tmp/` directory
* The log files are on a daily rotation. Meaning there will be a new log file created every day to prevent log files gets too large.
* For production usage, we recommend connect your jac-cloud logs to an Elastic instance.
# Quick Start: Integration with Elasitc
* Assuming you have a running Elastic instance, you just need to use filebeat to ingest the log files into elastic.
* We provide a template filebeat config file to get started at `scripts/filebeat-template.yaml`. If you want to adopt the default configuration, simply change the `hosts` and `api_key` field.
  * Change the hosts field to point to your elastic instance. 

> :warning: It seems that filebeat automatically append a 9200 port to the host URL if no port is specified. If your elastic instance is behind a load balancer and simply has a URL without a custom port, you will need to add either :80 or :443 to the hosts config. For example, `hosts: ["https://my_elastic_instance.me.com:443/]`

* Then simply run `filebeat -e -c scripts/filebeat-template.yaml`.

## More Details on Configuring and Starting Filebeat
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
    - `sudo cp filebeat.yml /etc/filebeat/filebeat.yml`
    - `sudo filebeat -e`
- normal run
    - `filebeat -e -c filebeat.yml`
- for complete documentation
    - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-search-use-cases-python-logs.html
    - https://www.elastic.co/guide/en/beats/filebeat/current/configuring-howto-filebeat.html

## Additional Env Vars to customize logger
| **NAME**  | **DESCRIPTION**   | **DEFAULT**   |
|-----------|-------------------|---------------|
| LOGGER_NAME   | Specified logger name | app   |
| LOGGER_LEVEL  | Control log level     | debug |
| LOGGER_FILE_PATH | Log directory and name | /tmp/jac_cloud_logs/jac-cloud.log |
| LOGGER_ROLLOVER_INTERVAL | M = every minute, H = hourly, D = daily, W = weekly | D |
| LOGGER_MAX_BACKUP | Maximum number of backup files before it will deletes old file. Non positive value will not have maximum | -1 |
| LOGGER_ROLLOVER_MAX_FILE_SIZE | Maximum file size in bytes before it will rollover to new file | 10000000 |
| LOGGER_USE_UTC | If logger will use UTC | false |