import yaml


def load_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except yaml.YAMLError as exc:
        print(f"Error: An error occurred while parsing YAML file - {exc}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


if __name__ == "__main__":
    # Example usage
    config = load_yaml_file('config.yml')
    if config:
        print(config)
