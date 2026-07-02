# 🚛 Haji Barkat Khan (HBK) Jadoon — Advanced Fleet Management System

Welcome to the **HBK Jadoon Goods Transport — Advanced Fleet & Finance Portal**. 

This application is a premium, client-side Single Page Application (SPA) designed to run entirely in the browser with **zero dependencies**. It stores all data securely in your local browser (`localStorage`) and allows easy export/import for cloud backups.

---

## 🚀 How to Run the App

1. Navigate to this folder (`c:\Users\AFZAL COMPUTERS\Desktop\softhware\`).
2. Double-click on **`index.html`** to open it instantly in Google Chrome, Microsoft Edge, or Firefox.
3. No servers, no installation, and no database configuration are needed!

---

## 📦 Part 1 — Share on Local Office Network
If you want multiple computers in your office or home to access the app:

1. Open PowerShell on the hosting computer and run:
   ```bash
   npx -y serve "C:\Users\AFZAL COMPUTERS\Desktop\softhware" -p 8080
   ```
2. Find the host computer's IP address:
   * Open Command Prompt, type `ipconfig`, and look for the **IPv4 Address** (e.g., `192.168.10.15`).
3. Anyone on your local network can now open:
   `http://192.168.10.15:8080`

---

## 🌍 Part 2 — Deploy Publicly (Free Forever)

### 🥇 Method 1: GitHub Pages (Recommended)
1. Sign up for a free account at [GitHub](https://github.com).
2. Create a new repository named `hbk-fleet` (set it to **Public**).
3. Click "uploading an existing file" and upload your `index.html`.
4. Go to **Settings** → **Pages** (in the sidebar).
5. Under **Build and deployment**, set the Source to **Deploy from a branch**, select the **main** branch and **/** root folder, then click **Save**.
6. After 1-2 minutes, your live link will be ready at:
   `https://YOUR-GITHUB-USERNAME.github.io/hbk-fleet/`

### 🥈 Method 2: Netlify (Drag & Drop)
1. Go to [Netlify](https://app.netlify.com) and log in.
2. Go to **Sites** → click **Add new site** → select **Deploy manually**.
3. Drag and drop the `softhware` folder into the upload window.
4. Your application will be online instantly.

---

## 📧 Part 3 — Gmail Integration (Automatic Email Alerts)
You can configure the application to send automatic email notifications (e.g., when salary is marked paid, or when stock is low) using Google Apps Script.

1. Go to [Google Apps Script](https://script.google.com).
2. Click **New Project** and paste the following script:
   ```javascript
   function doPost(e) {
     const data = JSON.parse(e.postData.contents);
     MailApp.sendEmail({
       to: data.to,
       subject: data.subject,
       htmlBody: `
         <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
           <div style="background:#07111f;color:#fff;padding:20px;border-radius:12px 12px 0 0">
             <h2 style="margin:0;color:#ff8a3d">🚛 HBK Jadoon Goods Transport</h2>
             <p style="margin:4px 0 0;color:#97a3c4;font-size:13px">Fleet Management System</p>
           </div>
           <div style="background:#f8f9fa;padding:24px;border-radius:0 0 12px 12px">
             <p style="font-size:16px;font-weight:600;color:#333">${data.message}</p>
             <pre style="background:#e9ecef;padding:14px;border-radius:8px;font-size:13px">${data.details||''}</pre>
             <p style="color:#999;font-size:12px;margin-top:20px">Sent by HBK Fleet Management System — ${new Date().toLocaleString()}</p>
           </div>
         </div>
       `
     });
     return ContentService.createTextOutput(JSON.stringify({success:true}))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```
3. Click **Deploy** → **New deployment**.
4. Select **Web app**, set **Execute as** to **Me**, and **Who has access** to **Anyone**.
5. Copy the deployment URL.
6. Open your `index.html` and replace `GMAIL_WEBHOOK = '...'` (near the top/bottom JavaScript) with your copied URL.

---

## ☁️ Part 4 — Google Drive Integration (Backups)

### Manual Backup (Simple)
* In the Settings panel of the application, click **Export Data Backup** to download a `.json` backup file.
* You can drag and drop this file into your Google Drive for safekeeping.
* To restore, click **Import Backup File** in Settings and select your backup.

### Automated Backups (Advanced)
To automatically save a JSON backup to your Google Drive every time you make changes:
1. Create another project in [Google Apps Script](https://script.google.com).
2. Paste this code:
   ```javascript
   function doPost(e) {
     const data = e.postData.contents;
     const filename = `HBK-Fleet-Backup-${new Date().toISOString().slice(0,10)}.json`;
     const existing = DriveApp.getFilesByName(filename);
     while (existing.hasNext()) existing.next().setTrashed(true); // Remove previous backup for today
     DriveApp.createFile(filename, data, MimeType.PLAIN_TEXT);
     return ContentService.createTextOutput(JSON.stringify({success:true, filename}))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```
3. Deploy as a **Web app** with access set to **Anyone**. Copy the URL.
4. Open `index.html` and update the `DRIVE_WEBHOOK` constant with your URL.

---

## 🔐 Part 5 — User & Staff Roles (Access Controls)
The system supports two access modes:
1. **👑 Admin Mode:** Full operational control (adding/editing/deleting staff, marking salaries paid, marking attendance, viewing full financial/income analytics reports).
2. **👤 Staff Mode:** Limited interface (restricted to viewing their own profile, viewing their personal attendance history, submitting work expenses, checking inventory stock levels, printing their own salary slip, and checking assigned shipments).
