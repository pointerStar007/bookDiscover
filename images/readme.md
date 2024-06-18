
# 本地测试
```
docker pull redis
docker pull mongo
docker pull mysql:5.7
```

# k8s 部署项目
- 先安装好 k8s ,这里所使用的 k8s 版本为 v1.20 版本

# 创建命名空间
~~~
kubectl create ns biquge
~~~

# 部署 mysql 应用

1. 创建一个 secret
~~~
apiVersion: v1  
kind: Secret  
metadata:  
  name: mysql-secret
  namespace: biquge  
type: Opaque  
data:  
  mysql-root-password: <base64-encoded-password>
~~~
- 例如：你希望的root密码是 123456， 将root密码 进行base 64 编码
~~~
echo -n 'your-password' | base64
~~~
- 或者你直接通过其他工具进行编码然后复制过来
- 执行构建
~~~
kubectl apply -f mysql-secret.yaml
~~~

2. 创建一个 nfs 制备器
~~~
metadata:  
  name: nfs-client-provisioner
  namespace: kube-system
  labels:
    app: nfs-client-provisioner      
spec:  
  replicas: 1   
  strategy:  
    type: Recreate  
  selector:  
    matchLabels:  
      app: nfs-client-provisioner  
  template:  
    metadata:  
      labels:  
        app: nfs-client-provisioner  
    spec:  
      serviceAccountName: nfs-client-provisioner # 确保你有一个匹配的ServiceAccount  
      containers:  
        - name: nfs-client-provisioner  
          image: 192.168.1.3:5000/nfs-subdir-external-provisioner:latest # 替换为你想要的版本  
          imagePullPolicy: IfNotPresent
          volumeMounts:  
            - name: nfs-client-root  
              mountPath: /persistentvolumes  
          env:  
            - name: PROVISIONER_NAME  
              value: example.com/nfs # 这应该与StorageClass中的provisioner名称匹配  
            - name: NFS_SERVER  
              value: 192.168.184.135 # 你的NFS服务器地址  
            - name: NFS_PATH  
              value: /nfs/data # NFS导出的路径  
      volumes:  
        - name: nfs-client-root  
          nfs:  
            server: 192.168.184.135 # NFS服务器地址  
            path: /nfs/data # NFS导出的路径
~~~
- 在构建制备器之前你还需要有一个 serviceAccountName，以及目录必要的权限
~~~
chmod 777 /nfs/data # 提权
# service_account_role.yaml # 创建 serviceAccountName 和 权限赋予
---
apiVersion: v1  
kind: ServiceAccount  
metadata:  
  name: nfs-client-provisioner  
  namespace: kube-system  
  
---  
apiVersion: rbac.authorization.k8s.io/v1  
kind: ClusterRole  
metadata:  
  name: nfs-client-provisioner-runner  
rules:  
  - apiGroups: [""]  
    resources: ["persistentvolumes"]  
    verbs: ["get", "list", "watch", "create", "delete"]  
  - apiGroups: [""]  
    resources: ["persistentvolumeclaims"]  
    verbs: ["get", "list", "watch", "update"]  
  - apiGroups: ["storage.k8s.io"]  
    resources: ["storageclasses"]  
    verbs: ["get", "list", "watch"]  
  - apiGroups: [""]  
    resources: ["endpoints"]  
    verbs: ["get", "create", "update", "patch"]  
  - apiGroups: [""]  
    resources: ["events"]  
    verbs: ["create", "update", "patch"]
  
---  
apiVersion: rbac.authorization.k8s.io/v1  
kind: ClusterRoleBinding  
metadata:  
  name: run-nfs-client-provisioner  
subjects:  
  - kind: ServiceAccount  
    name: nfs-client-provisioner  
    namespace: kube-system  
roleRef:  
  kind: ClusterRole  
  name: nfs-client-provisioner-runner  
  apiGroup: rbac.authorization.k8s.io
~~~
- 现在依次执行 service_account_role.yaml 和 制备器的 yaml 文件

3. 创建一个 StorageClass
~~~
apiVersion: storage.k8s.io/v1  
kind: StorageClass  
metadata:  
  name: nfs-storage  
  namespace: biquge
provisioner: example.com/nfs # 这里应替换为你的NFS Provisioner的provisioner名称  
parameters:  
  archiveOnDelete: "false"  
  # 其他NFS Provisioner特定的参数（如果有的话）

~~~
4. 创建 mysql 的 deployment和对应的service
~~~
apiVersion: v1  
kind: PersistentVolumeClaim  
metadata:  
  name: mysql-pvc  
  namespace: biquge
  labels:  
    app: mysql  
spec:  
  accessModes:  
    - ReadWriteMany  
  resources:  
    requests:  
      storage: 10Gi   # 10个 G 应该够用了目前，如果不够再进行扩容即可
  storageClassName: nfs-storage # 如果使用StorageClass动态创建PV，请指定类名
---
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: mysql  
  namespace: biquge
