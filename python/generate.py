from common import *

import commands as _commands
import concepts as _concepts
import resources as _resources

concept_model = _concepts.ConceptModel()
resource_model = _resources.ResourceModel()
command_model = _commands.CommandModel()

concept_model.resource_model = resource_model
concept_model.command_model = command_model
concept_model.concept_model = concept_model

resource_model.concept_model = concept_model
resource_model.command_model = command_model
resource_model.resource_model = resource_model

command_model.concept_model = concept_model
command_model.resource_model = resource_model
command_model.command_model = command_model

def generate_objects():
    resource_model.check()
    command_model.check()

    _concepts.generate(concept_model)
    _resources.generate(resource_model)
    _commands.generate(command_model)

    # for obj in concept_model.objects:
    #     print(obj, obj.id)
    # for obj in resource_model.objects:
    #     print(obj, obj.id)
    # for obj in command_model.objects:
    #     print(obj, obj.id)
    #     for sc in obj.subcommands:
    #         print(sc, sc.id)

def generate_index():
    append = StringBuilder()

    append("---")
    append("body_class: object index")
    append("---")
    append()
    append("# Refdog")
    append()
    append("<div style=\"display: flex;\">")
    append("<div style=\"margin-right: 4em;\">")
    append()
    append("#### Concepts")
    append()

    append("[Concept overview](concepts/overview.html)<br/>")
    append("[Concept index](concepts/index.html)")
    append()

    append()
    append("</div>")
    append("<div style=\"margin-right: 4em;\">")
    append()
    append("#### Resources")
    append()
    append("[Resource overview](resources/overview.html)<br/>")
    append("[Resource index](resources/index.html)")
    append()

    append()
    append("</div>")
    append("<div style=\"margin-right: 4em;\">")
    append()
    append("#### Commands")
    append()
    append("[Command overview](commands/overview.html)<br/>")
    append("[Command index](commands/index.html)")
    append()

    append()
    append("</div>")
    append("</div>")
    append()

    append.write("input/index.md")
