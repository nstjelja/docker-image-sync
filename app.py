import docker, yaml, json, requests, click



def push_image(configuration,client, pulled_image, tag):
    new_tag = "{}/{}/{}".format(configuration["registry"]["url"],configuration["registry"]["namespace"],tag)
    pulled_image.tag(new_tag)
    client.images.push(new_tag)
    client.images.remove(new_tag)

@click.command()
@click.option("--configuration", default=1, help="Configuration file to load",type=click.File('rb'))
@click.option("--registry-username", envvar="REGISTRY_USERNAME")
@click.option("--registry-password", envvar="REGISTRY_PASSWORD",prompt=True, hide_input=True)
def start(configuration, registry_username, registry_password):
    
    click.secho(message="Loading configuration from: {}".format(configuration.name), fg="yellow")
    configuration = yaml.safe_load(configuration)

    click.secho(message="Registering into registry: {}".format(configuration["registry"]["url"]), fg="yellow")
    client = docker.from_env()
    client.login(registry_username,registry_password, registry=configuration["registry"]["url"])
    
    click.secho(message="Fetching images: #{}".format(len(configuration["images"])), fg="blue")
    for image in configuration["images"]:
        pulled_images=client.images.pull("{}".format(image))
        
        click.secho(message="Fetching image: {}".format(image), fg="yellow")
        for pulled_image in pulled_images:
    
            for tag in pulled_image.tags[:10]:
                if "-" in tag.split(":")[1]:
                    break
                push_image(configuration,client,pulled_image, tag)

if __name__ == '__main__':
    start()


