
Authentication Microservice
1. Build out authentication flow 
2. Get server to a healthy state
3. begin being able to handle simple requests
4. deploy the server


commands
1. Deactive env - deactivate
2. activate env - source venv/bin/activate
3. run server : uvicorn main:app --reload
4. python -m uvicorn main:app --reload # the only way it works


Useful routes
1. Docs route: http://127.0.0.1:8000/docs


---- controller return format ---- 
return (True, "Success message", data)   # happy path
return (False, "Error message", None)    # failure path

---- Router return format ---- 
ok, msg, data = controller_function(...)
if not ok:
    raise HTTPException(status_code=400, detail=msg)
return {"message": msg, "data": data}