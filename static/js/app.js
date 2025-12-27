// DOM Elements
const domainInput = document.getElementById('domain');
const levelButtons = document.querySelectorAll('.level-btn');
const generateBtn = document.getElementById('generateBtn');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');
const resultsSection = document.getElementById('resultsSection');
const tabButtons = document.querySelectorAll('.tab-btn');
const treeTab = document.getElementById('treeTab');
const diagramTab = document.getElementById('diagramTab');
const jsonTab = document.getElementById('jsonTab');
const treeView = document.getElementById('treeView');
const mermaidDiagram = document.getElementById('mermaidDiagram');
const jsonView = document.getElementById('jsonView');
const roadmapTitle = document.getElementById('roadmapTitle');
const roadmapLevel = document.getElementById('roadmapLevel');
const totalWeeks = document.getElementById('totalWeeks');
const downloadBtn = document.getElementById('downloadBtn');
const copyBtn = document.getElementById('copyBtn');
const newRoadmapBtn = document.getElementById('newRoadmapBtn');

// State
let selectedLevel = 'Beginner';
let currentRoadmap = null;

// Initialize Mermaid
mermaid.initialize({
    startOnLoad: false,
    theme: 'dark',
    securityLevel: 'loose',
    flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
    }
});

// Event Listeners
levelButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        levelButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedLevel = btn.dataset.level;
    });
});

generateBtn.addEventListener('click', generateRoadmap);
retryBtn.addEventListener('click', generateRoadmap);
newRoadmapBtn.addEventListener('click', resetToInput);
downloadBtn.addEventListener('click', downloadRoadmap);
copyBtn.addEventListener('click', copyToClipboard);

domainInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        generateRoadmap();
    }
});

tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        switchTab(tab);
    });
});

// Functions
async function generateRoadmap() {
    const domain = domainInput.value.trim();
    
    if (!domain) {
        showError('Please enter an engineering domain');
        domainInput.focus();
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                domain: domain,
                level: selectedLevel
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate roadmap');
        }
        
        currentRoadmap = data.roadmap;
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    }
}

function showLoading() {
    document.querySelector('.input-section').classList.add('hidden');
    errorSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
}

function showError(message) {
    loadingSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    document.querySelector('.input-section').classList.remove('hidden');
    errorSection.classList.remove('hidden');
    errorMessage.textContent = message;
}

function displayResults(data) {
    loadingSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    document.querySelector('.input-section').classList.remove('hidden');
    resultsSection.classList.remove('hidden');
    
    // Set header
    roadmapTitle.textContent = `🧭 ${data.roadmap.domain} Roadmap`;
    roadmapLevel.textContent = data.roadmap.level;
    totalWeeks.textContent = `${data.roadmap.total_weeks || 16} Weeks`;
    
    // Render tree view
    renderTreeView(data.roadmap);
    
    // Render JSON view
    jsonView.textContent = JSON.stringify(data.roadmap, null, 2);
    
    // Render Mermaid diagram
    renderMermaidDiagram(data.mermaid);
    
    // Switch to tree tab
    switchTab('tree');
}

function renderTreeView(roadmap) {
    let html = '';
    const phases = roadmap.phases || [];
    
    phases.forEach((phase, phaseIdx) => {
        html += `
            <div class="phase-card">
                <div class="phase-header">
                    <span class="phase-weeks">📅 ${phase.weeks}</span>
                    <span class="phase-name">${phase.name}</span>
                    ${phase.description ? `<span class="phase-description">${phase.description}</span>` : ''}
                </div>
                <div class="phase-content">
        `;
        
        const topics = phase.topics || [];
        topics.forEach((topic, topicIdx) => {
            const topicId = `topic-${phaseIdx}-${topicIdx}`;
            html += `
                <div class="topic-card">
                    <div class="topic-header" onclick="toggleTopic('${topicId}')">
                        <span class="topic-icon">📚</span>
                        <span class="topic-name">${topic.name}</span>
                        <button class="topic-toggle" id="toggle-${topicId}">▼</button>
                    </div>
                    <div class="topic-content" id="${topicId}">
            `;
            
            const subtopics = topic.subtopics || [];
            subtopics.forEach((subtopic) => {
                html += `
                    <div class="subtopic-card">
                        <div class="subtopic-name">${subtopic.name}</div>
                        <div class="items-list">
                `;
                
                const items = subtopic.items || [];
                items.forEach((item) => {
                    html += `<span class="item-tag">${item}</span>`;
                });
                
                html += `
                        </div>
                    </div>
                `;
            });
            
            html += `
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
        
        // Add flow arrow between phases (except last)
        if (phaseIdx < phases.length - 1) {
            html += `<div class="flow-arrow">⬇️</div>`;
        }
    });
    
    treeView.innerHTML = html;
}

// Toggle topic visibility
function toggleTopic(topicId) {
    const content = document.getElementById(topicId);
    const toggle = document.getElementById(`toggle-${topicId}`);
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        toggle.classList.remove('collapsed');
    } else {
        content.style.display = 'none';
        toggle.classList.add('collapsed');
    }
}

async function renderMermaidDiagram(mermaidCode) {
    // Extract just the mermaid code without the markdown wrapper
    let code = mermaidCode
        .replace(/```mermaid\n?/g, '')
        .replace(/```\n?/g, '')
        .trim();
    
    try {
        mermaidDiagram.innerHTML = '';
        const { svg } = await mermaid.render('mermaid-svg', code);
        mermaidDiagram.innerHTML = svg;
    } catch (error) {
        console.error('Mermaid render error:', error);
        mermaidDiagram.innerHTML = `<pre style="color: #ef4444;">Failed to render diagram</pre>`;
    }
}

function switchTab(tab) {
    tabButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    
    treeTab.classList.toggle('active', tab === 'tree');
    treeTab.classList.toggle('hidden', tab !== 'tree');
    diagramTab.classList.toggle('active', tab === 'diagram');
    diagramTab.classList.toggle('hidden', tab !== 'diagram');
    jsonTab.classList.toggle('active', tab === 'json');
    jsonTab.classList.toggle('hidden', tab !== 'json');
}

function resetToInput() {
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
    document.querySelector('.input-section').classList.remove('hidden');
    domainInput.value = '';
    domainInput.focus();
}

function downloadRoadmap() {
    if (!currentRoadmap) return;
    
    const blob = new Blob([JSON.stringify(currentRoadmap, null, 2)], {
        type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentRoadmap.domain.toLowerCase().replace(/\s+/g, '_')}_roadmap.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Show feedback
    showButtonFeedback(downloadBtn, '✅ Downloaded!');
}

async function copyToClipboard() {
    if (!currentRoadmap) return;
    
    try {
        await navigator.clipboard.writeText(JSON.stringify(currentRoadmap, null, 2));
        showButtonFeedback(copyBtn, '✅ Copied!');
    } catch (error) {
        showButtonFeedback(copyBtn, '❌ Failed');
    }
}

function showButtonFeedback(btn, text) {
    const originalText = btn.innerHTML;
    btn.innerHTML = text;
    setTimeout(() => {
        btn.innerHTML = originalText;
    }, 2000);
}

// Check API health on load
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('API Status:', data);
    } catch (error) {
        console.warn('API may not be running:', error);
    }
}

checkHealth();
