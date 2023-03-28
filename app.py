from fastapi import FastAPI
import uvicorn
from config import app, db
from routers import northbound, southbound, SVO, vu_interface

#@app.route('/', methods=['GET', 'POST'])
#def db():
    #db.create_all()
    #db.session.commit()
    #return"ok"
#flask run -h localhost -p 3000

app.include_router(southbound.router)
app.include_router(northbound.router)
app.include_router(SVO.router)
app.include_router(vu_interface.router)

if __name__ == '__main__':
    uvicorn.run(app)

