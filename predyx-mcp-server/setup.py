"""
Predyx MCP Server - Bitcoin-native prediction market data provider
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="predyx-mcp-server",
    version="1.0.0",
    author="Dia AI",
    author_email="dia@dia-ai.com",
    description="Bitcoin-native prediction market data provider for AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dia-ai/predyx-mcp-server",
    packages=find_packages(),
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
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "predyx-mcp-server=predyx_mcp_server:main",
        ],
    },
    keywords="mcp, model-context-protocol, prediction-market, bitcoin, lightning-network, ai-agents",
    project_urls={
        "Bug Reports": "https://github.com/dia-ai/predyx-mcp-server/issues",
        "Documentation": "https://docs.dia-ai.com/predyx-mcp",
        "Source": "https://github.com/dia-ai/predyx-mcp-server",
        "MCP Registry": "https://registry.modelcontextprotocol.io/servers/io.github.dia-ai/predyx-mcp-server",
    },
)
