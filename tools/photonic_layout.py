"""gdsfactory layout of the photonic SNN core: SVD mesh for an N x N matrix.

Light path, left to right: N input modes -> Vt mesh (Clements, N columns of
2x2 MZIs with heaters) -> attenuator columns (one 1x1 MZI per mode, even and
odd modes staggered) -> sign column (one heater per mode) -> U mesh -> N
output ports (to off-layout coherent receivers). Generic gdsfactory PDK, not a
foundry PDK: geometry only, no foundry DRC, no electrical routing or pads.

    .venv/bin/python tools/photonic_layout.py 4 8 16     # writes GDS, PNG, JSON
"""

import json
import sys
from pathlib import Path

import gdsfactory as gf

OUT = Path(__file__).resolve().parents[1] / "wiki/raw/assets/photonic"
PITCH = 30.0      # mode pitch (um): two modes per 56 um tall MZI
FAN = 40.0        # s-bend length from mode pitch to MZI port pitch (um)
CELL = "mzi2x2_2x2_phase_shifter"  # 2x2 MZI with a metal heater, 291 x 56 um


def build(n: int) -> tuple[gf.Component, dict]:
    c = gf.Component(f"photonic_svd_mesh_{n}")
    mzi = getattr(gf.components, CELL)()
    att = gf.components.mzi_phase_shifter()
    heater = gf.components.straight_heater_metal()
    stub = gf.components.straight(length=1.0)
    heads = []
    for m in range(n):
        s = c << stub
        s.dmove((0, m * PITCH))
        c.add_port(f"in{m}", port=s.ports["o1"])
        heads.append(s.ports["o2"])
    counts = {"mzi": 0, "attenuator": 0, "heater": 0}

    def advance(m, ref_in, ref_out, port_in, port_out):
        gf.routing.route_single_sbend(c, heads[m], ref_in.ports[port_in])
        heads[m] = ref_out.ports[port_out]

    def pass_through(x_end):
        for m in range(n):
            if heads[m].dcenter[0] < x_end:
                s = c << gf.components.straight(length=x_end - heads[m].dcenter[0])
                s.connect("o1", heads[m])
                heads[m] = s.ports["o2"]

    def mesh():
        for col in range(n):
            x0 = max(h.dcenter[0] for h in heads)
            pass_through(x0)
            for m in range(col % 2, n - 1, 2):
                r = c << mzi
                r.dmove((x0 + FAN + 10.0, (m + 0.5) * PITCH))
                gf.routing.route_single_sbend(c, heads[m], r.ports["o1"])
                gf.routing.route_single_sbend(c, heads[m + 1], r.ports["o2"])
                heads[m], heads[m + 1] = r.ports["o4"], r.ports["o3"]
                counts["mzi"] += 1
            x1 = max(h.dcenter[0] for h in heads)
            for m in range(n):  # back to mode pitch before the next column
                if abs(heads[m].dcenter[1] - m * PITCH) > 1e-6:
                    s = c << stub
                    s.dmove((x1 + FAN, m * PITCH))
                    gf.routing.route_single_sbend(c, heads[m], s.ports["o1"])
                    heads[m] = s.ports["o2"]
            pass_through(max(h.dcenter[0] for h in heads))

    mesh()  # Vt
    for parity in (0, 1):  # attenuators: 56 um tall, so even and odd modes in turn
        x0 = max(h.dcenter[0] for h in heads)
        pass_through(x0)
        for m in range(parity, n, 2):
            r = c << att
            r.connect("o1", heads[m])
            heads[m] = r.ports["o2"]
            counts["attenuator"] += 1
    pass_through(max(h.dcenter[0] for h in heads))
    for m in range(n):  # sign column
        r = c << heater
        r.connect("o1", heads[m])
        heads[m] = r.ports["o2"]
        counts["heater"] += 1
    pass_through(max(h.dcenter[0] for h in heads))
    mesh()  # U
    for m in range(n):
        c.add_port(f"out{m}", port=heads[m])
    info = {"n": n, "cell": CELL, "gdsfactory": gf.__version__, **counts,
            "width_um": c.dxsize, "height_um": c.dysize,
            "bbox_mm2": c.dxsize * c.dysize / 1e6}
    return c, info


def main(ns) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gf.gpdk.PDK.activate()
    results = []
    for n in ns:
        c, info = build(n)
        assert info["mzi"] == n * (n - 1), info  # two meshes of N(N-1)/2
        if n <= 16:
            c.write_gds(OUT / f"svd_mesh_{n}.gds")
        results.append(info)
        print(json.dumps(info))
    path = OUT / "layout_areas.json"
    old = {r["n"]: r for r in json.loads(path.read_text())} if path.exists() else {}
    old.update({r["n"]: r for r in results})
    path.write_text(json.dumps(sorted(old.values(), key=lambda r: r["n"]), indent=1) + "\n")


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or [4, 8, 16])
