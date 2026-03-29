"""
Predyx MCP Server - Bitcoin-native prediction market data provider
"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="predyx-mcp-server",
    version="1.0.0",
    author="Dia AI",
    author_email="dia@dia-ai.com",
    description="Bitcoin-native prediction market data provider for AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arould001/predyx-mcp-server",
    packages=["predyx_mcp_server"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.11",
    install_requires=[
        "mcp>=1.0.0",
        "pydantic>=2.0.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "predyx-mcp-server=predyx_mcp_server:main",
        ],
    },
    keywords="mcp, model-context-protocol, prediction-market, bitcoin, lightning-network, ai-agents",
    project_urls={
        "Bug Reports": "https://github.com/arould001/predyx-mcp-server/issues",
        "Documentation": "https://github.com/arould001/predyx-mcp-server#readme",
        "Source": "https://github.com/arould001/predyx-mcp-server",
        "MCP Registry": "https://registry.modelcontextprotocol.io/servers/io.github.arould001/predyx-mcp-server",
    },
)
