# mxklabs-bucket-cloudrun-wrapper

The code in this repository is designed to run on Google's [Cloud Run](https://cloud.google.com/compute/cloud-run) service to serve a static website using a [Cloud Storage bucket](https://cloud.google.com/storage/) as the back-end file store. Google have their own [tutorial](https://cloud.google.com/storage/docs/hosting-static-website) for as to how to configure a bucket to host a static website but, as it turns out, this requires setting up two load balancers and reserving an IP address, amounting to a non-insignificant cost per month. In contrast, Cloud Run is essentially zero scale and hence using this solution will cost you a few pennies if your website is low traffic.



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

