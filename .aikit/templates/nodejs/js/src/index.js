/** Node.js HTTP server entrypoint.
 *
 *  Keeps HTTP wiring thin so business logic stays testable outside
 *  of the web framework.  Routes validate at the boundary and delegate
 *  to plain functions.
 */

import { createServer } from 'node:http';

// ---------------------------------------------------------------------------
// In-memory store (replace with repository layer in production)
// ---------------------------------------------------------------------------

/** @type {Array<{id: string, title: string, status: string}>} */
const taskStore = [
  { id: '1', title: 'Learn JavaScript', status: 'pending' },
  { id: '2', title: 'Build something cool', status: 'in_progress' },
];

// ---------------------------------------------------------------------------
// Core logic (pure, testable without HTTP)
// ---------------------------------------------------------------------------

/** @returns {Array<{id: string, title: string, status: string}>} */
function listTasks() {
  return taskStore;
}

/** @returns {{status: string}} */
function healthCheck() {
  return { status: 'ok' };
}

// ---------------------------------------------------------------------------
// Structured logging
// ---------------------------------------------------------------------------

/** @param {string} method
 *  @param {string} url
 *  @param {number} statusCode
 */
function logRequest(method, url, statusCode) {
  const timestamp = new Date().toISOString();
  console.log(JSON.stringify({ timestamp, method, url, statusCode }));
}

/** @param {string} method
 *  @param {string} url
 *  @param {Error} error
 */
function logError(method, url, error) {
  const timestamp = new Date().toISOString();
  console.error(JSON.stringify({ timestamp, method, url, error: error.message }));
}

// ---------------------------------------------------------------------------
// HTTP boundary helpers
// ---------------------------------------------------------------------------

/** @param {import('node:http').ServerResponse} res
 *  @param {number} statusCode
 *  @param {unknown} payload
 */
function sendJson(res, statusCode, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
}

/** @param {import('node:http').ServerResponse} res
 *  @param {number} statusCode
 *  @param {string} message
 */
function sendError(res, statusCode, message) {
  sendJson(res, statusCode, { error: message });
}

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

/** @param {import('node:http').IncomingMessage} req
 *  @param {import('node:http').ServerResponse} res
 */
function handleRequest(req, res) {
  const method = req.method ?? 'UNKNOWN';
  const url = req.url ?? '/';

  try {
    if (method === 'GET' && url === '/health') {
      const payload = healthCheck();
      sendJson(res, 200, payload);
      logRequest(method, url, 200);
      return;
    }

    if (method === 'GET' && url === '/tasks') {
      const payload = listTasks();
      sendJson(res, 200, payload);
      logRequest(method, url, 200);
      return;
    }

    if (method === 'POST' || method === 'PUT' || method === 'DELETE') {
      sendError(res, 405, 'Method not allowed');
      logRequest(method, url, 405);
      return;
    }

    sendError(res, 404, 'Not found');
    logRequest(method, url, 404);
  } catch (err) {
    const error = err instanceof Error ? err : new Error(String(err));
    logError(method, url, error);
    sendError(res, 500, 'Internal server error');
  }
}

// ---------------------------------------------------------------------------
// Server lifecycle
// ---------------------------------------------------------------------------

/** @param {number} port
 *  @returns {{listen: () => Promise<void>, close: () => Promise<void>, getServer: () => import('node:http').Server}}
 */
export function createAppServer(port) {
  const server = createServer(handleRequest);

  return {
    listen: () =>
      new Promise((resolve) => {
        server.listen(port, () => {
          console.log(`Server listening on port ${port}`);
          resolve();
        });
      }),
    close: () =>
      new Promise((resolve, reject) => {
        server.close((err) => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        });
      }),
    getServer: () => server,
  };
}

// Only start if this file is the entrypoint (not imported in tests)
if (import.meta.url === new URL(process.argv[1], import.meta.url).href) {
  const port = parseInt(process.env.PORT ?? '3000', 10);
  const app = createAppServer(port);
  app.listen();
}
