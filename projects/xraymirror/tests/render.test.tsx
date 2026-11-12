// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest';
import { createRoot } from 'react-dom/client';
import { act } from 'react';
import App from '../src/App';

function clickText(container: HTMLElement, text: string): void {
  const buttons = [...container.querySelectorAll('button')];
  const button = buttons.find((entry) => entry.textContent?.includes(text));
  if (!button) throw new Error(`Button not found: ${text}`);
  button.dispatchEvent(new MouseEvent('click', { bubbles: true }));
}

describe('studio shell', () => {
  let host: HTMLElement | null = null;

  afterEach(() => {
    host?.remove();
    host = null;
  });

  it('renders navigation, camera gate and plugin views without a camera', async () => {
    host = document.createElement('div');
    document.body.appendChild(host);
    const root = createRoot(host);
    await act(async () => {
      root.render(<App />);
    });
    expect(host.querySelector('h1')?.textContent).toContain('X-Ray Mirror Studio');
    expect(host.innerHTML).toContain('Autoriser la caméra');
    expect(host.innerHTML).toContain('Limites assumées');

    await act(async () => {
      clickText(host!, 'Plugins');
    });
    expect(host.innerHTML).toContain('Centre de plugins');
    expect(host.innerHTML).toContain('planned.vlm');

    await act(async () => {
      clickText(host!, 'Nutrition');
    });
    expect(host.innerHTML).toContain('Open Food Facts');

    await act(async () => {
      clickText(host!, 'Limites & sécurité');
    });
    expect(host.innerHTML).toContain('Aucune identification de personne');

    await act(async () => {
      root.unmount();
    });
  });
});
