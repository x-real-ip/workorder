#!/bin/sh

uvicorn app_api:app --reload & python test.py