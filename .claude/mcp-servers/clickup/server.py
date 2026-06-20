#!/usr/bin/env python3
"""
ClickUp MCP Server
Provides tools to interact with ClickUp API for task management
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import BaseModel, Field


class ClickUpClient:
    """Client for ClickUp API v2"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to ClickUp API"""
        url = f"{self.base_url}/{endpoint}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()

    async def get_workspaces(self) -> List[Dict]:
        """Get all workspaces (teams)"""
        result = await self._request("GET", "team")
        return result.get("teams", [])

    async def get_spaces(self, team_id: str) -> List[Dict]:
        """Get all spaces in a workspace"""
        result = await self._request("GET", f"team/{team_id}/space")
        return result.get("spaces", [])

    async def get_folders(self, space_id: str) -> List[Dict]:
        """Get all folders in a space"""
        result = await self._request("GET", f"space/{space_id}/folder")
        return result.get("folders", [])

    async def get_lists(self, folder_id: str) -> List[Dict]:
        """Get all lists in a folder"""
        result = await self._request("GET", f"folder/{folder_id}/list")
        return result.get("lists", [])

    async def create_folder(
        self,
        space_id: str,
        name: str
    ) -> Dict:
        """Create a new folder in a space"""
        data = {"name": name}
        return await self._request("POST", f"space/{space_id}/folder", data=data)

    async def create_list(
        self,
        folder_id: str,
        name: str,
        content: Optional[str] = None,
        priority: Optional[int] = None,
        status: Optional[str] = None
    ) -> Dict:
        """Create a new list in a folder"""
        data = {"name": name}
        if content:
            data["content"] = content
        if priority:
            data["priority"] = priority
        if status:
            data["status"] = status

        return await self._request("POST", f"folder/{folder_id}/list", data=data)

    async def create_task(
        self,
        list_id: str,
        name: str,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        assignees: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        status: Optional[str] = None,
        due_date: Optional[int] = None,
        time_estimate: Optional[int] = None,
        custom_fields: Optional[List[Dict]] = None
    ) -> Dict:
        """Create a new task in a list"""
        data = {"name": name}

        if description:
            data["description"] = description
        if priority:
            data["priority"] = priority
        if assignees:
            data["assignees"] = assignees
        if tags:
            data["tags"] = tags
        if status:
            data["status"] = status
        if due_date:
            data["due_date"] = due_date
        if time_estimate:
            data["time_estimate"] = time_estimate * 60 * 60 * 1000  # Convert hours to milliseconds
        if custom_fields:
            data["custom_fields"] = custom_fields

        return await self._request("POST", f"list/{list_id}/task", data=data)

    async def update_task(
        self,
        task_id: str,
        **kwargs
    ) -> Dict:
        """Update an existing task"""
        return await self._request("PUT", f"task/{task_id}", data=kwargs)

    async def create_task_comment(
        self,
        task_id: str,
        comment: str
    ) -> Dict:
        """Add a comment to a task"""
        data = {"comment_text": comment}
        return await self._request("POST", f"task/{task_id}/comment", data=data)

    async def get_folder_details(self, folder_id: str) -> Dict:
        """Get details of a specific folder"""
        return await self._request("GET", f"folder/{folder_id}")


# Initialize MCP server
app = Server("clickup-mcp-server")

# Global client instance (will be initialized with API token)
clickup_client: Optional[ClickUpClient] = None


