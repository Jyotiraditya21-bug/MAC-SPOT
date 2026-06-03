from setuptools import setup, find_packages

setup(
    name="mac-spot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai>=0.5.0",
        "rich>=13.0.0",
        "typer>=0.12.0",
        "pyperclip>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "mac-spot=mac_spot.cli:app",
        ],
    },
    author="MAC-SPOT Architect",
    description="Your AI-powered dev assistant for macOS — powered by Gemini",
)
