Got it 😄 You want **only the README content**, cleanly formatted so you can copy-paste it directly into GitHub — no extra instructions, no weird nested code blocks.

Copy everything below:

# 🌐 Website Health Checker

A Python + Playwright QA automation tool that checks the health of a website automatically.

## 🚀 Features

* ✅ Check website HTTP status
* ⏱️ Measure page load time
* 🏷️ Check page title
* 🔗 Detect broken links
* ⏱️ Detect link timeouts
* 🖼️ Detect missing/broken images
* 🚨 Detect HTTP 4xx/5xx errors
* 📊 Generate an HTML health report

## 🛠️ Tech Stack

* Python
* Playwright
* Google Chrome
* HTML/CSS

## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/mrashwini/website-health-checker.git
cd website-health-checker
```

Create a virtual environment:

```
python -m venv venv
```

Activate it on Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## ▶️ Usage

Run the application:

```
python main.py
```

Enter a website URL when prompted:

```
Enter website URL: https://example.com
```

The tool will perform the health checks and generate an HTML report.

## 📋 Example Output

```
==============================
   WEBSITE HEALTH CHECKER
==============================

URL: https://example.com
HTTP Status: 200
Page Load Time: 0.74 seconds
Page Title: ✅ Example Domain

==============================
BROKEN LINK REPORT
==============================

Total Links: 1
Working Links: 0
Broken Links: 0
Timeout Links: 1

==============================
IMAGE REPORT
==============================

Total Images: 0
Missing Images: 0

==============================
HTTP ERROR REPORT
==============================

HTTP Errors Found: 0
✅ No HTTP errors detected!
```

## 🎯 QA Skills Demonstrated

* Browser automation
* Functional testing
* Link validation
* HTTP response validation
* Network monitoring
* Performance measurement
* Error detection
* Automated test reporting

## 🔮 Future Improvements

* Slow page detection
* Accessibility testing
* SEO checks
* Screenshot capture for failures
* GitHub Actions CI/CD
* Web-based dashboard

## 👩‍💻 Author

**Ashwini Singh**

GitHub: [https://github.com/mrashwini](https://github.com/mrashwini)
