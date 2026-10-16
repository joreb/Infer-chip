# Agentic SNN-Chip Design Loop PoC — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** One autonomous agent loop that designs AI-inference chips across three device targets — digital LIF (OpenROAD→GDS), photonic MZI-mesh, memristive crossbar — with journal, Pareto reporting, and swappable agent backends (stub/cc/api).

**Architecture:** Orchestrator drives rounds: backend proposes config → target `evaluate(cfg)` produces sim+flow verdicts and metrics → journal record appended → next config proposed from journal tail. Targets implement one `evaluate` interface; agent backends implement one `propose/analyze` interface. Digital target is the only GDS commitment; photonic/memristive are numpy device models.

**Tech Stack:** Python 3.13 (uv), numpy, cocotb+iverilog (digital sim), docker OpenROAD-flow-scripts (sky130), matplotlib (report charts), pytest.

**Spec:** `docs/superpowers/specs/2026-10-17-snn-agentic-chip-design.md`

## Global Constraints

- Python 3.13, uv-managed venv. Runtime dep: numpy. Dev deps: pytest, cocotb, matplotlib. No torch (numpy suffices for both model-level targets).
- No shell-outs to EDA from model-level targets; `docker` (present: 28.5.2) is the only external runtime for the digital flow.
- Stage failures are verdict dicts in the journal — never exceptions out of the loop.
- Journal record schema: `{"round": int, "target": str, "config": dict, "sim": dict, "flow": dict, "agent_note": str}` — field is named `flow` for ALL targets (digital included).
- Agent backends receive `journal tail` and return plain dicts/str; no LLM API on the cc path.
- Repo root `<proj>` = `/mnt/d/Work/Github/Agentic_AI_native_chip_design`.

## Review Focus

- **RTL with non-power-of-two neuron count (e.g. 300):** generator must pad the fabric to 512 and route only the first 300 — expected: parity sim still passes and no synthesis error. Test in Task 4.
- **All-zero / repeated spike trains at t=0:** cocotb TB and golden model must agree (no hangs, no spurious first-cycle spikes). Test in Task 4.
- **Journal lines missing `flow` or containing NaN metrics:** Pareto reporter must skip malformed entries, not crash. Test in Task 13.
- **Config exceeding the 8 GB RAM ceiling:** orchestrator logs a warning and proceeds; only the digital flow may later fail, and its failure is a verdict. Test in Task 12.
- **Non-JSON reply from `claude -p` (cc backend):** fallback = carry last config forward unchanged, note recorded; loop continues. Test in Task 11.

---

### Task 1: Scaffold + config validation

**Files:**
- Create: `common/config.py`
- Modify: `pyproject.toml` (uv add numpy; dev group pytest, cocotb, matplotlib)
- Test: `tests/test_config.py`

**Interfaces:**
- Produces: `REQUIRED_KEYS: dict[str, list[str]]` with keys `digital` (needs `["neurons","fanout","weight_width","timesteps","util_target","clock_ns"]`), `photonic` (needs `["mesh_depth","precision_bits","laser_mw","wavelength_nm"]`), `memristive` (needs `["xbar_rows","xbar_cols","variability_frac","adc_bits"]`). And `validate_config(target: str, cfg: dict) -> list[str]` (warnings; also `estimate_digital_rams(cfg: dict) -> int` bytes = `neurons * fanout * weight_width * timesteps`, warn threshold 5 GB inside `validate_config` as a "ram-ceiling" warning).

- [ ] **Step 1: Write failing test** — `REQUIRED_KEYS["digital"] == ["neurons","fanout","weight_width","timesteps","util_target","clock_ns"]`; `validate_config("digital", {"neurons": 4096, "fanout": 1024, "weight_width": 8, "timesteps": 1024, "util_target": 60, "clock_ns": 4.0})` returns a list containing a "ram-ceiling" warning; `validate_config("digital", {"neurons": 256, ...sane rest...})` returns `[]` for missing-keys.
- [ ] **Step 2:** Run `pytest tests/test_config.py -v` → FAIL (module missing).
- [ ] **Step 3:** Implement `common/config.py`.
- [ ] **Step 4:** Run pytest → PASS. Also `uv add numpy && uv add --dev pytest cocotb matplotlib`.
- [ ] **Step 5:** Commit `feat: scaffold + config validation`.

### Task 2: Digital golden LIF model

