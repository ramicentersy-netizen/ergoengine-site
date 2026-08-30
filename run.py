import uvicorn

if __name__ == "__main__":
    print("=========================================================")
    print("Starting ErgoEngine - AI Affiliate Content Engine")
    print("Local Server: http://localhost:8000")
    print("Admin Intelligence Dashboard: http://localhost:8000/admin")
    print("=========================================================")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
