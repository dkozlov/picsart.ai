## Configs for GKE cluster deployment

# [Multi-stage Serverless on Kubernetes with OpenFaaS and GKE](https://github.com/stefanprodan/openfaas-gke/blob/master/gke-preemptible.md)

This is a step-by-step guide on setting up OpenFaaS on GKE with the following characteristics:
* two OpenFaaS instances, one for staging and one for production use, isolated with network policies 
* a dedicated node pool for OpenFaaS long-running services
* a dedicated node pool of preemptible VMs for OpenFaaS functions 
* autoscaling for functions and their underling infrastructure 
* secure OpenFaaS ingress with Let's Encrypt TLS and authentication
