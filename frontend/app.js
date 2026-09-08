/**
 * Semantic Group Chat Search - Frontend Client
 * Communicates with FastAPI backend for dense vector search, context expansion,
 * participant attribution, and temporal filtering.
 */

(function () {
  'use strict';

  // Determine API base URL (works seamlessly when served by FastAPI or standalone)
  const API_BASE = window.location.origin.startsWith('http') ? '' : 'http://127.0.0.1:8000';

  // DOM Elements
  const searchForm = document.getElementById('searchForm');
  const searchInput = document.getElementById('searchInput');
  const clearBtn = document.getElementById('clearBtn');
  const searchSubmitBtn = document.getElementById('searchSubmitBtn');
  const btnSpinner = searchSubmitBtn.querySelector('.btn-spinner');
  const btnText = searchSubmitBtn.querySelector('.btn-text');

  // Filter Elements
  const filterToggleBtn = document.getElementById('filterToggleBtn');
  const filterPanel = document.getElementById('filterPanel');
  const filterActiveBadge = document.getElementById('filterActiveBadge');
  const senderFilter = document.getElementById('senderFilter');
  const dateFromFilter = document.getElementById('dateFromFilter');
  const dateToFilter = document.getElementById('dateToFilter');
  const topKFilter = document.getElementById('topKFilter');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');
  const applyFiltersBtn = document.getElementById('applyFiltersBtn');

  // Meta Section Elements
  const queryMetaSection = document.getElementById('queryMetaSection');
  const metaQueryText = document.getElementById('metaQueryText');
  const metaResultsCount = document.getElementById('metaResultsCount');
  const metaLatency = document.getElementById('metaLatency');
  const parsedFiltersBar = document.getElementById('parsedFiltersBar');

  // States & Results Elements
  const welcomeState = document.getElementById('welcomeState');
  const loadingState = document.getElementById('loadingState');
  const emptyState = document.getElementById('emptyState');
  const errorState = document.getElementById('errorState');
  const errorMessage = document.getElementById('errorMessage');
  const retryBtn = document.getElementById('retryBtn');
  const resultsList = document.getElementById('resultsList');

  // Health Elements
  const healthDot = document.getElementById('healthDot');
  const healthStatus = document.getElementById('healthStatus');
  const statMessages = document.getElementById('statMessages');
  const statModel = document.getElementById('statModel');
  const statDateRange = document.getElementById('statDateRange');

  // Query chips
  const queryChips = document.querySelectorAll('.query-chip');

  // Participant color palette
  const PARTICIPANT_COLORS = {
    'Rahul Sharma': '#3b82f6',
    'Priya Patel': '#ec4899',
    'Aman Verma': '#10b981',
    'Sneha Reddy': '#f59e0b',
    'Vikram Malhotra': '#8b5cf6',
    'Neha Gupta': '#06b6d4',
    'Rohan Mehta': '#14b8a6',
    'Ananya Iyer': '#f97316',
    'Kabir Das': '#6366f1'
  };

  const DEFAULT_AVATAR_COLOR = '#64748b';

  // =========================================================================
  // Initialize Application
  // =========================================================================

  document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    bindEvents();
  });

  function bindEvents() {
    // Search form submission
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      executeSearch();
    });

    // Clear input button
    searchInput.addEventListener('input', () => {
      clearBtn.classList.toggle('visible', searchInput.value.length > 0);
    });

    clearBtn.addEventListener('click', () => {
      searchInput.value = '';
      clearBtn.classList.remove('visible');
      searchInput.focus();
    });

    // Demo query chips
    queryChips.forEach((chip) => {
      chip.addEventListener('click', () => {
        const query = chip.getAttribute('data-query');
        if (query) {
          searchInput.value = query;
          clearBtn.classList.add('visible');
          executeSearch();
        }
      });
    });

    // Filter toggle
    filterToggleBtn.addEventListener('click', () => {
      const isExpanded = filterToggleBtn.getAttribute('aria-expanded') === 'true';
      filterToggleBtn.setAttribute('aria-expanded', (!isExpanded).toString());
      filterPanel.classList.toggle('collapsed', isExpanded);
    });

    // Filter changes - update badge
    [senderFilter, dateFromFilter, dateToFilter, topKFilter].forEach((el) => {
      el.addEventListener('change', updateActiveFilterBadge);
    });

    // Reset filters
    resetFiltersBtn.addEventListener('click', () => {
      senderFilter.value = '';
      dateFromFilter.value = '';
      dateToFilter.value = '';
      topKFilter.value = '10';
      updateActiveFilterBadge();
    });

    // Apply & Search
    applyFiltersBtn.addEventListener('click', () => {
      executeSearch();
    });

    // Retry button in error state
    retryBtn.addEventListener('click', () => {
      executeSearch();
    });
  }

  // =========================================================================
  // System Health
  // =========================================================================

  async function checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/health`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      healthDot.className = 'status-dot status-online';
      healthStatus.textContent = 'System Online';

      if (data.indexed_messages) {
        statMessages.querySelector('.stat-value').textContent = data.indexed_messages.toLocaleString();
      }
      if (data.model) {
        // Shorten model name if long
        const shortModel = data.model.replace('paraphrase-multilingual-', '').replace('-v2', '');
        statModel.querySelector('.stat-value').textContent = shortModel;
        statModel.title = data.model;
      }
      if (data.data_date_range) {
        statDateRange.querySelector('.stat-value').textContent = data.data_date_range;
      }
    } catch (err) {
      console.warn('Health check failed:', err);
      healthDot.className = 'status-dot status-error';
      healthStatus.textContent = 'Backend Offline';
    }
  }

  // =========================================================================
  // Search Execution
  // =========================================================================

  async function executeSearch() {
    const rawQuery = searchInput.value.trim();
    if (!rawQuery) {
      searchInput.focus();
      return;
    }

    // Build payload
    const payload = {
      query: rawQuery,
      top_k: parseInt(topKFilter.value, 10) || 10
    };

    if (senderFilter.value) {
      payload.sender = senderFilter.value;
    }
    if (dateFromFilter.value) {
      payload.date_from = dateFromFilter.value;
    }
    if (dateToFilter.value) {
      payload.date_to = dateToFilter.value;
    }

    // Switch UI to loading state
    setLoading(true);
    const startTime = performance.now();

    try {
      const res = await fetch(`${API_BASE}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const latencyMs = Math.round(performance.now() - startTime);

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server returned HTTP ${res.status}`);
      }

      const data = await res.json();
      displayResults(data, latencyMs);
    } catch (err) {
      console.error('Search request failed:', err);
      displayError(err.message || 'An unexpected error occurred while searching.');
    } finally {
      setLoading(false);
    }
  }

  // =========================================================================
  // UI State Rendering
  // =========================================================================

  function setLoading(isLoading) {
    if (isLoading) {
      welcomeState.classList.add('hidden');
      emptyState.classList.add('hidden');
      errorState.classList.add('hidden');
      resultsList.innerHTML = '';
      loadingState.classList.remove('hidden');

      searchSubmitBtn.disabled = true;
      btnSpinner.classList.remove('hidden');
      btnText.textContent = 'Searching...';
    } else {
      loadingState.classList.add('hidden');
      searchSubmitBtn.disabled = false;
      btnSpinner.classList.add('hidden');
      btnText.textContent = 'Search';
    }
  }

  function displayError(msg) {
    welcomeState.classList.add('hidden');
    resultsList.innerHTML = '';
    queryMetaSection.classList.add('hidden');
    errorMessage.textContent = msg;
    errorState.classList.remove('hidden');
  }

  function displayResults(data, latencyMs) {
    welcomeState.classList.add('hidden');
    errorState.classList.add('hidden');

    const results = data.results || [];

    // Render Query Meta Bar
    queryMetaSection.classList.remove('hidden');
    metaQueryText.textContent = `"${data.query}"`;
    metaResultsCount.textContent = `${results.length} result${results.length === 1 ? '' : 's'}`;
    metaLatency.textContent = `• ${latencyMs} ms`;

    renderParsedFilterBadges(data.parsed_filters);

    if (results.length === 0) {
      emptyState.classList.remove('hidden');
      resultsList.innerHTML = '';
      return;
    }

    emptyState.classList.add('hidden');
    resultsList.innerHTML = '';

    results.forEach((item, index) => {
      const card = createResultCard(item, index + 1);
      resultsList.appendChild(card);
    });
  }

  function renderParsedFilterBadges(parsed) {
    parsedFiltersBar.innerHTML = '';
    if (!parsed) return;

    let hasBadge = false;

    if (parsed.detected_sender) {
      hasBadge = true;
      const badge = document.createElement('span');
      badge.className = 'filter-badge badge-highlight';
      badge.innerHTML = `👤 Sender Detected: <strong>${escapeHtml(parsed.detected_sender)}</strong> ${parsed.is_strict_sender ? '(Strict)' : '(Boosted)'}`;
      parsedFiltersBar.appendChild(badge);
    }

    if (parsed.date_label) {
      hasBadge = true;
      const badge = document.createElement('span');
      badge.className = 'filter-badge badge-highlight';
      badge.innerHTML = `📅 Timeframe Detected: <strong>${escapeHtml(parsed.date_label)}</strong>`;
      parsedFiltersBar.appendChild(badge);
    } else if (parsed.date_from || parsed.date_to) {
      hasBadge = true;
      const badge = document.createElement('span');
      badge.className = 'filter-badge';
      const range = `${parsed.date_from || 'Start'} → ${parsed.date_to || 'End'}`;
      badge.innerHTML = `📅 Date Range: <strong>${escapeHtml(range)}</strong>`;
      parsedFiltersBar.appendChild(badge);
    }

    if (parsed.clean_query && parsed.clean_query !== searchInput.value.trim()) {
      hasBadge = true;
      const badge = document.createElement('span');
      badge.className = 'filter-badge';
      badge.innerHTML = `🎯 Semantic Vector Query: <em>"${escapeHtml(parsed.clean_query)}"</em>`;
      parsedFiltersBar.appendChild(badge);
    }

    parsedFiltersBar.style.display = hasBadge ? 'flex' : 'none';
  }

  // =========================================================================
  // Result Card Construction
  // =========================================================================

  function createResultCard(item, rank) {
    const card = document.createElement('article');
    card.className = 'result-card';
    card.setAttribute('data-id', item.id);

    const initials = getInitials(item.sender);
    const avatarColor = PARTICIPANT_COLORS[item.sender] || DEFAULT_AVATAR_COLOR;
    const formattedTime = formatTimestamp(item.timestamp);
    const scorePct = Math.min(100, Math.max(0, Math.round(item.score * 100)));

    let scoreClass = 'score-high';
    if (item.score < 0.65) scoreClass = 'score-moderate';
    else if (item.score < 0.8) scoreClass = 'score-medium';

    const hasContext = Array.isArray(item.context) && item.context.length > 0;
    const contextCount = hasContext ? item.context.length : 0;

    card.innerHTML = `
      <div class="card-top-header">
        <div class="author-meta">
          <div class="author-avatar" style="background-color: ${avatarColor};" title="${escapeHtml(item.sender)}">
            ${initials}
          </div>
          <div class="author-info">
            <span class="author-name">${escapeHtml(item.sender)}</span>
            <span class="message-time" title="${item.timestamp}">${formattedTime}</span>
          </div>
        </div>

        <div class="card-badges">
          <span class="rank-badge">#${rank}</span>
          <span class="match-reason-pill" title="Retrieval explanation">${escapeHtml(item.match_reason)}</span>
          <div class="score-badge ${scoreClass}">
            <span class="score-bar-mini">
              <span class="score-bar-fill" style="width: ${scorePct}%;"></span>
            </span>
            <span>${(item.score * 100).toFixed(1)}% Match</span>
          </div>
        </div>
      </div>

      <div class="message-body">
        <p class="message-text">${escapeHtml(item.text)}</p>
        <div class="message-meta-row">
          <span class="meta-tag">ID: ${item.id}</span>
          <span class="meta-tag">Conv: ${item.conversation_id}</span>
          ${item.forwarded ? '<span class="meta-tag meta-forwarded">↗ Forwarded</span>' : ''}
          ${item.reply_to ? `<span class="meta-tag meta-reply">↩ Reply to ${item.reply_to}</span>` : ''}
        </div>
      </div>

      ${hasContext ? `
        <div class="context-accordion">
          <button type="button" class="context-toggle-btn" aria-expanded="false">
            <span class="context-chevron">▼</span>
            <span>View Conversation Context (${contextCount} messages)</span>
          </button>
          <div class="context-thread-container collapsed">
            ${renderContextMessages(item.context)}
          </div>
        </div>
      ` : ''}
    `;

    // Bind context toggle button inside this card
    if (hasContext) {
      const toggleBtn = card.querySelector('.context-toggle-btn');
      const threadContainer = card.querySelector('.context-thread-container');
      toggleBtn.addEventListener('click', () => {
        const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
        toggleBtn.setAttribute('aria-expanded', (!isExpanded).toString());
        threadContainer.classList.toggle('collapsed', isExpanded);
        toggleBtn.querySelector('span:last-child').textContent = isExpanded
          ? `View Conversation Context (${contextCount} messages)`
          : `Hide Conversation Context (${contextCount} messages)`;
      });
    }

    return card;
  }

  function renderContextMessages(context) {
    return context.map((msg) => {
      const isMatch = !!msg.is_match;
      const formattedTime = formatTimestamp(msg.timestamp);
      const matchedClass = isMatch ? 'context-item context-item-matched' : 'context-item';

      return `
        <div class="${matchedClass}">
          <div class="context-item-header">
            <span class="context-author">
              ${escapeHtml(msg.sender)}
              ${isMatch ? '<span class="matched-badge-pill">🎯 MATCHED MESSAGE</span>' : ''}
            </span>
            <span class="context-time">${formattedTime}</span>
          </div>
          <p class="context-text">${escapeHtml(msg.text)}</p>
        </div>
      `;
    }).join('');
  }

  // =========================================================================
  // Helpers & Formatting
  // =========================================================================

  function updateActiveFilterBadge() {
    let count = 0;
    if (senderFilter.value) count++;
    if (dateFromFilter.value) count++;
    if (dateToFilter.value) count++;
    if (topKFilter.value && topKFilter.value !== '10') count++;

    if (count > 0) {
      filterActiveBadge.textContent = `${count} active`;
      filterActiveBadge.classList.remove('hidden');
    } else {
      filterActiveBadge.classList.add('hidden');
    }
  }

  function getInitials(name) {
    if (!name) return '?';
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  function formatTimestamp(isoStr) {
    if (!isoStr) return '';
    try {
      const d = new Date(isoStr);
      if (isNaN(d.getTime())) return isoStr;

      return d.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      });
    } catch {
      return isoStr;
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

})();
