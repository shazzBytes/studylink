#!/usr/bin/env python
"""Quick test to debug the enum serialization issue"""
from app.models.institution import InstitutionType, Institution
from app.schemas.institution import InstitutionCreate

# Create an institution schema with a string type value
data = {
    "name": "Test University",
    "domain": "test.edu",
    "institution_type": "university",
    "description": "Test",
    "is_verified": True,
    "onboarding_enabled": True
}

schema = InstitutionCreate(**data)
print(f"Schema object: {schema}")
print(f"Institution Type: {schema.institution_type}")
print(f"Type of institution_type: {type(schema.institution_type)}")

dumped = schema.model_dump()
print(f"\nModel dump: {dumped}")
print(f"Dumped institution_type: {dumped['institution_type']}")
print(f"Type of dumped institution_type: {type(dumped['institution_type'])}")

# Check the enum values
print(f"\nEnum VALUE: {InstitutionType.UNIVERSITY.value}")
print(f"Enum NAME: {InstitutionType.UNIVERSITY.name}")

# Now try creating an Institution object
print("\n--- Creating Institution object ---")
institution = Institution(**dumped)
print(f"Institution.institution_type: {institution.institution_type}")
print(f"Type: {type(institution.institution_type)}")
print(f"Value if enum: {institution.institution_type if not isinstance(institution.institution_type, InstitutionType) else institution.institution_type.value}")

# Try model_dump on Institution
print("\n--- Institution model_dump ---")
inst_dump = institution.model_dump()
print(f"Institution dump institution_type: {inst_dump['institution_type']}")
print(f"Type: {type(inst_dump['institution_type'])}")

