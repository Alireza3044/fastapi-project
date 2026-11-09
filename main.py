from fastapi import FastAPI
import database, models, routers

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(routers.user_router)
app.include_router(routers.todo_router)
app.include_router(routers.admin_router)
