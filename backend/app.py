from fastapi import FastAPI
from database import Base, engine, SessionLocal
from models import Part


PART_LIFE = {
    "oleo": 1000,
    "Freio": 20000,
    "Óleo do Motor": 15000
}

app = FastAPI()
Base.metadata.create_all(engine)

@app.post("/update")
def update_part(moto: str, part_name: str, km: int, troca: bool = True):
    session = SessionLocal()

    part = session.query(Part).filter_by(moto=moto, part_name=part_name).first()

    life = PART_LIFE.get(part_name.lower(), 10000)

    if part:
        part.current_km = km
        part.life_km = life


        # Se houve troca, registra nova troca
        if troca:
            part.last_change_km = km

    else:
        # Primeiro cadastro da peça
        part = Part(
            moto=moto,
            part_name=part_name,
            last_change_km=km,
            current_km=km,
            life_km=life
        )
        session.add(part)

    session.commit()

    used = part.current_km - part.last_change_km
    remaining = part.life_km - used

    percent = (remaining / part.life_km) * 100

    if percent <= 10:
        alert = "🔴 Trocar agora"
    elif percent <= 30:
        alert = "🟡 Atenção"
    else:
        alert = "🟢 OK"

    session.close()

    return {
        "part": part.part_name,
        "last_change": part.last_change_km,
        "current_km": part.current_km,
        "next_change": part.last_change_km + part.life_km,
        "remaining_km": remaining,
        "status": alert
    }
