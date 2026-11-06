import { cp, mkdir, readFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
const root = fileURLToPath(new URL("../", import.meta.url));
const destination = fileURLToPath(new URL("../../public/attendance/", import.meta.url));
await mkdir(destination, { recursive: true });
// Retain old hashed chunks so an already open client can finish its attendance.
await cp(root + "out/", destination, { recursive: true });
const html = await readFile(destination + "index.html");
const hash = createHash("sha256").update(html).digest("hex").slice(0, 16);
console.log("Published attendance app", hash);
