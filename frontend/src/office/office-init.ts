/**
 * Office.js initialization with timeout
 */

export const initializeOffice = (): Promise<void> => {
  return new Promise((resolve, reject) => {
    // Set a timeout to prevent infinite loading
    const timeout = setTimeout(() => {
      console.warn('Office.js initialization timeout - continuing anyway');
      resolve();
    }, 2000); // 2 second timeout

    if (typeof Office !== 'undefined') {
      Office.onReady((info) => {
        clearTimeout(timeout);
        if (info.host === Office.HostType.PowerPoint) {
          console.log('Office.js initialized for PowerPoint');
          resolve();
        } else {
          console.warn('Not running in PowerPoint, but Office.js is ready');
          resolve();
        }
      });
    } else {
      // Office.js not loaded (running in browser, not PowerPoint)
      clearTimeout(timeout);
      console.warn('Office.js not available - running in browser mode');
      resolve();
    }
  });
};

export const isOfficeInitialized = (): boolean => {
  return typeof Office !== 'undefined' && Office.context !== undefined;
};
