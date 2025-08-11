"""
Utility functions for creating Pydantic models from JSON strings or dict objects for custom entity and edge types.
"""

import json
import logging
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel, create_model

logger = logging.getLogger(__name__)

# Type mapping for converting string type names to Python types
TYPE_MAPPING = {
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': list,
    'dict': dict,
    'List[str]': List[str],
    'List[int]': List[int], 
    'List[float]': List[float],
    'Dict[str, Any]': Dict[str, Any],
    'Dict[str, str]': Dict[str, str],
    'Dict[str, int]': Dict[str, int],
}


def parse_json_to_entity_types(json_str: str) -> dict[str, type[BaseModel]]:
    """
    Parse JSON string to create dynamic Pydantic entity models.
    
    Expected JSON format:
    {
        "EntityName": {
            "fields": {"field1": "str", "field2": "int", ...},
            "docstring": "Optional description for LLM guidance"
        }
    }
    
    Args:
        json_str: JSON string with entity definitions
        
    Returns:
        Dictionary mapping entity names to Pydantic model classes
        
    Raises:
        ValueError: If JSON is malformed
        TypeError: If field types are not supported
    """
    try:
        entity_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format for entity types: {e}")
    
    entity_types = {}
    
    for entity_name, entity_config in entity_data.items():
        if not isinstance(entity_config, dict) or 'fields' not in entity_config:
            raise ValueError(f"Entity '{entity_name}' must have 'fields' key")
        
        fields = entity_config['fields']
        docstring = entity_config.get('docstring', '')
        
        # Convert field definitions to Pydantic field format
        pydantic_fields = {}
        for field_name, field_type_str in fields.items():
            if field_type_str not in TYPE_MAPPING:
                raise TypeError(f"Unsupported field type '{field_type_str}' for field '{field_name}' in entity '{entity_name}'. Supported types: {list(TYPE_MAPPING.keys())}")
            
            pydantic_fields[field_name] = (TYPE_MAPPING[field_type_str], ...)
        
        # Create dynamic Pydantic model
        try:
            model = create_model(entity_name, **pydantic_fields)
            if docstring:
                model.__doc__ = docstring
            entity_types[entity_name] = model
            logger.info(f"Created custom entity type: {entity_name}")
        except Exception as e:
            raise ValueError(f"Failed to create entity model '{entity_name}': {e}")
    
    return entity_types


def parse_json_to_edge_types(json_str: str) -> dict[str, type[BaseModel]]:
    """
    Parse JSON string to create dynamic Pydantic edge models.
    
    Expected JSON format:
    {
        "EdgeTypeName": {
            "fields": {"field1": "str", "field2": "float", ...},
            "docstring": "Optional description for LLM guidance"  
        }
    }
    
    Args:
        json_str: JSON string with edge type definitions
        
    Returns:
        Dictionary mapping edge type names to Pydantic model classes
        
    Raises:
        ValueError: If JSON is malformed
        TypeError: If field types are not supported
    """
    # Edge types use the same parsing logic as entity types
    try:
        return parse_json_to_entity_types(json_str)
    except Exception as e:
        raise ValueError(f"Failed to parse edge types: {e}")


def parse_json_to_edge_mappings(json_str: str) -> dict[tuple[str, str], list[str]]:
    """
    Parse JSON string to create edge mappings between entity types.
    
    Expected JSON format:
    {
        "('SourceEntity', 'TargetEntity')": ["EDGE_TYPE1", "EDGE_TYPE2", ...],
        "('Entity1', 'Entity2')": ["RELATES_TO", "DEPENDS_ON"]
    }
    
    Args:
        json_str: JSON string with edge mappings
        
    Returns:
        Dictionary mapping entity type pairs to lists of allowed edge types
        
    Raises:
        ValueError: If JSON is malformed or key format is invalid
    """
    try:
        edge_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format for edge mappings: {e}")
    
    edge_mappings = {}
    
    for key_str, edge_list in edge_data.items():
        # Parse key format: "('Source', 'Target')" -> ('Source', 'Target')
        if not key_str.startswith("('") or not key_str.endswith("')"):
            raise ValueError(f"Invalid edge mapping key format: '{key_str}'. Expected format: \"('Source', 'Target')\"")
        
        try:
            # Extract content between "(' and ')"
            content = key_str[2:-2]  # Remove "(' and ')"
            parts = [part.strip().strip("'\"") for part in content.split("',")]
            
            if len(parts) != 2:
                raise ValueError(f"Edge mapping key must have exactly 2 entities: '{key_str}'")
            
            key_tuple = (parts[0], parts[1])
            
            if not isinstance(edge_list, list):
                raise ValueError(f"Edge list for key '{key_str}' must be a list, got: {type(edge_list)}")
            
            edge_mappings[key_tuple] = edge_list
            logger.info(f"Created edge mapping: {key_tuple} -> {edge_list}")
            
        except Exception as e:
            raise ValueError(f"Failed to parse edge mapping key '{key_str}': {e}")
    
    return edge_mappings


