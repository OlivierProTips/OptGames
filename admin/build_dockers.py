import os
import docker
import config

def build_docker_images():
    client = docker.from_env()
    
    dockers_dir = f"{config.ASSET_DIR}/dockers"

    if not os.path.isdir(dockers_dir):
        print(f"The directory '{dockers_dir}' does not exist.")
        return

    for sub_dir in os.listdir(dockers_dir):
        sub_dir_path = os.path.join(dockers_dir, sub_dir)
        dockerfile_path = os.path.join(sub_dir_path, "Dockerfile")

        # Check if it's a directory and contains a Dockerfile
        if os.path.isdir(sub_dir_path) and os.path.isfile(dockerfile_path):
            image_name = f"challenge_{sub_dir}"
            try:
                print(f"Building Docker image for '{sub_dir}'...")
                # Build the Docker image
                image, logs = client.images.build(
                    path=sub_dir_path,
                    tag=f"{image_name.lower()}"
                )
                print(f"Successfully built image '{image_name}'.")
            except docker.errors.BuildError as build_error:
                print(f"Build error for '{sub_dir}': {build_error}")
            except docker.errors.APIError as api_error:
                print(f"Docker API error for '{sub_dir}': {api_error}")
        else:
            print(f"No Dockerfile found in '{sub_dir_path}', skipping.")

if __name__ == "__main__":
    build_docker_images()
