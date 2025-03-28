#!/bin/bash

# Proje kök dizinini oluştur
mkdir -p task-tracker/src/{controllers,services,repositories,models,routes}
mkdir -p task-tracker/tests
mkdir -p task-tracker/docs

# Ana dosyaları oluştur
touch task-tracker/app.py
touch task-tracker/config.py
touch task-tracker/requirements.txt
touch task-tracker/score.json

# __init__.py dosyaları
touch task-tracker/src/__init__.py
touch task-tracker/src/controllers/__init__.py
touch task-tracker/src/services/__init__.py
touch task-tracker/src/repositories/__init__.py
touch task-tracker/src/models/__init__.py
touch task-tracker/src/routes/__init__.py

# Controllers
touch task-tracker/src/controllers/task_controller.py
touch task-tracker/src/controllers/user_controller.py
touch task-tracker/src/controllers/admin_controller.py

# Services
touch task-tracker/src/services/google_sheet_service.py
touch task-tracker/src/services/task_service.py
touch task-tracker/src/services/user_service.py
touch task-tracker/src/services/scoring_service.py
touch task-tracker/src/services/auth_service.py

# Repositories
touch task-tracker/src/repositories/task_repository.py
touch task-tracker/src/repositories/user_repository.py
touch task-tracker/src/repositories/scoring_repository.py

# Models
touch task-tracker/src/models/task_model.py
touch task-tracker/src/models/user_model.py
touch task-tracker/src/models/scoring_model.py

# Routes
touch task-tracker/src/routes/task_routes.py
touch task-tracker/src/routes/user_routes.py
touch task-tracker/src/routes/admin_routes.py

# Tests
touch task-tracker/tests/test_task_service.py
touch task-tracker/tests/test_user_service.py
touch task-tracker/tests/test_scoring_service.py

# Docs
touch task-tracker/docs/README.md

echo "✅ Proje klasör yapısı başarıyla oluşturuldu!"
