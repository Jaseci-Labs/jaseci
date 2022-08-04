# JAC Release Pipeline

Description of JAC pipeline into Azure DevOps.

## Sentinel Set on the Server

Download the '.jac' file and 'sentinel.json' file artifact.

```bash
pip install jaseci   # install jaseci
pip install jq       # jq command is used for reading JSON data.

jsctl login <url>  --username <username> --password <password>  # login to Jaseci
jid=$(cat sentinel.json | jq '.jid' | tr -d '"') # get jid from 'sentinel.json' file and store to ENV variable
jsctl sentinel set <jacCode> -mode code  -snt $jid
```