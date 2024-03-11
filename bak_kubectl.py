import subprocess
lwidth=170
def get_api_resources():
    try:
        # Execute kubectl command to get API resources

        print(f"  =====================================================================================".ljust(lwidth), end='')
        print("=========")
        print(f"  kubectl api-resources --verbs=list -o wide --namespaced=true --no-headers=true".ljust(lwidth), end='')
        print("getting verbs")
        print(f"  =====================================================================================".ljust(lwidth), end='')
        print("=========")
        api_resources_output = subprocess.check_output(["/usr/bin/kubectl", "api-resources", "--verbs=list", "-o", "wide", "--namespaced=true", "--no-headers=true"], text=True)
        api_resources_lines = api_resources_output.strip().split("\n")
        return [line.split()[0] for line in api_resources_lines]
    except subprocess.CalledProcessError:
        print("Error retrieving API resources. Make sure kubectl is properly configured.")
        return []

def process_api_resource(api_resource):
    try:
        # Execute kubectl command to get resource names
        print("  =====================================================================================".ljust(lwidth), end='')
        print("=========")
        print(f"  kubectl get {api_resource} -o custom-columns=:metadata.name".ljust(lwidth), end='')
        print(f"getting {api_resource}")
        print("  =====================================================================================".ljust(lwidth), end='')
        print("=========")
        resource_names_output = subprocess.check_output(["/usr/bin/kubectl", "get", api_resource, "-o", "custom-columns=:.metadata.name"], text=True)
        resource_names = resource_names_output.strip().split("\n")

        # Generate YAML files for each resource
        for name in resource_names:
            if (name == ''):
                print(f"  *** No Resources Created for: {api_resource} ***".ljust(lwidth), end='')
                print("---N/A---")
            else:
                print(f"  kubectl get {name} -o yaml > {api_resource}_{name}.yaml".ljust(lwidth), end='')
                yaml_output = subprocess.check_output(["/usr/bin/kubectl", "get", api_resource, name, "-o", "yaml"], text=True)
                with open(f"{api_resource}_{name}.yaml", "w") as yaml_file:
                    yaml_file.write(yaml_output)
                print(f"Generated")

        if not resource_names:
            print(f"  No {api_resource} resources found.".ljust(lwidth), end='')
            print("---N/A---")
    except subprocess.CalledProcessError:
        print(f"  ** Error processing {api_resource} resources. **".ljust(lwidth), end='')
        print("---ERR---")

def main():
    api_resources = get_api_resources()
    for api_resource in api_resources:
        process_api_resource(api_resource)

if __name__ == "__main__":
    main()
