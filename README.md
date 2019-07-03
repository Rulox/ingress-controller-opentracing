# OpenTracing Examples for NGINX Ingress Controller

Example apps for testing [opentracing module](https://github.com/opentracing-contrib/nginx-opentracing) for NGINX and NGINX Plus in a Kubernetes cluster (**minikube**) using 
[NGINX Ingress Controller](https://github.com/nginxinc/kubernetes-ingress).

This guide assumes you have a running k8s cluster and the Ingress Controller installed and configured
with OpenTracing module enabled. It also assumes you are using Jaeger tracer with the basic configuration.

For simplicity, enable opentracing globally for all Ingress/VS/VSR resources with the ConfigMap key `opentracing: True`

## HTTP Tracing

Before start, set the following env variable in your terminal:
```bash
export IC_IP=$(minikube ip)
```

The server in `app.py` is a basic Flask app with an endpoint `/trace` that will perform a change in the span
 (add a message log) that comes from NGINX using the Jaeger client and sending the new information to Jaeger. 
 This will 

Prerequisites:

1. Change the host/port of your jaeger tracer if necessary (by default, these values work if you followed the
example in NGINX Ingress Controller examples folder)
```python
JAEGER_HOST = 'jaeger-agent.default.svc.cluster.local'
JAEGER_PORT = '6831'
```

Test:
 
1. Build the server-app image (if you are using minikube remember to use  `eval $(minikube docker-env)` before building)
```bash
cd server-app
docker build -t python-opentracing:latest .
```

2. Deploy the example server app to the cluster (this will also create an Ingress Resource)
```bash
kubectl apply -f app.yaml
```

3. Make a request
```bash
 curl --resolve opentracing.example.com:80:$IC_IP http://opentracing.example.com:80/trace --insecure 
```

In your Jaeger UI you should see the request has gone through NGINX and the Flask App.


## gRPC Tracing


Prerequisites:

Add the ConfigMap Key for HTTP2 (required for hRPC):
```yaml
http2: "True"
```

1. For simplicity, add the minikube ip to the hosts file of your machine for the host `opentracing.example.com`. 
```bash
minikube ip
sudo vim /etc/hosts
```

For example, if `minikube ip` gave you the ip: 192.168.99.187. Add the following line:
```
192.168.99.187 opentracing.example.com
```
2. Deploy the gRPC example app (python grpc example app https://github.com/tobegit3hub/grpc-helloworld)
```bash
cd server-app-grpc
kubectl aply -f app.yaml
```
 
3. Install a [gRPC curl tool](https://github.com/fullstorydev/grpcurl) to test:
```bash
brew install grpcurl
```

4. Send a request
```bash
grpcurl -insecure opentracing.example.com:443 helloworld.Greeter/SayHello 
```
There will be an error in the console, but if you check in the Jaeger UI, the trace was done correctly.


Have Fun :)