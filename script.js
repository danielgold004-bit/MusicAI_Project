const API_BASE_URL = "http://127.0.0.1:8000/api";

console.log("🚀 AI Music Studio - Connected to Backend");

// TABS
function switchTab(tab) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  
  document.querySelector(`button[onclick="switchTab('${tab}')"]`).classList.add('active');
  document.getElementById(tab + '-section').classList.add('active');
}

// Copy Text
function copyText(id) {
  const text = document.getElementById(id).innerText || document.getElementById(id).textContent;
  navigator.clipboard.writeText(text).then(() => alert('✅ Copied!'));
}

function toggleDarkMode() {
  document.body.classList.toggle('dark');
}

// Generate Beat Blueprint
async function generateMusic() {
  const btn = document.getElementById('music-btn');
  const errEl = document.getElementById('music-error');
  const output = document.getElementById('music-output');
  const result = document.getElementById('music-result');

  errEl.textContent = '';
  output.style.display = 'block';
  result.innerHTML = `<div class="loader"></div><p>Generating beat blueprint...</p>`;

  btn.disabled = true;
  btn.textContent = 'Generating...';

  try {
    const response = await fetch(`${API_BASE_URL}/music/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        genre: document.getElementById('genre').value,
        mood: document.getElementById('mood').value,
        tempo: document.getElementById('tempo').value,
        notes: document.getElementById('music-notes').value.trim()
      })
    });

    const data = await response.json();
    result.textContent = data.blueprint;
  } catch (error) {
    errEl.textContent = '⚠️ ' + error.message;
    output.style.display = 'none';
  } finally {
    btn.disabled = false;
    btn.textContent = '▶ Generate Beat Blueprint';
  }
}

// Generate Lyrics
async function generateLyrics() {
  const btn = document.getElementById('lyrics-btn');
  const errEl = document.getElementById('lyrics-error');
  const output = document.getElementById('lyrics-output');
  const result = document.getElementById('lyrics-result');

  errEl.textContent = '';
  output.style.display = 'block';
  result.innerHTML = `<div class="loader"></div><p>Generating lyrics with Groq...</p>`;

  btn.disabled = true;
  btn.textContent = 'Writing...';

  try {
    const response = await fetch(`${API_BASE_URL}/lyrics/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic: document.getElementById('lyric-topic').value.trim() || "success and hustle",
        genre: document.getElementById('genre-lyrics').value,
        flow_style: document.getElementById('flow-style').value,
        structure: document.getElementById('structure').value
      })
    });

    const data = await response.json();
    
    let formatted = data.lyrics.replace(/\[(Verse|Chorus|Bridge|Pre-Chorus|Outro|Intro).*?\]/gi, 
      match => `<strong style="color:#6c63ff;">${match}</strong>`);
    
    result.innerHTML = formatted.replace(/\n/g, '<br>');
  } catch (error) {
    errEl.textContent = '⚠️ ' + error.message;
    output.style.display = 'none';
  } finally {
    btn.disabled = false;
    btn.textContent = '✍️ Generate Lyrics';
  }
}
// ====================== GENERATE LYRICS FROM UPLOADED BEAT ======================
async function generateFromBeat() {
  const fileInput = document.getElementById('beat-upload');
  if (!fileInput.files.length) {
    document.getElementById('upload-error').textContent = '⚠️ Please select a beat file!';
    return;
  }

  const genre = document.getElementById('upload-genre').value;
  const flowStyle = document.getElementById('upload-flow').value;
  const notes = document.getElementById('upload-notes').value.trim();

  const btn = document.getElementById('upload-btn');
  const output = document.getElementById('upload-output');
  const result = document.getElementById('upload-result');
  const errEl = document.getElementById('upload-error');

  errEl.textContent = '';
  output.style.display = 'block';
  result.innerHTML = `<div class="loader"></div><p>Processing beat...</p>`;

  btn.disabled = true;
  btn.textContent = 'Generating...';

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('genre', genre);
  formData.append('flow_style', flowStyle);
  formData.append('notes', notes);

  try {
    const response = await fetch(`${API_BASE_URL}/lyrics/from-beat`, {   // ← Make sure this is correct
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (data.error) throw new Error(data.error);

    let formatted = data.lyrics.replace(/\[(Verse|Chorus|Bridge|Pre-Chorus|Outro|Intro).*?\]/gi, 
      match => `<strong style="color:#6c63ff;">${match}</strong>`);
    
    result.innerHTML = formatted.replace(/\n/g, '<br>');
  } catch (error) {
    errEl.textContent = '⚠️ ' + error.message;
    output.style.display = 'none';
  } finally {
    btn.disabled = false;
    btn.textContent = '🎤 Generate Lyrics for this Beat';
  }
}