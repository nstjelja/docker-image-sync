# Create development password for the registry

```
htpasswd -Bbn admin password > /auth

```

```
export REGISTRY_PASSWORD=password
python app.py --configuration images.yaml --registry-username admin
```

# TODO
1. Admin and password - env file, command line and input.
2. Dockerize
3. Try running as open shift project