from setuptools import setup, find_packages

setup(
    name="claude-computer-use",
    version="1.0.0",
    description="Claude Computer Use Assistant",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.7.0",
        "pillow>=9.0.0",
        "pyautogui>=0.9.54",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.8",
)