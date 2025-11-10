/**
 * Office.js initialization
 */

export const initializeOffice = (): Promise<void> => {
  return new Promise((resolve, reject) => {
    Office.onReady((info) => {
      if (info.host === Office.HostType.PowerPoint) {
        console.log('Office.js initialized for PowerPoint');
        resolve();
      } else {
        console.warn('Not running in PowerPoint, but Office.js is ready');
        resolve();
      }
    });
  });
};

export const isOfficeInitialized = (): boolean => {
  return typeof Office !== 'undefined' && Office.context !== undefined;
};
