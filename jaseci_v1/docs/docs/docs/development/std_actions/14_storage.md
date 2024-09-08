# **`Storage Actions`**
- These actions will allow managing of files thru 3rd party cloud storage. It also supports multiple provider via preferred provider referrencing mapping
- These actions also requires storage service and this service is powered by [apache-libcloud](https://libcloud.apache.org/)'s [storage driver](https://libcloud.readthedocs.io/en/stable/storage/api.html)
- You may see supported cloud service [here](https://libcloud.readthedocs.io/en/stable/storage/supported_providers.html) and their supported methods

## **HOW TO SETUP**
First, make sure **`Storage Service`** is enabled by setting the `enabled` field in `STORE_CONFIG` to be true. We first get the current config via the `config_get` endpoint. (We are going to use jsctl for the following examples but you can also use API requests)

Run the following command in `jsctl` shell.

```bash
config get STORE_CONFIG
```

This will return a json of the current configuration for the Storage Service. Check the field and make sure they are configured to your needs. (More details on the configuration attributes below.)

Update the `enabled` field to be True if it is not already.
Then save it with `config_set`.

```bash
config set STORE_CONFIG -value JSON_STRING_OF_THE_CONFIG
```

Final step to enable **`Storage Service`** is to refresh allow the updated configuration to take effect.

```bash
service refresh store
```

JSORC will then refresh the Storage service and storage actions should now be working.

### **CONFIGURATION**

#### **`ATTRIBUTES`**

| Attribute                                             | Description                                                           |
| ----------------------------------------------------- | --------------------------------------------------------------------- |
| enabled                                               | If service is enabled in config. The service can be available (upon building) but not enabled (from config)                 |
| quiet                                                 | if error logs should be suppressed                                    |
| default                                               | default provider reference used                                       |
| providers                                             | your provider referrence mapping                                      |
| providers\[`"mapping_name ex: azure"`\].provider      | your provider's driver                                                |
| providers\[`"mapping_name ex: azure"`\].container     | your default container if support by cloud storage                    |
| providers\[`"mapping_name ex: azure"`\].credentials   | driver's credentials. Please see `credential structure` for reference   |
#### **`credentials structure`**
```js
"credentials": {
    "key": "this is required!", // (str) – API key or username to be used (required)
    "secret": "this is required!", // (str) – Secret password to be used (required)
    //-------------------------------------------------//
    //                 OPTIONAL FIELDS                 //
    //-------------------------------------------------//
    "secure": true, // (bool) – Whether to use HTTPS or HTTP. Note: Some providers only support HTTPS, and it is on by default.
    "host": null, // (str) – Override hostname used for connections.
    "port": null, // (int) – Override port used for connections.
    "api_version": null, // (str) – Optional API version. Only used by drivers which support multiple API versions.
    "region": null, // (str) – Optional driver region. Only used by drivers which support multiple regions.
    //-------------------------------------------------//
}
```
### **`DEFAULT CONFIG`**

```js
STORE_CONFIG = {
    "enabled": False,
    "quiet": False,
    "default": None,
    "providers": {},
}

// defaults to empty
// admin can declare here if they wish to deploy their own cloud storage inside the cluster
STORE_MANIFEST = {/* KUBE MANIFEST */}
```

### **`ENABLED CONFIG`**

```js
//-------------------------------------------------//
//                PROVIDER'S DRIVER                //
//-------------------------------------------------//
// ALIYUN_OSS = "aliyun_oss"
// AURORAOBJECTS = "auroraobjects"
// AZURE_BLOBS = "azure_blobs"
// BACKBLAZE_B2 = "backblaze_b2"
// CLOUDFILES = "cloudfiles"
// DIGITALOCEAN_SPACES = "digitalocean_spaces"
// GOOGLE_STORAGE = "google_storage"
// KTUCLOUD = "ktucloud"
// LOCAL = "local"
// NIMBUS = "nimbus"
// NINEFOLD = "ninefold"
// OPENSTACK_SWIFT = "openstack_swift"
// S3 = "s3"
// S3_AP_NORTHEAST = "s3_ap_northeast"
// S3_AP_NORTHEAST1 = "s3_ap_northeast_1"
// S3_AP_NORTHEAST2 = "s3_ap_northeast_2"
// S3_AP_SOUTH = "s3_ap_south"
// S3_AP_SOUTHEAST = "s3_ap_southeast"
// S3_AP_SOUTHEAST2 = "s3_ap_southeast2"
// S3_CA_CENTRAL = "s3_ca_central"
// S3_CN_NORTH = "s3_cn_north"
// S3_CN_NORTHWEST = "s3_cn_northwest"
// S3_EU_WEST = "s3_eu_west"
// S3_EU_WEST2 = "s3_eu_west_2"
// S3_EU_CENTRAL = "s3_eu_central"
// S3_EU_NORTH1 = "s3_eu_north_1"
// S3_SA_EAST = "s3_sa_east"
// S3_US_EAST2 = "s3_us_east_2"
// S3_US_WEST = "s3_us_west"
// S3_US_WEST_OREGON = "s3_us_west_oregon"
// S3_US_GOV_WEST = "s3_us_gov_west"
// S3_RGW = "s3_rgw"
// S3_RGW_OUTSCALE = "s3_rgw_outscale"
// MINIO = "minio"
// SCALEWAY = "scaleway"
// OVH = "ovh"
//-------------------------------------------------//

STORE_CONFIG = {
	"enabled": true,
	"quiet": false,
	"default": "YOUR_DEFAULT_PROVIDER_REFENCE_EX: azure",
	"providers": {
		"azure": { // your preferred provider "reference" name
			"provider": "azure_blobs", // your preferred provider's driver
			"container": "zsb-testing", // your default container if support by cloud storage
			"credentials": { // your cloud storage credentials to allow api calls
				"key": "zsbstoragetesting",
				"secret": "J1V5OFQYQdLzoy0bnLn4igpAtNZYmgd6gD4Lu8W7EpYWPcqtf4l5QGJsCatZRU9+Ql7ZWjPmusvf+ASt0E3+zQ=="
			}
		}
	}
}
```
## store.**`upload`**
> **`Arguments`:** \
> **file**: *str* \
> **provider**: *str* = None \
> **container**: *str* = None
>
> **`Return`:** \
> returns file cdn url with expiration
>
> **`Usage`:** \
> Uploading files to your cloud storage
>
> **`Remarks`:** \
> file requires uuid from file handler (`fh`) actions or from file type field on walker run
##### **`HOW TO TRIGGER USING FILE HANDLER`**
```js
file = fh.new("testing.txt");
fh.open(file, "w"); // open the created file
fh.write(file, "testing only"); // write some text on it
fh.close(file); // closing the file

store.upload(file, "azure"); // upload the file on azure provider
// or
store.upload(file); // upload the file on your default provider reference
```
##### **`HOW TO TRIGGER USING WALKER RUN FILE UPLOAD`**
```js
walker sample {
    has files;
    can store.upload;

    with entry {
        store.upload(files[0], "azure"); // upload the file on azure provider
        // or
        store.upload(files[0]); // upload the file on your default provider reference
    }
}

```
---
## store.**`download`**
> **`Arguments`:** \
> **file**: *str* \
> **provider**: *str* = None \
> **container**: *str* = None
>
> **`Return`:** \
> file's uuid *(`str`)*
>
> **`Usage`:** \
> downloading file from your cloud storage
>
> **`Remarks`:** \
> param file is the absolute_name of the file if it's uploaded via store.upload \
> you may get it before uploading the file by triggering fh.`attr`("file's uuid")["absolute_name"]
##### **`HOW TO TRIGGER`**
```js
store.download("3201ea8f-7c2a-4633-a132-2b0dbbda6c3d-testing.txt");
```
---
## store.**`delete`**
> **`Arguments`:** \
> **file**: *str* \
> **provider**: *str* = None \
> **container**: *str* = None
>
> **`Return`:** \
> bool - true if success
>
> **`Usage`:** \
> removing file from your cloud storage
>
> **`Remarks`:** \
> param file is the absolute_name of the file if it's uploaded via store.upload \
> you may get it before uploading the file by triggering fh.`attr`("file's uuid")["absolute_name"]
##### **`HOW TO TRIGGER`**
```js
store.delete("3201ea8f-7c2a-4633-a132-2b0dbbda6c3d-testing.txt");
```

create_container(name: str, provider: str = None):
has_container(name: str, provider: str = None):
delete_container(name: str, provider: str = None):
---
## store.**`create_container`**
> **`Arguments`:** \
> **container**: *str* \
> **provider**: *str* = None
>
> **`Return`:** \
> bool - true if success
>
> **`Usage`:** \
> Adding additional container
##### **`HOW TO TRIGGER`**
```js
store.create_container("container1");
```
---
## store.**`has_container`**
> **`Arguments`:** \
> **container**: *str* \
> **provider**: *str* = None
>
> **`Return`:** \
> bool - true if success
>
> **`Usage`:** \
> checking if container exists
##### **`HOW TO TRIGGER`**
```js
store.has_container("container1");
```
---
## store.**`delete_container`**
> **`Arguments`:** \
> **container**: *str* \
> **provider**: *str* = None
>
> **`Return`:** \
> bool - true if success
>
> **`Usage`:** \
> Adding additional container
##### **`HOW TO TRIGGER`**
```js
store.delete_container("container1");
```