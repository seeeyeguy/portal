"""
`Program Review Tool` PowerBI export utilities

This module provides functionality for exporting reports from PowerBI,
including initiating exports, polling for completion, and retrieving files.
"""

import json
import logging
import os
import requests
import time
from typing import Any, Dict, List, Optional, Tuple

from program_review_tool.exceptions import ProgramReviewToolError


LOGGER = logging.getLogger(__name__)

# PowerBI API endpoints
POWERBI_API_BASE = os.getenv("AZURE_POWERBI_URI_MYORG", "https://api.high.powerbigov.us/v1.0/myorg")

# Export polling configuration
MAX_POLL_ATTEMPTS = 60  # Maximum number of polling attempts
POLL_INTERVAL_SECONDS = 5  # Seconds between polling attempts

# Export format
EXPORT_FORMAT = "PNG"

# PowerBI export states
class ExportState:
    """PowerBI export state constants."""
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"


def build_export_request_body(
    page_name: str,
    project_ids: List[str],
    project_filter_table: str,
    project_filter_column: str,
    identity: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build the request body for PowerBI export API.
    
    Accepts:
        * page_name (str): The PowerBI page name to export.
        * project_ids (List[str]): List of project IDs to filter on.
        * project_filter_table (str): Table name for filtering.
        * project_filter_column (str): Column name for filtering.
        * identity (Optional[Dict[str, Any]]): Effective identity for RLS.
        
    Returns:
        * Dict[str, Any]: Request body for export API.
    """
    request_body: Dict[str, Any] = {
        "format": EXPORT_FORMAT,
        "powerBIReportConfiguration": {
            "pages": [{"pageName": page_name}]
        }
    }
    
    LOGGER.info(f"build_export_request_body():project_filter_table: {project_filter_table}")
    LOGGER.info(f"build_export_request_body():project_filter_column: {project_filter_column}")
    
    # Add filter if we have the necessary information
    if project_filter_table and project_filter_column and project_ids:
        # Build filter string: "TableName/ColumnName in ('PA1', 'PA2', ...)"
        project_ids_quoted = "', '".join(project_ids)
        filter_string = f"{project_filter_table}/{project_filter_column} in ('{project_ids_quoted}')"
        
        request_body["powerBIReportConfiguration"]["reportLevelFilters"] = [
            {
                "filter": filter_string
            }
        ]
        LOGGER.debug(f"Added filter: {filter_string}")
    
    # Add effective identity if required
    if identity:
        request_body["powerBIReportConfiguration"]["identities"] = [
            {
                "username": identity["username"],
                "roles": [identity["role"]],
                "datasets": [identity["dataset_id"]]
            }
        ]
        LOGGER.debug(f"Added effective identity for user: {identity['username']}")
    
    return request_body


def initiate_export(
    workspace_id: str,
    report_id: str,
    request_body: Dict[str, Any],
    token: str
) -> str:
    """
    Initiate a PowerBI report export.
    
    Accepts:
        * workspace_id (str): PowerBI workspace GUID.
        * report_id (str): PowerBI report GUID.
        * request_body (Dict[str, Any]): Export request configuration.
        * token (str): Azure AD access token.
        
    Returns:
        * str: Export ID for polling.
        
    Raises:
        * ProgramReviewToolError: If export initiation fails.
    """
    url = f"{POWERBI_API_BASE}/groups/{workspace_id}/reports/{report_id}/ExportTo"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    LOGGER.info(f"Initiating export for report {report_id} in workspace {workspace_id}")
    LOGGER.info(f"URI: {url}")
    LOGGER.info(f"Export request body: {json.dumps(request_body, indent=2)}")
    LOGGER.info(f"token: {token}")
    LOGGER.info(f"headers: {headers}")
    
    try:
        response = requests.post(url, headers=headers, json=request_body, timeout=30)
        
        LOGGER.info(f"response object: {response}")
        
        if response.status_code == 202:
            # Export initiated successfully
            export_data = response.json()
            export_id = export_data.get("id")
            
            if not export_id:
                raise ProgramReviewToolError(
                    "Export initiated but no export ID returned",
                    500
                )
            
            LOGGER.info(f"Export initiated successfully. Export ID: {export_id}")
            return export_id
            
        else:
            error_msg = f"Failed to initiate export. Status: {response.status_code}, Response: {response.text}"
            LOGGER.error(error_msg)
            raise ProgramReviewToolError(error_msg, response.status_code)
            
    except requests.RequestException as exc:
        error_msg = f"Network error initiating export: {exc}"
        LOGGER.error(error_msg)
        raise ProgramReviewToolError(error_msg, 500) from exc
    except Exception as exc:
        error_msg = f"Unexpected error initiating export: {exc}"
        LOGGER.error(error_msg)
        raise ProgramReviewToolError(error_msg, 500) from exc


def poll_export_status(
    workspace_id: str,
    report_id: str,
    export_id: str,
    token: str,
    max_attempts: int = MAX_POLL_ATTEMPTS,
    poll_interval: int = POLL_INTERVAL_SECONDS
) -> str:
    """
    Poll PowerBI export status until completion or timeout.
    
    Accepts:
        * workspace_id (str): PowerBI workspace GUID.
        * report_id (str): PowerBI report GUID.
        * export_id (str): Export ID from initiate_export.
        * token (str): Azure AD access token.
        * max_attempts (int): Maximum polling attempts.
        * poll_interval (int): Seconds between polls.
        
    Returns:
        * str: Export state (should be 'Succeeded' on success).
        
    Raises:
        * ProgramReviewToolError: If export fails or times out.
    """
    url = f"{POWERBI_API_BASE}/groups/{workspace_id}/reports/{report_id}/exports/{export_id}"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    LOGGER.info(f"Polling export status for export ID: {export_id}")
    
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code in [200, 202]:
                export_data = response.json()
                status = export_data.get("status")
                percent_complete = export_data.get("percentComplete", 0)
                
                LOGGER.debug(
                    f"Export {export_id} - Attempt {attempt}/{max_attempts}: "
                    f"Status={status}, Progress={percent_complete}%"
                )
                
                if status == ExportState.SUCCEEDED:
                    LOGGER.info(f"Export {export_id} completed successfully")
                    return status
                    
                elif status == ExportState.FAILED:
                    error = export_data.get("error", {})
                    error_msg = (
                        f"Export {export_id} failed. "
                        f"Error: {error.get('message', 'Unknown error')}"
                    )
                    LOGGER.error(error_msg)
                    raise ProgramReviewToolError(error_msg, 500)
                    
                elif status == ExportState.RUNNING:
                    # Export still in progress
                    if attempt < max_attempts:
                        time.sleep(poll_interval)
                        continue
                    else:
                        error_msg = (
                            f"Export {export_id} timed out after "
                            f"{max_attempts * poll_interval} seconds"
                        )
                        LOGGER.error(error_msg)
                        raise ProgramReviewToolError(error_msg, 504)
                        
                else:
                    error_msg = f"Export {export_id} has unknown status: {status}"
                    LOGGER.warning(error_msg)
                    if attempt < max_attempts:
                        time.sleep(poll_interval)
                        continue
                    else:
                        raise ProgramReviewToolError(error_msg, 500)
                        
            else:
                error_msg = (
                    f"Failed to poll export status. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
                LOGGER.error(error_msg)
                raise ProgramReviewToolError(error_msg, response.status_code)
                
        except requests.RequestException as exc:
            error_msg = f"Network error polling export status: {exc}"
            LOGGER.error(error_msg)
            if attempt < max_attempts:
                LOGGER.info(f"Retrying in {poll_interval} seconds...")
                time.sleep(poll_interval)
                continue
            else:
                raise ProgramReviewToolError(error_msg, 500) from exc
                
        except ProgramReviewToolError:
            # Re-raise our own exceptions
            raise
            
        except Exception as exc:
            error_msg = f"Unexpected error polling export status: {exc}"
            LOGGER.error(error_msg)
            raise ProgramReviewToolError(error_msg, 500) from exc
    
    # Should not reach here, but just in case
    raise ProgramReviewToolError(f"Export {export_id} timed out", 504)


def check_export_status(
    workspace_id: str,
    report_id: str,
    export_id: str,
    token: str
) -> str:
    """
    Check the status of a PowerBI export (single check, non-blocking).
    
    This function performs a single status check without polling/waiting.
    Used by concurrent export implementations to check multiple exports
    in rotation.
    
    Accepts:
        * workspace_id (str): PowerBI workspace GUID
        * report_id (str): PowerBI report GUID
        * export_id (str): Export operation ID
        * token (str): PowerBI authentication token
        
    Returns:
        * str: Export status ("Running", "Succeeded", "Failed", or "Unknown")
    """
    url = f"{POWERBI_API_BASE}/groups/{workspace_id}/reports/{report_id}/exports/{export_id}"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # Accept both 200 OK and 202 Accepted
        if response.status_code in [200, 202]:
            export_data = response.json()
            status = export_data.get("status", "Unknown")
            LOGGER.debug(
                f"Export {export_id[:20]}... status: {status} "
                f"({export_data.get('percentComplete', 0)}% complete)"
            )
            return status
        else:
            LOGGER.warning(
                f"Unexpected status code {response.status_code} when checking "
                f"export {export_id[:20]}...: {response.text[:100]}"
            )
            return "Unknown"
            
    except requests.RequestException as exc:
        LOGGER.error(f"Network error checking export status: {exc}")
        return "Unknown"
    except Exception as exc:
        LOGGER.error(f"Error checking export status: {exc}")
        return "Unknown"


def retrieve_export_file(
    workspace_id: str,
    report_id: str,
    export_id: str,
    output_path: str,
    token: str
) -> str:
    """
    Retrieve the exported file from PowerBI.
    
    Accepts:
        * workspace_id (str): PowerBI workspace GUID.
        * report_id (str): PowerBI report GUID.
        * export_id (str): Export ID from initiate_export.
        * output_path (str): Path to save the exported file.
        * token (str): Azure AD access token.
        
    Returns:
        * str: Path to the saved file.
        
    Raises:
        * ProgramReviewToolError: If file retrieval fails.
    """
    url = f"{POWERBI_API_BASE}/groups/{workspace_id}/reports/{report_id}/exports/{export_id}/file"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    LOGGER.info(f"Retrieving export file for export ID: {export_id}")
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        
        if response.status_code == 200:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write file in chunks
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(output_path)
            LOGGER.info(
                f"Export file saved successfully to {output_path} "
                f"(size: {file_size:,} bytes)"
            )
            
            return output_path
            
        else:
            error_msg = (
                f"Failed to retrieve export file. "
                f"Status: {response.status_code}, Response: {response.text}"
            )
            LOGGER.error(error_msg)
            raise ProgramReviewToolError(error_msg, response.status_code)
            
    except requests.RequestException as exc:
        error_msg = f"Network error retrieving export file: {exc}"
        LOGGER.error(error_msg)
        raise ProgramReviewToolError(error_msg, 500) from exc
    except IOError as exc:
        error_msg = f"File I/O error: {exc}"
        LOGGER.error(error_msg)
        raise ProgramReviewToolError(error_msg, 500) from exc
    except Exception as exc:
        error_msg = f"Unexpected error retrieving export file: {exc}"
        LOGGER.error(error_msg)
        raise ProgramReviewToolError(error_msg, 500) from exc


def export_powerbi_report_page(
    workspace_id: str,
    report_id: str,
    page_name: str,
    output_path: str,
    token: str,
    project_ids: Optional[List[str]] = None,
    project_filter_table: Optional[str] = None,
    project_filter_column: Optional[str] = None,
    identity: Optional[Dict[str, Any]] = None
) -> str:
    """
    Complete workflow to export a PowerBI report page to a file.
    
    This function orchestrates the full export process:
    1. Initiate export
    2. Poll until complete
    3. Retrieve file
    
    Accepts:
        * workspace_id (str): PowerBI workspace GUID.
        * report_id (str): PowerBI report GUID.
        * page_name (str): PowerBI page name to export.
        * output_path (str): Path to save the exported file.
        * token (str): Azure AD access token.
        * project_ids (Optional[List[str]]): Project IDs for filtering.
        * project_filter_table (Optional[str]): Table name for filtering.
        * project_filter_column (Optional[str]): Column name for filtering.
        * identity (Optional[Dict[str, Any]]): Effective identity for RLS.
        
    Returns:
        * str: Path to the saved file.
        
    Raises:
        * ProgramReviewToolError: If any step of the export fails.
    """
    start_time = time.perf_counter()
    
    LOGGER.info(f"export_powerbi_report_page():project_filter_column: {project_filter_column}")
    LOGGER.info(f"export_powerbi_report_page():project_filter_column: {project_filter_column}")
    
    try:
        # Step 1: Build request body
        request_body = build_export_request_body(
            page_name=page_name,
            project_ids=project_ids or [],
            project_filter_table=project_filter_table or "",
            project_filter_column=project_filter_column or "",
            identity=identity
        )
        
        # Step 2: Initiate export
        export_id = initiate_export(
            workspace_id=workspace_id,
            report_id=report_id,
            request_body=request_body,
            token=token
        )
        
        # Step 3: Poll for completion
        status = poll_export_status(
            workspace_id=workspace_id,
            report_id=report_id,
            export_id=export_id,
            token=token
        )
        
        if status != ExportState.SUCCEEDED:
            raise ProgramReviewToolError(
                f"Export did not complete successfully. Status: {status}",
                500
            )
        
        # Step 4: Retrieve file
        file_path = retrieve_export_file(
            workspace_id=workspace_id,
            report_id=report_id,
            export_id=export_id,
            output_path=output_path,
            token=token
        )
        
        elapsed = time.perf_counter() - start_time
        LOGGER.info(
            f"Complete export workflow finished in {elapsed:.2f} seconds. "
            f"File saved to: {file_path}"
        )
        
        return file_path
        
    except ProgramReviewToolError:
        # Re-raise our own exceptions
        raise
    except Exception as exc:
        error_msg = f"Unexpected error in export workflow: {exc}"
        LOGGER.error(error_msg)
        raise ProgramReviewToolError(error_msg, 500) from exc
