# Generic Build and Deploy Pipeline

This Jenkinsfile contains the generic pipeline for
building and deploying a containerized microservice
at Capsule.

## Usage

Check out [Using the Generic Pipeline](https://capsulerx.atlassian.net/wiki/spaces/devops/pages/1275396097/Using+the+Generic+Pipeline)
for a quick look at how to setup this pipeline in Jenkins to begin
building and deploying your application.

If you're interested in providing custom build-args, tags, etc. you'll want
refer to [Jenkins Pipeline Functions](https://capsulerx.atlassian.net/wiki/spaces/devops/pages/982516013/Jenkins+Pipeline+Functions)
for all the parameters you can tweak.

## Multi-dockerfile considerations

If your repo contains multiple Dockerfiles you want to build as part
of the CI/CD process, refer to
[Multi-Dockerfile Build and Deploy Pipeline](https://capsulerx.atlassian.net/wiki/spaces/devops/pages/1321795902/Multi-Dockerfile+Build+and+Deploy+Pipeline)
for an example pipeline using `generic.buildImages`.
