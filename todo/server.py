from fastapi import FastAPI


server = FastAPI(debug=True)

from todo import api