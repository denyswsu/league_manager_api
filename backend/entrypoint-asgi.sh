#! /bin/bash
exec daphne config.asgi:application -b 0.0.0.0 -p 9000