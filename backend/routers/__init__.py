from routers.auth import router as auth_router
from routers.progression import router as progression_router
from routers.sequence import router as sequence_router
from routers.session import router as session_router
from routers.resource import router as resource_router # Importez resource_router
from routers.objective import router as objective_router # Importez objective_router

# Importez d'autres routeurs ici si nécessaire
# from routers.autre import router as autre_router

__all__ = ["auth_router", "progression_router", "sequence_router", "session_router", "resource_router", "objective_router"] # Ajoutez objective_router
