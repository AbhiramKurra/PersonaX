# 🚨 PersonaX – Advanced OSINT Investigation & Intelligence Tool

PersonaX is an evolving, GUI-based **Open-Source Intelligence (OSINT)** investigation framework designed to gather, correlate, and analyze digital footprints across the open web, social media platforms, dark web sources, metadata, breached datasets, and more.

It supports cybersecurity teams, digital forensic units, and government-investigation workflows.

> ⚠️ **Note:** This project is *not yet complete*.  
> If you would like to contribute, collaborate, or help develop any module, you are welcome to reach out!

---

## 🌐 Core Features

### 🔎 1. Username Hunter
- Scan usernames across 500+ platforms  
- Inspired by Maigret & Sherlock  
- Fast parallel scanning  
- Identity correlation across platforms  

### 📧 2. Email Breach Lookup
- Scrapes public breach databases  
- Pastebin/Ghostbin leak search  
- Search-engine OSINT  
- Combines results from multiple sources  

### 🖼️ 3. Image Intelligence Module *(Planned)*
- Reverse image search (Google/Bing/Yandex via Selenium)  
- Facial recognition & similarity  
- EXIF metadata extraction  
- GPS → Map plotting  
- Timeline reconstruction  

### 🌑 4. Dark Web Scanner *(Planned)*
- Tor-based `.onion` scanning  
- Dark web engine scraping  
- Marketplace & leak-site lookup  
- Proxy/Anonymity support  

### 🌍 5. Geo-Locator
- EXIF GPS extraction  
- Multi-source geocoding  
- Map visualization  
- Location history building  

### 📱 6. Social Media Scraper
Supports: Twitter, Instagram, Facebook, Reddit, LinkedIn, GitHub, TikTok, Pinterest, Snapchat, YouTube  
- Public profile info  
- Activity footprints  
- Username mapping  
- Social graph linkage  

---

# 🖥️ New GUI Version (Current)

- Tkinter-based GUI  
- No virtual environment required  
- Modules included:
  - Username scan  
  - Email lookup  
  - Web search scraping  
  - Social media presence detection  

---

# ⚙️ Installation

### 1. Clone the repository
```
git clone https://github.com/AbhiramKurra/PersonaX.git
cd PersonaX
```

### 2. Install dependencies (system-wide)
```
pip install requests beautifulsoup4 selenium pillow
```

### 3. Optional (for image scraping)
Download ChromeDriver from:  
https://chromedriver.chromium.org/downloads

---

# 🚀 Running PersonaX

```
python main.py
```

GUI will open and allow OSINT searches.

---

# ⚖️ Ethical Use Policy
PersonaX is for:
- Cybersecurity research  
- Digital forensics  
- Lawful OSINT investigations  
- Academic training  

Illegal use is prohibited.

---

# 🤝 Contributing
The project is active and evolving.  
If you'd like to help enhance it — you are welcome!

📩 **Contact:**  
Mail: kurra.abhiram@gmail.com

---

# 📜 License
Licensed under **MIT License**.

---

# ⚠️ Disclaimer
PersonaX is for **legal OSINT purposes only**.  
The developer is not responsible for misuse.


