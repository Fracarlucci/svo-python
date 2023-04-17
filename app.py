import uvicorn
from config import app
from routers import northbound, southbound, SVO, vu_interface

app.include_router(southbound.router)
app.include_router(northbound.router)
app.include_router(SVO.router)
app.include_router(vu_interface.router)

if __name__ == '__main__':
    uvicorn.run(app)
