from resources import *

def generate(model):
    notice("Generating commands")

    make_dir("input/commands")

    append = StringBuilder()

    append("---")
    append("refdog_links:")
    append("  - title: Command overview")
    append("    url: overview.html")
    append("  - title: Concept index")
    append("    url: /concepts/index.html")
    append("  - title: Resource index")
    append("    url: /resources/index.html")
    append("---")
    append()
    append("# Skupper commands")
    append()

    for group in model.groups:
        append(f"#### {group.title}")
        append()

        for command in group.objects:
            append("<table class=\"objects\">")

            if command.subcommands:
                summary = f"Overview of {command.name} commands"

                append(f"<tr><th><a href=\"{command.href}\">{command.title}</a></th><td>{summary}</td></tr>")

                for sc in command.subcommands:
                    append(f"<tr><th><a href=\"{sc.href}\">{sc.title}</a></th><td>{sc.summary}</td></tr>")
            else:
                append(f"<tr><th><a href=\"{command.href}\">{command.title}</a></th><td>{command.summary}</td></tr>")

            append("</table>")
            append()

        append()

    append.write("input/commands/index.md")

    for command in model.commands:
        generate_command(command)

        for subcommand in command.subcommands:
            generate_command(subcommand)

def generate_command(command):
    notice(f"Generating {command.input_file}")

    append = StringBuilder()

    append("---")
    append(generate_object_metadata(command))
    append("---")
    append()
    append(f"# {command.title_with_type}")
    append()
    append("~~~ shell")
    append(f"{generate_usage(command)}")
    append("~~~")
    append()

    if command.description and not command.subcommands:
        append(command.description.strip())
        append()

    append(generate_command_fields(command))
    append()

    if command.output:
        append("## Output")
        append()
        append("~~~ console")
        append(command.output.strip())
        append("~~~")
        append()

    if command.subcommands:
        append("## Subcommands")
        append()
        append("<table class=\"objects\">")

        for sc in command.subcommands:
            append(f"<tr><th><a href=\"{sc.href}\">{sc.title}</a></th><td>{sc.summary}</td></tr>")

        append("</table>")
        append()
    else:
        if command.examples:
            append("## Examples")
            append()
            append("~~~ console")
            append(command.examples.strip())
            append("~~~")
            append()

        if command.options:
            append("## Primary options")
            append()

            for group in ("positional", "required", "frequently-used", None, "advanced"):
                for option in command.options:
                    if option.group == group:
                        generate_option(option, append)

            append("## Global options")
            append()

            for option in command.options:
                if option.group == "global":
                    generate_option(option, append)

        if command.errors:
            append("## Errors")
            append()

            for error in command.errors:
                generate_error(error, append)

    append.write(command.input_file)

def generate_usage(command):
    parts = ["skupper"]
    parts.extend([x.name for x in reversed(list(command.ancestors))])
    parts.append(command.name)

    if command.subcommands:
        parts.append("[subcommand]")

    for option in command.options:
        if option.positional:
            if option.required:
                parts.append(f"<{option.name}>")
            else:
                parts.append(f"[{option.name}]")

    parts.append("[options]")

    return " ".join(parts)

def generate_command_fields(command):
    rows = list()

    rows.append(f"<tr><th>Platforms</th><td>{', '.join(command.platforms)}</td>")

    if command.wait:
        rows.append(f"<tr><th>Waits for</th><td>{command.wait}</td>")

    return f"<table class=\"fields\">{''.join(rows)}</table>"

def generate_option(option, append):
    debug(f"Generating {option}")

    classes = ["attribute"]
    flags = list()
    prefix = ""
    option_key = option.syntax_name
    type_info = option.type

    if not option.positional and option.type != "boolean":
        if option.placeholder:
            type_info = f"&lt;{option.placeholder}&gt;"
        else:
            type_info = f"&lt;{option.type}&gt;"

    if option.short_option:
        type_info = f"(-{option.short_option}) {type_info}"

    if option.group:
        if option.group == "positional":
            if option.required:
                flags.append("required")
            else:
                flags.append("optional")
        else:
            flags.append(option.group.replace("-", " "))

    if option.group not in ("positional", "required", "frequently-used", None):
        classes.append("collapsed")

    append(f"<div class=\"{' '.join(classes)}\">")
    append(f"<div class=\"attribute-heading\">")
    append(f"<h3 id=\"{option.id}\">{option_key}</h3>")
    append(f"<div class=\"attribute-type-info\">{type_info}</div>")

    if flags:
        append(f"<div class=\"attribute-flags\">{', '.join(flags)}</div>")

    append("</div>")
    append("<div class=\"attribute-body\">")
    append()

    if option.description:
        append(option.description.strip())
        append()

    append(generate_attribute_fields(option))
    append()
    append("</div>")
    append("</div>")
    append()

def generate_error(error, append):
    append(f"- **{error.message}**")
    append()

    if error.description:
        append(f"  <p>{error.description.strip()}</p>")
        append()

class CommandModel(Model):
    def __init__(self):
        super().__init__(Command, "config/commands")

        self.option_data = read_yaml(join(self.config_dir, "options.yaml"))

        self.init(exclude=["options.yaml"])

    @property
    def commands(self):
        return self.objects

    def check(self):
        for command in self.commands:
            for option in command.options:
                if not option.name:
                    fail(f"{command}: {option} has no name")

                if not option.type:
                    fail(f"{command}: {option} has no type")

            for subcommand in command.subcommands:
                for option in subcommand.options:
                    if not option.name:
                        fail(f"{subcommand}: {option} has no name")

                    if not option.type:
                        fail(f"{subcommand}: {option} has no type")

