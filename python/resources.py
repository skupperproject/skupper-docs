from common import *

def generate(model):
    notice("Generating resources")

    make_dir("input/resources")

    append = StringBuilder()

    append("---")
    append("refdog_links:")
    append("  - title: Resource overview")
    append("    url: overview.html")
    append("  - title: Concept index")
    append("    url: /concepts/index.html")
    append("  - title: Command index")
    append("    url: /commands/index.html")
    append("---")
    append()
    append("# Skupper resources")
    append()

    for group in model.groups:
        append(f"#### {group.title}")
        append()
        append("<table class=\"objects\">")

        for resource in group.objects:
            append(f"<tr><th><a href=\"{resource.href}\">{resource.title}</a></th><td>{resource.summary}</td></tr>")

        append("</table>")
        append()

    append.write("input/resources/index.md")

    for resource in model.resources:
        generate_resource(resource)

def generate_resource(resource):
    notice(f"Generating {resource.input_file}")

    if resource.hidden:
        debug(f"{resource} is hidden")
        return

    append = StringBuilder()

    append("---")
    append(generate_object_metadata(resource))
    append("---")
    append()
    append(f"# {resource.title_with_type}")
    append()

    if resource.description:
        append(resource.description.strip())
        append()

    if resource.examples:
        append("## Examples")
        append()

        for example in resource.examples:
            append(example["description"].strip() + ":")
            append()
            append("~~~ yaml")
            append(example["yaml"].strip())
            append("~~~")
            append()

    append("## Metadata properties")
    append()

    for prop in resource.metadata_properties:
        generate_property(prop, append)

    append("## Spec properties")
    append()

    for group in ("required", "frequently-used", None, "advanced"):
        for prop in resource.spec_properties:
            if prop.group == group:
                generate_property(prop, append)

    append("## Status properties")
    append()

    for group in ("required", "frequently-used", None, "advanced"):
        for prop in resource.status_properties:
            if prop.group == group:
                generate_property(prop, append)

    append.write(resource.input_file)

def generate_property(prop, append):
    debug(f"Generating {prop}")

    if prop.hidden:
        debug(f"{prop} is hidden")
        return

    classes = ["attribute"]
    flags = list()

    if prop.format:
        type_info = f"{prop.type} ({prop.format})"
    else:
        type_info = prop.type

    if prop.group:
        flags.append(prop.group.replace("-", " "))

    if prop.group not in ("required", "frequently-used", None):
        classes.append("collapsed")

    append(f"<div class=\"{' '.join(classes)}\">")
    append(f"<div class=\"attribute-heading\">")
    append(f"<h3 id=\"{prop.id}\">{prop.name}</h3>")
    append(f"<div class=\"attribute-type-info\">{type_info}</div>")

    if flags:
        append(f"<div class=\"attribute-flags\">{', '.join(flags)}</div>")

    append("</div>")
    append("<div class=\"attribute-body\">")
    append()

    if prop.description:
        append(prop.description.strip())
        append()

    append(generate_attribute_fields(prop))
    append()
    append("</div>")
    append("</div>")
    append()

