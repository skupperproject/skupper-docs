import mistune as _mistune
import plano as _plano
import re as _re

StringBuilder = _plano.StringBuilder
capitalize, join, plural = _plano.capitalize, _plano.join, _plano.plural
debug, notice, warning, error, fail = _plano.debug, _plano.notice, _plano.warning, _plano.error, _plano.fail
emit_yaml, read_yaml = _plano.emit_yaml, _plano.read_yaml
list_dir, make_dir = _plano.list_dir, _plano.make_dir
string_matches_glob = _plano.string_matches_glob

_named_links = read_yaml("config/links.yaml")

def make_fragment_id(name):
    return name.lower().replace(" ", "-")

def generate_object_metadata(obj):
    from concepts import Concept
    from resources import Resource
    from commands import Command

    link_data = list()

    def add_link(other):
        link_data.append({
            "title": other.title_with_type,
            "url": other.href.removeprefix("{{site_prefix}}"),
        })

    for name in obj.links:
        if name not in _named_links:
            fail(f"{obj}: Link '{name}' not found")

        link_data.append({
            "title": _named_links[name]["title"],
            "url": _named_links[name]["url"],
        })

    for other in obj.corresponding_objects:
        add_link(other)

    for concept in obj.related_concepts:
        add_link(concept)

    for resource in obj.related_resources:
        add_link(resource)

    for command in obj.related_commands:
        add_link(command)

    data = {
        "body_class": "object {}".format(obj.__class__.__name__.lower()),
        "refdog_object_has_attributes": True,
        "refdog_links": link_data,
    }

    if isinstance(obj, Concept):
        del data["refdog_object_has_attributes"]

    return emit_yaml(data).strip()

def generate_attribute_fields(attr):
    rows = list()

    # No default for status fields
    if attr.default is not None and getattr(attr, "group", None) != "status":
        default = attr.default

        if default is True:
            default = str(default).lower()
        elif isinstance(default, str):
            if not default.startswith("_"):
                default = f"`{default}`"

            default = _convert_markdown(default)

        rows.append(f"<tr><th>Default</th><td>{default}</td>")

    if attr.choices:
        rows.append(f"<tr><th>Choices</th><td>{generate_attribute_choices(attr)}</td>")

    if attr.platforms:
        rows.append(f"<tr><th>Platforms</th><td>{', '.join(attr.platforms)}</td>")

    if attr.updatable:
        rows.append(f"<tr><th>Updatable</th><td>{attr.updatable}</td>")

    links = generate_attribute_links(attr)

    if links:
        rows.append(f"<tr><th>See also</th><td>{links}</td>")

    if rows:
        return f"<table class=\"fields\">{''.join(rows)}</table>"

    return ""

def generate_attribute_choices(attr):
    rows = list()

    for choice_data in attr.choices:
        name = choice_data["name"]
        description = choice_data["description"].replace("\n", " ").strip()
        description = _convert_markdown(description)

        rows.append(f"<tr><th><code>{name}</code></th><td>{description}</td></tr>")

    return "<table class=\"choices\">{}</table>".format("".join(rows))

def generate_attribute_links(attr):
    out = list()

    for link in attr.gather_links():
        title, url = link

        if url.startswith("/"):
            url = "{{site_prefix}}" + url

        out.append(f"<a href=\"{url}\">{title}</a>")

    return ", ".join(out)

def object_property(name, default=None, required=False):
    def get(obj):
        value = obj.get_value(name, default)

        if required and value is None:
            fail(f"{obj}: Property '{name}' is required")

        return value

    return property(get)

class Model:
    def __init__(self, object_class, config_dir):
        self.object_class = object_class
        self.config_dir = config_dir

        debug(f"Initializing {self}")

        self.objects = list()
        self.objects_by_id = dict()
        self.groups = list()

    def __repr__(self):
        return self.__class__.__name__

    def init(self, exclude=[]):
        for yaml_file in list_dir(self.config_dir):
            if yaml_file == "groups.yaml":
                continue

            if yaml_file in exclude:
                continue

            obj_data = read_yaml(join(self.config_dir, yaml_file))
            obj = self.object_class(self, obj_data)

            self.objects.append(obj)
            self.objects_by_id[obj.id] = obj

        for group_data in read_yaml(join(self.config_dir, "groups.yaml")):
            self.groups.append(ModelObjectGroup(self, group_data))

class ModelObjectGroup:
    title = object_property("title", required=True)
    description = object_property("description")

    def __init__(self, model, data):
        self.model = model
        self.data = data

        debug(f"Initializing {self}")

        self.objects = list()

        for id in self.data.get("objects", []):
            try:
                self.objects.append(self.model.objects_by_id[id])
            except KeyError:
                fail(f"{self}: {self.model.object_class.__name__} '{id}' not found")

    def __repr__(self):
        return f"{self.__class__.__name__} '{self.title}'"

    def get_value(self, name, default):
        return self.data.get(name, default)

    @property
    def id(self):
        return make_fragment_id(self.title)

