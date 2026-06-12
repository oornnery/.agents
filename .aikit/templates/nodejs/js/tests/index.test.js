/** Application-level API tests using vitest and node:http. */

import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createAppServer } from '../src/index.js';

describe('HTTP Server', () => {
  const port = 0; // 0 lets OS assign an ephemeral port
  const app = createAppServer(port);
  /** @type {string} */
  let serverUrl;

  beforeAll(async () => {
    await app.listen();
    const address = app.getServer().address();
    if (address && typeof address === 'object') {
      serverUrl = `http://localhost:${address.port}`;
    } else {
      throw new Error('Server did not bind to a TCP port');
    }
  });

  afterAll(async () => {
    await app.close();
  });

  it('GET /health returns 200 and status ok', async () => {
    // Act
    const response = await fetch(`${serverUrl}/health`);

    // Assert
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.status).toBe('ok');
  });

  it('GET /tasks returns a list of tasks', async () => {
    // Act
    const response = await fetch(`${serverUrl}/tasks`);

    // Assert
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(Array.isArray(data)).toBe(true);
    expect(data.length).toBe(2);
    expect(data[0].title).toBe('Learn JavaScript');
    expect(data[1].status).toBe('in_progress');
  });

  it('GET /unknown returns 404', async () => {
    // Act
    const response = await fetch(`${serverUrl}/unknown`);

    // Assert
    expect(response.status).toBe(404);
    const data = await response.json();
    expect(data.error).toBe('Not found');
  });

  it('POST /tasks returns 405 method not allowed', async () => {
    // Act
    const response = await fetch(`${serverUrl}/tasks`, { method: 'POST' });

    // Assert
    expect(response.status).toBe(405);
    const data = await response.json();
    expect(data.error).toBe('Method not allowed');
  });
});
