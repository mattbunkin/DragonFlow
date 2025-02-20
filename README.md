# 🐲 DragonFlow - CI102

## 🚀 Getting started
To make it easy for you to get started with GitLab, here's a list of recommended next steps.


## Add Your Files
```bash
cd existing_repo
git add . 
git commit -m "send message"

# if there are unsaved changes from other members commits..
git pull origin main
git push origin main
```

## 📌 Project Information
### 📝 Description
DragonFlow is a comprehensive student success planner designed specifically for Drexel University students. It helps optimize academic planning by providing personalized course recommendations, schedule planning, and success metrics based on individual student needs.

## ✨ Key Features

🎓 **Smart Course Planning**
- Personalized course recommendations
- Major requirement tracking
- CO-OP period integration
- Schedule conflict detection

📊 **Success Metrics**
- Course success prediction
- GPA projections
- Workload analysis
- Term balance optimization

👩‍🏫 **Professor Insights**
- Rating integration
- Teaching style information
- Historical grade distributions

### 🛠️ Tech Stack
- 🐍 Backend: Python Flask
- 💾 Database: SQLAlchemy ORM
- 🔐 Authentication: Flask-Login
- ✅ Schema Validation: Marshmallow
- 💻 Frontend: Svelte5, TypeScript, MeltUI
- 


## 💻 Installation
1. Clone the repository
```bash
git clone https://gitlab.cci.drexel.edu/cid/2425/ws1023/60/12/drgaonflow-ci102.git
```

2. Set up virtual environment (might differ if on Windows)
```bash
# Instructions for virtual environment setup
    cd dragonflow-ci102/backend
    source venv/bin/activate
    pip install -r requirements.txt

# Change Python interpreter for VSCODE (MacOS)
    which python3 # copy output  
    # CMD + SHIFT + P
    # select-interpreter -> enter interpreter path
    # copy and paste to interpreter path

# Change Python interpreter for VSCODE (Windows)
    where python3 # copy output   
    # CTRL + SHIFT + P
    # select-interpreter -> enter interpreter path
    # copy and paste to interpreter path
```

3. Install Front-End dependencies (MUST HAVE NPM INSTALLED)
```bash
    cd [your-git-lab-repo]
    # Navigate to svelte-kit to install dependencies 
    cd .svelte-kit
    npm install

    # once all dependencies are all installed; start dev server
    npm run dev
    
# Instructions for dependency installation
```

3.5 Before pulling big changes:
    1. Make sure you have Node.js v18+ installed
    2. After pulling (make sure your inside repo directory), run:
```bash
    npm install 

    # 3. If you see any TypeScript errors about missing types, run:
    npm install -D @types/node @types/cookie @types/estree @types/json-schema @types/prop-types

    # 4. If you're having trouble with component imports run
    npx svelte-kit sync

    # 5. Finally development server should work
    npm run dev
```
## 👥 Contributing
This project is part of CI102. Contributors:
Matt Bunkin, Soumil Patel, Rikhil Amonkar, Andrey Barriga

---
*Note: This project is part of the CI102 course at Drexel University CCI and not officially affiliated with Drexel.*