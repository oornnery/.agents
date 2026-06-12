/** Node.js HTTP server entrypoint.
 *
 *  Keeps HTTP wiring thin so business logic stays testable outside
 *  of the web framework.  Routes validate at the boundary and delegate
 *  to plain functions.
 */

import { createServer, IncomingMessage, ServerResponse } from 'node:http';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface Task {
  id: string;
  title: string;
  status: 'pending' | 'in_progress' | 'done';
}

interface HealthResponse {
  status: string;
}

interface ErrorResponse {
  error: string;
}

// ---------------------------------------------------------------------------
// In-memory store (replace with repository layer in production)
// ---------------------------------------------------------------------------

const taskStore: Task[] = [
  { id: '1', title: 'Learn TypeScript', status: 'pending' },
  { id: '2', title: 'Build something cool', status: 'in_progress' },
];

// ---------------------------------------------------------------------------
// Core logic (pure, testable without HTTP)
// ---------------------------------------------------------------------------

function listTasks(): Task[] {
  return taskStore;
}

function healthCheck(): HealthResponse {
  return { status: 'ok' };
}

// ---------------------------------------------------------------------------
// Structured logging
// ---------------------------------------------------------------------------

function logRequest(method: string, url: string, statusCode: number): void {
  const timestamp = new Date().toISOString();
  console.log(JSON.stringify({ timestamp, method, url, statusCode }));
}

function logError(method: string, url: string, error: Error): void {
  const timestamp = new Date().toISOString();
  console.error(JSON.stringify({ timestamp, method, url, error: error.message }));
}

// ---------------------------------------------------------------------------
// HTTP boundary helpers
// ---------------------------------------------------------------------------

function sendJson<T>(res: ServerResponse, statusCode: number, payload: T): void {
  const body = JSON.stringify(payload);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
}

function sendError(res: ServerResponse, statusCode: number, message: string): void {
  const payload: ErrorResponse = { error: message };
  sendJson(res, statusCode, payload);
}

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

function handleRequest(req: IncomingMessage, res: ServerResponse): void {
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

export function createAppServer(port: number) {
  const server = createServer(handleRequest);

  return {
    listen: (): Promise<void> =>
      new Promise((resolve) => {
        server.listen(port, () => {
          console.log(`Server listening on port ${port}`);
          resolve();
        });
      }),
    close: (): Promise<void> =>
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
if (import.meta.url === `file://${process.argv[1]}`) {
  const port = parseInt(process.env.PORT ?? '3000', 10);
  const app = createAppServer(port);
  app.listen();
}
