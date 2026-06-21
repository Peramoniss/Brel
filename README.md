# Brel
Brel is an automatic song translation system. It is distributed as a terminal app, an API, and a webpage. The name references Jacques Brel, who inspired the development of this app.

## 📁 Project Structure
The project is split into:
- a **static front-end** (GitHub Pages)
- a **Python API** (Render)

The folder structure of the source project is as follows:

```
Brel/
│
├── api/ # Python API
│ ├── src/
│ │ ├── app.py # FastAPI application
│ └──── test.py # Quick test script
│ 
├── script/ # Terminal version
│ ├── html/ # Store HTMLs generated
│ ├── originals/ # Stores txt files with song lyrics
│ └── local.py # The terminal app
│
├── index.html # Web app
├── requirements.txt
└── README.md
```
---

## Architecture Overview
This project uses a **static architecture**. All heavy processing is done remotely.

This allows:
- modularization
- simple maintanence
- minimal server costs
- simple deployment

---

## API Version

- Built with **FastAPI library**
- Deployed on [Render](https://opearatic.onrender.com)

### Endpoints

- POST /translate/

More detailed information on the api on https://opearatic.onrender.com/docs.

### 🔐 CORS

The API only allows requests from:

`https://peramoniss.github.io`


This prevents unauthorized usage while keeping the frontend functional. For that to work, the Render environment has the variable `ENV: PROD`. Changing to `DEV` allows requests from localhosts.  

## Web app Version
- built upon the api
- user-friendly
- allows the user to interactively change the lyrics
- no file or terminal dependencies

## Script Version
The script version is terminal-based and was developed to make an easily modifiable script so that you can massively generate translated versions of songs. It has a txt file as input and outputs an HTML to visualize the translation. It uses terminal arguments that allow to configure several details of the HTML. To learn what you can do with it, run:

```
cd script
python local.py --help
```

## 🚀 Deployment

### Frontend
- GitHub Pages

### Backend
- Render (Free Tier)
- Auto-deploy on new commits
- Hosted in Virginia (USA)
- API start command is:
```
cd api
uvicorn src.app:app --host 127.0.0.1 --port 8000
``` 

The API may take around 50 seconds to wake up after inactivity.

## 🤝 Contribute or Fork
To make contribute, you must:
- Fork the repository
- [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the forked repository to your local machine 
- Set the [remote](https://docs.github.com/en/get-started/git-basics/managing-remote-repositories) in your development environment
- Program your changes
- [Stage](https://www.w3schools.com/git/git_staging_environment.asp?remote=github) and [commit](https://www.w3schools.com/git/git_commit.asp?remote=github) them
- [Push](https://www.w3schools.com/git/git_push_to_remote.asp?remote=github) the changes to the GitHub repository

If this is your own version, you will already have it up and running after GitHub pages is deployed!

If you want to contribute, GitHub will show you a button suggesting a Pull Request. Click it and I'll analyze the contribution!

### Test the app
While developing, you can run the API locally for testing using:
```
cd api
uvicorn src.app:app --reload
```
After that, use "Run Live" extension or any other local webserver application to open a local server containing the index.html.

You can also test the api by simply running:
```
cd api
python test.py
```

Or test the script version by using:
```
cd script
python local.py "originals/Mathilde - Jacques Brel.txt" --lang=en
```
---

## 📄 License

Personal project.

---

## 🗂️ Assets
[Logo icon](https://pngtree.com/freepng/globe-with-headset-icon-isolated_5261087.html)