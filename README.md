# mxklabs-bucket-cloudrun-wrapper

ℹ️: | Google have their own [tutorial](https://cloud.google.com/storage/docs/hosting-static-website) describing how you can configure a Google Storage bucket to host a static website but, as it turns out, this solution uses two load balancers and reserving an IP address, amounting to a significant monthly cost. In contrast, Cloud Run is zero scale and hence using this solution will have minimal cost for a low traffic web site.
:---: | :---

The code in this repository is designed to host a static web site run on [Cloud Run](https://cloud.google.com/compute/cloud-run), serving files as stored in a [Storage Bucket](https://cloud.google.com/storage/).

## Deploy on Google Cloud

#### 

#### Optional Environment Variables



## Development

Create service account: https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python

Storage Object Viewer

Create a service account key:

In the Cloud Console, click the email address for the service account that you created.
Click Keys.
Click Add key, then click Create new key.
Click Create. A JSON key file is downloaded to your computer.
Click Close.

Enable Cloud Run API

Deploy any changes using the following commands:
```
gcloud config set project <project-name>
gcloud builds submit
```

==

gcloud auth configure-docker

docker build -t gcr.io/snapscraprepeat/wrapper:latest --cache-from gcr.io/snapscraprepeat/wrapper:latest .

docker push gcr.io/snapscraprepeat/wrapper:latest