**Files:**
- Create: `targets/digital/model.py`
- Test: `tests/test_lif_model.py`

**Interfaces:**
- Produces: `class LIFModel: __init__(self, cfg: dict)`; `step(self, spikes: np.ndarray) -> np.ndarray` (one timestep, input/output shape `[N]`, values 0/1, `dtype=np.int8`); `run(self, spike_train: np.ndarray) -> np.ndarray` returns `[T, N]` int8. LIF update per neuron: `v' = decay*(v - rest) + sum_j w_ij * s_j_current_timestep - leak; if v >= threshold: emit 1 and reset v = rest`. Defaults pinned in cfg: `threshold=1.0, decay=0.9, rest=0.0, leak=0.0`; weights drawn from `weight_width`-bounded ints in `±(2**weight_width-1)` scaled by `1/2**weight_width`. Seeded deterministically from `cfg.get("seed", 1)` via `np.random.default_rng`.

- [ ] **Step 1: Failing test** — all-zero train returns all-zero; ref-neuron scenario hand-computed (one neuron, one weight, two spike steps — assert exact voltage trajectory and emitted spikes); determinism: same cfg+seed → identical `run` output on random train.
- [ ] **Step 2:** pytest → FAIL.
- [ ] **Step 3:** Implement. (numpy, no loops over neuron dimension)
- [ ] **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: golden LIF reference model`.

### Task 3: Digital RTL generator

**Files:**
- Create: `targets/digital/rtl_gen.py`
- Test: `tests/test_rtl_gen.py`

**Interfaces:**
- Consumes: cfg keys from Task 1 (`neurons, fanout, weight_width, timesteps`).
- Produces: `generate_rtl(cfg: dict) -> str` (complete Verilog-2005 text); `module_name(cfg: dict) -> str` = `f"snn_core_{cfg['neurons']}"`. Module interface (fixed for all configs): `clk, rst_n, inject_valid, inject_addr[15:0], inject_data, spike_out_valid, spike_out_addr[15:0], spike_out_data`. Internals: fabric padded up to next power of two; only first `neurons` routed.

- [ ] **Step 1: Failing test** — `generate_rtl({"neurons":300, ...})` contains `module snn_core_300` and no `module snn_core_512`; padded size appears in a localparam; 256-neuron output compiles with `iverilog -tnull -o /tmp/x.vp` (subprocess assert returncode 0).
- [ ] **Step 2:** pytest → FAIL.
- [ ] **Step 3:** Implement — plain f-string templating, one file.
- [ ] **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: parameterized LIF fabric RTL generator`.

### Task 4: Cocotb RTL parity test

**Files:**
- Create: `tests/digital/test_rtb.py`

**Interfaces:**
- Consumes: `generate_rtl`, `module_name` (Task 3), `LIFModel` (Task 2).
- Produces: pytest-level test proving sim-vs-golden parity. Uses cocotb's python runner API (`from cocotb.runner import get_runner`), simulator `"icarus"`.

- [ ] **Step 1:** Ensure iverilog present: `which iverilog || sudo apt-get install -y iverilog` (install needs user confirmation — surface the prompt).
- [ ] **Step 2: Write failing test** — build RTL for `{"neurons":256,"fanout":8,"weight_width":4,"timesteps":64}`, deterministic inject pattern: alternating cycles of an all-zero frame and a fixed single-spike frame for 64 steps; drive `inject_*` per cycle; collect `spike_out_*`; compare full output matrix against `LIFModel` outputs (same weights — weights must be emitted by `generate_rtl` from the same seeded rng so the TB can instantiate the same model). Assert equal across all 64 steps (this pins both Review Focus inputs).
- [ ] **Step 3:** pytest → FAIL (test constructs, but run to see it exercised; implementation already exists from Task 3 — if it passes immediately, verify it fails when the golden model is perturbed by ×2 decay, then restore).
- [ ] **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `test: cocotb sim-vs-golden LIF parity`.

### Task 5: ORFS flow wrapper

**Files:**
- Create: `targets/digital/flow.py`
- Test: `tests/digital/test_flow_parse.py`

