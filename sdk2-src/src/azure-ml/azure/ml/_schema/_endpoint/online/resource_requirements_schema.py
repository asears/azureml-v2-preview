# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import Any
from marshmallow import fields, post_load
from azure.ml._schema.schema import PatchedBaseSchema
from azure.ml._restclient.machinelearningservices.models import ContainerResourceRequirementsAutoGenerated


class ResourceRequirementsSchema(PatchedBaseSchema):
    cpu = fields.Float()
    memory_in_gb = fields.Float()
    gpu = fields.Int()
    cpu_limit = fields.Int(data_key="cpu_cores_limit")
    memory_in_gb_limit = fields.Float()

    @post_load
    def make(self, data: Any, **kwargs: Any) -> ContainerResourceRequirementsAutoGenerated:
        return ContainerResourceRequirementsAutoGenerated(**data)