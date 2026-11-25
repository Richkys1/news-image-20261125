// Entry point for the 25 November 2026 front page (Node 22, standard
// library only). The image is the entry.png beside this file, rendered at
// build time by generate.py; this program just copies it to the output
// directory the harness expects, so every run writes byte-identical output.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'),
);
