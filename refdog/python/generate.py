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
    append("render_macros: false")
    append("---")
    append()
    append("# Refdog")
    append()
    append("[Skupper concepts](concepts/index.html)")
    append()
    append("[API reference](resources/index.html)")
    append()
    append("[CLI reference](commands/index.html)")
    append()

    append.write("input/index.md")
