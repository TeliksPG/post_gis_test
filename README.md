# 🌎GEO API

## 👨🏻‍💻Features:
- CRUD operations for places
- Filtering by user and place name
- Finding the nearest objects
- Telegram bot for notifications of creating the new objects
- JWT token authentication
- Only registered users can create new objects

## 💻Technologies used:
- Django REST Framework
- PostgreSQL(with PostGIS extension)
- Docker

## 🐋Run with docker:

```shell
    git clone https://github.com/ProdyRodion/post_gis_test.git
    cd post_gis_test
    
    change .env.sample to .env and set your own values
    
    For notifications in telegram you should join group https://t.me/GeoGisBot_test
    
    docker-compose up --build
```

## ⚙️Run locally
```shell
    git clone https://github.com/ProdyRodion/post_gis_test.git
    cd post_gis_test
    OSGeo4W -> should be already installed
    
    # You should set the path to the GDAL and GEOS libraries in settings.py
    GDAL_LIBRARY_PATH = "C:/OSGeo4W/bin/gdal307.dll"
    GEOS_LIBRARY_PATH = "C:/OSGeo4W/bin/geos_c.dll"
    os.environ["PROJ_LIB"] = "C:/OSGeo4W/share/proj"
    
    For notifications in telegram you should join group https://t.me/GeoGisBot_test

    python -m venv venv
    source venv/bin/activate (Linux/MacOS)
    venv\Scripts\activate (on Windows)
    pip install -r requirements.txt
```




## 🧪Test coverage:
- Test for some custom logic