def get_client() -> ClickUpClient:
    """Get or initialize ClickUp client"""
    global clickup_client
    if clickup_client is None:
        api_token = os.getenv("CLICKUP_API_TOKEN")
        if not api_token:
            raise ValueError("CLICKUP_API_TOKEN environment variable not set")
        clickup_client = ClickUpClient(api_token)
    return clickup_client


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available ClickUp tools"""
    return [
        Tool(
            name="clickup_list_workspaces",
            description="List all ClickUp workspaces (teams) accessible with the API token",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="clickup_list_spaces",
            description="List all spaces in a workspace",
            inputSchema={
                "type": "object",
                "properties": {
                    "team_id": {
                        "type": "string",
                        "description": "The workspace/team ID"
                    }
                },
                "required": ["team_id"]
            }
        ),
        Tool(
            name="clickup_list_folders",
            description="List all folders in a space",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "The space ID"
                    }
                },
                "required": ["space_id"]
            }
        ),
        Tool(
            name="clickup_get_folder_details",
            description="Get details of a specific folder including its lists",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_id": {
                        "type": "string",
                        "description": "The folder ID"
                    }
                },
                "required": ["folder_id"]
            }
        ),
        Tool(
            name="clickup_list_lists",
            description="List all lists in a folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_id": {
                        "type": "string",
                        "description": "The folder ID"
                    }
                },
                "required": ["folder_id"]
            }
        ),
        Tool(
            name="clickup_create_folder",
            description="Create a new folder in a space",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "The space ID where the folder will be created"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of the folder"
                    }
                },
                "required": ["space_id", "name"]
            }
        ),
        Tool(
            name="clickup_create_list",
            description="Create a new list in a folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_id": {
                        "type": "string",
                        "description": "The folder ID where the list will be created"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of the list"
                    },
                    "content": {
                        "type": "string",
                        "description": "Description/content of the list"
                    },
                    "priority": {
                        "type": "integer",
                        "description": "Priority level (1=urgent, 2=high, 3=normal, 4=low)"
                    }
                },
                "required": ["folder_id", "name"]
            }
        ),
        Tool(
            name="clickup_create_task",
            description="Create a new task in a list with detailed information",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_id": {
                        "type": "string",
                        "description": "The list ID where the task will be created"
                    },
                    "name": {
                        "type": "string",
                        "description": "Task name/title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed task description (supports Markdown)"
                    },
                    "priority": {
                        "type": "integer",
                        "description": "Priority level (1=urgent, 2=high, 3=normal, 4=low)"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of tag names"
                    },
                    "time_estimate": {
                        "type": "integer",
                        "description": "Time estimate in hours"
                    }
                },
                "required": ["list_id", "name"]
            }
        ),
        Tool(
            name="clickup_add_task_comment",
            description="Add a comment to an existing task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The task ID"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Comment text (supports Markdown)"
                    }
                },
                "required": ["task_id", "comment"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    try:
        client = get_client()

        if name == "clickup_list_workspaces":
            result = await client.get_workspaces()
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "clickup_list_spaces":
            result = await client.get_spaces(arguments["team_id"])
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "clickup_list_folders":
            result = await client.get_folders(arguments["space_id"])
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "clickup_get_folder_details":
            result = await client.get_folder_details(arguments["folder_id"])
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "clickup_list_lists":
            result = await client.get_lists(arguments["folder_id"])
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "clickup_create_folder":
            result = await client.create_folder(
                space_id=arguments["space_id"],
                name=arguments["name"]
            )
            return [TextContent(
                type="text",
                text=f"✅ Folder created successfully!\n\n{json.dumps(result, indent=2)}"
            )]

        elif name == "clickup_create_list":
            result = await client.create_list(
                folder_id=arguments["folder_id"],
                name=arguments["name"],
                content=arguments.get("content"),
                priority=arguments.get("priority")
            )
            return [TextContent(
                type="text",
                text=f"✅ List created successfully!\n\n{json.dumps(result, indent=2)}"
            )]

        elif name == "clickup_create_task":
            result = await client.create_task(
                list_id=arguments["list_id"],
                name=arguments["name"],
                description=arguments.get("description"),
                priority=arguments.get("priority"),
                tags=arguments.get("tags"),
                time_estimate=arguments.get("time_estimate")
            )
            return [TextContent(
                type="text",
                text=f"✅ Task created successfully!\n\n{json.dumps(result, indent=2)}"
            )]

        elif name == "clickup_add_task_comment":
            result = await client.create_task_comment(
                task_id=arguments["task_id"],
                comment=arguments["comment"]
            )
            return [TextContent(
                type="text",
                text=f"✅ Comment added successfully!\n\n{json.dumps(result, indent=2)}"
            )]

        else:
            return [TextContent(
                type="text",
                text=f"❌ Unknown tool: {name}"
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
