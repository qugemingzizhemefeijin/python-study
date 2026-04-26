import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP Demo")


@mcp.tool()
def ls():
    """列出目录中的文件名"""
    return os.listdir(".")


if __name__ == "__main__":
    mcp.run()
