from fastapi import FastAPI, HTTPException, Depends
from app.menuItem import MenuItem
from .schemas import CreateItemRequest
from sqlalchemy.orm import Session
from .database import get_db
from .models import Item

menu_items: list[MenuItem] = [
    MenuItem(0, 'First dish', 'First desc', 200),
    MenuItem(1, 'Second dish', 'Second desc', 250),
    MenuItem(2, 'Third dish', 'Third desc', 150),
    MenuItem(3, 'Forth dish', 'Forth desc', 100)
]

app = FastAPI()

# Jaeger
###########

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

resource = Resource(attributes={
    SERVICE_NAME: "menu-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

###########

# Prometheus
###########

from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

###########


@app.get("/v1/menu_items")
def get_all(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    products = db.query(Item).offset(skip).limit(limit).all()
    return products

# @app.get("/v1/menu_items/{id}")
# async def get_menu_item_by_id(id: int):
#     result = [item for item in menu_items if item.id == id]
#     if len(result) > 0:
#         return result[0]
#     raise HTTPException(status_code=404, detail="Menu item not found")

@app.post("/v1/menu_items")
def create(details: CreateItemRequest, db: Session = Depends(get_db)):
    to_create = Item(
        name = details.name,
        description = details.description,
        price = details.price
    )
    db.add(to_create)
    db.commit()
    return{
        "success": True,
        "created_id": to_create.id
    }
@app.get("/v1/menu_items/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Item).filter(Item.id == id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return result

@app.delete("/v1/menu_items/delete/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    db.query(Item).filter(Item.id == id).delete()
    db.commit()
    return {"success": True}

@app.get("/__health")
async def check_service():
    return 