Frontend for Indian Food Nutrition Predictor

Overview
========
A modern, animated static frontend that communicates with a small Flask API server to obtain predictions and similar-dish matches.

Files
-----
- `index.html` — main UI
- `styles.css` — styles and animations
- `script.js` — frontend logic (fetch to /api/predict)

Quick start (local)
-------------------
1. Ensure the model & scaler are created by running training: `python main.py` (this will generate `linear_regression_model.joblib` and `scaler.joblib`).
2. Start the API server (project root):

   ```pwsh
   python server.py
   ```

   Server listens on http://127.0.0.1:5000

3. Serve the `frontend` folder (any static server). Example using Python's simple HTTP server from the project `frontend` folder:

   ```pwsh
   cd nutrition_regression_project\frontend
   python -m http.server 8000
   ```

   Then open http://127.0.0.1:8000 in your browser. The frontend will call the API at `/api/predict` on the server host — if you host static files and API on different origins, enable CORS or set `API_BASE` in `script.js`.

Deployment notes
----------------
- For production, serve the static frontend from the same domain as the Flask API and set `API_BASE` accordingly.
- The Flask server is minimal; consider running behind Gunicorn / uWSGI for production.

If you want, I can also add a small `docker-compose.yml` to run API + static frontend together.