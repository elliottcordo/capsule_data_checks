# jenkins-template

This repository contains the generic pipelines which can
be used and extended by SWE applications. You'll want to
check out [Creating a New Application](https://capsulerx.atlassian.net/wiki/spaces/devops/pages/1242955881/Creating+a+New+Application)
for a better overview of how these pipelines fit into your application.

## Structure

There's a README bundled with each pipeline that should
give you a better idea how/when to use them.

For SWE:
- [Generic Build and Deploy](.jenkins)
- [PR tests](.jenkins/pr-tests)

For SRE:
- [Build](.jenkins/build)
- [Deploy](.jenkins/deploy)