**Interfaces:**
- Produces: `write_design(cfg: dict, out_dir: Path) -> dict` (writes `out_dir/orfs/` with `config.mk`, `snn_core.v`; returns paths); `run_pnr(cfg: dict, out_dir: Path, timeout_s: int = 3600) -> dict` — runs ORFS in docker for the design config, returns metrics dict `{"verdict": "pass"|"fail", "reason": str|None, "area_mm2": float|None, "pwr_w": float|None, "worst_slack_ns": float|None, "drc": int|None, "wirelength_um": float|None}`; `parse_metrics(results_dir: Path) -> dict` (extract the same keys from ORFS report files under `results/sky130*/<design>/base/reports/`); on docker missing or timeout: one retry, then `{"verdict":"fail", "reason": ...}` — never raises. Env: `ORFS_ROOT` (path to a shallow clone of OpenROAD-flow-scripts; clone instructions live in this task's docstring), image `openroad/orfs` pulled on demand via `docker pull`.

- [ ] **Step 1: Failing test** — `parse_metrics` on a fixture report tree (committed under `tests/digital/fixtures/orfs_reports/` with representative ORFS filenames: worst slack rpt, utilization/area rpt, DRC file, power rpt) returns the exact metric keys with float/int types and `verdict:"pass"`.
- [ ] **Step 2:** pytest → FAIL.
- [ ] **Step 3:** Implement `parse_metrics` + `write_design` + `run_pnr` (run_pnr body: docker invocation per ORFS docs; parse via `parse_metrics`).
- [ ] **Step 4:** pytest → PASS.
- [ ] **Step 5:** Integration smoke (manual, recorded in commit message): clone ORFS shallow, run `run_pnr` on the 256-neuron config, record area/drc values. Commit `feat: ORFS docker flow wrapper + metrics parser`.

### Task 6: Memristive crossbar model

**Files:**
- Create: `targets/memristive/crossbar.py`
- Test: `tests/test_crossbar.py`

**Interfaces:**
- Produces: `class CrossbarModel: __init__(self, cfg: dict)`; `run(self, inputs: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, dict]` — inputs `[B, xbar_rows]`, weights `[xbar_rows, xbar_cols]`, returns (outputs `[B, xbar_cols]`, metrics). Metrics dict keys: `{"energy_per_mac_pj": float, "area_mm2": float, "max_err": float, "verdict": "pass"}`. Physics: ideal currents `G*v` where G encodes weights into conductance bounds `[g_min, g_max]` from cfg `variability_frac` (per-cell multiplicative lognormal noise, seeded rng); ADC quantization to `adc_bits` levels; energy = `macs * (v_read**2 * g_max) * 1e12 + adc_energy_model`; area = `rows*cols*cell_area + adc_area(adc_bits)`, constants pinned in docstring.

- [ ] **Step 1: Failing test** — zero inputs → zero-energy metric `energy_per_mac_pj == 0.0`; variability sweep: `max_err` increases monotonically for `variability_frac` in [0, 0.05, 0.2]; determinism with same seed; output shape correct.
- [ ] **Step 2:** pytest → FAIL.
- [ ] **Step 3:** Implement.
- [ ] **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: RRAM crossbar device model + PPA`.

### Task 7: Photonic MZI-mesh model

**Files:**
- Create: `targets/photonic/mesh.py`
- Test: `tests/test_mesh.py`

**Interfaces:**
- Produces: `class MeshModel: __init__(self, cfg: dict)`; `run(self, inputs: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, dict]` — matrix-vector via transfer-matrix cascade of MZI unitaries + phase shifters encoding weights; metrics `{"energy_per_mac_pj": float, "loss_db": float, "footprint_mm2": float, "max_err": float, "verdict": "pass"}`. Energy model: `energy/mac = modulation_energy + detector_energy + heater_energy*mesh_depth` with constants pinned in docstring; loss = `insertion_loss_per_mzi * mzis`; footprint from unit-cell area × mesh_depth². cfg keys: `mesh_depth, precision_bits, laser_mw, wavelength_nm`.

- [ ] **Step 1: Failing test** — identity mesh (zero phase) reproduces inputs within `max_err < 1e-6`; loss grows linearly with `mesh_depth` (assert slope>0 across three depths); determinism; shapes.
- [ ] **Step 2:** pytest → FAIL.
- [ ] **Step 3:** Implement (numpy complex arithmetic; rectangular/clement mesh — implementer's reasonable choice, documented in docstring).
- [ ] **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: photonic MZI-mesh device model + PPA`.

### Task 8: Target registry

**Files:**
- Create: `targets/__init__.py`, `targets/base.py`; targets/digital gains `evaluate.py`, targets/photonic + memristive gain `evaluate.py`
- Test: `tests/test_targets.py`

**Interfaces:**
- Produces: class `Target` base with attributes `name: str`, `required_keys: list[str]` and method `evaluate(self, cfg: dict, out_dir: Path) -> dict` returning exactly `{"sim": dict, "flow": dict, "config": dict}`. Implementations: `DigitalTarget` (build = `write_design`, sim = cocotb runner invoked programmatically reusing Task 4 logic, flow = `run_pnr`, short-circuit: if sim fails, flow is skipped and `flow == {"verdict": "skipped", "reason": "sim failed"}`); `PhotonicTarget` and `MemristiveTarget` (sim = model `run()` on a fixed seeded benchmark workload, self-check verdict pass if `max_err` below bound in their evaluate; flow = deterministic model PPA). Registry: `get_target(name: str) -> Target` with `"digital"|"photonic"|"memristive"`, `KeyError` otherwise.

- [ ] **Step 1: Failing test** — `get_target("digital").name == "digital"`; `get_target("nope")` raises KeyError; photonic `evaluate` on sane config returns both dicts with `verdict == "pass"` and numeric metrics; digital evaluate is smoke-tested with flow monkeypatched to a fixed verdict (unit-level only — real ORFS run happens in Task 13/14).
- [ ] **Step 2:** pytest → FAIL.
- [ ] **Step 3:** Implement `evaluate.py` per target + registry.
- [ ] **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: target registry + evaluate contract`.

### Task 9: Journal

**Files:**
- Create: `common/journal.py`
- Test: `tests/test_journal.py`

**Interfaces:**
- Produces: `class Journal: __init__(self, path: Path)`, `append(self, rec: dict) -> None` (JSONL, one line each), `tail(self, n: int) -> list[dict]`, `entries(self, target: str | None = None) -> list[dict]` (skips lines that don't parse as JSON with the required round/target keys — malformed lines are tolerated, this pins Review Focus input 3).

- [ ] **Step 1: Failing test** — append 3 valid + 1 malformed line; `tail(2)` returns last 2 valid; `entries("digital")` filters; malformed line silently skipped.
- [ ] **Step 2:** pytest → FAIL. **Step 3:** Implement. **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: JSONL design journal`.

### Task 10: Agent backends — base + stub

**Files:**
- Create: `agents/__init__.py`, `agents/base.py`, `agents/stub.py`
- Test: `tests/test_agents.py`

**Interfaces:**
- Produces: `class Backend(Protocol): def propose_config(self, journal_tail: list[dict], target: str) -> dict | None; def analyze_failure(self, stage: str, logs: str, cfg: dict) -> str`. `class StubBackend: __init__(self, sequences: dict[str, list[dict]])` — pops configs in order per target; returns `None` when exhausted (loop ends). `get_backend(name: str, **kw) -> Backend` for `"stub"|"cc"|"api"` (api = built later; KeyError with message "api backend deferred to stage-1" until Task 12 wires it — actually registered but raising `NotImplementedError` is worse; plan: register only stub+cc, api added in Task 12 optional).

- [ ] **Step 1: Failing test** — stub yields sequence in order, None at end; get_backend("stub") works; get_backend("api") raises with the deferral message.
- [ ] **Step 2:** pytest → FAIL. **Step 3:** Implement. **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: agent backend contract + stub`.

### Task 11: Claude-Code backend

**Files:**
- Create: `agents/cc.py`
- Test: `tests/test_cc_backend.py`

**Interfaces:**
- Consumes: Backend protocol (Task 10).
- Produces: `class CcBackend: __init__(self, journal_path: Path, binary: str = "claude", timeout_s: int = 600)`. `propose_config` builds a prompt (journal tail serialized, target, cfg requirement list from Task 1), shells `claude -p "<prompt>"`, parses the LAST JSON object in stdout (regex over fenced/whole output) as config dict; **any failure (nonzero exit, timeout, non-JSON) returns `journal_tail[-1]["config"] if exists else None`** (pins Review Focus input 5). `analyze_failure` shells the same binary with a fix-note prompt, returns raw text (unparseable → `"no analysis"`).

- [ ] **Step 1: Failing test** — with binary monkeypatched to a fake script emitting `noise\n{"neurons": 512, ..., "round_hint": 2}`: config parsed, integer/float coercion applied; fake emitting `abc` (no JSON): falls back to previous config; fake exiting 3: same fallback.
- [ ] **Step 2:** pytest → FAIL. **Step 3:** Implement. **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: claude-code agent backend (shellout, JSON-coerced)`.

### Task 12: Orchestrator

**Files:**
- Create: `orchestrator.py`
- Test: `tests/test_orchestrator.py`

**Interfaces:**
- Consumes: `get_target`(T8), `get_backend`(T10), `Journal`(T9), `validate_config`(T1).
- Produces: `run_loop(target: str, backend: Backend, rounds: int, out_root: Path, config_override: dict | None = None, retries: int = 2) -> Path` (journal path). Round cycle: backend.propose_config → validate (fallback: keep previous config; first round without config → target's `DEFAULT_CFG` constant defined in its evaluate module) → `target.evaluate(cfg, runs/<target>/round_<n>/)` → journal append with agent_note from backend.analyze_failure on any failed stage → next round. Loop stops when: rounds exhausted OR backend returns None. Memory-ceiling warning from `validate_config` printed to stderr, loop proceeds (pins Review Focus input 4). CLI `main()`: `argparse` with `--target --rounds --backend --seed-config`. Returns journal path even when all rounds fail.

- [ ] **Step 1: Failing test** — fake `Target` (monkeypatched into registry) always failing: `run_loop` with StubBackend of 3 configs, retries=2 → journal has 3 entries, each with `"flow": {"verdict": "fail" ...}` and `agent_note` non-empty; loop journal path exists. Fake backend returning None after round 1 → exactly 1 entry. Oversized digital config → warning line on stderr captured via capsys, loop still runs.
- [ ] **Step 2:** pytest → FAIL. **Step 3:** Implement. **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: orchestrator round loop with journal + bounded retries`.

### Task 13: Pareto reporter

**Files:**
- Create: `report/pareto.py` (`report/__init__.py`)
- Test: `tests/test_report.py`

**Interfaces:**
- Consumes: Journal (T9).
- Produces: `pareto_front(entries: list[dict], x: str, y: str) -> list[dict]` (minimize both; entries lacking numeric x/y or with NaN skipped); `write_report(journal_path: Path, out_md: Path) -> Path` — markdown with per-target tables (round, config summary, verdicts, metrics) + per-target Pareto chart PNG (`out_md.with_suffix('')/` PNG path passed back in the md). Axis mapping per target: digital `(area_mm2, pwr_w)`, photonic `(footprint_mm2, energy_per_mac_pj)`, memristive `(max_err, energy_per_mac_pj)`.

- [ ] **Step 1: Failing test** — fixture journal with NaN and missing-field lines: `pareto_front` returns only the true front (3 crafted points where point 2 is dominated); `write_report` produces markdown containing each target header and 0 crash on malformed lines.
- [ ] **Step 2:** pytest → FAIL. **Step 3:** Implement. **Step 4:** pytest → PASS.
- [ ] **Step 5:** Commit `feat: Pareto front + markdown report generator`.

### Task 14: End-to-end demo run (verification task)

**Files:**
- Modify: none required (optional: `README.md` run instructions)

**Interfaces:**
- Consumes: whole stack.

- [ ] **Step 1:** Pull ORFS docker image, clone ORFS shallow (Task 5 docstring), verify bundled example flow runs once (this validates toolchain independent of our RTL).
- [ ] **Step 2:** Run `uv run python orchestrator.py --target digital --backend stub --rounds 3 --seed-config examples/digital_128.json` (committed example config: 128 neurons — faster than 256 for first full run) → expect journal with ≥3 rounds, RTL closes or fails with verdict reasons recorded.
- [ ] **Step 3:** Run with cc backend (`--backend cc`), 5+ rounds, journal shows distinct configs + agent notes; run `write_report` → Pareto PNG + markdown.
- [ ] **Step 4:** Run same for `--target photonic` and `--target memristive` (model-level, minutes).
- [ ] **Step 5:** Commit any fixes discovered (`fix: e2e run fixes`), record demo artifacts under `runs/` (git-ignored except final report + one GDS render path in README).

---

## Deferred (stage-1, NOT in this plan)

- `AGENTS_BACKEND=api` LLM router implementation (registered but deferred; `get_backend("api")` raises with deferral message)
- gdsfactory/Meep/SAX layout closure for photonic/memristive targets
- Agents writing RTL from scratch; leading-edge PDK post-signoff