class ModelObject:
    hidden = object_property("hidden", default=False)
    name = object_property("name", required=True)
    description = object_property("description")
    links = object_property("links", default=[])
    notes = object_property("notes")

    def __init__(self, model, data):
        self.model = model
        self.data = data

    def __repr__(self):
        return f"{self.__class__.__name__} '{self.name}'"

    def get_value(self, name, default):
        return self.data.get(name, default)

    @property
    def name(self):
        return self.data["name"]

    @property
    def id(self):
        # Convert camel case to hyphenated
        name = _re.sub(r"(?<!^)(?=[A-Z])", "-", self.name)

        return make_fragment_id(name)

    @property
    def title(self):
        return f"{capitalize(self.name)}"

    @property
    def title_with_type(self):
        type = self.__class__.__name__.lower()

        if type == "subcommand":
            type = "command"

        return f"{self.title} {type}"

    @property
    def summary(self):
        return _extract_first_sentence(self.description)

    @property
    def input_file(self):
        type = self.__class__.__name__.lower()
        return f"input/{plural(type)}/{self.id}.md"

    @property
    def href(self):
        type = self.__class__.__name__.lower()
        return f"{{{{site_prefix}}}}/{plural(type)}/{self.id}.html"

    @property
    def corresponding_objects(self):
        from concepts import Concept
        from resources import Resource
        from commands import Command

        id = self.id

        if isinstance(self, Command) and self.parent is not None:
            id = self.parent.id

        if not isinstance(self, Concept):
            try:
                yield self.model.concept_model.objects_by_id[id]
            except KeyError:
                pass

        if not isinstance(self, Resource):
            try:
                yield self.model.resource_model.objects_by_id[id]
            except KeyError:
                pass

        if not isinstance(self, Command):
            try:
                yield self.model.command_model.objects_by_id[id]
            except KeyError:
                pass

    @property
    def related_concepts(self):
        for id in self.data.get("related_concepts", []):
            try:
                yield self.model.concept_model.objects_by_id[id]
            except KeyError:
                fail(f"{self}: Related concept '{id}' not found")

    @property
    def related_resources(self):
        for id in self.data.get("related_resources", []):
            try:
                yield self.model.resource_model.objects_by_id[id]
            except KeyError:
                fail(f"{self}: Related resource '{id}' not found")

    @property
    def related_commands(self):
        for id in self.data.get("related_commands", []):
            try:
                yield self.model.command_model.objects_by_id[id]
            except KeyError:
                fail(f"{self}: Related command '{id}' not found")

class ModelObjectAttribute:
    group = object_property("group")
    description = object_property("description")
    platforms = object_property("platforms", default=["Kubernetes", "Docker", "Podman", "Linux"])
    updatable = object_property("updatable", default=False)
    links = object_property("links", default=[])
    notes = object_property("notes")
    hidden = object_property("hidden", default=False)

    def __init__(self, model, object, data):
        self.model = model
        self.object = object
        self.data = data

        debug(f"Loading {self}")

    def __repr__(self):
        return f"{self.__class__.__name__} '{self.name}'"

    def get_value(self, name, default):
        return self.data.get(name, default)

    @property
    def name(self):
        return self.data["name"]

    @property
    def id(self):
        # Convert camel case to hyphenated
        name = _re.sub(r"(?<!^)(?=[A-Z])", "-", self.name)

        return make_fragment_id(name)

    @property
    def group(self):
        if self.required:
            return "required"

        return self.data.get("group")

    def gather_links(self):
        links = list()

        for id in self.data.get("related_concepts", []):
            try:
                obj = self.model.concept_model.objects_by_id[id]
            except KeyError:
                fail(f"{self}: Related concept '{id}' not found")

            links.append((obj.title_with_type, obj.href))

        # Other related things here?

        for id in self.links:
            try:
                link_data = _named_links[id]
            except KeyError:
                fail(f"{self}: Link '{id}' not found")

            links.append((link_data["title"], link_data["url"]))

        return links

def _extract_first_sentence(text):
    if text is None:
        return ""

    text = text.replace("\n", " ")
    text = _convert_markdown(text)
    text = _re.sub(r"<[^>]*>", "", text) # Strip tags

    match = _re.search(r"(.+?)\.\s+", text, _re.DOTALL)

    if match is None:
        return text.removesuffix(".")

    return match.group(1)

def _convert_markdown(text):
    return _mistune.html(text)
