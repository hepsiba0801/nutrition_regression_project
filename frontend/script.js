// Frontend JS: send values to backend and update UI
const form = document.getElementById('predict-form');
const meterFill = document.getElementById('meter-fill');
const scoreNumber = document.getElementById('score-number');
const scoreLabel = document.getElementById('score-label');
const matchesEl = document.getElementById('matches');
const clearBtn = document.getElementById('clear');

const API_BASE = ''  // same origin; running from Flask server

function setLoading(state){
  if(state){
    scoreNumber.textContent = '...';
    scoreLabel.textContent = 'Predicting...';
    meterFill.style.width = '6%';
  }
}

function updateScoreUI(score, label){
  const pct = Math.round(score);
  meterFill.style.width = pct + '%';
  scoreNumber.textContent = score.toFixed(2);
  scoreLabel.textContent = label;
}

function renderMatches(matches){
  matchesEl.innerHTML = '';
  if(!matches || matches.length === 0){
    matchesEl.innerHTML = '<p class="muted">No matches found</p>';
    return;
  }
  matches.forEach((m, i) =>{
    const div = document.createElement('div');
    div.className = 'match';
    div.style.animationDelay = (i*120)+'ms';
    div.innerHTML = `
      <div class="title">${m['Dish Name']}</div>
      <div class="meta">Score: ${m.Nutritional_Score.toFixed(2)} · Calories: ${m['Calories (kcal)']} kcal</div>
    `;
    matchesEl.appendChild(div);
  })
}

async function predict(values){
  setLoading(true);
  try{
    const res = await fetch(API_BASE + '/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(values)
    });
    if(!res.ok){
      const text = await res.text();
      throw new Error(text || 'Server error');
    }
    const data = await res.json();
    updateScoreUI(data.score, data.category);
    renderMatches(data.matches);
  }catch(err){
    scoreNumber.textContent = '—';
    scoreLabel.textContent = 'Error';
    matchesEl.innerHTML = `<div class="match"><div class="title">Error</div><div class="meta">${err.message}</div></div>`;
    console.error(err);
  }
}

form.addEventListener('submit', (e)=>{
  e.preventDefault();
  const values = {
    calories: Number(document.getElementById('calories').value || 0),
    protein: Number(document.getElementById('protein').value || 0),
    carbs: Number(document.getElementById('carbs').value || 0),
    sugar: Number(document.getElementById('sugar').value || 0)
  };
  predict(values);
});

clearBtn.addEventListener('click', ()=>{
  form.reset();
  meterFill.style.width = '0%';
  scoreNumber.textContent = '—';
  scoreLabel.textContent = 'No prediction yet';
  matchesEl.innerHTML = '';
});

// small UX: auto-predict on load with default values
window.addEventListener('load', ()=>{
  const values = {
    calories: Number(document.getElementById('calories').value || 0),
    protein: Number(document.getElementById('protein').value || 0),
    carbs: Number(document.getElementById('carbs').value || 0),
    sugar: Number(document.getElementById('sugar').value || 0)
  };
  // don't auto-call if API likely not running; try-catch inside
  predict(values);
});