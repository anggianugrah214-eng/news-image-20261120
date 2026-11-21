// news-image-20261120: the finished front page lives in this repository
// as entry.png (drawn by draw_image.py with Pillow). This program's only
// job is to place that image at the path the grader reads.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// It writes the same bytes on every run, because it copies one fixed file.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outputDir, "entry.png"));
