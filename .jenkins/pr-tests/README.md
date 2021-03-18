# PR Tests Pipeline

This Jenkinsfile contains a pipeline you can
extend to run our infrastructure tests on your PRs
as well a stage which you can easily add your unit tests
to.

## Usage

Check out [Creating a New Application](https://capsulerx.atlassian.net/wiki/spaces/devops/pages/1242955881/Creating+a+New+Application#Setting-up-CI/CD-in-Jenkins-for-your-application).
The second section of the Setting up CI/CD portion covers how to set up the pr-tests pipeline.

Before this pipeline is completely ready to run application tests, you'll need to:

1. Create a `jenkins.yaml` (in your `.jenkins/pr-tests` directory)
   with a pod configured to run your test container:
   ```yaml
    kind: Pod
    apiVersion: v1
    metadata:
      name: myapp-pr-tests
      namespace: jenkins
    spec:
      containers:
      - name: test-runner
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1
            memory: 1Gi
        image: node:alpine
        command: ["/bin/sh", "-ec", "while :; do echo '.'; sleep 5 ; done"]
   ```
2. Update the agent configuration in the `Jenkinsfile` to pick up the pod:
   ```groovy
    agent {
      kubernetes {
        cloud 'eks-internal-cluster'
        label k8s.formatJobLabel(env.JOB_NAME, env.BUILD_NUMBER)
        yamlFile '.jenkins/pr-tests/jenkins.yaml'
      }
    }
   ```
