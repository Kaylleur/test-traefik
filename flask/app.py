from flask import Flask, Response
import yaml
import os

app = Flask(__name__)

@app.route('/traefik/config')
def traefik_config():
    # Lecture du fichier YAML dynamique
    with open("/config/routes.yaml", "r") as f:
        data = yaml.safe_load(f)

    # Construction de la config Traefik
    config = {"http": {"routers": {}, "services": {}}}

    for idx, route in enumerate(data.get('routes', [])):
        router_name = f"router-{idx}"
        service_name = f"service-{idx}"
        host = route['host']
        service_url = route['service_url']

        config["http"]["routers"][router_name] = {
            "rule": f"Host(`{host}`)",
            "service": service_name,
            "entryPoints": ["web"]
        }

        config["http"]["services"][service_name] = {
            "loadBalancer": {
                "servers": [{"url": service_url}]
            }
        }

    yaml_config = yaml.dump(config)
    return Response(yaml_config, mimetype='application/x-yaml')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

