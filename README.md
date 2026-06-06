# ⚡ Dynamic File Compression Utility (DFC Engine) v1.0.0

An advanced, production-ready lossless data compression platform built in Python. This utility features a dual-engine core: a custom algorithmic **Huffman Coding Engine** constructed from scratch using optimized Binary Trees and Min-Heap Priority Queues, alongside an automated **Heuristic Routing Matrix** that samples live file telemetry data to auto-allocate the absolute best modern storage codec (`zstd`, `brotli`, `lzma`, `gzip`) in real-time.

---

## 🚀 Core Architecture & Workflow

The platform dynamically inspects incoming data payloads using mathematical entropy metrics before routing them through the compression stream to eliminate processing overhead and maximize storage efficiency:

```text
 [INPUT FILE] ───> [Telemetry Profiling & Shannon Entropy Check] ───> [Strategy Router]
                                                                             │
           ┌─────────────────────────────────────────────────────────────────┘
           ▼
     ├──> [Strategy: Custom Huffman Engine] ──> Min-Heap Node Merging ──> Bit-Packing Stream Out
     └──> [Strategy: Enterprise Codecs] ───> Fixed Buffer Chunk I/O ───> Automated Metadata DFC Manifest