class Command(ModelObject):
    usage = object_property("usage")
    output = object_property("output")
    examples = object_property("examples")
    wait = object_property("wait")

    def __init__(self, model, data, parent=None):
        super().__init__(model, data)

        self.parent = parent
        self.subcommands = list()

        self.options = list()
        self.options_by_name = dict()

        for data in self.merge_option_data():
            option = Option(self.model, self, data)

            self.options.append(option)
            self.options_by_name[option.name] = option

        self.errors = list()

        for error_data in self.data.get("errors", []):
            self.errors.append(Error(self, error_data))

        for command_data in self.data.get("subcommands", []):
            command = Command(model, command_data, self)

            self.subcommands.append(command)
            self.model.objects_by_id[command.id] = command

    def __repr__(self):
        if self.parent:
            return f"{self.__class__.__name__} '{self.parent.name} {self.name}'"
        else:
            return super().__repr__()

    def merge_option_data(self):
        model_options = self.model.option_data
        included_keys = list()

        for pattern in self.data.get("include_options", []):
            for key in model_options:
                if string_matches_glob(key, pattern):
                    included_keys.append(key)

        for pattern in self.data.get("exclude_options", []):
            for key in included_keys:
                if string_matches_glob(key, pattern):
                    included_keys.remove(key)

        included_options = {model_options[x]["name"]: model_options[x] for x in included_keys}
        specific_options = {x["name"]: x for x in self.data.get("options", [])}

        included_names = [x for x in included_options if x not in specific_options]
        merged_names = list(specific_options.keys()) + included_names
        merged_options = list()

        for name in merged_names:
            included_data = included_options.get(name, {})
            specific_data = specific_options.get(name, {})

            merged_data = dict(included_data)
            merged_data.update(specific_data)

            if "description" in included_data and "description" in specific_data:
                included_description = included_data["description"]
                specific_description = specific_data["description"]

                merged_data["description"] = specific_description.replace("@description@", included_description)

            merged_options.append(merged_data)

        return merged_options

    def get_resource(self):
        resource_id = self.data.get("resource")

        if resource_id is None and self.parent:
            resource_id = self.parent.data.get("resource")

        if resource_id is None:
            return

        try:
            return self.model.resource_model.objects_by_id[resource_id]
        except KeyError:
            fail(f"{self}: Resource '{resource_id}' not found")

    def get_value(self, name, default):
        resource = self.get_resource()

        if resource:
            default = getattr(resource, name, default)

        return super().get_value(name, default)

    @property
    def ancestors(self):
        command = self.parent

        while command is not None:
            yield command
            command = command.parent

    @property
    def id(self):
        if self.parent:
            return self.parent.id + "/" + super().id

        return super().id

    @property
    def title(self):
        if self.parent:
            return f"{capitalize(self.parent.name)} {self.name}"

        return f"{capitalize(self.name)}"

    @property
    def platforms(self):
        value = self.get_value("platforms", [])

        if not value and self.parent:
            value = self.parent.get_value("platforms", [])

        if not value:
            value = ["Kubernetes", "Docker", "Podman", "Linux"]

        return value

    @property
    def input_file(self):
        if self.subcommands:
            return f"input/commands/{self.id}/index.md"

        return super().input_file

    @property
    def href(self):
        if self.subcommands:
            return f"{{{{site_prefix}}}}/commands/{self.id}/index.html"

        return super().href

    @property
    def description(self):
        value = super().description
        resource = self.get_resource()

        if resource and resource.description:
            value = value.replace("@resource_description@", resource.description)

        return value

    @property
    def related_concepts(self):
        concepts = list(super().related_concepts)

        if self.parent:
            concepts.extend(self.parent.related_concepts)

        return concepts

    @property
    def related_resources(self):
        resources = list(super().related_resources)

        if self.parent:
            resources.extend(self.parent.related_resources)

        return resources

    @property
    def related_commands(self):
        commands = list(super().related_commands)

        if self.parent:
            commands.extend(self.parent.related_commands)

        return commands

    @property
    def links(self):
        links = set(super().links)

        if self.parent:
            links.update(self.parent.links)

        return links

class Option(ModelObjectAttribute):
    type = object_property("type")
    required = object_property("required", default=False)
    placeholder = object_property("placeholder")
    short_option = object_property("short_option")
    default = object_property("default")
    choices = object_property("choices")

    def get_property(self):
        property_name = self.data.get("property")

        if property_name is None:
            return

        resource = self.object.get_resource()

        assert resource is not None, self.object

        if property_name not in resource.spec_properties_by_name:
            fail(f"{self}: Property '{property_name}' not found on {resource}")

        return resource.spec_properties_by_name[property_name]

    # Get the default value from property if set
    def get_value(self, name, default):
        property = self.get_property()

        if property:
            default = getattr(property, name, default)

        return super().get_value(name, default)

    @property
    def id(self):
        return f"option-{super().id}"

    @property
    def syntax_name(self):
        if self.positional:
            if self.required:
                return f"&lt;{self.name}&gt;"
            else:
                return f"[{self.name}]"
        else:
            return f"--{self.name}"

    @property
    def positional(self):
        default = self.required and self.default is None
        return self.data.get("positional", default)

    @property
    def group(self):
        if self.positional:
            return "positional"

        if self.required:
            return "required"

        return super().group

    @property
    def description(self):
        value = super().description
        property = self.get_property()

        if property and property.description:
            value = value.replace("@property_description@", property.description)

        return value

class Error:
    message = object_property("message", required=True)
    description = object_property("description")
    notes = object_property("notes")

    def __init__(self, model, data):
        self.model = model
        self.data = data

    def __repr__(self):
        return f"{self.__class__.__name__} '{self.message}'"

    def get_value(self, name, default):
        return self.data.get(name, default)