class ResourceModel(Model):
    def __init__(self):
        super().__init__(Resource, "config/resources")

        self.property_data = read_yaml(join(self.config_dir, "properties.yaml"))

        self.init(exclude=["properties.yaml"])

        self.resources_by_name = dict()
        self.crds_by_name = dict()

        for resource in self.resources:
            self.resources_by_name[resource.name] = resource

        for crd_file in list_dir("crds"):
            if crd_file == "skupper_cluster_policy_crd.yaml":
                continue

            crd_data = read_yaml(join("crds", crd_file))

            if crd_data["kind"] != "CustomResourceDefinition":
                continue

            kind = crd_data["spec"]["names"]["kind"]

            self.crds_by_name[kind] = crd_data

    @property
    def resources(self):
        return self.objects

    def check(self):
        for crd_name, crd_data in self.crds_by_name.items():
            try:
                resource = self.resources_by_name[crd_name]
            except KeyError:
                warning(f"Resource '{crd_name}' is missing")
                continue

            for name, data in crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"].items():
                if name not in resource.spec_properties_by_name:
                    warning(f"{resource}: Spec property '{name}' is missing")

            for name, data in crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["status"]["properties"].items():
                if name not in resource.status_properties_by_name:
                    warning(f"{resource}: Status property '{name}' is missing")

        for resource in self.resources:
            try:
                crd_data = self.crds_by_name[resource.name]
            except KeyError:
                warning(f"Resource '{resource.name}' is extra")
                continue

            for prop in resource.spec_properties:
                if prop.name not in crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]:
                    warning(f"{resource}: Spec property '{prop.name}' is extra")

            for prop in resource.status_properties:
                if prop.name not in crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["status"]["properties"]:
                    warning(f"{resource}: Status property '{prop.name}' is extra")

    def get_schema(self, resource):
        try:
            return self.crds_by_name[resource.name]["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
        except KeyError:
            return {}

    def get_schema_property(self, prop):
        if prop.object is None:
            return {}

        schema = self.get_schema(prop.object)

        try:
            return schema["properties"][prop.section]["properties"][prop.name]
        except KeyError:
            return {}

class Resource(ModelObject):
    examples = object_property("examples", default=[])
    description = object_property("description")

    def __init__(self, model, data):
        super().__init__(model, data)

        self.metadata_properties = list()
        self.metadata_properties_by_name = dict()

        if "metadata" in self.data:
            for data in self.merge_property_data("metadata"):
                prop = Property(self.model, self, data, "metadata")

                self.metadata_properties.append(prop)
                self.metadata_properties_by_name[prop.name] = prop

        self.spec_properties = list()
        self.spec_properties_by_name = dict()

        if "spec" in self.data:
            for data in self.merge_property_data("spec"):
                prop = Property(self.model, self, data, "spec")

                self.spec_properties.append(prop)
                self.spec_properties_by_name[prop.name] = prop

        self.status_properties = list()
        self.status_properties_by_name = dict()

        if "status" in self.data:
            for data in self.merge_property_data("status"):
                prop = Property(self.model, self, data, "status")

                self.status_properties.append(prop)
                self.status_properties_by_name[prop.name] = prop

    def merge_property_data(self, section):
        model_props = self.model.property_data
        included_keys = list()

        for pattern in self.data[section].get("include_properties", []):
            for key in model_props:
                if string_matches_glob(key, pattern):
                    included_keys.append(key)

        for pattern in self.data[section].get("exclude_properties", []):
            for key in included_keys:
                if string_matches_glob(key, pattern):
                    included_keys.remove(key)

        included_props = {model_props[x]["name"]: model_props[x] for x in included_keys}
        specific_props = {x["name"]: x for x in self.data[section].get("properties", [])}

        included_names = [x for x in included_props if x not in specific_props]
        merged_names = list(specific_props.keys()) + included_names
        merged_props = list()

        for name in merged_names:
            included_data = included_props.get(name, {})
            specific_data = specific_props.get(name, {})

            merged_data = dict(included_data)
            merged_data.update(specific_data)

            if "description" in included_data and "description" in specific_data:
                included_description = included_data["description"]
                specific_description = specific_data["description"]

                merged_data["description"] = specific_description.replace("@description@", included_description)

            merged_props.append(merged_data)

        return merged_props

class ResourceGroup(ModelObjectGroup):
    def __init__(self, model, data):
        super().__init__(model, data)

        self.resources = list()

        for resource_name in self.data.get("resources", []):
            try:
                self.resources.append(self.model.resources_by_name[resource_name])
            except KeyError:
                fail(f"{self}: Resource '{resource_name}' not found'")

def property_property(name):
    def get(obj):
        default = obj.model.get_schema_property(obj).get(name)
        return obj.data.get(name, default)

    return property(get)

class Property(ModelObjectAttribute):
    type = property_property("type")
    format = property_property("format")
    description = property_property("description")

    def __init__(self, model, resource, data, section):
        super().__init__(model, resource, data)

        self.resource = resource
        self.section = section

    @property
    def id(self):
        return f"{self.section}-{super().id}"

    @property
    def required(self):
        default = None

        if self.section in ("spec", "status"):
            schema = self.model.get_schema(self.object)
            required_names = schema["properties"][self.section].get("required", [])
            default = self.name in required_names

        return self.data.get("required", default)

    @property
    def default(self):
        default = False if self.type == "boolean" else None
        return self.data.get("default", default)

    @property
    def choices(self):
        default = self.model.get_schema_property(self).get("enum")
        return self.data.get("choices", [])
