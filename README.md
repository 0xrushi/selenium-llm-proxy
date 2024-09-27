# Selenium LLM Proxy 🌐🤖

**Easily connect browser-based LLMs with your favorite AI tools!**

This project allows for the automation of AI interactions within websites using tools like Selenium or Websockets. Additionally, it provides a way to connect those automated
interactions with Language Model (LLM) software components such as apps, agents, or libraries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-%5E4.0.0-green)](https://www.selenium.dev/)

## 🚀 Features

- 🌐 Automate browser-based ChatGPT effortlessly with Selenium
- 🔌 Works seamlessly with popular AI tools like:
  - Cursor
  - AI Agents
  - LangChain
  - And more!
- 💰 A slow but budget-friendly experimentation alternative to API keys

## ⚠️ Important Note

- ⏱️ Performance is slower compared to official APIs, but good enough for experimentation
- 🔄 You may need to periodically update Selenium scripts and chromedriver to ensure compatibility
- Implementing it with CrewAI is more challenging due to their architecture, but it works with Langgraph

## Demo video

[<img src="images/video_thumbnail.png" width="80%">](https://odysee.com/@rushi:2/demo_selenium_proxy:0)


## 🛠️ Installation

To get started, clone the repository and install the required packages:

```bash
git clone https://github.com/0xrushi/selenium-llm-proxy.git
cd selenium-llm-proxy
pip install -r requirements.txt
```

## 🔧 Example

1. Launch LLM server with 
   ```python
   python main.py
   ```

2. Execute the agent experiment in another terminal
   ```bash
   python langgraph_experiment.py
   ```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


⭐️ If you find this project helpful, please consider giving it a star!