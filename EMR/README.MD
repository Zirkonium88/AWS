# Amazon EMR

Elastic mapre reduce jobs with AWS are pretty easy to fulfill. 

## Configure Zeppelin

* I like to use [Zeppelin](https://zeppelin.apache.org). It's more capable, then Jupyternotebooks which can be used by default. By using this configuration file, no access are needed. Instead, use AWS roles on your instances. The config [file](https://github.com/Zirkonium88/AWS/blob/master/EMR/EMR-config-zeppelin.json) needs to be used under advanced options.

![alt text](https://github.com/Zirkonium88/AWS/blob/master/EMR/Screenshot.png)

```json
[
  {
      "Classification": "zeppelin-env", # Initialise the Zeppelin
      "Configurations": [
        {
          "Classification": "export", # Export your notebook to Amazon s3
          "Properties": {
            "ZEPPELIN_NOTEBOOK_S3_USER": "zeppelin-usernamer", # Bucket folder, named by user
            "ZEPPELIN_NOTEBOOK_S3_BUCKET": "myBucket-for-emr-jobs", # Define a bucket - needs already to exist
            "ZEPPELIN_NOTEBOOK_S3_ENDPOINT": "s3.amazonaws.com",
            "ZEPPELIN_NOTEBOOK_STORAGE": "org.apache.zeppelin.notebook.repo.S3NotebookRepo"
          },
        }
      ]
    }
  ]
  
  
````
