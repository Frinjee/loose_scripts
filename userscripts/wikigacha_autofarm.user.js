// ==UserScript==
// @name wikigacha_autofarm
// @namespace https://github.com/frinjee/userscripts/wikigacha_autofarm.user.js
// @version 1.0
// @description Automation too for wikigacha.com
// @author Frinjee
// @match https://wikigacha.com/*
// @icon https://www.google.com/s2/favicons?sz=64&domain=wikigacha.com
// @grant GM_setValue
// @grant GM_getValue
// @grant GM_addStyle
// @run-at document-start
// ==/UserScript==

(function () {
    'use strict';

    // ** DISABLE ALERTS **
    const killAlertsScript = document.createElement('script');
    killAlertsScript.textContent = `
        window.alert = function() { return true; };
        window.confirm = function() { return true; };
    `; (document.head || document.documentElement).appendChild(killAlertsScript);

    // ** STYLING **
    function addStyling() {
        const css = `
            * { transition: none !important; animation: none !important; }

            #gm-stats-panel {
                position: fixed; top: 10px; right: 10px; z-index: 10000;
                background: rgba(0,0,0,0.95) !important; color: #fff !important; padding: 12px !important;
                border-radius: 10px !important; border: 2px solid #06b6d4 !important; font-family: ui-sans-serif, system-ui, sans-serif !important;
                min-width: 220px !important;
                box-shadow: 0 4px 20px rgba(0,0,0,0.8) !important; pointer-events: auto !important;
                text-align: left !important;            
            }

            #gm-stats-panel.paused {
                border-color: #f97316 !important;
            }
            
            #gm-stats-panel .rarity-row {
                display: flex; justify-content: space-between; font-size: 0.8rem; margin-top: 3px;
            }
            
            #gm-stats-panel .lr { color: #a855f7; font-weight: bold; }
            #gm-stats-panel .ur { color: #eab308; font-weight: bold; }
            #gm-stats-panel .ssr { color: #ef4444; font-weight: bold; }
            #gm-stats-panel .sr { color: #eb82f6; font-weight: bold; }
            #gm-stats-panel .r { color: #22c55e; font-weight: bold; }
            #gm-stats-panel .uc { color: #94a3b8; font-weight: bold; }
            #gm-stats-panel .stats-main { border-bottom: 1px solid #333; margin-bottom: 6px; padding-bottom: 4px; font-size: 0.9rem; }
            #gm-stats-panel .button { cursor: pointer; margin-top: 4px; font-size: 0.7rem; }
        `;
        if (typeof GM_addStyle !== 'undefined') {
            GM_addStyle(css);
        } else {
            const style = document.createElement('style');
            style.textContent = css;
            document.head.appendChild(style);
        }

    } // end addStyling()

    let panel;
    let statsRow = {};
    let lastSync = 0;

    let stats = GM_getValue('fullStats', {
        uniques: '...',
        totalPulls: '...',
        lr: '0',
        ur: '0',
        ssr: '0',
        sr: '0',
        r: '0',
        uc: '0',
        c: '0'
    });

    const config = GM_getValue('config', {
        loopIntervalMs: 1000,
        syncIntervalMs: 6000,
        autoRefiller: true
    });

    let isPaused = false;
    let autoRefilledEnabled = config.autoRefiller;
    let syncIntervalMs = config.syncIntervalMs;



    function init() {
        if (!document.body) { setTimeout(init, 50); return; }
        addStyling();

        panel = document.createElement('div');
        panel.id = 'gm-stats-panel';

        const header = document.createElement('div');
        header.className = 'stats-main';
        header.innerHTML = `
            Uniques: <span id='gm-uniques' style='color:#06b6d4'></span>
            | Pulls: <span id='gm-pulls' style='color:#06b6d4'></span>
        `;

        const pauseBtn = document.createElement('button');
        pauseBtn.textContent = 'Toggle Pause (Alt+P)';
        pauseBtn.addEventListener('click', () => {
            isPaused = !isPaused;
            panel.classList.toggle('paused', isPaused);
            console.log('[WIKIGACHA_AUTOFARM] STATE: ', isPaused);
        });

        const rows = [
            ['LR', 'lr', 'lr'],
            ['UR', 'ur', 'ur'],
            ['SSR', 'ssr', 'ssr'],
            ['SR', 'sr', 'sr'],
            ['R', 'r', 'r'],
            ['UC', 'uc', 'uc'],
            ['C', 'c', 'c']
        ];

        panel.appendChild(header);

        rows.forEach(([label, key, cls]) => {
            const row = document.createElement('div');
            row.className = 'rarity-row';
            const spanLabel = document.createElement('span');
            spanLabel.textContent = label;
            if (cls) spanLabel.className = cls;
            const spanValue = document.createElement('span');
            statsRow[key] = spanValue;
            row.appendChild(spanLabel);
            row.appendChild(spanValue);
            panel.appendChild(row);
        });

        panel.appendChild(pauseBtn);
        document.body.appendChild(panel);
    }

    init();

    // ** STATS HELPERS **
    function statsEqual(a, b) {
        return a.uniques === b.uniques &&
            a.totalPulls === b.totalPulls &&
            a.lr === b.lr &&
            a.ur === b.ur &&
            a.ssr === b.ssr &&
            a.sr === b.sr &&
            a.r === b.r &&
            a.uc === b.uc &&
            a.c === b.c;
    }

    function updateStatsIfChanged(newStats) {
        if (!statsEqual(stats, newStats)) {
            stats = newStats;
            GM_setValue('fullStats', stats);
        }
    }

    function updateDisplay() {
        if (!panel) return;
        const uniquesEl = document.getElementById('gm-uniques');
        const pullsEl = document.getElementById('gm-pulls');

        if (uniquesEl) uniquesEl.textContent = stats.uniques;
        if (pullsEl) pullsEl.textContent = stats.totalPulls;

        Object.entries(statsRow).forEach(([key, el]) => {
            if (el) el.textContent = stats[key];
        });

        panel.classList.toggle('paused', isPaused);
    }

    // ** SCRAPING **

    function scrapeCollectionAndReturn(gachaBtn, observer) {
        const containers = Array.from(document.querySelectorAll('div')).filter(el => el.innerText.includes('/') 
                                                                            && el.innerText.length < 50);
        const getRarityVal = (label) => {
            const box = containers.find(c => c.innerText.startsWith(label));
            if(box) {
                const m = box.innerText.match(/(\d+)[\/\s]/);
                return m ? m[1] : '0';
            }
            return '0';
        };

        const mainText = document.body.innerText;
        const uMatch = mainText.match(/Unique Cards:\s*([\d\s,]+)/);
        const tMatch = mainText.match(/Total Pulls:\s*([\d\s,]+)/);

        const newStats = {
            uniques: uMatch ? uMatch[1].split('/')[0].trim() : stats.uniques,
            totalPulls: tMatch ? tMatch[1].trim() : stats.totalPulls,
            lr: getRarityVal('LR'),
            ur: getRarityVal('UR'),
            ssr: getRarityVal('SSR'),
            sr: getRarityVal('SR'),
            r: getRarityVal('R'),
            uc: getRarityVal('UC'),
            c: getRarityVal('C')
        };

        updateStatsIfChanged(newStats);
        gachaBtn.click();
        lastSync = Date.now();

        if (observer) observer.disconnect();
    }

    // ** FORCE SYNC **
    function forceSync() {
        try {
            const collBtn = Array.from(document.querySelectorAll('button, a'))
                                 .find(el => el.textContent.includes('Collection'));
            const gachaBtn = Array.from(document.querySelectorAll('button, a'))
                                  .find(el => el.textContent.includes('Gacha'));

            if (!collBtn || !gachaBtn) return;

            collBtn.click();

            const observer = new MutationObserver((mutations, obs) => {
                if (document.body.innerText.includes('Unique Cards') &&
                    document.body.innerText.includes('Total Pulls')) {
                        scrapeCollectionAndReturn(gachaBtn, obs);
                    }
            });

            observer.observe(document.body, { childList: true, subtree: true });
        } catch (e) {
            console.error('[WIKIGACHA_AUTOFARM] forceSync error:', e);
        }
    }

    // ** INPUT HANDLERS **
    
    // toggle autorefiller w/hotkey
    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key.toLowerCase() === 'r') {
            autoRefilledEnabled = !autoRefilledEnabled;
            config.autoRefiller = autoRefilledEnabled;
            GM_setValue('config', config);
            console.log('[WIKIGACHA_AUTOFARM] REFILL STATE: ', autoRefilledEnabled);
        }
    // toggle pause w/hotkey
        if (e.altKey && e.key.toLowerCase() === 'p') {
            isPaused = !isPaused;
            if (panel) panel.classList.toggle('paused', isPaused);
            console.log('[WIKIGACHA_AUTOFARM] STATE: ', isPaused);
        } 
    });

    // ** MAIN LOOP **
    function mainLoopTick() {
        if (document.visibilityState !== 'visible') return;
        if (isPaused) return;

        updateDisplay();

        if (Date.now() - lastSync > syncIntervalMs) { forceSync(); return; }

        const handleAd = document.querySelector('button.bg-cyan-500')
                                 || Array.from(document.querySelectorAll('button'))
                                 .find(b => b.textContent.toLowerCase().includes('close'));
        if (handleAd) { handleAd.click(); return; }

        const refill = document.querySelector('button.from-blue-700')
                               || Array.from(document.querySelectorAll('button'))
                               .find(b => b.textContent.toLowerCase().includes('refill'));
        if (refill && autoRefilledEnabled) {
            refill.click();
            return;
        }

        const returnToPacks = Array.from(document.querySelectorAll('button'))
                                   .find(b => b.textContent.includes('BACK TO PACKS'));
        if (returnToPacks) { returnToPacks.click(); return; }

        const packCheck = document.querySelector('img[alt*="PACK"]')
            || document.querySelector('img[src*="pack"]');
        
        if (packCheck) {
            const _btn = packCheck.closest('button') || packCheck;
            _btn.click();
        }
    }

    // use config.loopIntervalMs when utilizing setInterval
    setInterval(() => {
        try {
            mainLoopTick();
        } catch (e) {
            console.error('[WIKIGACHA_AUTOFARM] main loop error: ', e);
        }
    }, config.loopIntervalMs);

}) ();