spec:  
  selector:  
    matchLabels:  
      app: mysql  
  replicas: 1   
  template:  
    metadata:  
      labels:  
        app: mysql  
    spec:  
      containers:  
      - name: mysql  
        image: mysql:5.7  
        env:  
        - name: MYSQL_ROOT_PASSWORD  
          valueFrom:  
            secretKeyRef:  
              name: mysql-secret  
              key: mysql-root-password  
        ports:  
        - containerPort: 3306  
          name: mysql  
        volumeMounts:  
        - name: mysql-persistent-storage  
          mountPath: /var/lib/mysql  
      volumes:  
      - name: mysql-persistent-storage  
        persistentVolumeClaim:  
          claimName: mysql-pvc
---
apiVersion: v1  
kind: Service  
metadata:  
  name: mysql  
  namespace: biquge
spec:  
  selector:  
    app: mysql  
  ports:  
    - protocol: TCP  
      port: 3306  
      targetPort: 3306
~~~
5. 进入pod，创建数据库
~~~
[root@master ~]# kubectl get pod -n biquge
NAME                     READY   STATUS    RESTARTS   AGE
mysql-6964cc7d58-h5rgx   1/1     Running   0          16m
[root@master ~]# kubectl exec -it mysql-6964cc7d58-h5rgx -n biquge -- mysql -u root -p

~~~

# 部署redis应用
~~~
apiVersion: v1  
kind: PersistentVolumeClaim  
metadata:  
  name: redis-data-pvc  
  namespace: biquge
spec:  
  accessModes:  
    - ReadWriteOnce  
  resources:  
    requests:  
      storage: 8Gi # 根据需要设置存储容量
  storageClassName: nfs-storage
---
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: redis-deployment
  namespace: biquge  
  labels:  
    app: redis  
spec:  
  replicas: 1  
  selector:  
    matchLabels:  
      app: redis  
  template:  
    metadata:  
      labels:  
        app: redis  
    spec:  
      containers:  
      - name: redis  
        image: 192.168.1.3:5000/redis:latest # 替换为你的Redis镜像和标签  
        ports:  
        - containerPort: 6379  
        volumeMounts:  
        - name: redis-data  
          mountPath: /data # Redis数据目录  
      volumes:  
      - name: redis-data  
        persistentVolumeClaim:  
          claimName: redis-data-pvc # 确保PVC已经创建
---
apiVersion: v1  
kind: Service  
metadata:  
  name: redis-service  
  namespace: biquge
spec:  
  ports:  
  - port: 6379  
    targetPort: 6379  
  selector:  
    app: redis       
~~~
# 部署 mongo
~~~
---
apiVersion: v1  
kind: ConfigMap  
metadata:  
  name: mongo-config  
  namespace: biquge
data:  
  mongod.conf: |  
    storage:  
      dbPath: /data/db  
    systemLog:  
      destination: file  
      logAppend: true  
      path: /var/log/mongodb/mongod.log  
    net:  
      port: 27017  
      bindIp: 0.0.0.0  
    replication:  
      replSetName: rs0

---
apiVersion: apps/v1  
kind: StatefulSet  
metadata:  
  name: mongo  
  namespace: biquge
spec:  
  selector:  
    matchLabels:  
      app: mongo  
  serviceName: "mongo"  
  replicas: 5  
  template:  
    metadata:  
      labels:  
        app: mongo  
    spec:  
      terminationGracePeriodSeconds: 10  
      containers:  
      - name: mongo  
        image: 192.168.1.3:5000/mongo:latest  
        command:  
        - mongod  
        - "--config"  
        - "/etc/mongo/mongod.conf"  
        - "--replSet"  
        - "rs0"  
        - "--bind_ip"
        - 0.0.0.0
        volumeMounts:  
        - name: mongo-persistent-storage  
          mountPath: /data/db  
        - name: mongo-config  
          mountPath: /etc/mongo  
      volumes:  
      - name: mongo-config  
        configMap:  
          name: mongo-config  
          items:  
          - key: mongod.conf  
            path: mongod.conf  
  volumeClaimTemplates:  
  - metadata:  
      name: mongo-persistent-storage  
    spec:  
      accessModes: [ "ReadWriteOnce" ]  
      resources:  
        requests:  
          storage: 50Gi
      storageClassName: nfs-storage
---
apiVersion: v1  
kind: Service  
metadata:  
  name: mongo 
  namespace: biquge  
spec:  
  selector:  
    app: mongo  # 确保这个 selector 与您的 StatefulSet 中的 Pods 的 labels 匹配  
  ports:  
  - port: 27017  
    targetPort: 27017  
  clusterIP: None
  # 注意这里没有 clusterIP 字段，Kubernetes 会自动分配    
~~~
- 初始化副本集，请在全部pod Running 之后进入任意一个pod
~~~
mongosh # 进入mongo的 shell
kubectl exec -it mongo-0 -n biquge -- bash
mongosh

rs.initiate({  
  _id: "rs0",  
  version: 1,  
  members: [  
    { _id: 0, host: "mongo-0.mongo.biquge.svc.cluster.local:27017" },  
    { _id: 1, host: "mongo-1.mongo.biquge.svc.cluster.local:27017" },  
    { _id: 2, host: "mongo-2.mongo.biquge.svc.cluster.local:27017" },  
    { _id: 3, host: "mongo-3.mongo.biquge.svc.cluster.local:27017" },  
    { _id: 4, host: "mongo-4.mongo.biquge.svc.cluster.local:27017" },  
  ]  
});

~~~


