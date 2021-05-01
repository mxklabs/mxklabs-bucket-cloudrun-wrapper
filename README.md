This repository enables you to host a static web site from a [Cloud Storage Bucket](https://cloud.google.com/storage/) using [Cloud Run](https://cloud.google.com/compute/cloud-run) and Google APIs.

If your website is relatively low-traffic and the files in your bucket are not obscenely large, this repository offers a very cost-effective way of hosting a static web site. I generally pay less than £0.10/month in [Cloud Run](https://cloud.google.com/compute/cloud-run) and [Cloud Bucket](https://cloud.google.com/storage/docs/creating-buckets) costs. In contrast, hosting a static website using the method explained in Google's own [tutorials](https://cloud.google.com/storage/docs/hosting-static-website) will set you back the cost of two load balancers and an IP address reservation which, in my experiments, totals at about £15/month. There is no need to pay for load balancers or IP address reservations when you use [Cloud Run](https://cloud.google.com/compute/cloud-run).

### Prerequisites

The instructions below make the following assumptions:

* You have access to a Google Cloud Platform account.
* You have a Google Cloud Project with billing enabled (more info [here](https://cloud.google.com/billing/docs/how-to/modify-project)). 
* You have set environment variable `$MY_PROJECT` to your project's name, for example:
  ```
  export MY_PROJECT=example
  ```
* You have a domain that Google has verified as a domain you own or manage.
* You have set environment variable `$MY_DOMAIN` to your domain name, for example:
  ```
  export MY_PROJECT=files.example.com
  ```
* You have `git`, `docker` and `gcloud` set up on your computer.

### Creating a Cloud Storage Bucket

In these steps we'll create a [Cloud Storage Bucket](https://cloud.google.com/storage/) responsible for storing the files that make up your web site:

* Create a new Cloud Storage Bucket (more info [here](https://cloud.google.com/storage/docs/creating-buckets)). For Access Control, the easiest option is to choose Uniform. Optionally, add `allUsers` with roles `Storage Legacy Bucket Reader` and a `Storage Legacy Object Reader` to make your bucket's content available publically.
* Create a static website comprising of, e.g., `.html`, `.js` and `.css` files and upload the files to your bucket (more info [here](https://cloud.google.com/storage/docs/uploading-objects)). Make sure to add a `index.html` as your root document.
* Set environment variable `$MY_BUCKET` to the name of your bucket, for example:
  ```
  export MY_BUCKET=files.example.com
  ```

### Enable Container Registry & Build and Push Docker Image

In these steps we'll enable Google's [Container Registry](https://cloud.google.com/container-registry) for your project, build a Docker container and push it to the registry ready for deployment on [Cloud Run](https://cloud.google.com/compute/cloud-run):

* Log in to `gcloud`:
  ```
  gcloud auth login
  ```
* Set your project:
  ```
  gcloud config set project $MY_PROJECT
  ```
* Enable Google's docker container registry for your project:
  ```
  gcloud services enable containerregistry.googleapis.com
  ```
* Set up docker authenication for gcloud:
  ```
  gcloud auth configure-docker
  ```
* Clone the repository:
  ```
  git clone git@github.com:mxklabs/mxklabs-bucket-cloudrun-wrapper.git
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

### Deploy Docker Container to Cloud Run

In these steps we will deploy the Docker Container to [Cloud Run](https://cloud.google.com/compute/cloud-run):

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
* Deploy a new `wrapper` service (more info [here](https://cloud.google.com/sdk/gcloud/reference/run/deploy)):
  ```
  gcloud run deploy wrapper --image gcr.io/$MY_PROJECT/wrapper:latest --region us-central1 --platform managed --allow-unauthenticated --set-env-vars=BUCKET_NAME=$MY_BUCKET
  ```
* Set a domain mapping:
  ```
  gcloud beta run domain-mappings create --service=wrapper --domain=$MY_DOMAIN --platform=managed
  ```
* The previous command will output some DNS records that you have to set on your domain for the domain mapping to work. Set the DNS records as instructed using your domain registrar service (e.g. [Google Domains](https://domains.google.com/) or similar).

#### Notes on Development Environment

You can run the `main.py` script locally for testing purposes. However, unlike when running on [Cloud Run](https://cloud.google.com/compute/cloud-run), authentication is not automatic.

* Install Python 3.7 (more info [here](https://www.python.org/downloads/)).
* Install pip dependencies (more info [here](https://packaging.python.org/tutorials/installing-packages/)):
  ```
  pip install -r requirements.txt
  ```
* Create a service account and download a new JSON key file (more info [here](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python)).
* Set environment variable `$MY_KEY` to the path of the JSON file you just downloaded, for example:
  ```
  export MY_KEY=/home/jsmith/example-key.json
  ```
* Run the app as follows:
  ```
  GOOGLE_APPLICATION_CREDENTIALS=$MY_KEY BUCKET_NAME=$MY_BUCKET python main.py
  ```
* Open `http://0.0.0.0:8080` in your favorite browser.

If permissions are an issue, make sure the service account you created has the `Storage Object Viewer` permission for your bucket.

#### Notes on Environment Variables

The script supports the following environment variables:

| Variable    | Nature      | Default     | Description |
| ----------- | ----------- | ----------- | ----------- |
| BUCKET_NAME | Required    | N/A         | The name of the [Cloud Storage Bucket](https://cloud.google.com/storage/) to serve files from  |
| PORT        | Optional    | "8080"      | The port number the script will listen on (leave unset on [Cloud Run](https://cloud.google.com/compute/cloud-run)) |
| HOSTNAME    | Optional    | "0.0.0.0"   | The hostname the script will bind to (leave unset on [Cloud Run](https://cloud.google.com/compute/cloud-run)) |
| HOME_PAGE    | Optional    | "/index.html"   | The file to serve when an HTTP request for "/" is received. |
