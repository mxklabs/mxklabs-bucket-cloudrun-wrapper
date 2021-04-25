This repository enables you to host a static web site using [Cloud Run](https://cloud.google.com/compute/cloud-run) by serving files from a [Cloud Storage Bucket](https://cloud.google.com/storage/) via Google's APIs.

If your website is relatively low-traffic and the files in your bucket are not obscenely large, this is a very cost-effective way of hosting a static web site. The cost of the load balancers and IP addresses required in Google's tutorial](https://cloud.google.com/storage/docs/hosting-static-website) add up to about £15/month whereas I generally pay less than £0.10/month in [Cloud Run](https://cloud.google.com/compute/cloud-run) and [Cloud Bucket](https://cloud.google.com/storage/docs/creating-buckets) costs by using this repository.

### Assumptions & Prerequisites

* You have access to a Google Cloud Platform account.
* You have a Google Cloud Project with billing enabled (more info [here](https://cloud.google.com/billing/docs/how-to/modify-project)).
* You have a domain that you own or manage.
* You have `git`, `docker` and `gcloud` set up on your computer.

### Setting up a Cloud Storage Bucket

* Create a new Cloud Storage Bucket (more info [here](https://cloud.google.com/storage/docs/creating-buckets)). For Access Control, the easiest option is to choose Uniform. Optionally, add `allUsers` with roles `Storage Legacy Bucket Reader` and a `Storage Legacy Object Reader` to make your bucket's content available publically.
* Create a static website comprising of, e.g., `.html`, `.js` and `.css` files and upload the files to your bucket (more info [here](https://cloud.google.com/storage/docs/uploading-objects)). Make sure to add a `index.html` as your root document.

### Building & pushing a Docker image

The instructions below assume `$MY_PROJECT` is your Google Cloud Project name.

* Clone this repo:
  ```
  git clone git@github.com:mxklabs/mxklabs-bucket-cloudrun-wrapper.git
  ```
* Log in to `gcloud`:
  ```
  gcloud auth login
  ```
* Set up docker authenication for gcloud:
  ```
  gcloud auth configure-docker
  ```
* Set your project:
  ```
  gcloud config set project $MY_PROJECT
  ```
* Build the docker container:
  ```
  cd mxklabs-bucket-cloudrun-wrapper
  docker build -t gcr.io/$MY_PROJECT/wrapper:latest --cache-from gcr.io/$MY_PROJECT/wrapper:latest .
  ```
* Push the container to Google's container registry:
  ```
  docker push gcr.io/$MY_PROJECT/wrapper:latest
  ```

### Deploy to Cloud Run

The instructions below assume `$MY_PROJECT` is your Google Cloud Project name and `$MY_BUCKET` is your bucket name. We also assume you already followed the steps above.

* Log in to `gcloud`:
  ```
  gcloud auth login
  ```
* Set your project:
  ```
  gcloud config set project $MY_PROJECT
  ```
* Enable Cloud Run API:
  ```
  gcloud services enable run.googleapis.com
  ```
* Enable Google Storage Client API:
  ```

  ```



#### 

#### Optional Environment Variables



## Local Development

The instructions below assume `$MY_BUCKET` is your bucket name and your key file is downloaded into `$KEY_FILE`. We also assume your current working directory is your clone of this git repository.

* Install Python 3.7 (more info [here](https://www.python.org/downloads/)).
* Install pip dependencies (preferably in a virtual env):
  ```
  pip install -r requirements.txt
  ```
* Create a service account and download a new JSON key file (more info [here](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python)).
* Run the app:
  ```
  GOOGLE_APPLICATION_CREDENTIALS=KEY_FILE BUCKET_NAME=$MY_BUCKET python main.py
  ```
  where 

Create service account: https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python

Storage Object Viewer

Create a service account key:

In the Cloud Console, click the email address for the service account that you created.
Click Keys.
Click Add key, then click Create new key.
Click Create. A JSON key file is downloaded to your computer.
Click Close.

Enable Cloud Run API


