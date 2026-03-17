# V10 Results Opening Draft

## 3.1 Comparator definition and stage17 protocol set

All stage17 deterministic results were generated with four explicitly defined comparators: standard RF (30 W / 30 s), HPSD (50 W / 10 s), fixed-power 90 W / 4 s, and generic temperature-limited 90 W / 4 s. The temperature-limited 90 W / 4 s case was implemented as a generic surface-adjacent feedback controller and should therefore be interpreted as a comparator definition within the reduced model rather than as a catheter-specific commercial control law. An 8 s post-pulse thermal latency window was applied to all four protocols so that short high-power outputs were not evaluated from end-of-pulse fields alone.

## 3.2 Effect of post-pulse thermal latency

The effect of thermal latency was first examined in a representative 90 W / 4 s fixed-power case. At wall thickness 4 mm, cooling coefficient 1500 W m^-2 K^-1, and insertion depth 1.0 mm, adding an 8 s post-pulse latency window increased lesion depth from 1.302 to 1.695 mm and lesion area from 3.486 to 4.599 mm^2, while the reported peak temperature remained 83.46 °C. This confirms that, within the present reduced framework, short high-power lesion formation is strongly affected by continued post-pulse heat diffusion and should not be interpreted from pulse termination alone.

## 3.3 Deterministic four-way comparison at representative conditions

At the same representative condition, standard RF produced the deepest lesion (3.113 mm), followed by HPSD (2.114 mm), fixed-power 90 W / 4 s (1.695 mm), and generic temperature-limited 90 W / 4 s (1.670 mm). Peak temperatures followed the opposite trend, with values of 65.77, 72.14, 83.46, and 81.95 °C, respectively. Relative to fixed-power 90 W / 4 s, the temperature-limited comparator reduced delivered energy from 360.0 to 354.9 J and mean applied power from 90.0 to 88.7 W, while causing only a modest depth reduction. Under these representative conditions, the main effect of control was therefore not a collapse of lesion formation, but a limited reduction in thermal severity.

## 3.4 Phase-preparation maps with fixed versus temperature-limited 90 W / 4 s

Across the full stage17 phase-preparation grid, the effect of temperature-limited control was threshold-dependent. In more aggressive cells, particularly those combining thinner walls, weaker cooling, and larger insertion depth, the controlled 90 W / 4 s comparator reduced delivered energy and peak temperature substantially relative to the fixed-power case. For example, at wall thickness 2 mm, cooling coefficient 800 W m^-2 K^-1, and insertion depth 1.5 mm, the fixed-power comparator reached 105.59 °C with an overheat-area proxy of 0.426 mm^2, whereas the temperature-limited comparator reduced peak temperature to 83.15 °C, reduced delivered energy to 271.3 J, and remained non-transmural under the present criterion. By contrast, in cooler cells the controller became effectively inactive and the controlled solution converged toward the fixed-power solution. These maps therefore show that comparator definition is itself a structured determinant of model output, rather than a minor implementation detail.

## 3.5 Boundary of interpretation

These stage17 maps should be interpreted as model-internal, assumption-bounded comparator analyses. The most defensible outputs are lesion depth, depth fraction, delivered energy, and peak-temperature trends. Lesion width and overheating-related quantities are retained for internal comparison, but they are not used here as primary validation targets or as device-level predictive claims.