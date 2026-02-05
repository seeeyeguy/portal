"""
`Program Review Tool` `Program` review export utils file
containing common functionality for getting the
PowerBI slide mapping used in the generation
of the PowerPoint export.

Updated to support JSON configuration format for PowerBI integration.
"""

import json
import logging
import os
import pandas as pd
from typing import Any, Dict, List, Optional

from jsonschema import validate, ValidationError

from program_review_tool.utils.review.export.config import ASSETS_DIR


LOGGER = logging.getLogger(__name__)

# Configuration file paths
SLIDES_CONFIG_PATH: str = os.path.join(ASSETS_DIR, "slides_config.json")
SLIDES_SCHEMA_PATH: str = os.path.join(ASSETS_DIR, "slides_config.schema.json")

# Legacy CSV support (for backward compatibility during migration)
LEGACY_SLIDES_CSV_PATH: str = os.path.join(ASSETS_DIR, "slides.csv")


class SlidesConfigError(Exception):
    """Exception raised for slides configuration errors."""
    pass


def load_slides_config(validate_schema: bool = True) -> Dict[str, Any]:
    """
    Load and optionally validate slides configuration from JSON.
    
    Accepts:
        * validate_schema (bool): Whether to validate against JSON schema.
        
    Returns:
        * Dict[str, Any]: Configuration dictionary containing 'version' and 'slides'.
        
    Raises:
        * SlidesConfigError: If configuration cannot be loaded or is invalid.
    """
    if not os.path.exists(SLIDES_CONFIG_PATH):
        error_msg = f"Slides configuration file not found: {SLIDES_CONFIG_PATH}"
        LOGGER.error(error_msg)
        raise SlidesConfigError(error_msg)
    
    try:
        with open(SLIDES_CONFIG_PATH, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            
        LOGGER.info(f"Loaded slides configuration from {SLIDES_CONFIG_PATH}")
        
        # Validate against schema if requested and schema exists
        if validate_schema and os.path.exists(SLIDES_SCHEMA_PATH):
            with open(SLIDES_SCHEMA_PATH, 'r', encoding='utf-8') as schema_file:
                schema = json.load(schema_file)
            validate(instance=config, schema=schema)
            LOGGER.info("Slides configuration validated successfully against schema")
            
        return config
        
    except json.JSONDecodeError as exc:
        error_msg = f"Invalid JSON in slides configuration: {exc}"
        LOGGER.error(error_msg)
        raise SlidesConfigError(error_msg) from exc
        
    except ValidationError as exc:
        error_msg = f"Slides configuration validation failed: {exc.message}"
        LOGGER.error(error_msg)
        raise SlidesConfigError(error_msg) from exc
        
    except Exception as exc:
        error_msg = f"Unexpected error loading slides configuration: {exc}"
        LOGGER.error(error_msg)
        raise SlidesConfigError(error_msg) from exc


def get_powerbi_slide_mapping_df(validate_schema: bool = True) -> pd.DataFrame:
    """
    Load PowerBI slide configuration and convert to DataFrame for compatibility
    with existing slide processing code.
    
    Accepts:
        * validate_schema (bool): Whether to validate the configuration against schema.
        
    Returns:
        * pd.DataFrame: DataFrame containing flattened slide configuration.
            Returns empty DataFrame if configuration cannot be loaded.
    """
    try:
        config = load_slides_config(validate_schema=validate_schema)
        slides = config.get('slides', [])
        
        if not slides:
            LOGGER.warning("No slides found in configuration")
            return pd.DataFrame()
        
        # Flatten nested structures for DataFrame compatibility
        flattened_slides = []
        for slide in slides:
            flat_slide = {
                # Basic slide info
                'slide_num': slide['slide_num'],
                'slide_title': slide['slide_title'],
                
                # PowerBI identifiers
                'workspace_id': slide['workspace_id'],
                'report_id': slide['report_id'],
                'pageName': slide['pageName'],
                
                # Project filter configuration
                'project_filter_column_name': slide['project_filter']['column_name'],
                'project_filter_table_name': slide['project_filter']['table_name'],
                
                # Identity/authentication
                'identity_required': slide['identity_required'],
                
                # Image dimensions
                'height': slide['image_size']['height'],
                'width': slide['image_size']['width'],
                
                # Layout positioning
                'top': slide.get('layout', {}).get('top', 0.0),
                'left': slide.get('layout', {}).get('left', 0.0),
                
                # Links and metadata
                'workspace_report_url': slide['workspace_report_url'],
                'linkUrl': slide['workspace_report_url'],  # Legacy compatibility
                
                # PA type flags
                'pa_type': slide['pa_type'],
                'isSinglePa': slide['pa_type'] == 'single',
                'isMultiPa': slide['pa_type'] == 'multi',
            }
            
            # Add identity fields if present (for authentication)
            if slide.get('identity') and slide['identity'] is not None:
                flat_slide.update({
                    'identity_username': slide['identity']['username'],
                    'identity_role': slide['identity']['role'],
                    'identity_dataset_id': slide['identity']['dataset_id'],
                })
            else:
                flat_slide.update({
                    'identity_username': None,
                    'identity_role': None,
                    'identity_dataset_id': None,
                })
            
            flattened_slides.append(flat_slide)
        
        df = pd.DataFrame(flattened_slides)
        LOGGER.info(f"Converted {len(flattened_slides)} slides to DataFrame")
        return df
        
    except SlidesConfigError as exc:
        LOGGER.error(f"Failed to load slides configuration: {exc}")
        return pd.DataFrame()
    except Exception as exc:
        LOGGER.error(f"Unexpected error creating slides DataFrame: {exc}")
        return pd.DataFrame()

# ============================================================================
# Validation and Utilities
# ============================================================================

def get_config_statistics() -> Dict[str, Any]:
    """
    Get statistics about the current slides configuration.
    
    Returns:
        * Dict[str, Any]: Dictionary containing configuration statistics.
    """
    try:
        config = load_slides_config(validate_schema=False)
        slides = config.get('slides', [])
        
        single_pa_count = sum(1 for s in slides if s['pa_type'] == 'single')
        multi_pa_count = sum(1 for s in slides if s['pa_type'] == 'multi')
        identity_required_count = sum(1 for s in slides if s['identity_required'])
        
        stats = {
            'version': config.get('version', 'unknown'),
            'total_slides': len(slides),
            'single_pa_slides': single_pa_count,
            'multi_pa_slides': multi_pa_count,
            'slides_requiring_identity': identity_required_count,
            'unique_workspaces': len(set(s['workspace_id'] for s in slides)),
            'unique_reports': len(set(s['report_id'] for s in slides)),
        }
        
        return stats
        
    except SlidesConfigError:
        return {'error': 'Failed to load configuration'}
