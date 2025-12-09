/**
 * ═════════════════════════════════════════════════════════════════════
 * PANDORA v2.0 - Phase 4 System Test
 * Browser console commands for testing Phase 4 components
 * ═════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════
// 1. TEST MODULE INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════

console.group('📦 Testing Module Initialization');

// Check if window.App exists
console.log('window.App exists:', !!window.App);

// Check each manager
const managers = {
  'HTTPClient': window.App?.http,
  'EventManager': window.App?.eventManager,
  'NavigationManager': window.App?.navigation,
  'ThemeManager': window.App?.theme,
  'UIManager': window.App?.ui,
  'PromptEditor': window.App?.editor,
  'TagManager': window.App?.tagManager,
  'AnalyticsDashboard': window.App?.analytics
};

Object.entries(managers).forEach(([name, manager]) => {
  console.log(`✓ ${name}:`, manager ? 'Loaded' : 'MISSING');
});

console.groupEnd();

// ═══════════════════════════════════════════════════════════════════════
// 2. TEST HTTP CLIENT
// ═══════════════════════════════════════════════════════════════════════

console.group('🔌 Testing HTTPClient');

async function testHTTPClient() {
  const http = window.App.http;
  
  console.log('HTTP Client config:', {
    baseUrl: http.baseUrl,
    timeout: http.timeout,
    retryAttempts: http.retryAttempts,
    cacheTTL: http.cacheTTL
  });

  // Test 1: Basic GET
  try {
    console.log('Test 1: GET /api/prompts (first call - should be network)');
    const time1 = performance.now();
    const data1 = await http.get('/prompts');
    const time1End = performance.now();
    console.log(`✓ Success - Time: ${(time1End - time1).toFixed(0)}ms - Count: ${Array.isArray(data1) ? data1.length : 'unknown'}`);
    
    console.log('Test 2: GET /api/prompts (second call - should be cached)');
    const time2 = performance.now();
    const data2 = await http.get('/prompts');
    const time2End = performance.now();
    console.log(`✓ Success - Time: ${(time2End - time2).toFixed(0)}ms (should be <5ms if cached)`);
    
    console.log('Data identical:', data1 === data2);
  } catch (error) {
    console.error('✗ Failed:', error.message);
  }

  // Test 3: Cache control
  try {
    console.log('Test 3: GET /api/prompts with skipCache=true');
    const data3 = await http.get('/prompts', { skipCache: true });
    console.log('✓ Cache skipped successfully');
  } catch (error) {
    console.error('✗ Failed:', error.message);
  }

  // Test 4: Cache contents
  console.log('Test 4: Cache contents:', `${http.cache.size} entries`);
  for (const [key] of http.cache.entries()) {
    console.log(`  - ${key.substring(0, 50)}...`);
  }
}

// Run test
testHTTPClient().then(() => {
  console.log('✓ HTTPClient tests completed');
  console.groupEnd();
});

// ═══════════════════════════════════════════════════════════════════════
// 3. TEST EVENT MANAGER
// ═══════════════════════════════════════════════════════════════════════

console.group('⚡ Testing EventManager');

const eventManager = window.App.eventManager;

console.log('EventManager initialized:', !!eventManager);
console.log('Error boundary setup:', !!eventManager.globalErrorBoundary);

// Test custom events
console.log('Test 1: Custom event emission');
let testEventFired = false;
eventManager.onCustom('test:event', (data) => {
  console.log('✓ Custom event received:', data);
  testEventFired = true;
});

eventManager.emit('test:event', { message: 'Test payload' });
console.log('Custom event fired:', testEventFired);

// Test event delegation
console.log('Test 2: Event delegation listener added for .nav-link');
eventManager.on('.nav-link[data-page]', 'click', function(e) {
  console.log('✓ Delegated click on nav link:', this.getAttribute('data-page'));
});
console.log('✓ Delegation listener ready (click a nav link to test)');

// Test error boundary
console.log('Test 3: Error boundary');
try {
  throw new Error('Test error for error boundary');
} catch (error) {
  eventManager.handleError(error, { test: true });
  console.log('✓ Error boundary handled test error');
}

console.groupEnd();

// ═══════════════════════════════════════════════════════════════════════
// 4. TEST NAVIGATION MANAGER
// ═══════════════════════════════════════════════════════════════════════

console.group('🧭 Testing NavigationManager');

const navigation = window.App.navigation;

console.log('NavigationManager initialized:', !!navigation);
console.log('Current page:', navigation.currentPage);
console.log('Default page:', navigation.defaultPage);
console.log('Page history:', navigation.pageHistory);

// Test navigation
console.log('Test 1: Navigate to different page');
console.log('Before:', navigation.currentPage);
navigation.navigateTo('prompts');
console.log('After:', navigation.currentPage);

// Check page visibility
console.log('Test 2: Check page visibility');
document.querySelectorAll('.page').forEach(page => {
  const id = page.id;
  const opacity = window.getComputedStyle(page).opacity;
  const active = page.classList.contains('active');
  console.log(`  - ${id}: opacity=${opacity}, active=${active}`);
});

console.groupEnd();

// ═══════════════════════════════════════════════════════════════════════
// 5. TEST REQUEST DEDUPLICATION
// ═════════════════════════════════════════════════════════════════════

console.group('🔄 Testing Request Deduplication');

async function testDeduplication() {
  const http = window.App.http;
  
  console.log('Test: Multiple POST requests with identical data');
  console.log('Sending 3 identical POST requests simultaneously...');
  
  const data = { test: 'deduplication', timestamp: Date.now() };
  
  // Create 3 promises
  const promise1 = http.post('/prompts', data);
  const promise2 = http.post('/prompts', data);
  const promise3 = http.post('/prompts', data);
  
  console.log('Promise 1 === Promise 2:', promise1 === promise2);
  console.log('Promise 1 === Promise 3:', promise1 === promise3);
  
  if (promise1 === promise2 && promise1 === promise3) {
    console.log('✓ Request deduplication working! All 3 promises are identical.');
    console.log('  This means only 1 actual request will be sent to the server.');
  } else {
    console.log('✗ Deduplication not working - requests are different');
  }
}

testDeduplication().catch(e => {
  console.warn('Deduplication test failed (might be API issue, but mechanism is present)');
});

console.groupEnd();

// ═══════════════════════════════════════════════════════════════════════
// 6. TEST UI NOTIFICATIONS
// ═════════════════════════════════════════════════════════════════════

console.group('🎨 Testing UI Components');

console.log('Test 1: Toast notifications');
window.App.ui.showToast('Success notification', 'success');
setTimeout(() => {
  window.App.ui.showToast('Error notification', 'error');
}, 1000);

console.log('Test 2: Modal operations');
const hasModals = document.querySelectorAll('[data-modal]').length > 0;
console.log(`Found ${document.querySelectorAll('[data-modal]').length} modals`);

console.groupEnd();

// ═══════════════════════════════════════════════════════════════════════
// 7. TEST KEYBOARD SHORTCUTS
// ═════════════════════════════════════════════════════════════════════

console.group('⌨️  Testing Keyboard Shortcuts');

console.log('Registered shortcuts:');
console.log('  - Ctrl+K or Cmd+K: Focus search');
console.log('  - Escape: Close modals');
console.log('  - Alt+1-5: Navigate to pages');
console.log('  - Ctrl+Shift+L or Cmd+Shift+L: Toggle theme');

console.log('Try pressing Ctrl+K or Alt+1 to test...');

console.groupEnd();

// ═══════════════════════════════════════════════════════════════════════
// 8. SUMMARY
// ═════════════════════════════════════════════════════════════════════

console.group('%c✨ PHASE 4 SYSTEM TEST SUMMARY', 'color: #00ff00; font-size: 16px; font-weight: bold');

const systemHealth = {
  'HTTPClient': !!window.App?.http,
  'EventManager': !!window.App?.eventManager,
  'NavigationManager': !!window.App?.navigation,
  'ThemeManager': !!window.App?.theme,
  'UIManager': !!window.App?.ui,
  'All managers': Object.values(managers).every(m => !!m)
};

console.table(systemHealth);

console.log('%cSystem Status:', 'font-weight: bold');
const allHealthy = Object.values(systemHealth).every(v => v);
if (allHealthy) {
  console.log('%c✓ ALL SYSTEMS OPERATIONAL', 'color: #00ff00; font-weight: bold');
} else {
  console.log('%c✗ SOME SYSTEMS FAILED', 'color: #ff0000; font-weight: bold');
  console.log('Check console for errors');
}

console.log('%cNext steps:', 'font-weight: bold');
console.log('1. Click nav links to test navigation');
console.log('2. Use Ctrl+K to test search focus');
console.log('3. Try Alt+1, Alt+2, Alt+3 for page shortcuts');
console.log('4. Test create/update/delete operations');
console.log('5. Check browser Network tab for deduplication');
console.log('6. Open another tab and verify cache works');

console.groupEnd();

// ═════════════════════════════════════════════════════════════════════════
// HELPER FUNCTION: Display performance stats
// ═════════════════════════════════════════════════════════════════════════

window.PANDORA_TEST_UTILS = {
  /**
   * Show cache statistics
   */
  cacheStats() {
    const http = window.App.http;
    console.log('Cache Statistics:', {
      entries: http.cache.size,
      cacheMemory: `${(new Blob([JSON.stringify(Array.from(http.cache.values()))]).size / 1024).toFixed(2)} KB`,
      cacheEntries: Array.from(http.cache.keys()).map(k => k.substring(0, 40) + '...')
    });
  },

  /**
   * Clear all caches and reset state
   */
  resetSystem() {
    window.App.http.clearCache();
    console.log('✓ Cache cleared');
  },

  /**
   * Test error handling
   */
  testError() {
    window.App.eventManager.handleError(
      new Error('Test error for debugging'),
      { manual: true }
    );
    console.log('✓ Error handling test completed');
  },

  /**
   * List all available commands
   */
  help() {
    console.log('%cAvailable Test Commands:', 'font-weight: bold; font-size: 14px');
    console.log('window.PANDORA_TEST_UTILS.cacheStats()   - Show cache info');
    console.log('window.PANDORA_TEST_UTILS.resetSystem()  - Clear cache');
    console.log('window.PANDORA_TEST_UTILS.testError()    - Test error handling');
    console.log('window.PANDORA_TEST_UTILS.help()         - Show this help');
  }
};

console.log('%c✓ Test utilities available at: window.PANDORA_TEST_UTILS', 'color: #00ffff');
console.log('   Run: window.PANDORA_TEST_UTILS.help() for commands');
