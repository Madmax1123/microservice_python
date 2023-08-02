from fastapi import FastAPI


app = FastAPI()
@app.get('/route')
def route():
    return True