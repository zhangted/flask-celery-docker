# Flask + Celery + Flower docker template
Quick start template for a dockerized flask api + celery bg jobs + bg job monitoring

## Start the app
```bash
  docker-compose up
```

## Run tests
```bash
  docker-compose run pytest
```

## Routes
- 127.0.0.1:5000 => flask server
- 127.0.0.1:5555 => flower (bg job monitor)
- 127.0.0.1:5000/queue_task => queue dummy job