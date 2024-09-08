# Velero
* Take backups of your cluster and restore in case of loss.
* Migrate cluster resources to other clusters.
* Replicate your production cluster to development and testing clusters.

## Installation
Prerequisites
* Access to a Kubernetes cluster.
* kubectl installed locally

you can use [Chocolatey](https://chocolatey.org/install) to install velero.

```bash
choco install velero
```

1. Create S3 bucket

Velero requires an object storage bucket to store backups in, preferably unique to a single Kubernetes cluster. Create an S3 bucket, replacing placeholders appropriately:
```bash
BUCKET=<YOUR_BUCKET>
REGION=<YOUR_REGION>
aws s3api create-bucket --bucket $BUCKET  --region $REGION
```
2. Create an AWS IAM user for Velero
* Create the IAM user:

```bash
aws iam create-user --user-name velero
```
* Attach policies to give velero the necessary permissions:
```bash
cat > velero-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:DescribeSnapshots",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": [
                "arn:aws:s3:::${BUCKET}/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::${BUCKET}"
            ]
        }
    ]
}
EOF
```

```bash
aws iam put-user-policy \
  --user-name velero \
  --policy-name velero \
  --policy-document file://velero-policy.json
```
* Create an access key for the user:
```bash
aws iam create-access-key --user-name velero
```
The result should look like:

```bash
{
  "AccessKey": {
        "UserName": "velero",
        "Status": "Active",
        "CreateDate": "2022-10-31T22:24:41.576Z",
        "SecretAccessKey": <AWS_SECRET_ACCESS_KEY>,
        "AccessKeyId": <AWS_ACCESS_KEY_ID>
  }
}
```

* Create a Velero-specific credentials file (credentials-velero) in your local directory:
```bash
[default]
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
```
3. Install and start Velero

Install Velero, including all prerequisites, into the cluster and start the deployment. This will create a namespace called velero, and place a deployment named velero in it.
```bash
velero install \
    --provider aws \
    --bucket $BUCKET \
    --secret-file ./credentials-velero \
    --backup-location-config region=$REGION \
    --snapshot-location-config region=$REGION
```

4. To check
   ```bash
   kubectl get all -n velero
   ```

# Backup
1. Schedule a Backup

The schedule operation allows you to create a backup of your data at a specified time, defined by a Cron expression.
```bash
velero schedule create <NAME> --schedule="* * * * *"
```
Cron schedules use the following format.
```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * *
```

2. Create a backup

```
velero backup create --from-schedule <NAME> --include-namespaces default
```

3. To check
```
velero backup describe <NAME>
```
# Restore
```
velero restore create --from-backup <NAME>

velero restore get
```