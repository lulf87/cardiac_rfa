# V10 Abstract Draft

## Abstract

Reduced electro-thermal models are attractive for broad protocol sweeps in RF cardiac ablation, but their interpretability depends strongly on comparator definition and on whether short high-power thermal latency is represented explicitly. In particular, treating a 90 W / 4 s condition as fixed power only may conflate comparator mis-specification with protocol behavior.

This study presents a comparator-aware reduced 2D electro-thermal methodology for irrigated RF ablation. A standard RF protocol (30 W / 30 s), an HPSD protocol (50 W / 10 s), a fixed-power 90 W / 4 s protocol, and a generic temperature-limited 90 W / 4 s protocol were compared. The framework includes an 8 s post-pulse thermal latency window and evaluates deterministic responses across wall thickness, effective cooling, and insertion-depth conditions. The temperature-limited 90 W / 4 s comparator is generic and is not intended to reproduce a catheter-specific commercial control law.

At a representative condition (wall thickness 4 mm, cooling coefficient 1500 W m^-2 K^-1, insertion depth 1.0 mm), adding the latency window increased fixed 90 W / 4 s lesion depth from 1.302 to 1.695 mm and lesion area from 3.486 to 4.599 mm^2. Under the same condition, the generic temperature-limited 90 W / 4 s comparator reduced delivered energy from 360.0 to 354.9 J and peak temperature from 83.46 to 81.95 °C, with a modest depth reduction from 1.695 to 1.670 mm. Across the phase-preparation grid, controller action was threshold-dependent: in more aggressive cells it reduced delivered energy and peak temperature substantially, whereas in cooler cells it became effectively inactive and converged toward the fixed-power solution.

These results support the use of reduced models for assumption-bounded comparator analysis, but not for device-level prediction. Within the present framework, lesion depth, depth fraction, delivered energy, and peak-temperature trends are the most defensible outpus, whereas lesion width and overheating-related quantities should remain secondary internal proxies.
