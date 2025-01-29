# the run.py file will run the entire app when the code is ran
from app import createapp

app = createapp()

# driver script
if __name__ == "__main__":
    app.run(debug=True)