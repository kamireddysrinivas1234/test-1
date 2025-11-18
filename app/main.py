from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .database import Base, engine
from .routers import calculations

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Calculation API")

CALC_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>FastAPI Calculator</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
    label { display: block; margin-top: 10px; }
    input, select, button { padding: 8px; margin-top: 5px; width: 100%; box-sizing: border-box; }
    button { margin-top: 15px; cursor: pointer; }
    #result-box { margin-top: 20px; padding: 10px; border-radius: 6px; background-color: #f4f4f4; }
    .error { color: #b00020; }
  </style>
</head>
<body>
  <h1>FastAPI Calculation UI</h1>
  <p>Enter two numbers and select an operation. This page calls the <code>/calculations/</code> API behind the scenes.</p>

  <label for="a">First number (a):</label>
  <input type="number" id="a" step="any" />

  <label for="b">Second number (b):</label>
  <input type="number" id="b" step="any" />

  <label for="type">Operation:</label>
  <select id="type">
    <option value="add">Add</option>
    <option value="sub">Subtract</option>
    <option value="mul">Multiply</option>
    <option value="div">Divide</option>
  </select>

  <button id="calc-btn">Calculate</button>

  <div id="result-box">
    <strong>Result:</strong> <span id="result-value">N/A</span>
    <div id="error" class="error"></div>
  </div>

  <p>API docs are available at <a href="/docs" target="_blank">/docs</a>.</p>

  <script>
    document.getElementById('calc-btn').addEventListener('click', async () => {
      const aValue = document.getElementById('a').value;
      const bValue = document.getElementById('b').value;
      const typeValue = document.getElementById('type').value;
      const resultSpan = document.getElementById('result-value');
      const errorDiv = document.getElementById('error');

      errorDiv.textContent = '';
      resultSpan.textContent = '...';

      if (aValue === '' || bValue === '') {
        errorDiv.textContent = 'Please fill in both numbers.';
        resultSpan.textContent = 'N/A';
        return;
      }

      try {
        const payload = { type: typeValue, a: parseFloat(aValue), b: parseFloat(bValue) };
        const response = await fetch('/calculations/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          const errData = await response.json().catch(() => ({}));
          errorDiv.textContent = errData.detail || 'Error performing calculation.';
          resultSpan.textContent = 'N/A';
          return;
        }

        const data = await response.json();
        resultSpan.textContent = data.result;
      } catch (err) {
        console.error(err);
        errorDiv.textContent = 'Network or server error.';
        resultSpan.textContent = 'N/A';
      }
    });
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def root_calc_page():
    return CALC_HTML

@app.get("/calc", response_class=HTMLResponse)
def calc_alias():
    return CALC_HTML

app.include_router(calculations.router)