def create_entity_types_from_dict(entity_data: dict[str, dict[str, Any]]) -> dict[str, type[BaseModel]]:
    """
    Create dynamic Pydantic entity models directly from dict data.
    
    Expected dict format:
    {
        "EntityName": {
            "fields": {"field1": "str", "field2": "int", ...},
            "docstring": "Optional description for LLM guidance"
        }
    }
    
    Args:
        entity_data: Dict with entity definitions
        
    Returns:
        Dictionary mapping entity names to Pydantic model classes
        
    Raises:
        ValueError: If dict structure is invalid
        TypeError: If field types are not supported
    """
    entity_types = {}
    
    for entity_name, entity_config in entity_data.items():
        if not isinstance(entity_config, dict) or 'fields' not in entity_config:
            raise ValueError(f"Entity '{entity_name}' must have 'fields' key")
        
        fields = entity_config['fields']
        docstring = entity_config.get('docstring', '')
        
        # Convert field definitions to Pydantic field format
        pydantic_fields = {}
        for field_name, field_type_str in fields.items():
            if field_type_str not in TYPE_MAPPING:
                raise TypeError(f"Unsupported field type '{field_type_str}' for field '{field_name}' in entity '{entity_name}'. Supported types: {list(TYPE_MAPPING.keys())}")
            
            pydantic_fields[field_name] = (TYPE_MAPPING[field_type_str], ...)
        
        # Create dynamic Pydantic model
        try:
            model = create_model(entity_name, **pydantic_fields)
            if docstring:
                model.__doc__ = docstring
            entity_types[entity_name] = model
            logger.info(f"Created custom entity type: {entity_name}")
        except Exception as e:
            raise ValueError(f"Failed to create entity model '{entity_name}': {e}")
    
    return entity_types


def convert_edge_mappings(edge_data: dict[str, list[str]]) -> dict[tuple[str, str], list[str]]:
    """
    Convert edge mappings from dict with string keys to dict with tuple keys.
    
    Expected dict format:
    {
        "('SourceEntity', 'TargetEntity')": ["EDGE_TYPE1", "EDGE_TYPE2", ...],
        "('Entity1', 'Entity2')": ["RELATES_TO", "DEPENDS_ON"]
    }
    
    Args:
        edge_data: Dict with edge mappings using string keys
        
    Returns:
        Dictionary mapping entity type pairs (as tuples) to lists of allowed edge types
        
    Raises:
        ValueError: If key format is invalid
    """
    edge_mappings = {}
    
    for key_str, edge_list in edge_data.items():
        # Parse key format: "('Source', 'Target')" -> ('Source', 'Target')
        if not key_str.startswith("('") or not key_str.endswith("')"):
            raise ValueError(f"Invalid edge mapping key format: '{key_str}'. Expected format: \"('Source', 'Target')\"")
        
        try:
            # Extract content between "(' and ')"
            content = key_str[2:-2]  # Remove "(' and ')"
            parts = [part.strip().strip("'\"") for part in content.split("',")]
            
            if len(parts) != 2:
                raise ValueError(f"Edge mapping key must have exactly 2 entities: '{key_str}'")
            
            key_tuple = (parts[0], parts[1])
            
            if not isinstance(edge_list, list):
                raise ValueError(f"Edge list for key '{key_str}' must be a list, got: {type(edge_list)}")
            
            edge_mappings[key_tuple] = edge_list
            logger.info(f"Created edge mapping: {key_tuple} -> {edge_list}")
            
        except Exception as e:
            raise ValueError(f"Failed to parse edge mapping key '{key_str}': {e}")
    
    return edge_mappings