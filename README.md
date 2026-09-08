<div align="center">

#  ᴍᴜʟᴛɪ ᴍᴇᴅɪᴀ

> *A multi-media downloader bot automatically extracts and sends high-quality videos directly to your chat when you share a social media link.*

<p align="center">
  <img src="https://i.ibb.co/B51GGLwk/43bf7589463203c278d2351b8b02c677.jpg" alt="girl-image" border="0">
</p>
</div>

---

<h2 align="center">ᴅᴇᴘʟᴏʏ ᴏɴ ʜᴇʀᴏᴋᴜ</h2>

---

<p align="center">
<a href="https://heroku.com/deploy?template=https://github.com/Akatsumo/MultiMedia">
  <img src="https://img.shields.io/badge/Deploy%20to%20Heroku-000000?style=for-the-badge&logo=heroku&logoColor=white" style="height: auto; width: 200px;">
</a>
</p>

---

<h2 align="center">ᴅᴇᴘʟᴏʏ ᴏɴ ᴠᴘꜱ</h2>

<details id="vps-deployment">
  <summary><b>▶ Click Here</b></summary>
  <br>
  
  <blockquote>
    <p><b>Note:</b> Make sure you have root access or sudo privileges on your Ubuntu/Debian server before starting.</p>
  </blockquote>

  <h3>1. Update & Upgrade System Packages</h3>
  <pre><code>sudo apt update && sudo apt upgrade -y</code></pre>

  <h3>2. Install Dependencies</h3>
  <pre><code>sudo apt install python3 python3-pip git -y</code></pre>

  <h3>3. Clone Repository</h3>
  <pre><code>git clone https://github.com/Akatsumo/MultiMedia.git
cd MultiMedia</code></pre>

  <h3>4. Install Requirements</h3>
  <pre><code>pip3 install -r requirements.txt</code></pre>

  <h3>5. Environment Configuration</h3>
  <p>Create a <code>.env</code> file in the root directory and add your credentials:</p>
  <pre><code>nano .env</code></pre>
  
  <p>Paste the following variables into the file:</p>
  <pre><code>BOT_TOKEN=your_bot_token_here
OWNER_IDS=123456789
CHANNEL_IDS=-100123456789
MONGO_DB=your_mongodb_uri</code></pre>

  <h3>6. Run the Bot</h3>
  <pre><code>python3 -m MultiMedia</code></pre>

  <hr>

  <h3>7. Keep Bot Running 24/7 (Optional)</h3>
  <p><b>Option A: Using Screen</b></p>
  <pre><code>screen -S MultiMedia
python3 -m MultiMedia</code></pre>
  <p><i>Press <code>Ctrl + A</code> then <code>D</code> to detach.</i></p>

  <p><b>Option B: Using Tmux</b></p>
  <pre><code>tmux new -s MultiMedia
python3 -m MultiMedia</code></pre>
  <p><i>Press <code>Ctrl + B</code> then <code>D</code> to detach.</i></p>
</details>

---

<h2 align="center">ᴄᴏᴍᴍᴀɴᴅꜱ</h2>

---

| Command | Description |
|---------|------------|
| `/stats` | View bot statistics and overall user/system data |
| `/eval` | Execute Python code (Owner/Developer only) |
| `/addpremium` | Grant premium status to a user or chat |
| info-- | btw, autoremove already handled it! No need for this command /removepremium |
| `/removepremium` | Revoke premium status from a user or chat |
| `/check_premium` | check premium users active plan|
| `/broadcast` or `/announce` | Send a message to all users and channels |

---


