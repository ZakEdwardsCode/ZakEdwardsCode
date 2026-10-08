import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export const p = (...parts) => path.join(ROOT, ...parts);
export const DIRS = {
  posts: p('posts'),
  output: p('output'),
  screenshots: p('screenshots'),
  assets: p('assets'),
  brand: p('brand'),
  research: p('research'),
};
